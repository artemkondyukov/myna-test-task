import json
import os
import torch
from typing import List, TypedDict
from youtube_transcript_api import YouTubeTranscriptApi


class Segment(TypedDict):
    start: float
    end: float


class DiaSegment(TypedDict):
    segment: Segment
    track: str
    label: str


class DialogueExtractor:
    def __init__(self, store_dir: str):
        self.store_dir = store_dir
        self.diarization = torch.hub.load('pyannote/pyannote-audio', 'dia_ami')

    @staticmethod
    def __collapse_segments(dia_segments: List[DiaSegment]) -> List[DiaSegment]:
        result_segments = []
        current_segment = dia_segments[0].copy()

        for s in dia_segments[1:]:
            if s["label"] == current_segment["label"]:
                current_segment["segment"]["end"] = s["segment"]["end"]
            else:
                result_segments.append(current_segment)
                current_segment = s.copy()

        return result_segments

    def extract(self, video_ids: List[str]) -> None:
        """
        Takes Youtube video ids, relies on existing <YOUTUBE_ID>.wav files
        For each file do the following:
        - download youtube subtitles
        - diarize audio
        - find correspondance between speaker times and texts
        - save json file with all the info (start, end, speaker id, text)
        :param video_ids: list of ids, like `sp8smJFaKYE`
        :return: side effects
        """
        for video_id in video_ids:
            if os.path.exists(os.path.join(self.store_dir, f"{video_id}.json")):
                print(f"{video_id}.json is already created")
                continue
            else:
                print(f"Parsing {video_id}.wav")

            output = self.diarization({"audio": os.path.join(self.store_dir, f"{video_id}.wav")})
            collapsed_dicts = self.__collapse_segments(output.for_json()["content"])

            transcript = YouTubeTranscriptApi.get_transcript(video_id)

            transcript_idx = 0

            for col_dict in collapsed_dicts:
                col_dict["text"] = ""

                while True:
                    if transcript_idx >= len(transcript):
                        break

                    cur_transcript = transcript[transcript_idx]
                    cur_transcript["end"] = cur_transcript["start"] + cur_transcript["duration"]

                    if cur_transcript["end"] > col_dict["segment"]["end"] + .1:
                        break

                    col_dict["text"] += cur_transcript["text"] + " "

                    transcript_idx += 1

            json.dump(collapsed_dicts, open(os.path.join(self.store_dir, f"{video_id}.json"), "w"))
