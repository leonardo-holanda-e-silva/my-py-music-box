# T-09 — Play viewport follows the playhead

**SDD:** 02  
**Status:** doing

The Play cylinder already scrolls by hand (`QScrollArea`). During playback, if the playhead column leaves the visible rectangle, the view must shift so that column stays on screen.

Depends on T-03.

## Behavior

- While playing (and while paused with a playhead), keep the current step visible.
- Prefer scrolling horizontally with the cylinder; do not jump if the step is already inside the viewport.
- When playback stops, the playhead disappears; do not force a scroll reset unless useful.
- The user may still drag the scrollbar; the next playhead tick that goes off-screen follows again.

## Done when

- [ ] A 64-step score (for example `How Deep Is Your Music Box.caixa.json`) keeps the playhead in view as it walks past the right edge
- [ ] No jump/flicker while the playhead is still visible
- [ ] Stop still hides the playhead
