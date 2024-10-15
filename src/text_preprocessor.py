# text_preprocessor.py

import logging
import re
import unicodedata

import emoji
import nltk
from nltk.corpus import stopwords


class TextPreprocessor:
    def __init__(self):
        nltk.download('stopwords', quiet=True)
        self.stop_words = set(stopwords.words('english'))

    def preprocess_text(self, text, max_length=1024):
        try:
            if not text or not isinstance(text, str) or text.isspace():
                logging.debug(f"Ignoring invalid text: {text}")
                return None

            text = text.lower()
            text = re.sub(r'\d+', '', text)
            text = re.sub(r'http\S+|www\S+|https\S+', '', text)
            text = re.sub(r'\S+@\S+', '', text)
            text = emoji.replace_emoji(text, replace='')
            text = re.sub(r'\s+', ' ', text).strip()
            text = ''.join(
                c for c in unicodedata.normalize('NFKD', text)
                if not unicodedata.combining(c)
            )
            words = text.split()
            filtered_words = [word for word in words if word not in self.stop_words]

            if not filtered_words:
                logging.debug(f"Text became empty after filtering: {text}")
                return None

            processed_text = ' '.join(filtered_words)

            if len(processed_text) > max_length:
                logging.debug(f"Processed text exceeds {max_length} characters. It will be truncated.")
                processed_text = processed_text[:max_length].rsplit(' ', 1)[0]

            processed_text = processed_text.strip()

            if len(processed_text) < 2:
                return None

            return processed_text

        except Exception as e:
            logging.error(f"Error processing text: {e}")
            return None
