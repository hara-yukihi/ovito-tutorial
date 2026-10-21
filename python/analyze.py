"""OVITO Python モジュール (pip install ovito) の使い方サンプル。

multi-frame の xyz ファイルを読み込み、次の4つを行う:
  1. 各フレームの平均二乗変位 (MSD) を計算してグラフにする
  2. 共通近接解析 (CNA) で FCC 構造の割合をフレームごとに数える
  3. 最初と最後のフレームの動径分布関数 (RDF) を比べる
  4. 最初と最後のフレームの断面スナップショットを描画する

使い方 (リポジトリの一番上のフォルダで実行):
    python python/analyze.py data/sample.xyz
    python python/analyze.py data/sample.xyz --cutoff 4.0 --outdir results
"""
import argparse
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # 画面の無い環境でも PNG 保存できるようにする
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
    """コマンドライン引数を読み、値が妥当かを確認する。"""
    parser = argparse.ArgumentParser(description="OVITO で multi-frame xyz を解析する")
    parser.add_argument("xyz", help="入力ファイル (.xyz)")
    parser.add_argument("--cutoff", type=float, default=4.0,
                        help="RDF のカットオフ半径 [Å] (既定: 4.0)")
    parser.add_argument("--outdir", default="results",
                        help="結果を保存するフォルダ (既定: results)")
    args = parser.parse_args()

    # 入力ファイルのチェック: 存在するか・拡張子が .xyz か
    path = Path(args.xyz)
    if not path.is_file():
        sys.exit(f"エラー: ファイルが見つかりません: {path}")
    if path.suffix.lower() not in ALLOWED_SUFFIXES:
        sys.exit(f"エラー: .xyz ファイルを指定してください: {path}")
    # カットオフは正の妥当な範囲に限定する
    if not (0.5 <= args.cutoff <= 20.0):
        sys.exit("エラー: --cutoff は 0.5〜20.0 Å の範囲で指定してください")
    return path, args.cutoff, Path(args.outdir)


def main():
    xyz_path, cutoff, outdir = parse_args()
    outdir.mkdir(parents=True, exist_ok=True)

    # --- 1. 読み込み -------------------------------------------------------
    # import_file はフレームが複数あれば自動でまとめて読み込む
    pipeline = import_file(str(xyz_path))
    n_frames = pipeline.source.num_frames
    print(f"読み込み: {xyz_path}  ({n_frames} フレーム)")

    # --- 2. モディファイア（GUI の右側パネルに追加するものと同じ）を積む ----
    # フレーム0を基準にした変位。xyz にはセル情報が無いので周期境界は考えない。
    pipeline.modifiers.append(CalculateDisplacementsModifier(reference_frame=0))
    # 結晶構造の判定 (FCC / HCP / BCC / ICO / Other)
    pipeline.modifiers.append(CommonNeighborAnalysisModifier())
    # RDF (動径分布関数)
    pipeline.modifiers.append(
        CoordinationAnalysisModifier(cutoff=cutoff, number_of_bins=100))

    # --- 3. 全フレームを順番に計算 -----------------------------------------
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

    # --- 4. 結果を保存 -----------------------------------------------------
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
    print(f"保存: {outdir / 'analysis.png'}, {outdir / 'msd_fcc.txt'}")

    # --- 5. スナップショットを描画 -----------------------------------------
    # 描画するにはパイプラインをシーンに追加する。
    # CNA が原子を構造ごとに色付けする（緑=FCC, 白=Other）。
    # 最初と最後のフレームを描いて、結晶が崩れていく様子を比べる。
    # 表面の原子は FCC と判定されず白いので、Slice で中央の薄い層だけ残して内部を見せる。
    # （解析はもう終わっているので、ここで追加しても上の数値には影響しない）
    zc = float(np.mean(pipeline.compute(0).particles.positions[:, 2]))
    pipeline.modifiers.append(SliceModifier(normal=(0, 0, 1), distance=zc, slab_width=4.0))
    pipeline.add_to_scene()
    vp = Viewport(type=Viewport.Type.Top)  # 真上 (z 方向) から見る
    vp.zoom_all()
    for frame, name in [(0, "snapshot_first.png"), (n_frames - 1, "snapshot_last.png")]:
        vp.render_image(filename=str(outdir / name), size=(800, 600),
                        frame=frame, renderer=TachyonRenderer())
        print(f"保存: {outdir / name}")


if __name__ == "__main__":
    main()
