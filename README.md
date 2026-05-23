# MCP for Finance Teams

Model Context Protocol (MCP) server and client for finance teams to retrieve annual reports of publicly listed companies across global stock exchanges.

## Features

- Fetch annual reports for listed companies globally
- MCP-based client-server architecture
- Fast API integration for downstream finance workflows
- Designed for research, compliance, and financial analysis teams
- Lightweight setup with modern Python tooling

## Setup

### Create Environment with uv

```bash
uv venv
source .venv/bin/activate   # Linux / macOS

# Windows
.venv\Scripts\activate
```

### Install Dependencies

```bash
uv pip install -r requirements.txt
```

## Running the Project

Run the MCP server and client side by side in separate terminals.

### Start Server

```bash
python server.py
```

### Start Client

```bash
python client.py
```

## Example Use Cases

- Download annual reports from stock exchange websites
- Automate financial document collection
- Integrate reports into internal finance tools
- Build research and valuation pipelines

## License

MIT License
