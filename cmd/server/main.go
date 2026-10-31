package main

import (
	"encoding/json"
	"log"
	"net/http"

	"github.com/ayush9h/finance-mcp/internal/service"
)

func main() {
	mux := http.NewServeMux()

	// Health Check
	mux.HandleFunc("GET /health", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		w.Write([]byte(`{"status":"ok from go. The server has started running"}`))
	})

	// Scrape Check
	mux.HandleFunc("GET /scrape", func(w http.ResponseWriter, r *http.Request) {
		url := r.URL.Query().Get("url")

		if url == "" {
			w.WriteHeader(http.StatusBadRequest)
			json.NewEncoder(w).Encode(map[string]string{"error": "URL is required"})
			return
		}

		title, err := service.ScrapeTitle(url)
		if err != nil {
			w.WriteHeader(http.StatusBadRequest)
			json.NewEncoder(w).Encode(map[string]string{"error": "Scrape failed"})
			return
		}

		w.WriteHeader(http.StatusOK)
		json.NewEncoder(w).Encode(map[string]string{"url": url, "title": title})

	})

	server := &http.Server{
		Addr:    ":8080",
		Handler: mux,
	}

	log.Printf("server listening on %s", server.Addr)

	if err := server.ListenAndServe(); err != nil {
		log.Fatal(err)
	}
}
