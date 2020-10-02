import sys
import os
from os import path
import subprocess


class SongData(object):
    def __init__(self, song_status, file, artist, album, disc_number, track, title, date, duration):
        self.status = song_status
        self.file = file
        self.artist = artist
        self.album = album
        self.disc_number = disc_number
        self.track = track
        self.title = title
        self.date = date
        self.duration = duration


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
        art_file = cover_dir + '/' + data.album.replace('/', '') + '_' + data.artist + '.jpg'

        if not path.exists(art_file):
            subprocess.call(['ffmpeg', '-i', data.file, '-an', '-vcodec', 'copy', art_file])
        with open(cover_dir + '/current.txt', 'w') as current_f:
            current_f.write(art_file)


except Exception as err:
    with open(log_file, 'a') as f:
        f.write(str(err))
