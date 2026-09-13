# SDD-02 — Página Play

**ID:** `page.play`  
**Pacote:** `my_py_music_box.ui.pages.play`

## Propósito

Executar uma partitura já existente. Não é o editor.

## Conteúdo da tela

- Nome do arquivo aberto (ou “nenhuma partitura”)
- Controles: Tocar / Pausar / Parar
- Playhead sobre uma **vista somente leitura** do cilindro
- BPM e volume efetivos (herdados da partitura + Settings; volume sempre de Settings)
- Atalho “Abrir no Composer” (troca de página com o mesmo score)

## Comportamento

| Ação | Resultado |
|---|---|
| Tocar sem arquivo | Mensagem; não inicia stream |
| Tocar | Engine renderiza e dispara `sounddevice` |
| Parar | Fecha stream; playhead some |
| Trocar para Composer | Para a reprodução |
| Arquivo muda no disco | Não recarrega sozinho; botão Recarregar |

## Fora de escopo desta página

- Clicar para cravar pino
- Criar partitura nova
- Escolher device (isso é Settings)

## Critérios de pronto

- [ ] Abre um `.caixa.json` válido e toca
- [ ] Rejeita JSON inválido sem crash
- [ ] Playhead acompanha o passo corrente
- [ ] Stop é imediato
