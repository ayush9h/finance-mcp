<p align="center">
  <img
    src="https://github.com/user-attachments/assets/1989124b-e891-4bd7-a9d8-95d1f7bfd3e0"
    alt="Finance MCP Banner"
    width="500"
  />
</p>
<h3 align="center"><strong>Finance</strong>MCP</h3>


<p align="center">
  Model Context Protocol (MCP) server to retrieve annual reports for companies listed on stock exchanges
</p>


<div align="center">

![Go](https://img.shields.io/badge/go-1.27-blue)
![License](https://img.shields.io/badge/license-MIT-green)

</div>


## Overview

FinanceMCP provides a lightweight MCP-compatible server for discovering and retrieving annual reports from publicly listed companies worldwide.

The project is designed for:

- Financial research teams
- Investment analysis platforms
- Internal finance automation systems


## Features

- Find report links on company pages with the `scrape_links` tool
- Open pages in a real browser, including pages that load links with JavaScript
- MCP over Streamable HTTP, protected by a bearer token
- Local files and internal addresses are rejected
- Easy integration into existing workflows
- Optimized for automation and research use cases


## Requirements

- Go 1.27+
- Chrome, Chromium, or Edge


## Setup

Create a `.env` file in the repository root:

```
MCP_TOKEN=<long random value>
PORT=8080
```

Both values are needed. Without `MCP_TOKEN`, every `/mcp` request returns 401. Without `PORT`, the server tries port 80.

## Running the Application

Start the server from the repository root:

```bash
go run ./cmd/server
```

Check that it is running:

```bash
curl http://localhost:8080/health
```

Run the tests:

```bash
go test ./...
```

On Linux, the browser needs a display. Start the server with `xvfb-run go run ./cmd/server`.

## Using the Server

Connect any MCP client to `http://localhost:8080/mcp` with the header `Authorization: Bearer <MCP_TOKEN>`.

For example, with Claude Code:

```bash
claude mcp add --transport http finance http://localhost:8080/mcp --header "Authorization: Bearer <MCP_TOKEN>"
```

### `scrape_links`

Opens a page in a browser and returns every link on it as `{"links": ["https://...", ...]}`.

| Input | Required | Description |
|---|---|---|
| `url` | Yes | Public `http` or `https` page to scrape |
| `wait_for` | No | CSS selector to wait for, for pages that load links with JavaScript. Defaults to the first link on the page |

A page with no links returns a timeout error after 30 seconds. Two scrapes run at a time, and further calls wait for a free slot.


## Example Use Cases

### Financial Research

Retrieve annual reports for public companies and integrate them into research workflows.

### Compliance Automation

Automate collection and archival of company disclosures and filings.

### Internal Tooling

Integrate report discovery into enterprise finance systems and dashboards.

## License

This project is licensed under the MIT License.
