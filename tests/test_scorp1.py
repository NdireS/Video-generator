"""Run with: python tests/test_scorp1.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "skills" / "scorp1" / "scripts"))
from scorp1 import align_script, caption_groups  # noqa: E402


def w(text, start, end):
    return {"text": text, "start": start, "end": end}


def test_align_script():
    # misheard name, an <unk> token, a split hyphen word and a filler
    heard = [w("Stayvore", 0.0, 0.8), w("is", 0.8, 0.9), w("um", 0.9, 1.0), w("short", 1.0, 1.4),
             w("stay", 1.4, 1.6), w("B<unk>B", 1.6, 2.0), w("hosts.", 2.0, 2.4)]
    got = align_script("Stavore is short-stay BnB hosts?", heard)
    assert [x["text"] for x in got] == ["Stavore", "is", "short-stay", "BnB", "hosts?"], got
    assert got[0]["start"] == 0.0 and got[2]["start"] == 1.0 and got[2]["end"] == 1.6, got
    assert got[-1]["end"] == 2.4, got
    # a script word the model didn't hear at all squeezes between its neighbours
    got = align_script("see your income", [w("see", 0.0, 0.2), w("income", 0.5, 0.9)])
    assert [x["text"] for x in got] == ["see", "your", "income"] and got[1]["start"] == 0.2, got
    assert align_script("anything", []) == []
    # a spoken URL heard as one word splits its time in order
    got = align_script("at stavore dot com", [w("at", 0.0, 0.2), w("stavor.com", 0.2, 1.1)])
    assert [x["start"] for x in got] == sorted(x["start"] for x in got), got


def test_caption_groups():
    words = [w(t, i * 0.4, i * 0.4 + 0.4) for i, t in enumerate("and saves it when you say YES.".split())]
    timing = {"vo": [{"text": "and saves it when you say YES.", "start": 0, "duration": 2.8, "words": words}]}
    assert [g["text"] for g in caption_groups(timing)] == ["and saves it when you say YES."]


if __name__ == "__main__":
    test_align_script()
    test_caption_groups()
    print("ok")
