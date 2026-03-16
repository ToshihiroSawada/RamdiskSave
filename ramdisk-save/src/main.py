"""main prosess"""

import pathlib
import subprocess
import sys

import my_logger

sys.path.append(str(pathlib.Path(__file__).parent.parent))
import settings


def list_dirs(path: str) -> list:
    """Get a list of folders directly under the specified path"""
    list_dirs = []
    for d in pathlib.Path(path).iterdir():
        print(d)
        if d.is_dir():
            list_dirs.append(d.name)
    return list_dirs


if __name__ == "__main__":
    logger = my_logger.my_logger(__name__)

    src_dirs = list_dirs(settings.src)
    dst_dirs = list_dirs(settings.dst)

    logger.info(src_dirs)
    logger.info(dst_dirs)

    if src_dirs == dst_dirs:
        try:
            logger.info(f"実行スクリプト:\n{settings.cmd}")

            # settings.cmdが複数行のスクリプトの場合、shell=Trueで直接渡すのではなく、
            # シェルの標準入力に渡すのが最も確実な方法です。
            # 'cmd.exe'を起動し、inputパラメータでスクリプトを渡します。
            result = subprocess.run(
                "cmd.exe",
                input=settings.cmd,
                capture_output=True,
                text=True,
                check=True,
                encoding="cp932",
            )

            logger.info("コマンドが正常に実行されました。")
            if result.stdout:
                logger.info(f"標準出力:\n{result.stdout}")
            if result.stderr:
                logger.warning(f"標準エラー出力:\n{result.stderr}")
        except subprocess.CalledProcessError as e:
            logger.error("コマンドの実行に失敗しました。")
            logger.error(f"リターンコード: {e.returncode}")
            logger.error(f"標準出力:\n{e.stdout}")
            logger.error(f"標準エラー出力:\n{e.stderr}")
