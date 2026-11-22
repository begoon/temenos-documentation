#!/usr/bin/env python3
"""Build the multi-page HTML site from jBC_Programmers_Reference_Guide.markdown.

The output reproduces the layout of the original jbc.temenos.com site:
index.html, index.css and one HTML file per chapter in pages/.

    python3 build.py                  build into _site/
    python3 build.py --serve 8000     build, serve and rebuild on change
    python3 build.py --verify DIR     compare a rebuild with a published copy

Only the Python standard library is used.
"""

import argparse
import http.server
import re
import sys
import tempfile
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "jBC_Programmers_Reference_Guide.markdown"
SITE = ROOT / "site"

# --------------------------------------------------------------------------
# Document model
# --------------------------------------------------------------------------


class Page:
    def __init__(self, title, is_group):
        self.title = title
        self.is_group = is_group
        self.lines = []

    @property
    def slug(self):
        return slugify(self.title)


def slugify(title):
    """'BREAK ON/OFF' -> 'break_on_off', '@FOOTER.BREAK' -> '@footerbreak'."""
    text = title.lower()
    text = re.sub(r"[ /]", "_", text)
    return re.sub(r"[^a-z0-9_@]", "", text)


def heading_text(line, marker):
    return line[len(marker):].strip().rstrip("#").strip()


def parse(text):
    """Split the guide into groups ('# ') of pages ('## ').

    Returns a list of (group_page, [chapter_page, ...]).
    """
    groups = []
    current = None
    for line in text.split("\n"):
        if line.startswith("# "):
            current = Page(heading_text(line, "# "), True)
            groups.append((current, []))
        elif line.startswith("## "):
            current = Page(heading_text(line, "## "), False)
            groups[-1][1].append(current)
        elif current is not None:
            current.lines.append(line)
    return groups


# --------------------------------------------------------------------------
# jBC syntax highlighting
# --------------------------------------------------------------------------


# The word lists hold every keyword the original generator is known to have
# highlighted; they were recovered from the pages it published.

FUNCTIONS = """
    ABS ABSS ADDS ALPHA ANDS ASCII ASSIGNED BITAND BITCHANGE BITCHECK
    BITLOAD BITNOT BITOR BITRESET BITSET BITTEST BITXOR BYTELEN CALLJEE
    CALLONEXIT CATS CHANGE CHANGETIMESTAMP CHAR CHARS CHDIR CHECKSUM COL1
    COL2 COMPARE CONVERT COS COUNT COUNTS CacheBucketList CacheClear
    CacheClearAll CacheClearStats CacheDelete CacheExists CacheGet
    CacheGetOption CacheKeyList CachePut CacheSetOption CacheStats DATE
    DCOUNT DECRYPT DIR DIV DIVS DOWNCASE DQUOTE DROUND DTX DYNTOXML EBCDIC
    ENCRYPT EQS EREPLACE EXIT EXP EXTRACT FADD FDIV FIELD FIELDS FILEINFO
    FMT FMTS FMUL FOLD FSUB GES GETCWD GETENV GETUSERGROUP GROUP ICONV
    ICONVS IFS INDEX INMAT INSERT INT IOCTL ISALNUM ISALPHA ISCNTRL ISDIGIT
    ISLOWER ISPRINT ISSPACE ISUPPER ITYPE JBASECOREDUMP JBASESubroutineExist
    JBASETHREADCreate JBASETHREADStatus JQLCOMPILE JQLEXECUTE JQLFETCH
    JQLGETPROPERTY JQLPUTPROPERTY KEYIN LATIN1 LEFT LEN LENDP LENS LES LN
    LOCALDATE LOCALTIME LOWCASE LOWER Logger MAKETIMESTAMP MATCHFIELD
    MAXIMUM MINIMUM MOD MODS MULS NEG NEGS NES NOT NOTS NUM NUMS OCONV
    OCONVS ORS PUTENV PWR QUOTE RAISE RECORDLOCKED REGEXP REPLACE REUSE
    RIGHT RND SADD SDIV SENTENCE SEQ SEQS SIN SMUL SORT SOUNDEX SPACE SPACES
    SPLICE SPOOLER SQRT SQUOTE SSUB STATUS STR STRS SUBS SUBSTRINGS SUM SWAP
    SYSTEM TAN TIME TIMEDATE TIMEDIFF TIMESTAMP TRANS TRANSQUERY TRIM TRIMBS
    TRIMFS UNASSIGNED UNIQUEKEY UPCASE UTF8 XLATE XMLTODYN XMLTOXML XTD
""".split()

