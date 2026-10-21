**English** | [日本語](README.ja.md)

# OVITO Tutorial (GUI and Python)

A beginner-friendly repository for visualizing and analyzing molecular dynamics (MD) results with [OVITO](https://www.ovito.org/).
The same dataset is used with both the **GUI (mouse operations)** and **Python (`pip install ovito`)**.

## Contents

| Folder | Description |
|---|---|
| [`data/`](data/) | Practice data `sample.xyz` (256 atoms × 30 frames) |
| [`gui/`](gui/README.md) | How to use the OVITO GUI (with screenshots) |
| [`python/`](python/README.md) | Installing the Python module and the analysis script `analyze.py` |
| [`notebooks/`](notebooks/) | A Jupyter notebook to try things one cell at a time |

## Suggested order

1. Start with [`gui/README.md`](gui/README.md): open the data and play with it
2. Set up Python with [`python/README.md`](python/README.md)
3. Run [`notebooks/ovito_intro.ipynb`](notebooks/ovito_intro.ipynb) from top to bottom
4. Once comfortable, run `python/analyze.py` on your own data

## About the practice data

`data/sample.xyz` is an artificial trajectory of a Cu FCC crystal (with some Ag near the center) that becomes increasingly disordered frame by frame.
It is not a physically correct MD simulation; it is only meant for practice.

File format (**repeated for every frame**):

```
256              ← line 1: number of atoms
frame 0          ← line 2: comment (frame number)
Cu -0.03527 0.02392 0.04973   ← line 3+: element x y z
Cu 1.82732 1.67876 0.05763
...
256
frame 1
...
```

> This format contains **no simulation cell (box) information**, so OVITO treats the system as non-periodic.
> If you need periodic boundaries, use the Extended XYZ format (with `Lattice="..."` on line 2) or the LAMMPS dump format.

## License

See [LICENSE](LICENSE).
