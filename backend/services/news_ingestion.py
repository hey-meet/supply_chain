import os
import re
from urllib.parse import urlparse

# -----------------------------------------------------------------------
# STEP 1: Clean & preprocess article text
# -----------------------------------------------------------------------
def clean_text(text: str) -> str:
    """
    Cleans the input text by removing unwanted characters and formatting.

    Args:
        text (str): The input text to be cleaned.

    Returns:
        str: Cleaned text.
    """
    if not text:
        return ""
    
    text = re.sub(r"<[^>]+>", "", text)  # Remove HTML tags

    text = re.sub(r"\s+", " ", text)  # Replace multiple whitespace with single space

    return text.strip()

# -----------------------------------------------------------------------
# STEP 2: Extract domain from URL
# -----------------------------------------------------------------------

def extract_domain(url: str) -> str:
    """
    Extracts the domain from a given URL.

    Args:
        url (str): The input URL.

    Returns:
        str: The extracted domain.
    """
    if not url:
        return "unknown"
    
    domain = urlparse(url).netloc # Extract the domain from the parsed URL
    
    return domain.replace("www.", "") if domain else "unknown"  # Remove 'www.' prefix if present

_stopwords = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "is", "are", "was", "were", "by", "from", "as", "it",
    "this", "that", "has", "have", "will", "be", "its", "after", "over",
}

# -----------------------------------------------------------------------
# STEP 3: Extract keywords from cleaned text
# -----------------------------------------------------------------------

def extract_keywords(text: str, top_n: int = 5) -> list[str]:
    """
    Extracts the top N keywords from the input text.

    Args:
        text (str): The input text from which to extract keywords.
        top_n (int): The number of top keywords to return.

    Returns:
        list[str]: A list of extracted keywords.
    """
    if not text:
        return []
    
    # Normalize text to lowercase and split into words
    words = re.findall(r"[a-zA-Z]+", text.lower())
    meaningful_words = [w for w in words if w not in _stopwords and len(w) > 3]
    
    # Count word frequencies
    word_counts = {}

    for word in meaningful_words:
        word_counts[word] = word_counts.get(word, 0) + 1

    # Sort words by frequency and return the top N keywords
    sorted_keywords = sorted(word_counts.items(), key=lambda item: item[1], reverse=True)

    return [word for word, count in sorted_keywords[:top_n]]
