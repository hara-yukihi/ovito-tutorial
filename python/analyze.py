"""Example of using the OVITO Python module (pip install ovito).

Reads a multi-frame xyz file and does four things:
  1. Computes the mean squared displacement (MSD) of every frame and plots it
  2. Counts the fraction of FCC atoms per frame with Common Neighbor Analysis (CNA)
  3. Compares the radial distribution function (RDF) of the first and last frames
  4. Renders cross-section snapshots of the first and last frames

Usage (run from the top folder of the repository):
    python python/analyze.py data/sample.xyz
    python python/analyze.py data/sample.xyz --cutoff 4.0 --outdir results
"""
import argparse
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # save PNGs even on machines without a display
import matplotlib.pyplot as plt
import numpy as np

from ovito.io import import_file
from ovito.modifiers import (
    CalculateDisplacementsModifier,
    CommonNeighborAnalysisModifier,
    CoordinationAnalysisModifier,
    SliceModifier,
)
from ovito.vis import TachyonRenderer, Viewport

ALLOWED_SUFFIXES = {".xyz"}


def parse_args():
    """Read command-line arguments and check that the values are valid."""
    parser = argparse.ArgumentParser(description="Analyze a multi-frame xyz file with OVITO")
    parser.add_argument("xyz", help="input file (.xyz)")
    parser.add_argument("--cutoff", type=float, default=4.0,
                        help="RDF cutoff radius in Å (default: 4.0)")
    parser.add_argument("--outdir", default="results",
                        help="folder for the results (default: results)")
    args = parser.parse_args()

    # Check the input file: it must exist and have the .xyz extension
    path = Path(args.xyz)
    if not path.is_file():
        sys.exit(f"Error: file not found: {path}")
    if path.suffix.lower() not in ALLOWED_SUFFIXES:
        sys.exit(f"Error: please give an .xyz file: {path}")
    # Keep the cutoff within a sensible positive range
    if not (0.5 <= args.cutoff <= 20.0):
        sys.exit("Error: --cutoff must be between 0.5 and 20.0 Å")
    return path, args.cutoff, Path(args.outdir)


def main():
    xyz_path, cutoff, outdir = parse_args()
    outdir.mkdir(parents=True, exist_ok=True)

    # --- 1. Load ------------------------------------------------------------
    # import_file automatically reads all frames of a multi-frame file
    pipeline = import_file(str(xyz_path))
    n_frames = pipeline.source.num_frames
    print(f"Loaded: {xyz_path}  ({n_frames} frames)")

    # --- 2. Add modifiers (the same ones you add in the GUI's right panel) --
    # Displacements relative to frame 0. The xyz file has no cell, so there are
    # no periodic boundaries.
    pipeline.modifiers.append(CalculateDisplacementsModifier(reference_frame=0))
    # Crystal structure identification (FCC / HCP / BCC / ICO / Other)
    pipeline.modifiers.append(CommonNeighborAnalysisModifier())
    # Radial distribution function (RDF)
    pipeline.modifiers.append(
        CoordinationAnalysisModifier(cutoff=cutoff, number_of_bins=100))

    # --- 3. Compute every frame in turn -------------------------------------
    msd, fcc_frac = [], []
    rdf_first = rdf_last = None
    for frame in range(n_frames):
        data = pipeline.compute(frame)

        disp = data.particles["Displacement Magnitude"]
        msd.append(np.mean(disp ** 2))

        n_fcc = data.attributes["CommonNeighborAnalysis.counts.FCC"]
        fcc_frac.append(n_fcc / data.particles.count)

        if frame == 0:
            rdf_first = data.tables["coordination-rdf"].xy()
        if frame == n_frames - 1:
            rdf_last = data.tables["coordination-rdf"].xy()

    # --- 4. Save the results ------------------------------------------------
    frames = np.arange(n_frames)
    np.savetxt(outdir / "msd_fcc.txt", np.column_stack([frames, msd, fcc_frac]),
               header="frame  MSD[A^2]  FCC_fraction", fmt="%d %.6f %.4f")

    fig, axes = plt.subplots(1, 3, figsize=(13, 3.8))
    axes[0].plot(frames, msd, "o-")
    axes[0].set(xlabel="frame", ylabel="MSD [Å²]", title="Mean squared displacement")
    axes[1].plot(frames, fcc_frac, "o-", color="tab:green")
    axes[1].set(xlabel="frame", ylabel="FCC fraction", ylim=(0, 1),
                title="CNA: FCC fraction")
    axes[2].plot(rdf_first[:, 0], rdf_first[:, 1], label="frame 0")
    axes[2].plot(rdf_last[:, 0], rdf_last[:, 1], label=f"frame {n_frames - 1}")
    axes[2].set(xlabel="r [Å]", ylabel="g(r)", title="RDF")
    axes[2].legend()
    fig.tight_layout()
    fig.savefig(outdir / "analysis.png", dpi=150)
    print(f"Saved: {outdir / 'analysis.png'}, {outdir / 'msd_fcc.txt'}")

    # --- 5. Render snapshots ------------------------------------------------
    # To render, the pipeline has to be added to the scene.
    # CNA colors atoms by structure (green = FCC, white = Other).
    # We render the first and last frames to compare how the crystal breaks down.
    # Surface atoms are not identified as FCC and appear white, so Slice keeps
    # only a thin layer in the middle to show the interior.
    # (The analysis above is already done, so adding Slice here does not change it.)
    zc = float(np.mean(pipeline.compute(0).particles.positions[:, 2]))
    pipeline.modifiers.append(SliceModifier(normal=(0, 0, 1), distance=zc, slab_width=4.0))
    pipeline.add_to_scene()
    vp = Viewport(type=Viewport.Type.Top)  # look straight down the z axis
    vp.zoom_all()
    for frame, name in [(0, "snapshot_first.png"), (n_frames - 1, "snapshot_last.png")]:
        vp.render_image(filename=str(outdir / name), size=(800, 600),
                        frame=frame, renderer=TachyonRenderer())
        print(f"Saved: {outdir / name}")


if __name__ == "__main__":
    main()
