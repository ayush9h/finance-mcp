# Finance MCP - Development Guidelines

## Overview

Finance MCP is a FastMCP-based application that discovers Investor Relations pages and Annual Report links for public companies.

The application flow:

1. User enters a company name and company country
2. Workflow searches for Investor Relations pages.
3. Relevant pages are scraped.
4. Annual report links are extracted.
5. Results are returned through MCP tools and displayed in Streamlit.


## Repository Structure

```text
finance-mcp/
│
├── app.py
│   └── Streamlit application entrypoint
│
├── server.py
│   └── FastMCP server startup
│
├── requirements.txt
│
├── README.md
│
├── CLAUDE.md
│
├── src/
│   │
│   ├── __init__.py
│   │
│   ├── workflow.py
│   │   └── Main workflow orchestration
│   │
│   ├── tools/
│   │   │
│   │   ├── __init__.py
│   │   │
│   │   ├── search_page_tool.py
│   │   │   └── Investor page discovery tool
│   │   │
│   │   └── scrape_page_tool.py
│   │       └── Page scraping tool
│   │
│   ├── services/
│   │   │
│   │   ├── __init__.py
│   │   │
│   │   ├── exec_ddgs.py
│   │   │   └── DuckDuckGo search wrapper
│   │   │
│   │   ├── scrape_inv_url.py
│   │   │   └── Investor page scraper
│   │   │
│   ├── utils/
│   │   │
│   │   ├── __init__.py
│   │   │
│   │   ├── logger.py
│   │   │
│   │   ├── helpers.py
│   │   │
│   │   └── deduplicate_links.py
```


## Coding Standards

### Python

* Python 3.12+
* Full type hints required
* Follow PEP8
* Use async/await for network operations
* Prefer composition over inheritance


### Service Layer Rules

All external integrations belong in:

```text
src/services/
```

Examples:

* Search providers
* Browser automation
* Scrapers
* Future APIs

Services must:

* Be independently testable
* Avoid UI dependencies
* Avoid FastMCP dependencies


### MCP Tool Rules

All MCP tools belong in:

```text
src/tools/
```

Responsibilities:

* Input validation
* Calling services
* Returning structured responses

Avoid:

* Complex business logic
* Scraping implementation
* Search implementation


## Logging

Always use project logger.

Example:

```python
from src.utils.logger import get_logger

logger = get_logger(__name__)
```

Log:

* Workflow start/end
* Tool execution
* Service failures
* Unexpected exceptions

Do not log:

* Secrets
* Credentials
* Tokens


## Error Handling

Preferred:

```python
try:
    result = await service.run()
except ServiceError as exc:
    logger.exception(exc)
```

Avoid:

```python
except Exception:
    pass
```

Rules:

* Never swallow exceptions
* Provide actionable messages
* Preserve root cause

## Performance Guidelines

Prefer:

* Async I/O
* Reused browser sessions
* Cached searches
* Batched operations

Avoid:

* Repeated browser launches
* Duplicate searches
* Blocking operations


## Security Guidelines

Never commit:

* API keys
* Tokens
* Passwords
* Session cookies