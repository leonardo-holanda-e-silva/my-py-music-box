from my_py_music_box.db.repository import Repository
from my_py_music_box.score.model import Pin, Score


def test_sqlite_round_trip(tmp_path):
    repo = Repository(tmp_path / "app.db")
    score = Score(steps=16, bpm=80, pins=[Pin(0, 3), Pin(4, 7)])
    score_id = repo.insert_score("Demo", score, source="user")
    loaded = repo.get_score(score_id)
    assert loaded is not None
    assert loaded.title == "Demo"
    assert loaded.score.bpm == 80
    assert [(p.step, p.tooth) for p in loaded.score.pins] == [(0, 3), (4, 7)]

    repo.set_volume(55)
    assert repo.get_volume() == 55
    repo.set_default_steps(64)
    assert repo.get_default_steps() == 64
    repo.set_last_score_id(score_id)
    assert repo.get_last_score_id() == score_id

    assert repo.delete_score(score_id) is True
    assert repo.get_score(score_id) is None
    repo.close()


def test_seed_builtins(tmp_path):
    repo = Repository(tmp_path / "app.db")
    repo.seed_builtins()
    scores = repo.list_scores()
    assert len(scores) >= 1
    assert all(s.source == "builtin" for s in scores)
    # second seed is a no-op
    repo.seed_builtins()
    assert len(repo.list_scores()) == len(scores)
    repo.close()
