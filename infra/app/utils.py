import re
from typing import Optional


def is_instagram_url(url: str) -> bool:
    """Check if URL is a valid Instagram URL"""
    pattern = r'https?://(www\.)?instagram\.com/(reel|p|tv)/[\w-]+/?'
    return bool(re.match(pattern, url))


def extract_instagram_shortcode(url: str) -> Optional[str]:
    """Extract the shortcode from an Instagram URL"""
    pattern = r'instagram\.com/(reel|p|tv)/([\w-]+)'
    match = re.search(pattern, url)
    if match:
        return match.group(2)
    return None


def get_instagram_post_type(url: str) -> str:
    """Determine if URL is a Reel, Post, or TV"""
    if '/reel/' in url:
        return 'reel'
    elif '/tv/' in url:
        return 'tv'
    elif '/p/' in url:
        return 'post'
    return 'unknown'
