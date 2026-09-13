# SDD-03 — Página Composer

**ID:** `page.composer`  
**Pacote:** `my_py_music_box.ui.pages.composer`

## Propósito

Criar e editar o cilindro: pinos, passos, BPM da peça.

## Conteúdo da tela

- Grade 21 × N (dente × passo), editável
- Contador de pinos
- Campos: passos, BPM da partitura
- Botões: Novo, Abrir, Salvar, Salvar como, Exemplo, Limpar
- Pré-escuta curta de um dente ao clicar no rótulo da linha (opcional na v0.1; tarefa própria)

## Comportamento

- Clique na célula: toggle do pino
- Alterar `steps` descarta pinos com `step >= steps`
- Sujo (unsaved) bloqueia “Novo” até confirmar
- Salvar escreve `caixa-musica-v1` via ScoreStore
- Play não é responsabilidade desta página; “Testar” pode mandar o score em memória para o Engine **sem** gravar disco (tarefa `T-04`)

## Critérios de pronto

- [ ] Toggle de pino
- [ ] Round-trip JSON (salvar / abrir idêntico em pinos e metadados)
- [ ] Exemplo carrega a melodia de `examples/`
- [ ] Título da janela indica arquivo sujo com `*`
