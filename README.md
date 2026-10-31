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

### 1. Sync up with the environment

```
uv sync
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

## Deploy the Go Server on Render

1. Create a new Web Service from this repository and choose the Docker runtime.
2. Add the environment variable `MCP_TOKEN` with a long random value, for example from `openssl rand -hex 32`.
3. Set the health check path to `/health`.

Clients connect to `https://<service>.onrender.com/mcp` with the header `Authorization: Bearer <MCP_TOKEN>`.

## Deploy the Go Server on a Linux VM

The server exposes MCP over HTTP at `/mcp` and needs `MCP_TOKEN` set. The browser runs with a visible window on an Xvfb virtual display.

Build locally and copy the files to the VM:

```bash
GOOS=linux GOARCH=amd64 go build -o finance-mcp ./cmd/server
scp finance-mcp deploy/finance-mcp.service <user>@<vm>:
```

Then on the VM (Debian or Ubuntu):

```bash
sudo apt update && sudo apt install -y xvfb xauth
curl -fLO https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install -y ./google-chrome-stable_current_amd64.deb

sudo useradd --system --create-home finance-mcp
sudo install finance-mcp /usr/local/bin/
sudo install -m 644 finance-mcp.service /etc/systemd/system/
echo "MCP_TOKEN=$(openssl rand -hex 32)" | sudo tee /etc/finance-mcp.env >/dev/null
sudo chmod 600 /etc/finance-mcp.env

sudo systemctl daemon-reload
sudo systemctl enable --now finance-mcp
```

Clients connect to `http://<vm>:8080/mcp` with the header `Authorization: Bearer <MCP_TOKEN>`. The server speaks plain HTTP, so put it behind a TLS proxy before exposing it to the internet.

## Example Use Cases

### Financial Research

Retrieve annual reports for public companies and integrate them into research workflows.

### Compliance Automation

Automate collection and archival of company disclosures and filings.

### Internal Tooling

Integrate report discovery into enterprise finance systems and dashboards.

## License

This project is licensed under the MIT License.
