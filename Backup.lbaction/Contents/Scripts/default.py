#!/usr/bin/env python
#
# LaunchBar Action Script
#
import os
import sys
import datetime
import zipfile
import subprocess


class Backuper(object):
    parent_dir = os.path.expanduser('~/iCloud/Backups/Daily')

    def __init__(self, basename='backup'):
        self.dir = os.path.join(self.parent_dir, datetime.date.today().isoformat())
        zipname = '{}-{}.zip'.format(basename, datetime.datetime.now().strftime('%H%M%S'))
        self.zipfn = os.path.join(self.dir, zipname)

    def _ensure_dir(self):
        if os.path.exists(self.dir):
            if os.path.isdir(self.dir):
                pass
            else:
                raise RuntimeError('Can not create a backup dir.')
        else:
            os.mkdir(self.dir)

    def _add_to_zip(self, fn, zippath):
        if os.path.isdir(fn):
            self.zipfile.write(fn, zippath)
            for sf in os.listdir(fn):
                self._add_to_zip(os.path.join(fn, sf), os.path.join(zippath, sf))
        else:
            self.zipfile.write(fn, zippath)

    def __enter__(self):
        self._ensure_dir()
        self.zipfile = zipfile.ZipFile(self.zipfn, 'w')
        return self

    def __exit__(self, *args, **kwargs):
        self.zipfile.close()

    def __call__(self, fn):
        self._add_to_zip(fn, os.path.basename(fn))


if __name__ == '__main__':
    fn = sys.argv[1]

    with Backuper(os.path.basename(fn).lower()) as b:
        b(fn)

    notification_script = u'display notification "File to backuped to {}" with title "Backup Finish"'
    notification_script = notification_script.format(b.zipfn.decode('utf-8'))

    subprocess.call(['/usr/bin/osascript', '-e', notification_script])
