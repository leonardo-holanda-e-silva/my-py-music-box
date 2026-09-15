# SDD-02 — Play page

**ID:** `page.play`  
**Package:** `my_py_music_box.ui.pages.play`

## Purpose

Play an existing score. This is not the editor.

## Screen content

- Name of the open file (or “no score”)
- Controls: Play / Pause / Stop
- Playhead over a **read-only** view of the cylinder
- Effective BPM and volume (inherited from the score + Settings; volume always comes from Settings)
- Shortcut “Open in Composer” (switches page with the same score)

## Behavior

| Action | Result |
|---|---|
| Play with no file | Message; does not start a stream |
| Play | Engine renders and starts `sounddevice` |
| Playhead leaves the visible cylinder | The view scrolls so the current step stays on screen |
| Stop | Closes the stream; playhead disappears |
| Stop | Closes the stream; playhead disappears |
| Switch to Composer | Stops playback |
| File changes on disk | Does not reload by itself; Reload button |

## Out of scope for this page

- Clicking to place a pin
- Creating a new score
- Choosing a device (that is Settings)

## Done when

- [ ] Opens a valid `.caixa.json` and plays it
- [ ] Rejects invalid JSON without crashing
- [ ] Playhead follows the current step
- [ ] Viewport follows the playhead when it would leave the visible area (task `T-09`)
- [ ] Stop is immediate
