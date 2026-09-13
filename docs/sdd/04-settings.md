# SDD-04 — Página Settings

**ID:** `page.settings`  
**Pacote:** `my_py_music_box.ui.pages.settings`

A lista abaixo é o **mínimo viável**. Itens marcados TBD não entram na v0.1.

## v0.1 (definir e persistir)

| Chave | Tipo | Padrão | Efeito |
|---|---|---|---|
| `volume` | 0–100 | 70 | Ganho na saída |
| `audio_device` | id ou `"default"` | `"default"` | Device do sounddevice |
| `last_score_path` | path ou null | null | Play/Composer reabrem |
| `default_bpm` | 30–180 | 72 | Usado em partitura nova |
| `default_steps` | 8–64 | 32 | Usado em partitura nova |

Persistência: arquivo JSON em diretório de config do usuário  
(`platformdirs` ou `QStandardPaths.AppConfigLocation` / `my-py-music-box/settings.json`).

## Depois (TBD)

- Idioma da UI (pt / en)
- Tema claro / escuro
- Qualidade do pente (síntese vs samples gravados)
- Continuar tocando ao trocar de página
- Pasta padrão de partituras

## Comportamento

- Apply imediato para volume
- Device só aplica no próximo Play (evita cortar o stream no meio)
- Valores inválidos no arquivo de config caem no padrão, sem crash

## Critérios de pronto

- [ ] Volume sobrevive a fechar e abrir o app
- [ ] Device inválido volta para default e avisa
- [ ] Página não importa Engine além de listar devices
