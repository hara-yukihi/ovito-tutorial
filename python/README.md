**English** | [日本語](README.ja.md)

# Using OVITO from Python (pip version)

With `pip install ovito`, you get the same analysis features as the GUI, from Python scripts.
This is handy when you want to analyze many files the same way or turn results into plots.

## 1. Get Python

**Python 3.11 or later** is required (for ovito 3.17). Check in a terminal:

```bash
python --version
```

If Python is not installed, get it from https://www.python.org/downloads/
(On Windows, check **Add python.exe to PATH** during installation.)

> Macs with Intel CPUs may not be supported by the latest ovito release. Ask if installation fails.

## 2. Create a virtual environment and install

A virtual environment (venv) is like a private room for this tutorial's Python packages, so they do not mix with other projects.
Run these commands in the top folder of the repository (where `README.md` is).

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -r python/requirements.txt
```

**Windows (PowerShell)**

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install -U pip
python -m pip install -r python/requirements.txt
```

If `(.venv)` appears at the start of the prompt, you are inside the virtual environment. Next time, you only need to run the `activate` line.

Check the installation:

```bash
python -c "import ovito; print(ovito.version_string)"
```

## 3. Run the analysis script

```bash
python python/analyze.py data/sample.xyz
```

The following files are created in the `results/` folder:

| File | Contents |
|---|---|
| `analysis.png` | Plots of MSD, FCC fraction and RDF |
| `msd_fcc.txt` | Per-frame values |
| `snapshot_first.png` / `snapshot_last.png` | Cross-section images of the first and last frames |

Options:

```bash
python python/analyze.py data/sample.xyz --cutoff 5.0 --outdir my_results
```

## 4. Try things step by step in the notebook

```bash
jupyter lab
```

When the browser opens, open `notebooks/ovito_intro.ipynb` and run the cells from the top with `Shift + Enter`.

## GUI ↔ Python

| GUI action | Python |
|---|---|
| File → Load File | `pipeline = import_file("data/sample.xyz")` |
| Add modification... | `pipeline.modifiers.append(CommonNeighborAnalysisModifier())` |
| Move the time slider | `data = pipeline.compute(frame)` |
| Render active viewport | `Viewport(...).render_image(...)` |

## Troubleshooting

- **`ModuleNotFoundError: No module named 'ovito'`** → You are probably not inside the virtual environment. Run the `activate` line again.
- **Only image rendering fails on a Linux server (Vulkan error)** → Install a Vulkan driver, e.g. `sudo apt install mesa-vulkan-drivers`. Plots and numeric output work without it.
- Official documentation: https://docs.ovito.org/python/
