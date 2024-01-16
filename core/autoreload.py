import os
from pathlib import Path

from django.utils.autoreload import autoreload_started


# Watch .conf files
def watch_extra_files(sender, *args, **kwargs):
    watch = sender.extra_files.add
    # List of file paths to watch
    watch_list = [
        './tmp.txt',
    ]
    for file in watch_list:
        print(1)
        if os.path.exists(file):
            watch(Path(file))


autoreload_started.connect(watch_extra_files)
