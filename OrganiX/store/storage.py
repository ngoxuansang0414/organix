from django.core.files.storage import Storage
from django.conf import settings
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STATICFILES_DIRS = os.path.join(BASE_DIR, "static_dev")
if settings.DEBUG:
    root = STATICFILES_DIRS
else:
    root = settings.STATIC_ROOT


class StaticStorage(Storage):
    def _open(self, name, mode="rb"):
        file_path = os.path.join(root, name)
        return open(file_path, mode)

    def _save(self, name, content):
        file_path = os.path.join(root, name)
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(file_path, "wb+") as f:
            for chunk in content.chunks():
                f.write(chunk)

        return name

    def exists(self, name):
        return os.path.exists(os.path.join(root, name))

    def url(self, name):
        return os.path.join(settings.STATIC_URL, name)
