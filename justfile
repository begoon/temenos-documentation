# The site as last published by hand; used for "Last update" stamps and checks.
published := "https://github.com/VladimirK2/vladimirk2.github.io"

# list the recipes
default:
    @just --list

# build the site into _site/
build:
    python3 build.py

# build, serve on http://localhost:<port>/ and rebuild on every change
dev port="8000":
    python3 build.py --serve {{port}}

# build, taking "Last update" stamps of unchanged pages from the published site
seed url=published:
    #!/usr/bin/env bash
    set -euo pipefail
    copy=$(mktemp -d)
    trap 'rm -rf "$copy"' EXIT
    git clone --quiet --depth 1 {{url}} "$copy/site"
    python3 build.py --previous "$copy/site"

# check that a rebuild reproduces the published site byte for byte
verify url=published:
    #!/usr/bin/env bash
    set -euo pipefail
    copy=$(mktemp -d)
    trap 'rm -rf "$copy"' EXIT
    git clone --quiet --depth 1 {{url}} "$copy/site"
    python3 build.py --verify "$copy/site" --redirect /pages/preface.html

# remove the build output
clean:
    rm -rf _site
