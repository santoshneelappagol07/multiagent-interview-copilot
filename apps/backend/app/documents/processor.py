import re

class TextNormalizer:
    @staticmethod
    def normalize(text: str) -> str:
        # Standardize line breaks and tabs
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        # Condense multiple blank lines
        text = re.sub(r'\n{3,}', '\n\n', text)
        # Condense spaces
        text = re.sub(r'[ \t]+', ' ', text)
        return text.strip()
