# SDD-01 — Domínio: pente, cilindro, partitura

## Pente

21 dentes, índice 0…20, nomes fixos:

```
G4 A4 B4 C5 D5 E5 F5 G5 A5 B5 C6 D6 E6 F6 G6 A6 B6 C7 D7 E7 F7
```

- Uma altura por dente.
- O mesmo dente pode ser pinado em vários passos.
- Não há dinâmica por pino nesta versão.

## Cilindro

- `steps`: número de colunas (8–64, padrão 32).
- `steps_per_beat`: padrão 4 (cada passo = semicolcheia se o beat é semínima).
- `bpm`: 30–180.
- Cada célula `(step, tooth)` tem no máximo um pino.

## Contrato de arquivo — `caixa-musica-v1`

Extensão preferida: `.caixa.json`

```json
{
  "format": "caixa-musica-v1",
  "notes": ["G4", "…", "F7"],
  "steps": 32,
  "bpm": 68,
  "steps_per_beat": 4,
  "pins": [
    {"step": 0, "tooth": 3, "note": "C5"}
  ]
}
```

Regras de validação:

- `format` obrigatório e igual a `caixa-musica-v1`
- `tooth` ∈ [0, 20]
- `step` ∈ [0, steps)
- `note`, se presente, deve coincidir com `NOTE_NAMES[tooth]`
- pinos duplicados `(step, tooth)` são colapsados

Arquivos inválidos não tocam; a UI mostra o erro e não altera a partitura em memória.

## Engine

Entrada: partitura válida + volume + device.  
Saída: buffer float32 44.1 kHz mono, misturando os 21 samples deslocados no tempo.

O timbre vive em `audio/` (síntese de dente). Trocar o gerador de sample **não** muda o contrato JSON.