COMMANDS = """
    ABORT AND APPEND AT BEFORE BEGIN BREAK BREAK  BY CALL CALLC CALLJ
    CALLdotNET CAPTURING CASE CHAIN CHANGE CLEAR CLEARCOMMON CLEARDATA
    CLEARFILE CLEARINPUT CLEARSELECT CLOSE CLOSESEQ COLLECTDATA COMMON
    CONTINUE CONVERT CREATE CRT DATA DEBUG DEFC DEFCE DEFFUN DEL DELETE
    DELETELIST DELETESEQ DICT DIM DIMENSION DO ECHO ECHO  ELSE END ENTER EQ
    EQU EQUATE ERROR EXECUTE EXIT FILELOCK FILEUNLOCK FIND FINDSTR FLOAT
    FLUSH FOOTING FOR FORMLIST FROM FUNCTION GE GET GETLIST GETX GO GOSUB
    GOTO GROUPSTORE GT HEADING HUSH IF IN INCLUDE INPUT INPUTCLEAR INPUTNULL
    INS INT LE LENGTH LOCATE LOCK LOCKED LOOP LT MAT MATBUILD MATCH MATCHES
    MATPARSE MATREAD MATREADU MATWRITE MATWRITEU MSLEEP NE NEXT NOBUF
    NODELAY NULL OBJEXCALLBACK OFF ON OPEN OPENDEV OPENINDEX OPENPATH
    OPENSEQ OPENSER OR OSBREAD OSBWRITE OSCLOSE OSDELETE OSOPEN OSREAD
    OSWRITE OUT PAGE PASSDATA PASSLIST PAUSE PERFORM PRECISION PRINT PRINTER
    PRINTERR PROCREAD PROCWRITE PROGRAM PROMPT READ READBLK READL READLIST
    READNEXT READONLY READPREV READSEQ READT READU READV READVU READXML
    RELEASE REMOVE REPEAT RETURN RETURNING REWIND RTNDATA RTNLIST SEEK
    SELECT SEND SENDX SETTING SLEEP SSELECT SSELECTN SSELECTV STATUS STEP
    STOP SUB SUBROUTINE SYNC THEN TIMEOUT TO TRANSABORT TRANSEND TRANSTART
    UNLOCK UNTIL USING VAR WAIT WAITING WAKE WEOF WEOFSEQ WHILE WITH WRITE
    WRITEBLK WRITELIST WRITESEQ WRITESEQF WRITET WRITEU WRITEV WRITEVU
    WRITEXML
""".split()

TYPES = """
    #else #endif #ifdef $INSERT @AM @CODEPAGE @DATA @DATE @DAY @EOF @FALSE
    @FILENAME @FM @ID @RECORD @SELECTED @SM @SYS.BELL @TIME @TM @TRUE @UID
    @USER.ROOT @USERSTATS @VM
""".split()

PHRASES = ["BREAK ON", "BREAK OFF", "ECHO ON", "ECHO OFF"]

# Spans are inserted as private-use marker characters and only turned into
# real tags at the end, so that later rules never match inside a tag.
OPEN = {
    "fun": "",
    "com": "",
    "num": "",
    "typ": "",
    "str": "",
    "rem": "",
    "lbl": "",
}
CLOSE = ""
TAGS = {
    OPEN["fun"]: '<span class="c-0fun">',
    OPEN["com"]: '<span class="c-1com">',
    OPEN["num"]: '<span class="c-2num">',
    OPEN["typ"]: '<span class="c-3typ">',
    OPEN["str"]: '<span class="c-4str">',
    OPEN["rem"]: '<span class="c-5com">',
    OPEN["lbl"]: '<span class="c-6lbl">',
    CLOSE: "</span>",
}
MARKERS = re.compile("[-]")


def wrap(kind, text):
    return OPEN[kind] + text + CLOSE


def alternation(words):
    return "|".join(re.escape(w) for w in sorted(words, key=lambda w: (-len(w), w)))


FUNCTION_RE = re.compile(r"(?<= )(%s)(?=\()" % alternation(FUNCTIONS))
PHRASE_RE = re.compile(r"(?<= )(%s)" % alternation(PHRASES))
COMMAND_RE = re.compile(r"(?<= )(%s)" % alternation(COMMANDS))
TYPE_RE = re.compile(r"(%s)" % alternation(TYPES))
NUMBER_RE = re.compile(r"(?<!\w)(-?\d+)(?!\w)")
DQ_RE = re.compile(r'(?<!\S)".*?"(?=\s|$)')
SQ_RE = re.compile(r"'[^']*'")
BS_RE = re.compile(r"(?<= )\\[^\\ ]+\\")
LINE_COMMENT_RE = re.compile(r"^(\s*)((?:\*|!|REM\b|//)[^$]*)")
SEMI_COMMENT_RE = re.compile(r"(?<=;)(\*[^$]*)")
SLASH_COMMENT_RE = re.compile(r"(//[^$]*)")


