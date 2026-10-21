[English](README.md) | **日本語**

# OVITO GUI の使い方

マウス操作だけで、`data/sample.xyz` を開いて・動かして・解析して・画像にするまでをやります。

## 1. インストール

1. https://www.ovito.org/ の Download ページから **OVITO Basic**（無料版）をダウンロード
2. 自分の OS（Windows / macOS / Linux）用のインストーラーを実行

> 有料の OVITO Pro でなくても、このチュートリアルの内容は全部 Basic でできます。

## 2. データを読み込む

1. このリポジトリの緑の **Code** ボタン → **Download ZIP** でダウンロードして展開
2. OVITO を起動し、メニューの **File → Load File** から `data/sample.xyz` を選ぶ
3. 列の対応を聞く画面が出たら、1列目 = `Particle Type`、2〜4列目 = `Position.X / Y / Z` になっていることを確認して **OK**

![ファイルを読み込んだところ](images/01_load_file.png)

## 3. 見た目を動かす

| 操作 | やり方 |
|---|---|
| 回転 | 左ドラッグ（Perspective ビュー） |
| 移動 | 中ボタンドラッグ（または右ドラッグ） |
| ズーム | ホイール |
| 全体を表示 | ビューポート左上の名前をクリック → **Adjust View / Zoom all**、またはダブルクリック |

## 4. アニメーション（複数フレーム）

画面下のタイムスライダーでフレームを切り替えられます。▶ ボタンで再生。
`sample.xyz` は 30 フレームあり、結晶が少しずつ乱れていく様子が見えます。

![タイムスライダー](images/02_timeline.png)

## 5. モディファイアで解析する

右側のパイプラインの **Add modification...** から次を追加してみてください。

1. **Common neighbor analysis** — 結晶構造ごとに色が付く（緑 = FCC、白 = Other）
2. **Slice** — Normal を `(0, 0, 1)`、Slab width を `4` くらいにすると、中の断面が見える
3. **Calculate displacements** — フレーム0からどれだけ動いたかを計算
4. **Color coding** — Input property を `Displacement Magnitude` にすると動いた量で色分け

![モディファイアを追加したところ](images/03_modifiers.png)

> 表面の原子が白い（FCC と判定されない）のは、周期境界が無く近接原子が足りないためです。Slice で中を見ると緑になっています。

## 6. 画像・動画を保存する

1. 右上のタブから **Render**（カメラのアイコン）を開く
2. **Save to file** にチェックを入れて保存先を指定
3. 静止画: **Render active viewport**
4. 動画: Rendering range を **Complete animation** にして、ファイル名を `.mp4` や `.gif` にしてから Render

![レンダリング設定](images/04_render.png)

## 7. セッションを保存する

**File → Save Session State** で、追加したモディファイアや視点を `.ovito` ファイルとして保存できます。次回はこれを開けば同じ状態から再開できます。
