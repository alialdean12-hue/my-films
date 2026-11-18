"""Narrator puppet parts for the episode builder.
parts() -> dict(defs, bg, puppet, head). The puppet has groups: larm, rarm, eyes; head is separate (tilts)."""
import os, re
_here = os.path.dirname(os.path.abspath(__file__))
def parts():
    ns = {}
    exec(open(os.path.join(_here, "host_src.py")).read(), ns)
    inner = re.search(r'<svg[^>]*>(.*)</svg>', ns["svg"], re.S).group(1)
    hi = inner.index('<g transform="rotate(-8 540 470)">')
    de = inner.index('</defs>') + 7
    body = inner[de:hi]
    be = body.index('<g filter="url(#glow)">')
    return dict(defs=inner[:de], bg=body[:be], puppet=body[be:], head=inner[hi:])
