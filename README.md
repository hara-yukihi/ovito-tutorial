# OVITO Tutorial (GUI and Python)

A beginner-friendly repository for visualizing and analyzing molecular dynamics (MD) results with [OVITO](https://www.ovito.org/).
The same dataset is used with both the **GUI (mouse operations)** and **Python (`pip install ovito`)**.

## Contents

| Folder | Description |
|---|---|
| [`data/`](data/) | Practice data `sample.xyz` (5 atoms × 30 frames) |
| [`gui/`](gui/README.md) | How to use the OVITO GUI (with screenshots) |
| [`pip/`](pip/README.md) | Installing the Python module and the render script `render_xyz.py` |

## Suggested order

1. Start with [`gui/README.md`](gui/README.md): open the data and play with it
2. Set up Python with [`pyip/README.md`](pip/README.md), and run `pip/render_xyz.py` on your own data

## About the practice data

`data/sample_xyz` is an artificial trajectory of SCFON molecule (it is not scientifically correct at all, just for demo).
`data/sample_original.xyz` is an artificial trajectory of a Cu FCC crystal (with some Ag near the center) that becomes increasingly disordered frame by frame.
It is not a physically correct MD simulation; it is only meant for practice.

File format (**repeated for every frame**):

```
5 ← line 1: number of atoms
frame 0 ← line 2: comment (frame number)
S     0.00000    0.00000    0.00000
C     1.68187    0.02677    0.00063
F     2.27988    1.21855    0.14151
O     2.20364   -0.84074    0.73030
N     2.11586   -0.42083   -1.10300
5
frame 1
...
```

> This format contains **no simulation cell (box) information**, so OVITO treats the system as non-periodic.
> If you need periodic boundaries, use the Extended XYZ format (with `Lattice="..."` on line 2) or the LAMMPS dump format.

## License

See [LICENSE](LICENSE).
