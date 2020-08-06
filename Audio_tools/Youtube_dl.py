import youtube_dl
from pprint import pprint

class Youtube_downloader(object):
    def __init__(self):
        self.format = 'bestaudio/best'
        self.ydl_opt = self.ydl_set_up()

    def ydl_set_up(self, ydl_format='bestaudio/best', template='FFmpegExtractAudio', codec='mp3', quality='320'):
        self.ydl_opt = {}

        def progress(chunk):
            if chunk['status'] == 'finished':
                print("Done Downloading ... Converting File")

        post_processor = {'key': template, 'preferredcodec': codec, 'preferredquality': quality}
        self.ydl_opt['format'] = ydl_format
        self.ydl_opt['postprocessors'] = [post_processor]
        self.ydl_opt['progress_hooks'] = [progress]
        return self.ydl_opt

    def download_audio(self, youtube_link):
        with youtube_dl.YoutubeDL(self.ydl_opt) as ydl:
            ydl.download([youtube_link])
