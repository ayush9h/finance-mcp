FROM golang:1.27.3 AS build
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY cmd ./cmd
COPY internal ./internal
RUN CGO_ENABLED=0 go build -o /finance-mcp ./cmd/financemcp

FROM debian:trixie-slim
RUN apt-get update \
    && apt-get install -y --no-install-recommends chromium xvfb dumb-init ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -m 1777 /tmp/.X11-unix
RUN echo 'export CHROMIUM_FLAGS="$CHROMIUM_FLAGS --no-sandbox"' > /etc/chromium.d/no-sandbox
RUN useradd --create-home finance-mcp
COPY --from=build /finance-mcp /usr/local/bin/finance-mcp
USER finance-mcp
ENV DISPLAY=:99
CMD ["dumb-init", "sh", "-c", "Xvfb :99 -screen 0 1920x1080x24 -nolisten tcp & exec finance-mcp"]
