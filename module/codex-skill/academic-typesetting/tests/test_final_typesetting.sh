#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TEST_DIR=$(mktemp -d)
trap 'rm -rf "$TEST_DIR"' EXIT
cat > "$TEST_DIR/main.tex" <<'TEX'
\documentclass{article}
\begin{document}
Valid paragraph. See Section~\ref{sec:one}.
\section{One}\label{sec:one}
\end{document}
TEX
bash "$ROOT/scripts/compile_latex.sh" "$TEST_DIR/main.tex" --strict --quiet
[[ -s "$TEST_DIR/main.pdf" && -s "$TEST_DIR/main.log" ]]
echo 'PASS: strict pdfLaTeX build, references and retained logs'
# Keep old PDF to test that a stale artifact cannot mask an error.
cat > "$TEST_DIR/main.tex" <<'TEX'
\documentclass{article}
\begin{document}
\notARealCommand
\end{document}
TEX
if bash "$ROOT/scripts/compile_latex.sh" "$TEST_DIR/main.tex" --strict --quiet > "$TEST_DIR/error.txt" 2>&1; then
 echo 'FAIL: erroneous source accepted'; exit 1
fi
[[ -s "$TEST_DIR/main.log" ]]
echo 'PASS: compiler error rejected despite existing PDF'
cat > "$TEST_DIR/unresolved.tex" <<'TEX'
\documentclass{article}
\begin{document}
Unresolved reference: \ref{absent} and citation \cite{missing}.
\end{document}
TEX
if bash "$ROOT/scripts/compile_latex.sh" "$TEST_DIR/unresolved.tex" --strict --quiet > "$TEST_DIR/error.txt" 2>&1; then
 echo 'FAIL: unresolved references accepted'; exit 1
fi
echo 'PASS: unresolved references and citations rejected'
if bash "$ROOT/scripts/compile_latex.sh" "$TEST_DIR/main.tex" --strict --auto-fix > "$TEST_DIR/error.txt" 2>&1; then
 echo 'FAIL: temporary source modification accepted'; exit 1
fi
echo 'PASS: strict mode refuses temporary source injection'
source "$ROOT/scripts/install_deps.sh"
if LATEX_SKILL_ALLOW_INSTALL=0 install_packages pandoc 2> "$TEST_DIR/dependency.txt"; then
 echo 'FAIL: dependency installation gate'; exit 1
fi
echo 'PASS: dependency installation requires authorization'
