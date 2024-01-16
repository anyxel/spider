import asyncio
import os
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from django.core.management.base import BaseCommand
from django.conf import settings

from core.helper import send_message_to_websocket, send_message_to_websocket_async


class TempTxtFileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        elif event.src_path.endswith('tmp.txt'):
            print(f'Temp.txt file {event.src_path} has been modified')

            # Trigger your desired actions here
            # For example, run Django management commands, update database, etc.

            asyncio.run(send_message_to_websocket_async('got'))

            f = open("tmp.txt", "r")
            print(f.read())


class Command(BaseCommand):
    help = 'Watch for changes in tmp.txt files and trigger actions'

    def handle(self, *args, **options):
        path_to_watch = os.path.join(settings.BASE_DIR, '')  # Change this to the directory where your temp.txt file is located
        event_handler = TempTxtFileHandler()

        observer = Observer()
        observer.schedule(event_handler, path=path_to_watch, recursive=False)
        observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
