# Mindmap Radial (midmap.py)

Gera um mapa mental radial (DOT → SVG/PNG) a partir de um arquivo `mindmap.md`. Útil para visualizar hierarquias com o nó central em destaque.

## Arquivos principais
- `midmap.py` — script Python que converte `mindmap.md` em `mindmap_radial.dot` e renderiza `mindmap_radial.svg` / `mindmap_radial.png`.
- `mindmap.md` — entrada em formato indentado (ex.: seu arquivo atual).
- `mindmap_radial.dot`, `mindmap_radial.svg`, `mindmap_radial.png` — artefatos gerados.

## Pré-requisitos (macOS)
- Python 3 (python3)
- Graphviz (dot)
  - Instalar: `brew install graphviz`

## Formato do `mindmap.md`
- Começar com a linha `mindmap`
- Hierarquia por indentação (espaços ou tabs)
- Para rótulos longos usar `((texto longo aqui))` — o script extrai o conteúdo entre parênteses duplos.
- Exemplo:
  mindmap
    root((Nó central))
      Tópico A
        Subtópico A1

## Como executar
Tornar executável (opcional) e rodar:
- `chmod +x midmap.py`
- `./midmap.py`
ou
- `python3 midmap.py`

Os arquivos `.dot`, `.svg` e `.png` serão gerados na mesma pasta.

Se receber erro de "import: command not found", verifique se o shebang (`#!/usr/bin/env python3`) está na primeira linha do `midmap.py` e execute com `python3`.

## Personalização rápida
- Editar paleta de cores / formas / tamanhos: variável `PALETTE` dentro de `midmap.py`.
- Mudar distância radial / engine: alterar `graph [layout=twopi, ...]` ou usar outro engine (`-Ktwopi` já usado).
- Layout alternativo (horizontal): ajustar `rankdir=LR` e usar `dot` normal (`dot -Tsvg`).

## Troubleshooting
- "Graphviz (dot) não encontrado": instalar com `brew install graphviz`
- Layout feio ou sobreposição: experimente ajustar `sep`, `nodesep` ou os tamanhos (`width`, `height`) em `PALETTE`.

## Publicando no GitHub (exemplo rápido)
1. `git init`
2. `git add .`
3. `git commit -m "Add midmap generator"`
4. Criar repositório no GitHub e seguir instruções para `git remote add origin ...` e `git push -u origin main`

## Licença
MIT — sinta-se livre para adaptar.

Se quiser eu gero um `LICENSE` (MIT) e um `.gitignore` básico para Python. Deseja isso?