def string(match):
    return wrap("str", MARKERS.sub("", match.group(0)))


def highlight(line):
    """Highlight one line of jBC code the way the original site did."""
    line = line.replace("<", "&lt;").replace(">", "&gt")
    line = FUNCTION_RE.sub(lambda m: wrap("fun", m.group(1)), line)
    line = PHRASE_RE.sub(lambda m: wrap("com", m.group(1)), line)
    line = COMMAND_RE.sub(lambda m: wrap("com", m.group(1)), line)
    line = TYPE_RE.sub(lambda m: wrap("typ", m.group(1)), line)
    line = NUMBER_RE.sub(lambda m: wrap("num", m.group(1)), line)
    line = DQ_RE.sub(string, line)
    line = SQ_RE.sub(string, line)
    line = BS_RE.sub(string, line)
    line = LINE_COMMENT_RE.sub(lambda m: m.group(1) + wrap("rem", m.group(2)), line)
    line = SEMI_COMMENT_RE.sub(lambda m: wrap("rem", m.group(1)), line)
    line = SLASH_COMMENT_RE.sub(lambda m: wrap("rem", m.group(1)), line)
    return MARKERS.sub(lambda m: TAGS[m.group(0)], line)


# --------------------------------------------------------------------------
# Markdown subset -> HTML
# --------------------------------------------------------------------------


def inline_line(line, slugs):
    def link(match):
        text, target = match.group(1), match.group(2)
        if target.startswith("#"):
            slug = slugify(target[1:])
            if slug not in slugs:
                # A mistyped anchor falls back to the page named by the text.
                slug = slugify(text)
            target = slug + ".html"
        return '<a href="%s">%s</a>' % (target, text)

    line = re.sub(r"!\[([^\]]*)\]\(([^)]*)\)", r'<img src="\2" alt="\1">', line)
    line = re.sub(r"\[([^\]]*)\]\(([^)]*)\)", link, line)
    # The original generator left emphasis alone on a line that opens with a
    # single character followed by an asterisk ("A **THEN** or ...").
    if re.match(r"\S \*", line):
        return line
    line = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", line)
    line = re.sub(r"__(.+?)__", r"<strong>\1</strong>", line)
    line = re.sub(r"\*(.+?)\*", r"<em>\1</em>", line)
    return line


def inline(lines, slugs):
    return "\n ".join(inline_line(line, slugs) for line in lines)


def is_code(line):
    return line.startswith("    ")


def render_content(page, slugs):
    lines = page.lines
    out = ["<h1>%s</h1>" % page.title]
    i, n = 0, len(lines)
    while i < n:
        line = lines[i]
        if not line.strip() or line.strip() == "<!--jBC-->":
            i += 1
        elif line.startswith("### "):
            out.append("<h2>%s</h2>" % heading_text(line, "### "))
            i += 1
        elif is_code(line):
            block = []
            while i < n and is_code(lines[i]):
                block.append(lines[i])
                i += 1
            spans = "".join("<span>%s\n</span>" % highlight(l) for l in block)
            out.append("<pre>%s</pre>" % spans)
        elif line.startswith("- "):
            # Every line of a list block becomes an item, continuation lines too.
            items = []
            while i < n and lines[i].strip():
                items.append(re.sub(r"^(- |\s+)", "", lines[i]))
                i += 1
            body = "".join("<li>%s\n</li>" % inline([x], slugs) for x in items)
            out.append("<ul>%s</ul>" % body)
        elif line.startswith("|"):
            rows = []
            while i < n and lines[i].startswith("|"):
                rows.append(lines[i])
                i += 1
            html_rows = []
            for r, row in enumerate(rows):
                if r == 1:
                    continue
                cells = [c.strip() for c in row.strip().strip("|").split("|")]
                tag = "th" if r == 0 else "td"
                html_rows.append(
                    "<tr>%s</tr>"
                    % "".join("<%s>%s</%s>" % (tag, inline([c], slugs), tag) for c in cells)
                )
            out.append("<table>%s</table>" % "".join(html_rows))
        else:
            block = []
            while i < n and lines[i].strip() and not lines[i].startswith(("### ", "|")):
                block.append(lines[i])
                i += 1
            out.append("<p>%s\n</p>" % inline(block, slugs))
    return "\n".join(out)


