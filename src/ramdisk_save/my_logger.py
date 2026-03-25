"""logging setting"""

import logging
import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).parent.parent))
import settings


def my_logger(name: str) -> logging.Logger:
    """Configure logging"""
    _st = settings
    log_level = getattr(logging, _st.LOG_LEVEL)
    # 実行ディレクトリに依存しないよう、このファイルを基準に絶対パスを設定
    filename = str(pathlib.Path(__file__).parent / "Result.log")
    logging.basicConfig(
        level=log_level,
        filename=filename,
        format="%(asctime)s, %(levelname)s, %(message)s, %(lineno)d",
        force=True,
    )
    return logging.getLogger(name)


def shutdown() -> None:
    """Shutdown logging"""
    log = logging
    # loggingの終了処理を明示的に行う
    log.shutdown()
