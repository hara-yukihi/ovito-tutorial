# OVITO を Python から使う（pip 版）

`pip install ovito` で、GUI と同じ解析機能を Python スクリプトから使えます。
大量のファイルを同じ手順で解析したいときや、結果をグラフにしたいときに便利です。

## 1. Python を用意する

**Python 3.11 以上** が必要です（ovito 3.17 の場合）。ターミナルで確認:

```bash
python --version
```

入っていなければ https://www.python.org/downloads/ からインストールしてください。
（Windows ではインストール時に **Add python.exe to PATH** にチェック）

> Intel CPU の Mac は、最新版の ovito では対応していない場合があります。うまく入らない時は相談してください。

## 2. 仮想環境を作ってインストール

仮想環境 (venv) は、このチュートリアル専用の Python の部屋のようなものです。他のプロジェクトとパッケージが混ざりません。
リポジトリの一番上のフォルダ（`README.md` がある場所）で実行します。

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

行頭に `(.venv)` と表示されていれば仮想環境に入っています。次回からは `activate` の行だけ実行すれば OK です。

インストールできたか確認:

```bash
python -c "import ovito; print(ovito.version_string)"
```

## 3. 解析スクリプトを動かす

```bash
python python/analyze.py data/sample.xyz
```

`results/` フォルダに次のファイルができます。

| ファイル | 内容 |
|---|---|
| `analysis.png` | MSD・FCC 割合・RDF のグラフ |
| `msd_fcc.txt` | フレームごとの数値 |
| `snapshot_first.png` / `snapshot_last.png` | 最初と最後のフレームの断面画像 |

オプション:

```bash
python python/analyze.py data/sample.xyz --cutoff 5.0 --outdir my_results
```

## 4. ノートブックで1つずつ試す

```bash
jupyter lab
```

ブラウザが開いたら `notebooks/ovito_intro.ipynb` を開き、上のセルから `Shift + Enter` で実行します。

## GUI との対応

| GUI の操作 | Python |
|---|---|
| File → Load File | `pipeline = import_file("data/sample.xyz")` |
| Add modification... | `pipeline.modifiers.append(CommonNeighborAnalysisModifier())` |
| タイムスライダーでフレーム移動 | `data = pipeline.compute(frame)` |
| Render active viewport | `Viewport(...).render_image(...)` |

## うまくいかない時

- **`ModuleNotFoundError: No module named 'ovito'`** → 仮想環境に入っていない可能性があります。`activate` をやり直してください。
- **Linux サーバーで画像の描画だけ失敗する (Vulkan のエラー)** → `sudo apt install mesa-vulkan-drivers` などで Vulkan ドライバを入れる必要があります。グラフと数値の出力までは問題なく動きます。
- 公式ドキュメント: https://docs.ovito.org/python/
