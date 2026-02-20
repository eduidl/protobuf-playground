# protobuf-playground

`proto2` / `proto3` の「空バイナリをデコードしたときの挙動」を、
Python（`google.protobuf`）と Rust（`prost`）で比較するための検証リポジトリです。

## 対象
- `proto/proto2_sample.proto`
- `proto/proto3_sample.proto`
- 検証対象フィールド:
  - `required`（proto2）
  - `optional`（scalar / message）
  - `optional` + `[default = ...]`（proto2）
  - `repeated`
  - `oneof`

## ディレクトリ構成
- `proto/`: 比較対象 `.proto`
- `python/`: Python 実装（`run_checks.py`）
- `rust/`: Rust 実装（`cargo run` で検証）

## 前提環境
- `protoc`（このリポジトリでは `libprotoc 3.21.12` で確認）
- Python 3 + `google.protobuf`（`4.21.12` で確認）
- Rust toolchain（`cargo` / `rustc`、このリポジトリでは `1.93.x` で確認）

## 動作確認（Python）
1. Python 用コード生成

```bash
mkdir -p python/gen
protoc --proto_path=proto --python_out=python/gen \
  proto/proto2_sample.proto proto/proto3_sample.proto
```

2. チェック実行

```bash
python3 python/run_checks.py
```

成功時は `All checks passed` を表示し、失敗時は `assert` で非0終了します。

## 動作確認（Rust）
```bash
cd rust
cargo run
```

- `build.rs` が `../proto/*.proto` を `prost-build` でコンパイルし、`rust/src/gen/` に生成します。
- 成功時は `All Rust/prost compatibility assertions passed.` を表示し、失敗時は `assert` で非0終了します。

## 共通点（Python / Rust）
- 空バイナリ入力後、`repeated` は空（`len == 0` / `Vec::is_empty()`）。
- `oneof` は未選択（`WhichOneof(...) is None` / `Option::None`）。
- `optional` な message は未設定扱い（presence は false / `None`）。
- `proto3 optional scalar` は presence を持つ（Python では `HasField`、Rust では `Option<T>`）。

## 主な違い（Python / Rust）
- presence API の提供形態
  - Python: `HasField`, `WhichOneof`, `IsInitialized` がある。
  - Rust(prost): `HasField` / `IsInitialized` 相当 API はなく、`Option<T>` / `Vec<T>` / 値型で表現。
- `proto2 required` の扱い
  - Python: 空入力後に required 未設定なら `IsInitialized() == False` を確認できる。
  - Rust(prost): 明示的な初期化検査APIはなく、デコード後は型のデフォルト値として読める。
- `proto2 optional + default`
  - Python: `HasField(...) == False` でも読み取り値は default（例: `7`）。
  - Rust(prost): 生値は `None` を保持しつつ、getter（例: `opt_with_default()`）で effective default を取得できる。
- `proto3` の非 optional scalar presence
  - Python: `HasField("plain_int")` は `ValueError`。
  - Rust(prost): そもそも presence 情報を持たず、値（例: `0`）のみを扱う。

## 検証仕様の要点
- すべて空バイナリ（Python: `ParseFromString(b"")` / Rust: `Message::decode(&[][..])`）で検証。
- 具体的な検証ロジック:
  - Python: `python/run_checks.py`
  - Rust: `rust/src/main.rs`

## 補足
- 詳細な比較表は `docs/compat-matrix.md` を参照。
- 言語別READMEの詳細は本READMEへ統合済み。
