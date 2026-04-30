import re
import unicodedata

def slugify(text: str) -> str:
    """
    Convert a string to a URL-friendly slug.
    Example: "Red Roses" -> "red-roses"
    """
    # Normalize unicode characters
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    # Lowercase and replace non-alphanumeric with hyphens
    text = re.sub(r'[^\w\s-]', '', text).lower()
    # Replace whitespace/multiple hyphens with a single hyphen
    text = re.sub(r'[-\s]+', '-', text).strip('-')
    return text
