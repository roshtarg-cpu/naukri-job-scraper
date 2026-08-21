"""HTML/JSON parsing functions for job listings."""

from typing import Any, Dict, List, Optional

from bs4 import BeautifulSoup

from .utils import clean_text, extract_experience, extract_salary


def parse_job_listing(html_content: str, from_json: bool = False, json_data: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """
    Parse job listings from HTML or JSON data.
    
    Args:
        html_content: Raw HTML content
        from_json: Whether to parse from JSON data
        json_data: Parsed JSON data (if available)
    
    Returns:
        List of job dictionaries
    """
    if from_json and json_data:
        return parse_from_json(json_data)
    else:
        return parse_from_html(html_content)


def parse_from_html(html_content: str) -> List[Dict[str, Any]]:
    """
    Parse job listings from HTML content.
    
    Args:
        html_content: Raw HTML content
    
    Returns:
        List of job dictionaries
    """
    soup = BeautifulSoup(html_content, 'lxml')
    jobs = []
    
    # Find all job articles - Naukri uses article tags with specific classes
    job_articles = soup.find_all('article', class_=lambda x: x and 'jobTuple' in x if x else False)
    
    # Alternative: look for job containers with different class names
    if not job_articles:
        job_articles = soup.find_all('div', class_=lambda x: x and 'srp-jobtuple' in x.lower() if x else False)
    
    # Another alternative: look for any article tags
    if not job_articles:
        job_articles = soup.find_all('article')
    
    for article in job_articles:
        try:
            job_data = extract_job_from_element(article)
            if job_data and job_data.get('jobTitle'):
                jobs.append(job_data)
        except Exception as e:
            # Skip individual job parsing errors
            continue
    
    return jobs


def extract_job_from_element(element) -> Dict[str, Any]:
    """
    Extract job data from a single HTML element.
    
    Args:
        element: BeautifulSoup element containing job data
    
    Returns:
        Job data dictionary
    """
    job = {
        "jobTitle": "",
        "companyName": "",
        "location": "",
        "experience": "",
        "salary": "Not disclosed",
        "jobUrl": "",
        "postedDate": "",
        "skills": [],
        "jobDescription": "",
    }
    
    # Job title - multiple possible selectors
    title_elem = (
        element.find('a', class_=lambda x: x and 'title' in x.lower() if x else False) or
        element.find('div', class_=lambda x: x and 'title' in x.lower() if x else False) or
        element.find('h2') or
        element.find('h3')
    )
    if title_elem:
        job['jobTitle'] = clean_text(title_elem.get_text())
        # Extract URL from title link
        if title_elem.name == 'a' and title_elem.get('href'):
            href = title_elem['href']
            if href.startswith('http'):
                job['jobUrl'] = href
            else:
                job['jobUrl'] = f"https://www.naukri.com{href}"
    
    # Company name
    company_elem = (
        element.find('a', class_=lambda x: x and 'comp' in x.lower() if x else False) or
        element.find('div', class_=lambda x: x and 'comp' in x.lower() if x else False)
    )
    if company_elem:
        job['companyName'] = clean_text(company_elem.get_text())
    
    # Experience
    exp_elem = (
        element.find('span', class_=lambda x: x and 'exp' in x.lower() if x else False) or
        element.find('li', class_=lambda x: x and 'exp' in x.lower() if x else False)
    )
    if exp_elem:
        job['experience'] = extract_experience(exp_elem.get_text())
    else:
        # Try to find in text content
        text_content = element.get_text()
        if text_content:
            job['experience'] = extract_experience(text_content)
    
    # Salary
    salary_elem = (
        element.find('span', class_=lambda x: x and 'sal' in x.lower() if x else False) or
        element.find('li', class_=lambda x: x and 'sal' in x.lower() if x else False)
    )
    if salary_elem:
        job['salary'] = extract_salary(salary_elem.get_text())
    
    # Location
    loc_elem = (
        element.find('span', class_=lambda x: x and 'loc' in x.lower() if x else False) or
        element.find('li', class_=lambda x: x and 'loc' in x.lower() if x else False)
    )
    if loc_elem:
        job['location'] = clean_text(loc_elem.get_text())
    
    # Posted date
    date_elem = (
        element.find('span', class_=lambda x: x and 'date' in x.lower() if x else False) or
        element.find('div', class_=lambda x: x and 'date' in x.lower() if x else False)
    )
    if date_elem:
        job['postedDate'] = clean_text(date_elem.get_text())
    
    # Skills - look for tags or skill lists
    skill_container = element.find('ul', class_=lambda x: x and 'tag' in x.lower() if x else False)
    if skill_container:
        skill_items = skill_container.find_all('li')
        job['skills'] = [clean_text(s.get_text()) for s in skill_items if s.get_text().strip()]
    
    # Alternative: look for span tags with skills
    if not job['skills']:
        skill_tags = element.find_all('span', class_=lambda x: x and 'tag' in x.lower() if x else False)
        if skill_tags:
            job['skills'] = [clean_text(s.get_text()) for s in skill_tags if s.get_text().strip()]
    
    # Job description - look for description div
    desc_elem = element.find('div', class_=lambda x: x and 'desc' in x.lower() if x else False)
    if desc_elem:
        job['jobDescription'] = clean_text(desc_elem.get_text())
    
    return job


def parse_from_json(json_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Parse job listings from JSON data.
    
    Args:
        json_data: Parsed JSON data
    
    Returns:
        List of job dictionaries
    """
    jobs = []
    
    # Try to find jobs array in various possible locations
    # This depends on the actual JSON structure from Naukri
    
    # Check if it's Next.js data
    if 'props' in json_data:
        page_props = json_data.get('props', {}).get('pageProps', {})
        job_list = page_props.get('jobs', []) or page_props.get('jobsList', [])
        
        for job_item in job_list:
            job = {
                "jobTitle": job_item.get('title', ''),
                "companyName": job_item.get('companyName', '') or job_item.get('company', ''),
                "location": job_item.get('location', ''),
                "experience": job_item.get('experience', ''),
                "salary": job_item.get('salary', 'Not disclosed'),
                "jobUrl": job_item.get('url', '') or f"https://www.naukri.com/job-listings-{job_item.get('id', '')}",
                "postedDate": job_item.get('postedDate', '') or job_item.get('createdDate', ''),
                "skills": job_item.get('skills', []) or job_item.get('tags', []),
                "jobDescription": job_item.get('description', ''),
            }
            jobs.append(job)
    
    return jobs
