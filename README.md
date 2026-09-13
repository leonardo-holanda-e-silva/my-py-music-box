# My Py Music Box

Aplicativo desktop que emula uma caixinha de música clássica de **21 dentes** de aço.

Três páginas:

- **Play** — executa uma partitura
- **Composer** — cria e edita o cilindro (pinos)
- **Settings** — preferências do app

Software de **código aberto** (licença [MIT](LICENSE)).  
Propriedade de **[LHES Tech Solutions](https://lhes.tech)**.

Identidade visual: [`branding/PALETTE.md`](branding/PALETTE.md).

## Requisitos

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)

## Desenvolvimento

```bash
uv sync
uv run my-py-music-box
```

Testes:

```bash
uv run pytest
```

## Documentação (SDD)

Comece por [`docs/sdd/00-overview.md`](docs/sdd/00-overview.md).

## Empacotamento

Ver [`docs/sdd/05-infrastructure.md`](docs/sdd/05-infrastructure.md) e [`docs/sdd/06-packaging.md`](docs/sdd/06-packaging.md).

```bash
uv sync --group packaging
uv run briefcase create
uv run briefcase build
uv run briefcase package
```
