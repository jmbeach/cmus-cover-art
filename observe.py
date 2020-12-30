import sys
import os
from os import path
import subprocess
import re
from functools import reduce
import imghdr
import traceback
import eyed3


class SongData(object):
    def __init__(self, song_status, file, artist, album, disc_number, track, title, date, duration):
        self.status: str = song_status
        self.file: str = file
        self.artist: str = artist
        self.album: str = album
        self.disc_number: int = disc_number
        self.track: int = track
        self.title: str = title
        self.date: str = date
        self.duration: str = duration


def get_song_data():
    status = sys.argv[sys.argv.index('status') + 1]
    file = sys.argv[sys.argv.index('file') + 1]
    artist = sys.argv[sys.argv.index('artist') + 1]
    album = sys.argv[sys.argv.index('album') + 1]
    disc_number = None
    if 'discnumber' in sys.argv:
        disc_number = sys.argv[sys.argv.index('discnumber') + 1]
    track = sys.argv[sys.argv.index('tracknumber') + 1]
    title = sys.argv[sys.argv.index('title') + 1]
    date = sys.argv[sys.argv.index('date') + 1]
    duration = sys.argv[sys.argv.index('duration') + 1]
    return SongData(status, file, artist, album, disc_number, track, title, date, duration)

def clean_string(s: str):
    reg_clean = r'[a-zA-Z0-9]+'
    cleaned: str = reduce(lambda a, b: f'{a}_{b}', re.findall(reg_clean, s))
    return cleaned

home = os.environ.get('HOME')
if home is None or home == '':
    home = '/tmp'
log_file = home + '/debug-cmus-cover-art.txt'
try:
    cover_dir = sys.argv[1]
    data = get_song_data()
    if data.status == 'playing':
        if not path.exists(cover_dir):
            os.mkdir(cover_dir)
        art_file_name = f'{clean_string(data.album)}_{clean_string(data.artist)}'
        matching_files = [*filter(lambda x: x.startswith(art_file_name) ,os.listdir(cover_dir))]
        found_match = matching_files is not None and len(matching_files) > 0
        art_file = f'{cover_dir}/{matching_files[0]}' if found_match else f'{cover_dir}/{art_file_name}'
        with open(log_file, 'a') as f:
            f.write(str(f'art file is: {art_file}\n'))
        if not path.exists(art_file):
            img = eyed3.load(data.file).tag.images[0]
            ext = img.mime_type.split("/")[1]
            with open(f'{art_file}.{ext}', 'wb') as image_file:
                image_file.write(img.image_data)
                art_file = f'{art_file}.{ext}'
        with open(cover_dir + '/current.txt', 'w') as current_f:
            current_f.write(art_file)


except Exception as err:
    with open(log_file, 'a') as f:
        tb = traceback.format_exc()
        f.write(str(f'{err}\n{tb}\n'))
