# Wave portrait — how to reproduce it

The hero artwork: a photograph rendered as horizontal signal traces, coloured
by amplitude with the `signal` ramp (dodgerblue → pale → orange).

Script: `portrait_wave.py`. Output: a single self-contained SVG.

---

## Quick start

Conda:

```bash
conda env create -f environment.yml
conda activate wave-portrait
python portrait_wave.py bio-photo-optimized.jpg -o assets/wave.svg
```

Or pip:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python portrait_wave.py bio-photo-optimized.jpg -o assets/wave.svg
```

Three env files are provided: `environment.yml` (conda, lower bounds),
`requirements.txt` (pip, same bounds), and `environment-lock.yml` with the
exact versions the artwork was verified against — reach for the lock file only
if regenerating ever stops matching.

`conda-forge` is required; `scikit-image` on the `defaults` channel lags far
enough behind to matter.

That is exactly the frozen version — `--ramp signal` is the default, as are
all the other parameters below. Verified: run with no flags on the same source
photo and every path, coordinate and colour matches the approved artwork
exactly (1906 paths, 180 KB); the only textual difference is the `aria-label`.

---

## How it works

Five steps.

**1 — Crop and resize.** Centre-crop to 4:5, resize to 416 × 520, convert to
grayscale in `[0, 1]`.

**2 — Subject mask, by focus not by brightness.** This is the part that
matters. Compute `E = gaussian(|laplace(gaussian(I, 1))|, 9)`, normalise, and
threshold at `0.13`. Sharp regions are the subject; the defocused background
falls an order of magnitude below.

| region | E |
|---|---|
| background corners | 0.02 |
| background mid-frame | 0.04 |
| face | 0.40 |
| clothing | 0.46 |

Then closing (disk 9) → fill holes → largest connected component → opening
(disk 4) → fill holes.

> **Why not brightness?** On this photo the face sits at 0.51, the sweater at
> 0.19, the corridor at 0.73. Otsu splits it into *dark things* vs *bright
> things*, so the "silhouette" comes out as the sweater blob and the face
> lands in the background. Every brightness threshold tried grabbed ~60 % of
> the frame because the corridor has dark vertical slats that touch the
> subject. Focus separates cleanly and ignores tone entirely.

**3 — Darkness field.** CLAHE local contrast equalisation
(`equalize_adapthist`, clip 0.02) at **native resolution before the
downscale** — the flat studio lighting leaves the face with almost no dynamic
range otherwise, and equalising after the resize gives a visibly different
result. Then `D = 1 - gaussian(I, σ=2)`, so `D = 1` is dark (subject) and
`D = 0` is light. The blur is essential — without it every trace turns into
hair-fuzz noise. Note the mask uses *raw* luminance while the traces use the
*equalised* one.

**4 — Sample rows.** 72 evenly spaced rows. Each averages the darkness over
±3 px vertically, then a 7-tap moving average along x. Outside the mask the
value is forced to 0, so traces flatten to a dead line over the background.
Amplitude is `D^1.35`, and each trace is drawn at `y = y₀ − D(x)·A`.

**5 — Colour by amplitude.** Amplitude is quantised into 6 buckets. Each row
is split at bucket boundaries into separate runs, so one trace changes colour
as it rises over the face — the colour is data, not decoration. Stroke width
rises with the bucket too (0.75 + 0.22·b), so bright is also heavy.

---

## Parameters

| Flag | Default | Effect |
|---|---|---|
| `--ramp` | `signal` | `signal`, `ember`, `accent`, `duo`, `mono` |
| `--rows` | `72` | More rows = finer, denser, bigger file |
| `--buckets` | `6` | Colour and width steps |
| `--width` | `416` | Working width; height follows `--aspect` |
| `--aspect` | `0.8` | Crop w/h. `0.8` = 4:5 |
| `--sigma` | `2.0` | Blur before sampling. **The most sensitive knob** |
| `--gamma` | `1.35` | >1 suppresses midtones, sharpens the subject |
| `--amp` | `1.95` | Amplitude in units of row spacing. >2 makes rows collide |
| `--step` | `2` | x sampling in px. Raise to shrink the file |
| `--focus-threshold` | `0.13` | Subject/background cut |
| `--no-mask` | off | Skip background removal |
| `--no-equalize` | off | Skip CLAHE. Use on already-contrasty photos |
| `--clip-limit` | `0.02` | CLAHE strength. Higher = harsher |
| `--stroke` / `--stroke-step` | `0.75` / `0.22` | Base weight and per-bucket increment |

`mono` emits no stroke colour and uses `currentColor`, so CSS drives it —
useful if a light theme ever lands.

---

## Tuning

- **Traces look like noise** → raise `--sigma` to 3.
- **Face has dissolved** → lower `--sigma` to 1.5, or lower `--gamma` to 1.1.
- **Rows collide** → lower `--amp` to 1.6, or raise `--rows`.
- **Too flat / low contrast** → raise `--gamma` to 1.6, or `--clip-limit 0.04`.
- **Blotchy / over-processed** → `--clip-limit 0.01`, or `--no-equalize` if the
  photo already has strong contrast.
- **File too big** → `--step 3 --rows 56`. Roughly halves it with little
  visible loss. 163 KB → 77 KB in testing.

## Troubleshooting the mask

The script prints the subject coverage. **Expect 50–70 %.**

- **"focus mask is empty"** → lower `--focus-threshold` to 0.06.
- **Coverage > 90 %** → the background is in focus too. Raise the threshold to
  0.25, or use `--no-mask` and accept background ripples.
- **Coverage < 20 %** → only part of the subject was caught. Lower to 0.08.
- **Background is sharp (no bokeh)** → focus segmentation will not work at
  all. Cut the subject out manually and run with `--no-mask`.

---

## Using it on the site

It ships inside the reveal component, layered over the photograph:

```html
<div class="reveal soft" data-reveal="pointer" tabindex="0" role="slider"
     aria-label="Reveal the wave rendering of the portrait"
     aria-valuemin="0" aria-valuemax="100" aria-valuenow="50">
  <img src="assets/portrait.jpg" alt="Mattia Piazza">
  <div class="art"><img src="assets/wave.svg" alt="" aria-hidden="true"></div>
  <div class="seam"></div>
</div>
```

Styles live in `custom.scss` under `.reveal`; behaviour in `assets/reveal.js`.

**Layering gotcha.** `clip-path` clips the element's background as well, so the
revealed layer needs `background: $mp-bg` in CSS — otherwise this SVG is
transparent, the photo shows through the gaps between traces, and the reveal
appears to do nothing. If you cannot control the CSS, bake the backdrop in
instead:

```bash
python portrait_wave.py photo.jpg -o wave.svg --background '#111310'
```

The SVG has no external dependencies and no embedded raster — pure paths, so
it stays crisp at any size.

**Palette rule — resolved.** Orange appears once per page *in type*; blue
means clickable *in type and chrome*. Generated artwork is exempt, because its
colour encodes data rather than decorating. `--ramp accent` remains a drop-in
if that ever feels like a cheat. See `DESIGN_NOTES.md` §2.

## Other renderers explored

Same 4-step pipeline, different step 5. Not kept, but cheap to rebuild:
surface plot with hidden-line removal, amplitude modulation, telemetry channel
stack, phase-space rings, RRT\* over the portrait as free space, trajectory
streamlines, Fourier epicycles of the silhouette and facial features, and a
velocity-profile version where each row is solved by forward–backward passes
and coloured by which constraint is active.
