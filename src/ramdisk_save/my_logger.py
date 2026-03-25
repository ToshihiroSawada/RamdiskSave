"""logging setting"""

import logging
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
from settings import LOG_LEVEL


def my_logger(name: str) -> logging.Logger:
    """Configure logging"""
    log_level = getattr(logging, LOG_LEVEL)
    # 実行ディレクトリに依存しないよう、このファイルを基準に絶対パスを設定
    filename = str(Path(__file__).parent / "../../Result.log")
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
