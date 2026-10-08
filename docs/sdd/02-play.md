# SDD-02 — Play (POC)

Library opens a score; Play renders the cylinder read-only.

Controls: Play / Pause / Stop, volume slider.

Engine renders NumPy audio to a temp WAV and plays via Kivy SoundLoader. Playhead follows `Engine.current_step()`.
