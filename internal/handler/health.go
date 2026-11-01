package handler

import "net/http"

func registerHealthRoute(mux *http.ServeMux) {
	mux.HandleFunc("GET /health", healthHandler)
}

func healthHandler(w http.ResponseWriter, _ *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)

	_, _ = w.Write([]byte(`{"status":"ok"}`))
}
