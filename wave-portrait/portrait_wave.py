#!/usr/bin/env python3
"""
portrait_wave.py — turn a photograph into a wave-trace portrait as SVG.

Each horizontal row of the image becomes one signal trace whose amplitude is
the local darkness of the subject. Traces are split into runs by amplitude and
coloured from a ramp, so a single trace changes colour as it rises over the
face. The background is removed by focus (defocused = background), not by
brightness, which is what makes it work on a photo where the skin is brighter
than the clothing.

    python portrait_wave.py photo.jpg -o wave.svg

Requires: numpy, pillow, scikit-image, scipy
    pip install numpy pillow scikit-image scipy
"""

import argparse
import sys

import warnings

import numpy as np
from PIL import Image, ImageOps
from scipy import ndimage as ndi
from skimage import exposure, filters, morphology, transform


# ── colour ramps ──────────────────────────────────────────────────────────
# Stops are interpolated to `--buckets` steps. Low amplitude first.
RAMPS = {
    # blue -> pale -> orange. Both brand colours, full range.
    "signal": ["#22303C", "#1E90FF", "#BFD8E8", "#E8722F"],
    # greys warming into orange at the peaks.
    "ember":  ["#2B2E29", "#5F5C57", "#A8927E", "#E8722F"],
    # near-monochrome, accent only in the top bucket.
    "accent": ["#3A3D38", "#5F5C57", "#8C8880", "#E8722F"],
    # straight complementary blend. Loudest.
    "duo":    ["#1E90FF", "#4E7FA8", "#9A7A6E", "#E8722F"],
    # single colour, let CSS decide via currentColor.
    "mono":   None,
}


def hex_lerp(c1, c2, t):
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02X%02X%02X" % tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def build_ramp(stops, n):
    out = []
    for i in range(n):
        t = i / (n - 1) * (len(stops) - 1)
        k = min(int(t), len(stops) - 2)
        out.append(hex_lerp(stops[k], stops[k + 1], t - k))
    return out


