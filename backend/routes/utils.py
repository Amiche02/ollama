import html
import re
import unicodedata

import langdetect
import nltk
from langdetect import detect
from nltk.corpus import stopwords

# Download stopwords if not already present
nltk.download("stopwords")

# Common stopwords dictionary (handles multiple languages)
STOPWORDS_DICT = {
    "en": set(stopwords.words("english")),
    "fr": set(stopwords.words("french")),
    "es": set(stopwords.words("spanish")),
    "de": set(stopwords.words("german")),
    "it": set(stopwords.words("italian")),
    "pt": set(stopwords.words("portuguese")),
    "default": set(),  # If the language is unknown
}


def clean_text(text):
    """Cleans web text but keeps emails and phone numbers."""

    if not text:
        return ""

    # Decode HTML entities (e.g., &amp; → &)
    text = html.unescape(text)

    # Normalize Unicode (fix accents and special characters)
    text = unicodedata.normalize("NFKD", text)

    # Remove HTML tags
    text = re.sub(r"<[^>]+>", "", text)

    # Preserve emails and phone numbers
    emails = re.findall(r"\S+@\S+", text)
    phones = re.findall(r"\+?\d{1,3}[ -]?\(?\d{1,4}\)?[ -]?\d{1,4}[ -]?\d{1,9}", text)

    # Remove URLs
    text = re.sub(r"http[s]?://\S+", "", text)

    # Remove unwanted metadata (multi-language)
    text = re.sub(
        r"(Afficher / masquer|Modifier le code|Voir l’historique|Read more|Facebook|Twitter|LinkedIn|YouTube|Instagram)",
        "",
        text,
        flags=re.IGNORECASE,
    )

    # Remove non-alphanumeric characters (except spaces, emails, and numbers)
    text = re.sub(r"[^a-zA-ZÀ-ÖØ-öø-ÿ0-9@.\-\s]", "", text)

    # Detect language and remove stopwords
    try:
        lang = detect(text)  # Detect the language
        stop_words = STOPWORDS_DICT.get(lang, STOPWORDS_DICT["default"])
        text = " ".join(
            [word for word in text.split() if word.lower() not in stop_words]
        )
    except langdetect.lang_detect_exception.LangDetectException:
        pass  # If language detection fails, keep original text

    # Reinsert extracted emails & phones
    text = text.strip()
    if emails:
        text += "\nEmails: " + ", ".join(emails)
    if phones:
        text += "\nPhones: " + ", ".join(phones)

    return text  # No length limit!


def clean_result(result):
    """Cleans each search result, removing embeddings and applying text cleaning."""
    return {
        "document_id": result.get("document_id"),
        "chunks": [
            {
                "chunk_index": chunk.get("chunk_index"),
                "content": clean_text(chunk.get("content", "")),
                "metadata": chunk.get("metadata"),
            }
            for chunk in result.get("chunks", [])
            if "content" in chunk
        ],
    }
