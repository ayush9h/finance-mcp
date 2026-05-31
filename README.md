<p align="center">
  <img
    src="https://github.com/user-attachments/assets/f9efa3fd-2d12-419e-a962-72a95609eb8d"
    alt="Finance MCP Banner"
    width="700"
  />
</p>
<h3 align="center">💵 Finance MCP</h3>

<p align="center">
  Model Context Protocol (MCP) server and client for retrieving annual reports of publicly listed companies across global stock exchanges.
</p>


<div align="center">

![Python](https://img.shields.io/badge/python-3.13-blue)
![License](https://img.shields.io/badge/license-MIT-green)

</div>


## Overview

Finance MCP provides a lightweight MCP-compatible server and client architecture for discovering and retrieving annual reports from publicly listed companies worldwide.

The project is designed for:

- Financial research teams
- Investment analysis platforms
- Internal finance automation systems


## Features

- Retrieve annual report URLs for globally listed companies
- MCP-compatible server and client implementation
- Simple Python-based architecture
- Easy integration into existing workflows
- Optimized for automation and research use cases


<img width="1881" height="815" alt="image" src="https://github.com/user-attachments/assets/ba334110-0053-4fd9-a42f-125b767ec992" />


## Requirements

- Python 3.13+
- `uv` package manager

Install `uv`:

```bash
pip install uv
```


## Setup

### 1. Create Virtual Environment

```bash
uv venv
```

Activate the environment:

#### Linux / macOS

```bash
source .venv/bin/activate
```

#### Windows

```powershell
.venv\Scripts\activate
```


### 2. Install Dependencies

```bash
uv pip install -r requirements.txt
```



## Running the Application

Start the MCP server and client in separate terminals.

### Start MCP Server

```bash
uvicorn server:app --host 0.0.0.0 --port 8000
```

### Start Streamlit 

```bash
streamlit run app.py
```

## Example Use Cases

### Financial Research

Retrieve annual reports for public companies and integrate them into research workflows.

### Compliance Automation

Automate collection and archival of company disclosures and filings.

### Internal Tooling

Integrate report discovery into enterprise finance systems and dashboards.

## License

This project is licensed under the MIT License.
