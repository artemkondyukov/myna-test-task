import argparse

from elon_youtube_fetcher.audio_fetcher import AudioFetcher
from elon_youtube_fetcher.dialogue_extractor import DialogueExtractor

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download quotes from https://elonmusknews.org")
    parser.add_argument("--id_list", type=str,
                        help="Path to the file with Youtube video ids to parse")
    parser.add_argument("--data_dir", type=str,
                        help="Path to the dir with wav files")

    args = parser.parse_args()

    with open(args.id_list, "r") as f:
        youtube_links = [s.strip() for s in f.readlines()]

    audio_fetcher = AudioFetcher(args.data_dir)
    audio_fetcher.fetch_audio(youtube_links)

    dialogue_extractor = DialogueExtractor(args.data_dir)
    dialogue_extractor.extract(youtube_links)