# --------------------------------------------------------------------------
# Page assembly
# --------------------------------------------------------------------------

CONTENT_OPEN = '<div id="content">'
TIMESTAMP_RE = re.compile(r'<div id="timestamp">Last update: ([^<]*)</div>')


def render_sidebar(groups, prefix, for_index=False):
    out = []
    for number, (group, pages) in enumerate(groups, 1):
        out.append("<h2>%s</h2>\n" % group.title)
        if for_index and number == len(groups):
            # The original index page lost the links of the last group; it
            # redirects to the preface straight away, so nobody sees it.
            out.append("\n")
        elif pages:
            items = "\n".join(
                '<li><a href="%s%s.html">%s</a></li>' % (prefix, p.slug, p.title)
                for p in pages
            )
            out.append("<ul>%s\n</ul>\n" % items)
    return "".join(out)


def fill(template, **values):
    return re.sub(r"\{\{(\w+)\}\}", lambda m: values[m.group(1)], template)


def split_page(text):
    """Return (content, timestamp) of a previously built page, or None."""
    start = text.find(CONTENT_OPEN)
    stamp = None
    for stamp in TIMESTAMP_RE.finditer(text):
        pass
    if start < 0 or stamp is None:
        return None
    return text[start + len(CONTENT_OPEN):stamp.start()], stamp.group(1)


TRAILING_SPACE_RE = re.compile(r"[ \t]+((?:</span>)*)$", re.M)


def same_text(one, two):
    """Compare two page bodies, ignoring whitespace at the end of source lines."""
    return TRAILING_SPACE_RE.sub(r"\1", one) == TRAILING_SPACE_RE.sub(r"\1", two)


def read_text(path):
    try:
        return path.read_bytes().decode("utf-8").replace("\r\n", "\n")
    except FileNotFoundError:
        return None


def write_text(path, text):
    data = text.encode("utf-8")
    if not path.exists() or path.read_bytes() != data:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return True
    return False


def build(source, out, previous=None, redirect="pages/preface.html", extras=True):
    """Build the site into `out`.

    A page keeps the "Last update" stamp it has in `previous` (by default the
    output directory itself) for as long as its text is unchanged, the same
    way the original generator worked.

    With `extras` the build also adds what is specific to this deployment:
    the analytics snippet in site/head.html, the contact line in
    site/footer.html and the CNAME file.

    Returns the list of files that were written.
    """
    previous = Path(previous) if previous else out
    now = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M UTC")
    template = (SITE / "template.html").read_text(encoding="utf-8")
    head = (SITE / "head.html").read_text(encoding="utf-8") if extras else ""
    footer = (SITE / "footer.html").read_text(encoding="utf-8").strip() if extras else ""
    groups = parse(source.read_text(encoding="utf-8").replace("\r\n", "\n"))
    pages = [page for group, chapters in groups for page in [group] + chapters]
    slugs = {page.slug for page in pages}
    if len(slugs) != len(pages):
        names = sorted(p.slug for p in pages)
        twice = sorted({n for n in names if names.count(n) > 1})
        raise SystemExit("Two chapters share a file name: %s" % ", ".join(twice))

    written = []

    def emit(relative, title, root, sidebar, content, redirect_line):
        old = read_text(previous / relative)
        parts = split_page(old) if old else None
        stamp = now
        if parts and same_text(parts[0], content):
            content, stamp = parts
        text = fill(
            template,
            title=title,
            root=root,
            sidebar=sidebar,
            content=content + '<div id="timestamp">Last update: %s</div>' % stamp,
            redirect=redirect_line,
            head=head,
            footer=footer,
        )
        if write_text(out / relative, text):
            written.append(relative)

    sidebar = render_sidebar(groups, "")
    for page in pages:
        emit(
            "pages/%s.html" % page.slug,
            page.title,
            "../",
            sidebar,
            render_content(page, slugs),
            "",
        )
    emit(
        "index.html",
        "jBC",
        "",
        render_sidebar(groups, "pages/", for_index=True),
        "",
        'window.location = "%s";' % redirect,
    )
    if write_text(out / "index.css", (SITE / "index.css").read_text(encoding="utf-8")):
        written.append("index.css")
    if extras and write_text(out / "CNAME", (SITE / "CNAME").read_text(encoding="utf-8")):
        written.append("CNAME")

    # Chapters that were renamed or removed leave no page behind.
    wanted = {"%s.html" % slug for slug in slugs}
    for path in sorted((out / "pages").glob("*.html")):
        if path.name not in wanted:
            path.unlink()
            written.append("pages/%s (removed)" % path.name)
    return written


