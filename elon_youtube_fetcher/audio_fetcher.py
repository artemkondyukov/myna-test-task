import os
from pydub import AudioSegment
from typing import List
import youtube_dl


class AudioFetcher:
    def __init__(self, store_dir: str):
        self.store_dir = store_dir

    def fetch_audio(self, video_ids: List[str]) -> None:
        """
        Takes Youtube video ids, downloads mp3 audio and
        converts it into wav. Stores wav files in store_dir
        attribute of the AudioFetcher class
        :param video_ids: list of ids, like `sp8smJFaKYE`
        :return: side effects
        """
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": f"{self.store_dir}/%(id)s.%(ext)s",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            for video_id in video_ids:
                if not os.path.exists(os.path.join(self.store_dir, f"{video_id}.mp3")):
                    ydl.download(f"https://www.youtube.com/watch?v={video_id}")
                else:
                    print(f"{video_id}.mp3 is already downloaded")

        for video_id in video_ids:
            if not os.path.exists(os.path.join(self.store_dir, f"{video_id}.wav")):
                print(f"Converting {video_id}.mp3 to wav")
                sound = AudioSegment.from_mp3(os.path.join(self.store_dir, f"{video_id}.mp3"))
                sound.export(os.path.join(self.store_dir, f"{video_id}.wav"), format="wav")
            else:
                print(f"{video_id}.wav is already converted")
