package main

import (
	"context"
	"log/slog"
	"net/http"
	"os"

	"github.com/ayush9h/finance-mcp/internal/handler"
	"github.com/joho/godotenv"
)

func main() {
	if err := godotenv.Load(); err != nil {
		slog.LogAttrs(context.Background(), slog.LevelError, "environment configuration not found", slog.String("message", err.Error()))
	}

	token := os.Getenv("MCP_TOKEN")

	var addr string
	if port := os.Getenv("PORT"); port != "" {
		addr = ":" + port
	}

	server := &http.Server{
		Addr:    addr,
		Handler: handler.New(token),
	}

	slog.LogAttrs(context.Background(), slog.LevelInfo, "server started running", slog.String("port", server.Addr))

	if err := server.ListenAndServe(); err != nil {
		slog.LogAttrs(context.Background(), slog.LevelError, "error in startup of server", slog.String("message", err.Error()))
	}
}
