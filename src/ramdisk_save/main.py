"""main process"""

import subprocess
import sys
from pathlib import Path

from my_logger import my_logger

# プロジェクトのルートディレクトリをパスに追加
sys.path.append(str(Path(__file__).resolve().parents[2]))
from settings import cmd, dst, src


def list_dirs(path: str) -> list:
    """Get a list of folders directly under the specified path"""
    list_dirs = []
    if Path(path).exists() is False:
        return list_dirs

    list_dirs.extend(d for d in Path(path).iterdir() if d.is_dir())
    return list_dirs


if __name__ == "__main__":
    logger = my_logger(__name__)

    src_dirs = list_dirs(src)
    dst_dirs = list_dirs(dst)

    logger.info(src_dirs)
    logger.info(dst_dirs)

    # dst_dirsの方がフォルダ数が多い場合、ロードが正しく終了していないのでセーブしない
    if len(src_dirs) < len(dst_dirs):
        logger.info(
            "RAMディスクへのロードが正しく行われていません。セーブを中止します。",
        )
        sys.exit(1)

    try:
        logger.info("実行スクリプト:\n%s", cmd)

        # Robocopyの終了コードを正しく取得するため、cmd.exe経由(input)ではなく
        # 直接実行し(shell=False)、check=Falseで例外化を防止
        result = subprocess.run(  # noqa: S603
            cmd,
            shell=False,
            capture_output=True,
            text=True,
            check=False,
            encoding="cp932",
        )

        # エラー判定を強化:
        # 1. 終了コードが8以上（Robocopyの重大エラー）  # noqa: RUF003
        # 2. または、標準エラー出力に何かが出力されている（コマンドが見つからない、構文エラーなど）  # noqa: E501, RUF003
        if result.returncode >= 8 or result.stderr:  # noqa: PLR2004
            logger.error("コマンド実行エラー (Return Code: %s)", result.returncode)
            logger.error("標準出力:\n%s", result.stdout)
            logger.error("標準エラー出力:\n%s", result.stderr)
            sys.exit(result.returncode)

        logger.info("コマンドが正常に実行されました (Return Code: %s)", result.returncode)
        # 正常時は詳細ログをデバッグレベルに留める
        if result.stdout:
            logger.debug("標準出力:\n%s", result.stdout)
        if result.stderr:
            logger.debug("標準エラー出力:\n%s", result.stderr)

    except Exception:
        logger.exception("予期せぬエラーが発生しました。")
