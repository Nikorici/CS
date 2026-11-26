#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 verify.py "${1:-report/output.txt}" report/output.txt
{ echo "$ python3 verify.py report/output.txt"; python3 verify.py report/output.txt; } > report/verify_run.txt
python3 - <<'PY'
import re
sections = {"msg": ("msg", "ascii", "hex", "m", "bits(m)"), "params": ("p", "bits(p)", "g")}
out = {name: [] for name in ("msg", "rsa", "params", "elgamal", "dh")}
for line in open("report/output.txt", encoding="utf-8"):
    key, value = line.rstrip("\n").split(" = ", 1)
    name = next((n for n, keys in sections.items() if key in keys), key.split(".")[0].replace("aes", "dh"))
    if len(value) > 90 and re.fullmatch(r"[0-9a-f]+", value):
        out[name].append(f"{key} =")
        out[name] += ["    " + value[i:i + 86] for i in range(0, len(value), 86)]
    else:
        out[name].append(f"{key} = {value}")
for name, lines in out.items():
    open(f"report/out_{name}.txt", "w", encoding="utf-8").write("\n".join(lines) + "\n")
PY
cd report
T="$HOME/.TinyTeX/bin/x86_64-linux"
"$T/latexmk" -pdf -pdflatex="$T/pdflatex -interaction=nonstopmode -halt-on-error" -silent Lab5_DanielNicorici_FAF-243.tex >/dev/null
"$T/latexmk" -c Lab5_DanielNicorici_FAF-243.tex >/dev/null
echo "built report/Lab5_DanielNicorici_FAF-243.pdf"
