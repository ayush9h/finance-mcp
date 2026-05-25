<p align="center">
  <img 
    src="https://github.com/user-attachments/assets/6c0fe3a3-f5ee-4c35-a7d3-b57afcd09351"
    alt="Finance MCP Banner"
    width="100%"
  />
</p>

<h3 align="center">💵 Finance MCP</h3>

<p align="center">
  Model Context Protocol (MCP) server and client for retrieving annual reports of publicly listed companies across global stock exchanges.
</p>

<p align="center">
  Built for financial research, compliance workflows, and automated document pipelines.
</p>



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


## Requirements

- Python 3.10+
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
python server.py
```

### Start Streamlit 

```bash
streamlit run app.py
```

<img width="1919" height="878" alt="image" src="https://github.com/user-attachments/assets/d2bd8f1b-9968-408d-82c5-df923d5e662b" />


## Example Use Cases

### Financial Research

Retrieve annual reports for public companies and integrate them into research workflows.

### Compliance Automation

Automate collection and archival of company disclosures and filings.

### Internal Tooling

Integrate report discovery into enterprise finance systems and dashboards.

## License

This project is licensed under the MIT License.
