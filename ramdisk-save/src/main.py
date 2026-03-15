"""main prosess"""

import pathlib
import subprocess
import sys

sys.path.append(str(pathlib.Path(__file__).parent.parent))
import settings


def list_dirs(path):
    list_dirs = []
    for d in pathlib.Path(path).iterdir():
        print(d)
        if d.is_dir():
            list_dirs.append(d.name)
    return list_dirs


src_dirs = list_dirs(settings.src)
dst_dirs = list_dirs(settings.dst)

if src_dirs == dst_dirs:
    subprocess.call(settings.cmd, shell=True)
