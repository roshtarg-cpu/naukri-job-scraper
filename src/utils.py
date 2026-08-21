"""Utility functions for the Naukri scraper."""

import json
import re
from typing import Any, Dict, Optional
from urllib.parse import quote_plus


def build_search_url(query: str = "", location: str = "", experience: str = "") -> str:
    """
    Build Naukri.com search URL with parameters.
    
    Args:
        query: Job title or keywords
        location: Location filter
        experience: Experience level (e.g., "0-3", "3-5")
    
    Returns:
        Complete search URL
    """
    base_url = "https://www.naukri.com"
    
    if query:
        # Create URL-friendly query
        query_slug = query.lower().replace(" ", "-")
        url = f"{base_url}/{query_slug}-jobs"
        
        # Add location if provided
        if location:
            location_slug = location.lower().replace(" ", "-")
            url += f"-in-{location_slug}"
    else:
        # Default to all jobs
        url = f"{base_url}/jobs-in-india"
    
    # Add query parameters
    params = []
    if experience:
        params.append(f"experience={quote_plus(experience)}")
    
    if params:
        url += "?" + "&".join(params)
    
    return url


def extract_json_data(html_content: str) -> Optional[Dict[str, Any]]:
    """
    Extract JSON data from HTML (e.g., __NEXT_DATA__ or embedded JSON).
    
    Args:
        html_content: Raw HTML content
    
    Returns:
        Parsed JSON data if found, None otherwise
    """
    # Look for __NEXT_DATA__ (Next.js sites)
    next_data_pattern = r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>'
    match = re.search(next_data_pattern, html_content, re.DOTALL)
    
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass
    
    # Look for other JSON patterns
    json_pattern = r'window\.__INITIAL_STATE__\s*=\s*({.*?});'
    match = re.search(json_pattern, html_content, re.DOTALL)
    
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass
    
    return None


def clean_text(text: Optional[str]) -> str:
    """
    Clean and normalize text content.
    
    Args:
        text: Raw text
    
    Returns:
        Cleaned text
    """
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def extract_experience(text: str) -> str:
    """
    Extract experience requirement from text.
    
    Args:
        text: Text containing experience info
    
    Returns:
        Normalized experience string
    """
    if not text:
        return ""
    
    # Look for patterns like "3-5 Yrs", "0-2 years", etc.
    match = re.search(r'(\d+)\s*-\s*(\d+)\s*(?:Yrs?|years?)', text, re.IGNORECASE)
    if match:
        return f"{match.group(1)}-{match.group(2)} years"
    
    # Look for "Fresher" or "0 years"
    if re.search(r'fresher|0\s*years?', text, re.IGNORECASE):
        return "Fresher"
    
    return clean_text(text)


def extract_salary(text: str) -> str:
    """
    Extract salary information from text.
    
    Args:
        text: Text containing salary info
    
    Returns:
        Normalized salary string
    """
    if not text:
        return "Not disclosed"
    
    # Look for "Not disclosed" or similar
    if re.search(r'not\s+disclosed', text, re.IGNORECASE):
        return "Not disclosed"
    
    return clean_text(text)
