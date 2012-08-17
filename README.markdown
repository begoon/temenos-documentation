What is this?
=============

This project contains files to generate the Temenos Banking Language
documentation.


How does it work?
=================

The documentation is in the [Markdown][] format. Why Markdown?

First. Instead of using binary or XML formats which are evil for
version control, smart people invented compromise formats combining
readability of text plain text and good looking of rich-text formats.

So, you can read and use the sources of a document, plus it is
possible to generate a nicely formatted and colored final document
(html, PDF, RTF, etc.) from it.

Second.  There are plenty markup languages like this: Markdown, ReST, 
Textile, etc.  Markdown is a good combination of simplicity and quite
powerful formatting features.

[Markdown][] syntax is explained on a single page.

[Markdown]: http://daringfireball.net/projects/markdown/syntax


How to generate HTML?
=====================

First, you need Windows (32- or 64-bit). To generate a HTML file
you need to run `build-html.cmd` script. It uses the 
`blackfriday-tool.exe` tool which is 32-bit and should work on both
types of Windows (32- and 64-bit). This tool is a standalone 
executable and doesn't require any external libraries or DLLs.

This script will compile a `jBC_Programmers_Reference_Guide.html`
file combining the `markdown.css` file and the output of the 
`blackfriday-tool.exe` converter.

The `blackfriday-tool.exe` provides a [few extensions to the standard
Markdown format][blackfriday extensions] (for example, tables).

[blackfriday extensions]: https://github.com/russross/blackfriday#extensions


A couple of guidelines
======================

- Use 80 character lines where ever possible. Only in code snippets
  or tables it may need using longer lines.
- Do NOT over use table. One good table is worth a million of words,
  so, please, put tables when it is really necessary.


What to do if I'm stuck?
========================

Regarding Markdown, scripts, tooling and documentation, please
contact Alexander Demin (ademin@temenos.com).
