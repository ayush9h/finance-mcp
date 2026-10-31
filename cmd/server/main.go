package main

import (
	"log"
	"net/http"
	"os"

	"github.com/ayush9h/finance-mcp/internal/handler"
	"github.com/joho/godotenv"
)

func main() {
	if err := godotenv.Load(); err != nil {
		log.Printf("Warning: .env file not found: %v", err)
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

	log.Printf("server listening on %s", server.Addr)

	if err := server.ListenAndServe(); err != nil {
		log.Fatal(err)
	}
}