# ── image preparation ─────────────────────────────────────────────────────
def load_luminance(path, width, aspect, equalize, clip_limit):
    """Centre-crop to `aspect` (w:h), return (raw, tone) at `width` px.

    `raw` is plain grayscale, used for the focus mask. `tone` is optionally
    CLAHE-equalised and used for the trace amplitudes. Equalisation happens at
    native resolution *before* the downscale — doing it after gives a
    noticeably different result.
    """
    im = Image.open(path).convert("RGB")
    w, h = im.size
    tw, th = int(h * aspect), h
    if tw > w:
        tw, th = w, int(w / aspect)
    im = im.crop(((w - tw) // 2, 0, (w - tw) // 2 + tw, th))
    full = np.asarray(ImageOps.grayscale(im), dtype=float) / 255.0

    height = int(round(width / aspect))
    raw = transform.resize(full, (height, width), anti_aliasing=True)
    if equalize:
        tone = transform.resize(
            exposure.equalize_adapthist(full, clip_limit=clip_limit),
            (height, width), anti_aliasing=True)
    else:
        tone = raw
    return raw, tone


def focus_mask(raw, threshold, min_size=2000):
    """Subject mask from defocus: sharp regions are the subject.

    A blurred |Laplacian| measures local high-frequency energy. On a portrait
    with a defocused background this separates subject from background by
    roughly an order of magnitude, regardless of tone — which brightness
    thresholding cannot do when skin is brighter than clothing.
    """
    energy = filters.gaussian(np.abs(filters.laplace(filters.gaussian(raw, 1.0))), 9)
    energy /= energy.max()

    m = energy > threshold
    m = morphology.closing(m, morphology.disk(9))
    m = ndi.binary_fill_holes(m)
    m = morphology.remove_small_objects(m, min_size)
    if not m.any():
        raise SystemExit("focus mask is empty — lower --focus-threshold")

    lab, _ = ndi.label(m)
    m = lab == (np.bincount(lab.ravel())[1:].argmax() + 1)   # largest blob
    m = morphology.opening(m, morphology.disk(4))
    return ndi.binary_fill_holes(m)


# ── trace generation ──────────────────────────────────────────────────────
def traces(darkness, mask, rows, step, amp, gamma, buckets):
    """Yield (bucket, [(x, y), ...]) runs of constant colour bucket."""
    H, W = darkness.shape
    xs = np.arange(0, W, step)
    for i in range(rows):
        yi = int(i / (rows - 1) * (H - 1))
        lo, hi = max(0, yi - 3), yi + 4
        band = np.convolve(darkness[lo:hi].mean(axis=0), np.ones(7) / 7, mode="same")

        if mask is not None:
            in_subject = mask[lo:hi].any(axis=0)
            vals = np.where(in_subject[xs], band[xs], 0.0)
        else:
            vals = band[xs]
        vals = vals ** gamma

        y0 = (i + 0.5) / rows * H
        ys = y0 - vals * (H / rows) * amp
        b = np.clip((vals * buckets).astype(int), 0, buckets - 1)

        run, cur = [], b[0]
        for k in range(len(xs)):
            if b[k] != cur and run:
                if len(run) > 1:
                    yield cur, run
                run, cur = [(xs[k - 1], ys[k - 1])], b[k]
            run.append((xs[k], ys[k]))
        if len(run) > 1:
            yield cur, run


def to_svg(runs, W, H, colours, buckets, base_width, width_step, background=None):
    grouped = [[] for _ in range(buckets)]
    for b, run in runs:
        grouped[b].append(run)

    body = ""
    for bi, group in enumerate(grouped):
        if not group:
            continue
        paths = "".join(
            '<path d="M' + " ".join(f"{x:.0f},{y:.1f}" for x, y in r) + '"/>'
            for r in group
        )
        stroke = f'stroke="{colours[bi]}" ' if colours else ""
        body += f'<g {stroke}stroke-width="{base_width + bi * width_step:.2f}">{paths}</g>'

    stroke_attr = "" if colours else ' stroke="currentColor"'
    # An opaque backdrop is required whenever the SVG is layered over another
    # image (e.g. a clip-path reveal) — otherwise the layer underneath shows
    # through the transparent gaps between traces.
    backdrop = (f'<rect width="{W}" height="{H}" fill="{background}"/>'
                if background else "")
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'role="img" aria-label="Portrait rendered as signal traces">'
        f'{backdrop}'
        f'<g fill="none"{stroke_attr} stroke-linecap="round" '
        f'stroke-linejoin="round">{body}</g></svg>'
    )


def main():
    warnings.filterwarnings("ignore", category=FutureWarning)

    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("image")
    p.add_argument("-o", "--out", default="wave.svg")
    p.add_argument("--ramp", default="signal", choices=sorted(RAMPS))
    p.add_argument("--rows", type=int, default=72,
                   help="number of traces (default 72)")
    p.add_argument("--buckets", type=int, default=6,
                   help="colour/width steps (default 6)")
    p.add_argument("--width", type=int, default=416,
                   help="working width in px (default 416)")
    p.add_argument("--aspect", type=float, default=0.8,
                   help="crop aspect w/h (default 0.8 = 4:5)")
    p.add_argument("--sigma", type=float, default=2.0,
                   help="blur before sampling (default 2.0)")
    p.add_argument("--gamma", type=float, default=1.35,
                   help="amplitude contrast; >1 flattens midtones (default 1.35)")
    p.add_argument("--amp", type=float, default=1.95,
                   help="amplitude as a multiple of row spacing (default 1.95)")
    p.add_argument("--step", type=int, default=2,
                   help="x sampling step in px; raise to shrink the file")
    p.add_argument("--focus-threshold", type=float, default=0.13)
    p.add_argument("--no-mask", action="store_true",
                   help="skip background removal")
    p.add_argument("--no-equalize", action="store_true",
                   help="skip CLAHE local contrast equalisation")
    p.add_argument("--clip-limit", type=float, default=0.02,
                   help="CLAHE clip limit (default 0.02)")
    p.add_argument("--background", default=None, metavar="HEX",
                   help="opaque backdrop, e.g. '#111310'. Required when the "
                        "SVG is layered over another image")
    p.add_argument("--stroke", type=float, default=0.75)
    p.add_argument("--stroke-step", type=float, default=0.22)
    args = p.parse_args()

    raw, tone = load_luminance(args.image, args.width, args.aspect,
                               not args.no_equalize, args.clip_limit)
    H, W = raw.shape

    mask = None if args.no_mask else focus_mask(raw, args.focus_threshold)
    if mask is not None:
        print(f"subject covers {mask.mean():.1%} of the frame", file=sys.stderr)

    darkness = 1.0 - filters.gaussian(tone, sigma=args.sigma)

    stops = RAMPS[args.ramp]
    colours = build_ramp(stops, args.buckets) if stops else None

    runs = traces(darkness, mask, args.rows, args.step,
                  args.amp, args.gamma, args.buckets)
    svg = to_svg(runs, W, H, colours, args.buckets,
                 args.stroke, args.stroke_step, args.background)

    with open(args.out, "w") as f:
        f.write(svg)
    print(f"wrote {args.out} ({len(svg) / 1024:.0f} KB)", file=sys.stderr)


if __name__ == "__main__":
    main()