def verify(reference, source, redirect):
    """Rebuild against `reference` and report every file that differs from it.

    Line endings and a final newline are ignored: some reference pages were
    saved on Windows.
    """
    normal = lambda text: text.rstrip("\n")
    with tempfile.TemporaryDirectory() as scratch:
        out = Path(scratch)
        build(source, out, reference, redirect, extras=False)
        names = sorted(
            {p.relative_to(out).as_posix() for p in out.rglob("*") if p.is_file()}
            | {
                p.relative_to(reference).as_posix()
                for p in reference.rglob("*")
                if p.is_file() and ".git" not in p.parts and p.suffix in (".html", ".css")
            }
        )
        different = []
        for name in names:
            mine, theirs = read_text(out / name), read_text(reference / name)
            if mine is None or theirs is None or normal(mine) != normal(theirs):
                different.append(name)
    print("%d files compared, %d differ" % (len(names), len(different)))
    for name in different:
        print("  " + name)
    return 1 if different else 0


RELOAD = b"""<script>
(function () {
  var seen = null;
  setInterval(function () {
    fetch("/__build").then(function (r) { return r.text(); }).then(function (now) {
      if (seen !== null && seen !== now) location.reload();
      seen = now;
    }).catch(function () {});
  }, 700);
})();
</script>
"""


def serve(source, out, previous, redirect, port):
    """Serve the site locally and rebuild whenever a source file changes."""
    watched = [source] + [SITE / name for name in ("template.html", "head.html", "footer.html", "index.css")]
    state = {"build": 0}

    def stamps():
        return [p.stat().st_mtime_ns if p.exists() else 0 for p in watched]

    def rebuild():
        try:
            written = build(source, out, previous, redirect)
            state["build"] += 1
            print("built: %d files changed" % len(written), flush=True)
        except (Exception, SystemExit) as error:
            print("build failed: %s" % error, flush=True)

    def watch():
        last = stamps()
        while True:
            time.sleep(0.4)
            now = stamps()
            if now != last:
                last = now
                rebuild()

    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(out), **kwargs)

        def reply(self, body, kind):
            self.send_response(200)
            self.send_header("Content-Type", kind)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            path = self.path.split("?")[0]
            if path == "/__build":
                return self.reply(str(state["build"]).encode(), "text/plain")
            local = Path(self.translate_path(path))
            if local.is_dir():
                local = local / "index.html"
            if local.suffix == ".html" and local.is_file():
                # The reload script is added on the fly; files on disk stay clean.
                page = local.read_bytes().replace(b"</body>", RELOAD + b"</body>")
                return self.reply(page, "text/html; charset=utf-8")
            return super().do_GET()

        def log_message(self, *args):
            pass

    rebuild()
    threading.Thread(target=watch, daemon=True).start()
    server = http.server.ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print("serving http://localhost:%d/ (Ctrl+C to stop)" % port, flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print()


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--source", type=Path, default=SOURCE, help="the markdown guide")
    parser.add_argument("--out", type=Path, default=ROOT / "_site", help="output directory")
    parser.add_argument(
        "--previous",
        type=Path,
        help="an earlier build to carry 'Last update' stamps over from "
        "(default: the output directory)",
    )
    parser.add_argument(
        "--redirect",
        default="pages/preface.html",
        help="where index.html sends the browser (the original used /pages/preface.html)",
    )
    parser.add_argument("--serve", type=int, metavar="PORT", help="serve and rebuild on change")
    parser.add_argument(
        "--verify",
        type=Path,
        metavar="DIR",
        help="compare a rebuild with a published copy of the site instead of building",
    )
    args = parser.parse_args()
    if args.verify:
        return verify(args.verify, args.source, args.redirect)
    if args.serve:
        return serve(args.source, args.out, args.previous, args.redirect, args.serve)
    written = build(args.source, args.out, args.previous, args.redirect)
    total = len(list((args.out / "pages").glob("*.html")))
    print("%d pages in %s, %d files changed" % (total, args.out, len(written)))
    for name in written[:20]:
        print("  " + name)
    if len(written) > 20:
        print("  ... and %d more" % (len(written) - 20))


if __name__ == "__main__":
    sys.exit(main())
