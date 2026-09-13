# SDD-05 — Infraestrutura do código

## Layout

```
my-py-music-box/
  pyproject.toml          # uv + briefcase
  uv.lock                 # gerar com `uv lock` e commitar
  LICENSE                 # MIT
  .gitignore              # template do repo
  README.md
  docs/sdd/               # este conjunto
  docs/tasks/
  examples/               # partituras de exemplo
  packaging/              # notas e assets de instalador
  src/my_py_music_box/
    app.py                # entrypoint
    ui/shell.py           # janela + navegação
    ui/pages/play.py
    ui/pages/composer.py
    ui/pages/settings.py
    score/model.py
    score/store.py
    audio/bank.py
    audio/engine.py
  tests/
```

## Coordenação com uv

Fonte da verdade de dependências: `pyproject.toml`.

```bash
uv sync                     # cria .venv e instala
uv lock                     # atualiza uv.lock
uv run my-py-music-box      # sobe o app
uv run pytest
uv add pacote               # runtime
uv add --group dev pacote
uv add --group packaging briefcase
```

Não usar `requirements.txt` como fonte. O arquivo antigo do protótipo foi aposentado.

Python mínimo: 3.11.

## Pacote

- Código importável em `src/my_py_music_box`
- Script: `my-py-music-box`
- Testes não importam PyQt5 quando testam só score/áudio puro (quando possível)

## Qualidade

- Ruff no grupo `dev`
- Pytest para validação do JSON e mixer
- Sem rede em runtime

## O que o .gitignore já cobre

O `.gitignore` do repositório é o template Python padrão (inclui `.venv`, `dist/`, `build/`, `*.spec` do PyInstaller).  
`uv.lock` **não** está ignorado (a linha está comentada): o lock deve ser versionado.
