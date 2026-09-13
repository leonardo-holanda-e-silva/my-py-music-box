from my_py_music_box.score.model import Score, Pin


def test_round_trip():
    score = Score(steps=16, bpm=60, pins=[Pin(0, 3), Pin(0, 3), Pin(4, 7)])
    data = score.to_dict()
    again = Score.from_dict(data)
    assert again.steps == 16
    assert again.bpm == 60
    assert [(p.step, p.tooth) for p in again.pins] == [(0, 3), (4, 7)]


def test_rejects_bad_format():
    try:
        Score.from_dict({"format": "nope", "pins": []})
    except ValueError:
        return
    raise AssertionError("deveria rejeitar format")
