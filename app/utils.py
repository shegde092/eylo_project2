import re
from typing import Optional


def is_supported_url(url: str) -> bool:
    """Check if URL is from a supported platform (Instagram, YouTube, TikTok)"""
    return get_platform(url) != 'unknown'


def get_platform(url: str) -> str:
    """Identify the platform from the URL"""
    url = url.lower()
    if 'instagram.com' in url:
        return 'instagram'
    elif 'youtube.com' in url or 'youtu.be' in url:
        return 'youtube'
    elif 'tiktok.com' in url:
        return 'tiktok'
    return 'unknown'


def get_post_type(url: str) -> str:
    """Determine post type (reel, video, etc.)"""
    platform = get_platform(url)
    
    if platform == 'instagram':
        if '/reel/' in url:
            return 'reel'
        elif '/tv/' in url:
            return 'tv'
        elif '/p/' in url:
            return 'post'
    elif platform == 'youtube':
        if '/shorts/' in url:
            return 'youtube_short'
        return 'youtube_video'
    elif platform == 'tiktok':
        return 'tiktok_video'
        
    return 'unknown'
