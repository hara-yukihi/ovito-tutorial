# OVITO チュートリアル（GUI と Python）

分子動力学 (MD) シミュレーションの結果を、可視化・解析ソフト [OVITO](https://www.ovito.org/) で扱うための入門用リポジトリです。
同じデータを **GUI（マウス操作）** と **Python（`pip install ovito`）** の両方で扱います。

## 中身

| フォルダ | 内容 |
|---|---|
| [`data/`](data/) | 練習用データ `sample.xyz`（256原子 × 30フレーム） |
| [`gui/`](gui/) | OVITO GUI の使い方（スクリーンショット付き） |
| [`python/`](python/) | Python モジュールのインストールと解析スクリプト `analyze.py` |
| [`notebooks/`](notebooks/) | Jupyter で1セルずつ試せるノートブック |

## おすすめの順番

1. まず [`gui/README.md`](gui/README.md) で、データを開いて動かしてみる
2. 次に [`python/README.md`](python/README.md) で Python 環境を作る
3. [`notebooks/ovito_intro.ipynb`](notebooks/ovito_intro.ipynb) を上から実行する
4. 慣れたら `python/analyze.py` を自分のデータで動かす

## 練習用データについて

`data/sample.xyz` は、Cu の FCC 結晶（中心付近の一部が Ag）がフレームごとに乱れていく人工的な軌跡です。
物理的に正しい MD ではなく、操作練習用です。

ファイルの形式（**フレーム数だけ繰り返し**）:

```
256              ← 1行目: 原子数
frame 0          ← 2行目: コメント（フレーム番号）
Cu -0.03527 0.02392 0.04973   ← 3行目以降: 元素 x y z
Cu 1.82732 1.67876 0.05763
...
256
frame 1
...
```

> この形式には **シミュレーションセル（箱）の情報が入っていません**。そのため OVITO は周期境界なしの系として扱います。
> 周期境界を使いたい場合は、2行目に `Lattice="..."` を書く Extended XYZ 形式や LAMMPS の dump 形式を使ってください。

## ライセンス

[LICENSE](LICENSE) を参照してください。
