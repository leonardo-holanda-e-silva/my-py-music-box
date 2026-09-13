# SDD-00 — Visão geral e ligação entre componentes

**App:** My Py Music Box  
**Versão do documento:** 0.1.0  
**Status:** vigente  
**Repo:** https://github.com/leonardo-holanda-e-silva/my-py-music-box

Este arquivo é o mapa. Os demais SDD descrevem uma fatia. Se houver conflito, este overview + o contrato da partitura vencem.

## 1. Objetivo

Emular o mecanismo de uma caixinha de música:

- um **pente** de 21 dentes (alturas fixas)
- um **cilindro** com pinos
- rotação a um BPM constante
- som metálico de lâmina, não piano nem sample orquestral

O usuário entra por três páginas: Play, Composer, Settings.

## 2. Não-objetivos (nesta versão)

- Mais de 21 alturas
- Motor MIDI / SoundFont (pode virar backend depois, sem mudar o contrato)
- Conta na nuvem ou sync
- Notação clássica (pentagrama)

## 3. Mapa de documentos

| Arquivo | Responsabilidade |
|---|---|
| [00-overview.md](00-overview.md) | Ligação, limites, fluxo |
| [01-domain.md](01-domain.md) | Pente, cilindro, partitura |
| [02-play.md](02-play.md) | Página Play |
| [03-composer.md](03-composer.md) | Página Composer |
| [04-settings.md](04-settings.md) | Página Settings |
| [05-infrastructure.md](05-infrastructure.md) | Pacote Python, uv, testes |
| [06-packaging.md](06-packaging.md) | Instaladores Win / macOS / Linux |
| [../tasks/README.md](../tasks/README.md) | Fila de tarefas ligadas aos SDD |

## 4. Componentes e dependências

```
                    ┌────────────┐
                    │  Settings  │  preferências persistidas
                    └─────┬──────┘
                          │ lê
┌─────────┐         ┌─────▼──────┐         ┌──────────┐
│  Play   │────────▶│  Engine    │◀────────│ Composer │
└─────────┘  toca   │  (áudio +  │  grava  └──────────┘
                    │   score)   │
                    └─────┬──────┘
                          │
              ┌───────────┼───────────┐
              ▼           ▼           ▼
         AudioBank    ScoreStore   AudioOut
         (21 dentes)  (JSON)       (sounddevice)
```

- **UI** (`src/my_py_music_box/ui`) — shell com 3 páginas; não sintetiza som.
- **Score** (`src/my_py_music_box/score`) — lê/valida/grava `caixa-musica-v1`.
- **Audio** (`src/my_py_music_box/audio`) — banco de 21 dentes + mixer + device.
- **App** (`src/my_py_music_box/app.py`) — cria janela, carrega settings, roteia páginas.

Regras:

1. Play e Composer **não** se conhecem. Os dois falam com Score + Engine.
2. Settings **não** toca áudio. Só altera valores que Engine e UI lêem.
3. A partitura no disco é a fonte da verdade da melodia. Estado da UI é descartável.

## 5. Fluxos

### Abrir e tocar
Settings → último arquivo (se houver) → ScoreStore.load → Play.render → Engine.play

### Compor
Composer edita pinos em memória → Save → ScoreStore.write → Play pode recarregar o mesmo arquivo

### Trocar página
O shell troca o widget visível. O Engine para ao sair de Play, salvo se Settings definir “continuar em background” (não existe ainda; padrão = parar).

## 6. Stack

| Camada | Escolha |
|---|---|
| Linguagem | Python ≥ 3.11 |
| UI | PyQt5 |
| Áudio | NumPy + sounddevice |
| Projeto / lock | **uv** (`pyproject.toml` + `uv.lock`) |
| Empacote | Briefcase (ver SDD-06) |
| Licença | MIT — código aberto, propriedade da LHES Tech Solutions (https://lhes.tech) |
| Visual | `branding/PALETTE.md` + `ui/theme.py` |

A descrição antiga do GitHub cita Tkinter. A implementação vigente é **PyQt5**.

## 7. Como usar estes docs numa conversa

1. Abrir este overview.
2. Abrir o SDD da página ou da infra em discussão.
3. Abrir a tarefa em `docs/tasks/` se houver ID.
4. Só então ler o `.py` correspondente.
