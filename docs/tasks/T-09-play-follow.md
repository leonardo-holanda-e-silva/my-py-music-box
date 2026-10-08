# T-09 — Play viewport follows the playhead

**SDD:** 02  
**Status:** done

During playback, if the playhead column leaves the visible rectangle, `reveal_step` scrolls the cylinder so that column stays on screen. No jump while the step is still visible. Stop still hides the playhead.
