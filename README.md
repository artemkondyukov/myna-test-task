# myna-test-task

This repo contains scripts for fetching data about celebrities. 
Right now it scraps quotes of Elon Musk from `https://elonmusknews.org`
and extracts dialogues from Youtube videos.

## Installation

```shell script
cd <REPO_DIRECTORY>
virtualenv -p python3.8 .env
source .env/bin/activate
pip install -r requirements.txt
```

## Elon Musk quotes
This data source is quite straightforward to work with: 
use BeautifulSoup, scrap several pages, parse them and store the data

Obtained data is stored in data/quotes.txt.
The data is pretty clean, several examples are:

```text
I also read a lot of comic books as I was growing up, 
and I think that might have influenced me just as much. 
I mean, they're always trying to save the world, with their 
underpants on the outside or these skin-tight iron suits, 
which is really pretty strange when you think about it. 
But they are trying to save the world.
```

and

```text
I think if you can solve genetic diseases. 
If you can prevent dementia, or Alzheimer's or something like 
that with genetic reprogramming that would be wonderful.
```

You can obtain data with:
```shell script
PYTHONPATH=. python elon_quotes_fetcher/fetch_quotes.py \
  --url_list elon_quotes_urls.txt \
  --out data/quotes.txt
```

## Youtube parser

Youtube stores several interviews with Elon, so it could be very
useful. Here we download audio for certain videos, do some ASR
magic and extract different speakers, obtain the subtitles and
merge speaker timings with subtitles.

Data could be found in data/*.json files and looks like:
```json
[
  {
    "segment": {
      "start": 5.361218750000001,
      "end": 33.59815625
    },
    "track": "D",
    "label": "A",
    "text": "Chris Anderson:\nElon, hey, welcome back to TED. It's great to have you here. Elon Musk: Thanks for having me. CA: So, in the next half hour or so, we're going to spend some time exploring your vision for what\nan exciting future might look like, which I guess makes\nthe first question a little ironic: Why are you boring? "
  },
  {
    "segment": {
      "start": 33.59815625,
      "end": 37.07271875
    },
    "track": "CL",
    "label": "B",
    "text": "EM: Yeah. I ask myself that frequently. "
  }
]
```

The next steps should include:
- detect which label corresponds to Elon
- do some fancy postprocessing (e.g. skip empty phrases)

The first task could be solved with emb_ami from pyannote,
whereas the second needs just common sense.

 You can obtain data with:
```shell script
PYTHONPATH=. python elon_youtube_fetcher/fetch_videos.py \
  --id_list youtube.txt \
  --data_dir data/
```
   