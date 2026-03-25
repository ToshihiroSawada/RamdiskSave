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

        result = subprocess.run(
            r"C:\Windows\system32\cmd.exe",
            input=cmd,
            capture_output=True,
            text=True,
            check=True,
            encoding="cp932",
        )

        logger.info("コマンドが正常に実行されました。")
        if result.stdout:
            logger.info("標準出力:\n%s", result.stdout)
        if result.stderr:
            logger.warning("標準エラー出力:\n%s", result.stderr)
    except subprocess.CalledProcessError as e:
        logger.exception("コマンドの実行に失敗しました。")
        logger.exception("リターンコード: %s", e.returncode)
        logger.exception("標準出力:\n%s", e.stdout)
        logger.exception("標準エラー出力:\n%s", e.stderr)
