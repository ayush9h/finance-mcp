FROM golang:1.27.3 AS build
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY cmd ./cmd
COPY internal ./internal
RUN CGO_ENABLED=0 go build -o /finance-mcp ./cmd/server

FROM debian:trixie-slim
RUN apt-get update \
    && apt-get install -y --no-install-recommends chromium xvfb xauth ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN echo 'export CHROMIUM_FLAGS="$CHROMIUM_FLAGS --no-sandbox"' > /etc/chromium.d/no-sandbox
RUN useradd --create-home finance-mcp
COPY --from=build /finance-mcp /usr/local/bin/finance-mcp
USER finance-mcp
CMD ["xvfb-run", "-a", "--server-args=-screen 0 1920x1080x24", "finance-mcp"]
