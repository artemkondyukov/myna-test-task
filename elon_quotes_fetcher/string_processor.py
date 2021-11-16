import re


class StringProcessor:
    @staticmethod
    def process(text: str) -> str:
        """
        Takes quote text from https://elonmusknews.org, removes
        excess brackets, parentheses, quotes etc
        :param text: input text
        :return: processed quote text
        """
        text = text.replace("”", '"')
        text = text.replace("“", '"')
        text = re.sub(r"\(\w+, \d+ \| \w+\)", "", text)
        text = text.replace("…", "...")

        if '"' in text:
            text = re.sub(r'(.*)"(.*)"(.*)', r"\2", text)

        text = text.strip('"')
        text = text.replace("[", "")
        text = text.replace("]", "")
        text = text.replace("’", "'")

        return text
