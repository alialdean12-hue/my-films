"""Style 11 · وثائقي كولاج: the documentary engine (doc.py) with collage layers:
a real full-screen photo + a cut-out sticker of the key person/object ("sticker": {"query", "pick", "x", "y", "size"}),
torn-paper captions with a yellow marker on the key word, red marker circles and arrows (doc overlays).
  python3 hybrid.py video.json OUTDIR [--preview]"""
import os
__STYLE__ = "hybrid"
_p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "doc.py")
exec(compile(open(_p).read(), _p, "exec"))
