#!/bin/bash
# citeproc drops raw LaTeX (\textbf{}) from BibTeX name fields, so the
# bold-author styling in bibliography.bib's *MYPUB entries never survives
# rendering. Bold the author's name directly in the rendered HTML instead.
set -euo pipefail

FILE="docs/publications.html"
if [ -f "$FILE" ]; then
  sed -i.bak 's/M\. Piazza/<strong>M. Piazza<\/strong>/g' "$FILE"
  rm -f "$FILE.bak"
fi
