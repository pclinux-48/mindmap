#!/usr/bin/env python3
# filepath: /Users/paulocesar/Documents/IFGoiano/1-Direito e Cidadania/5 Sem/midmap.py
# Gera mindmap_radial.dot / .svg / .png a partir de mindmap.md usando layout radial (twopi)

import re
import shutil
import textwrap
import subprocess
from pathlib import Path

p = Path(__file__).parent
src = p / "mindmap.md"
dot = p / "mindmap_radial.dot"
out_svg = p / "mindmap_radial.svg"
out_png = p / "mindmap_radial.png"

if not src.exists():
    print("Arquivo mindmap.md não encontrado em:", src)
    raise SystemExit(1)

lines = src.read_text(encoding="utf-8").splitlines()

# paleta por nível (nível 0 = root)
PALETTE = [
    {"fill": "#1f77b4", "font": "white", "shape": "oval", "fontsize": 16, "width": 3.2, "height": 1.2},  # root
    {"fill": "#2ca02c", "font": "white", "shape": "box",  "fontsize": 12, "width": 2.4, "height": 0.8},  # nível 1
    {"fill": "#ff7f0e", "font": "black", "shape": "box",  "fontsize": 10, "width": 2.0, "height": 0.7},  # nível 2
    {"fill": "#9467bd", "font": "white", "shape": "note", "fontsize": 9,  "width": 1.8, "height": 0.6},   # nível 3+
]

nodes = []
edges = []
indent_levels = []
parent_stack = {}
cnt = 0

def make_id(i):
    return f"n{i}"

def wrap_label(text, width=36):
    parts = []
    for para in text.splitlines():
        w = textwrap.wrap(para, width=width, break_long_words=True, replace_whitespace=False)
        parts.extend(w if w else [""])
    return "<BR/>".join([p.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;") for p in parts])

for raw in lines:
    if not raw.strip():
        continue
    if raw.strip().startswith("mindmap"):
        continue
    line = raw.replace('\t', '    ')
    indent = len(re.match(r'^\s*', line).group(0))
    text = line.strip()
    m = re.search(r'\(\((.*)\)\)', text)
    label_raw = m.group(1).strip() if m else text
    if indent not in indent_levels:
        indent_levels.append(indent)
        indent_levels.sort()
    level = indent_levels.index(indent)
    cnt += 1
    nid = make_id(cnt)
    label_html = wrap_label(label_raw)
    nodes.append((nid, label_html, level))
    if level > 0 and (level-1) in parent_stack:
        edges.append((parent_stack[level-1], nid))
    parent_stack[level] = nid
    for k in list(parent_stack.keys()):
        if k > level:
            del parent_stack[k]

# determine root node id (first node)
root_id = nodes[0][0] if nodes else "n1"

dot_lines = [
    'digraph G {',
    f'  graph [layout=twopi, overlap=false, splines=true, root="{root_id}", sep="+0.5", nodesep=0.6];',
    '  node [style="filled,rounded", penwidth=1.0, fontname="Helvetica"];',
    '  edge [arrowhead=none, color="#666666", pensize=1.0];',
]

# define nodes with per-level styles and HTML labels
for nid, label_html, level in nodes:
    style = PALETTE[min(level, len(PALETTE)-1)]
    fill = style["fill"]
    fontcolor = style["font"]
    shape = style["shape"]
    fsz = style["fontsize"]
    width = style.get("width", 1.8)
    height = style.get("height", 0.6)
    # root recebe destaque (maior e negrito)
    if level == 0:
        node_label = f'< <B><FONT POINT-SIZE="{fsz}" COLOR="{fontcolor}">{label_html}</FONT></B> >'
        extra = 'penwidth=1.8'
    else:
        node_label = f'< <FONT POINT-SIZE="{fsz}" COLOR="{fontcolor}">{label_html}</FONT> >'
        extra = ''
    # fixedsize ajuda a manter proporções no layout radial
    dot_lines.append(f'  {nid} [label={node_label}, shape={shape}, fillcolor="{fill}", fontname="Helvetica", width={width}, height={height}, fixedsize=false {"," + extra if extra else ""}];')

# edges
for a, b in edges:
    dot_lines.append(f'  {a} -> {b};')

dot_lines.append('}')

dot.write_text("\n".join(dot_lines), encoding="utf-8")
print("DOT gerado em:", dot)

if shutil.which("dot"):
    try:
        # usar -Ktwopi garante o engine radial; -Groot já está definido no .dot
        subprocess.run(["dot", "-Ktwopi", "-Tsvg", str(dot), "-o", str(out_svg)], check=True)
        subprocess.run(["dot", "-Ktwopi", "-Tpng", str(dot), "-o", str(out_png)], check=True)
        print("SVG gerado em:", out_svg)
        print("PNG gerado em:", out_png)
    except subprocess.CalledProcessError as e:
        print("Erro ao renderizar com dot:", e)
else:
    print("Graphviz (dot) não encontrado. Instale com: brew install graphviz")
    print("Para gerar manualmente: dot -Ktwopi -Tsvg mindmap_radial.dot -o mindmap_radial.svg && dot -Ktwopi -Tpng mindmap_radial.dot -o mindmap_radial.png")