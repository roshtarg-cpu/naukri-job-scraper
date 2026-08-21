# 🚀 Naukri.com Job Scraper

[![Apify Actor](https://img.shields.io/badge/Apify-Actor-00D4FF?style=flat-square&logo=apify)](https://apify.com)
[![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Apache%202.0-green?style=flat-square)](https://opensource.org/licenses/Apache-2.0)

Fast and reliable scraper for **Naukri.com**, India's #1 job portal with 35.6M monthly visitors. Extract comprehensive job listings including titles, companies, salaries, locations, skills, and more.

Perfect for AI agents, ChatGPT plugins, Claude integrations, MCP servers, job aggregators, recruitment automation, and market research. 🤖

---

## 🎯 Features

✅ **Comprehensive Data Extraction** - Job titles, companies, locations, salaries, experience requirements, skills, and descriptions  
✅ **Smart Parsing** - Automatically detects JSON data or falls back to HTML parsing  
✅ **Flexible Search** - Filter by keywords, location, and experience level  
✅ **Proxy Support** - Built-in Apify Proxy integration for reliable scraping  
✅ **Fast & Efficient** - Powered by Camoufox browser automation  
✅ **Clean Output** - Structured JSON data ready for analysis or integration  
✅ **AI-Ready** - Perfect for ChatGPT, Claude, and other AI agent integrations  

---

## 📊 Output Schema

Each job listing includes the following fields:

| Field | Type | Description |
|-------|------|-------------|
| `jobTitle` | String | Job title/position name |
| `companyName` | String | Hiring company name |
| `location` | String | Job location (city/region) |
| `experience` | String | Required experience level |
| `salary` | String | Salary range or "Not disclosed" |
| `jobUrl` | String | Direct link to job posting |
| `postedDate` | String | When the job was posted |
| `skills` | Array | Required skills/technologies |
| `jobDescription` | String | Full job description |
| `scrapedAt` | String | ISO timestamp of scraping |

---

## 🚀 Quick Start

### Running on Apify Platform

```json
{
  "searchQuery": "software engineer",
  "location": "bangalore",
  "experience": "3-5",
  "maxResults": 100,
  "proxyConfiguration": {
    "useApifyProxy": true
  }
}
```

### API Usage

```bash
curl "https://api.apify.com/v2/acts/fervent_bus~naukri-job-scraper/runs" \
  -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -d '{
    "searchQuery": "data analyst",
    "location": "mumbai",
    "maxResults": 50
  }'
```

### Python Integration

```python
from apify_client import ApifyClient

client = ApifyClient("YOUR_API_TOKEN")

run = client.actor("fervent_bus/naukri-job-scraper").call(
    run_input={
        "searchQuery": "python developer",
        "location": "bangalore",
        "maxResults": 100
    }
)

# Fetch results
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(f"{item['jobTitle']} at {item['companyName']}")
```

### JavaScript Integration

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: 'YOUR_API_TOKEN' });

const run = await client.actor("fervent_bus/naukri-job-scraper").call({
  searchQuery: "full stack developer",
  location: "pune",
  maxResults: 100
});

const { items } = await client.dataset(run.defaultDatasetId).listItems();
items.forEach(job => {
  console.log(`${job.jobTitle} at ${job.companyName}`);
});
```

---

## 🤖 AI Agent Integration

Perfect for integrating with AI assistants and automation tools:

### ChatGPT / Claude MCP Integration

Use this scraper as a tool in your AI agent workflows:

```python
# Example MCP tool definition
{
  "name": "search_naukri_jobs",
  "description": "Search for jobs on Naukri.com",
  "parameters": {
    "query": "Job title or keywords",
    "location": "City or region",
    "experience": "Experience level (e.g., 3-5)"
  }
}
```

### Zapier / Make.com Integration

Connect to 1000+ apps via webhooks:
1. Run actor via API
2. Get dataset results
3. Send to Google Sheets, Airtable, Slack, etc.

---

## ⚙️ Input Configuration

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `searchQuery` | String | No | `"software engineer"` | Job title or keywords to search |
| `location` | String | No | `""` | Location filter (e.g., bangalore, delhi) |
| `experience` | String | No | `""` | Experience requirement (e.g., 0-3, 3-5) |
| `maxResults` | Integer | No | `100` | Maximum number of jobs to scrape (1-1000) |
| `proxyConfiguration` | Object | No | `{useApifyProxy: true}` | Proxy settings for reliable scraping |

---

## 💡 Use Cases

🔹 **Recruitment Automation** - Automatically collect job postings for candidate matching  
🔹 **Market Research** - Analyze salary trends, skill demands, and hiring patterns  
🔹 **Job Aggregation** - Build job boards by combining multiple sources  
🔹 **AI Training Data** - Collect datasets for ML models and NLP applications  
🔹 **Competitive Analysis** - Monitor competitor hiring and job market trends  
🔹 **ChatGPT/Claude Integration** - Power AI assistants with real-time job data  

---

## 🛡️ Best Practices

1. **Use Apify Proxy** - Enable proxy configuration for reliable, unblocked scraping
2. **Respect Rate Limits** - Don't scrape more than you need
3. **Monitor Results** - Check output quality and adjust search parameters
4. **Handle Errors** - Implement retry logic in your integration
5. **Stay Updated** - Website structures change; report issues on GitHub

---

## 📈 Performance

- **Speed**: ~50-100 jobs per minute
- **Reliability**: 99%+ success rate with proxies
- **Data Quality**: Structured, validated output
- **Scalability**: Handles 1000+ results per run

---

## 🔧 Technical Details

**Technology Stack:**
- Python 3.11
- Playwright (Firefox browser automation)
- BeautifulSoup4 (HTML parsing)
- Apify SDK (actor framework)

**Features:**
- Automatic JSON/HTML detection
- Robust error handling
- Proxy rotation support
- Clean data normalization

---

## 📝 Example Output

```json
{
  "jobTitle": "Senior Software Engineer",
  "companyName": "Tech Corp India",
  "location": "Bengaluru",
  "experience": "3-5 years",
  "salary": "15-20 Lakhs",
  "jobUrl": "https://www.naukri.com/job-listings-...",
  "postedDate": "Today",
  "skills": ["Python", "Django", "AWS", "Docker"],
  "jobDescription": "We are looking for an experienced software engineer...",
  "scrapedAt": "2025-08-21T10:30:00Z"
}
```

---

## 🤝 Support & Contributing

- **Issues**: Report bugs or request features on [GitHub](https://github.com/roshtarg-cpu/naukri-job-scraper)
- **Questions**: Contact via Apify Console
- **Updates**: Follow for new features and improvements

---

## 📄 License

Apache 2.0 License - Free for commercial and personal use

---

## 🌟 Related Actors

- LinkedIn Job Scraper
- Indeed Job Scraper
- Monster Job Scraper
- Glassdoor Scraper

---

**Made with ❤️ for the AI and automation community**

*Disclaimer: This actor is not affiliated with Naukri.com. Always respect robots.txt and terms of service.*
