# RamdiskSave

RAMディスク上のデータを永続化（バックアップ）するためのPythonスクリプトです。
ロード（復元）が正しく行われていない可能性がある場合に、バックアップ先を空のデータや不完全なデータで上書きしてしまう事故を防ぐためのチェック機能を備えています。

## 機能

*   **安全なバックアップ**: ソース（RAMディスク）とバックアップ先（HDD/SSD）のフォルダ数を比較し、ソース側が少ない場合は「ロード失敗」とみなして保存処理を中止します。
*   **外部コマンド実行**: バックアップ処理自体は `robocopy` などの外部コマンド（`settings.py` で指定）を利用して行います。
*   **ログ出力**: 実行結果やエラー内容は `src/ramdisk_save/Result.log` に記録されます。

## 動作環境

*   Windows
*   Python 3.x

## ディレクトリ構成

```text
RamdiskSave/
├── src/
│   └── ramdisk_save/
│       ├── main.py          # メインスクリプト
│       └── my_logger.py     # ログ設定
|── settings.py              # 設定ファイル（ユーザー作成）
└── README.md
```

## セットアップ

ルートディレクトリ直下に `settings.py` を作成し、以下の変数を定義してください。

```python
# src/settings.py の例
src = r"R:\Path\To\Ramdisk"      # RAMディスクのパス
dst = r"D:\Backups\RamdiskSave"  # 保存先のパス
LOG_LEVEL = "INFO"               # ログレベル (INFO, DEBUG, WARNING など)

# 実行するコマンド（例: robocopy）
# 標準入力として cmd.exe に渡されます
cmd = f'robocopy /E /COPY:DAT /DCOPY:DAT /MIR /W:5 /R:3 /LOG:"{log_path}" /TEE "{src}" "{dst}"'
```

## 実行方法

プロジェクトのルートディレクトリで以下のコマンドを実行します。

```powershell
.venv\Scripts\pythonw.exe src/ramdisk_save/main.py
```