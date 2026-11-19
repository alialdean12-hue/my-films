# 73 collage motions (keys for the JSON)

Item keys: `enter`, `effect` (+`effect_at`, `fx`), `loop` (+`until`), `exit` (+`exit_at`), `size`: hero 62% · main 45% · small 32% · icon 13% of width.
Beat keys: `transition`, `camera: [{"kind","at",...}]`. Full working example: `examples/motions_demo.json`.
**Boil (12) only on characters** (`"loop":"boil"`), never on everything.

| # | Motion | Key |
|---|---|---|
| 10 | squash & stretch hop | enter `hop` |
| 13 | drop with bounce | enter `bounce` |
| 14 | slide in | enter `left/right/top/bottom` |
| 15 | spin in | enter `spin` |
| 16 | zoom from a point | enter `zoom` |
| 20 | tossed on the table | enter `toss` |
| 21 | taped down | enter `tape` (photo) |
| 22 | pinned | enter `pin` |
| 23 | lowered on a string | enter `string` |
| – | pop / drop / fade | enter `pop` `drop` `fade` |
| 17 | paper mask pulled off | effect `mask_reveal` |
| 18 / 19 | out of envelope / secret folder | effect `envelope` / `folder` |
| 2 / 3 | crumple & throw / uncrumple | effect `crumple` / `uncrumple` |
| 4 | sticker peeled off | effect `peel` |
| 5 / 24 | unfold / fold | effect `unfold` / `fold` |
| 7 | card flip | effect `flip` (`fx.back_svg`) |
| 25 | origami | effect `origami` |
| 26 | roll into a tube | effect `roll` |
| 27 | corner curls in wind | effect `curl` |
| 28 | paper waves | effect `wave` |
| 29 | paper plane | effect `plane` |
| 1 | torn in two | effect `tear` |
| 6 | strips in / out | effect `shred_in` / `shred_out` |
| 30 | strip torn from middle | effect `strip` |
| 31 | scissors cut | effect `scissors` |
| 32 | torn hole grows | effect `hole` |
| 33 | shatters into pieces | effect `shatter` |
| 34 | shredder | effect `shredder` |
| 35 | crop & enlarge a detail | effect `crop_zoom` (`fx.cx,cy,tx,ty,k`) |
| 40 | polaroid develops | effect `polaroid` |
| 57 | magnifier over a photo | effect `magnifier` (`fx.path,r,k`) |
| 8 | swing on a pin | loop `swing` |
| 12 | paper boil (characters) | loop `boil` |
| 45–51 | float, breathe, tremble, wind, parallax(`depth`), slow spin, flicker | loop `float` `breathe` `tremble` `wind` `parallax` `spin` `flicker` |
| – | exits | exit `fly_left` `fly_right` `drop` `shrink` `fade` |
| 11 | stamp slam + shake | text `style:"stamp"` (enter `slam`) |
| 52 / 53 / 54 | circle / arrow / underline | types `circle` `arrow` `underline` |
| 55 | scribble strike | type `strike` |
| 56 | yellow marker | `[y]..[/y]` in text |
| 58 | red string between pins | type `string` (`points`) |
| 59 | sticky note | text `style:"note"` (enter `stick`) |
| 60 | ✓ / ✗ drawn | types `check` / `cross` |
| 61 / 62 | map + route / pins drop | type `map` (`route`, `pins`) |
| 63 | timeline | type `timeline` (`events`) |
| 64 | bar chart rises | type `chart` (`values`, `labels`) |
| 65 | clock hands turn | type `clock` (`from`, `to`) |
| 66 | calendar pages flip | type `calendar` (`days`, `month`) |
| 67 | typewriter | text `style:"typed"`, `enter:"type"` |
| 73 | fast montage | type `montage` (`assets`, `every`) |
| 9, 36–39, 41–44 | punch, burn, ink, brush, scan, curtain, zoom_into, tear_screen, sheet (+`cut`) | beat `transition` |
| 68–72 | flash, spotlight, shake, snap_zoom, focus | beat `camera` |

Each motion has its own sound (rip, crumple, snip, thud, whoosh, pop) added automatically.
