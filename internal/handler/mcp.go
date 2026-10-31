package handler

import (
	"context"
	"crypto/subtle"
	_ "embed"
	"net/http"

	"github.com/ayush9h/finance-mcp/internal/service"
	"github.com/modelcontextprotocol/go-sdk/auth"
	"github.com/modelcontextprotocol/go-sdk/mcp"
)

//go:embed index.html
var indexHTML []byte

type scrapeInput struct {
	URL     string `json:"url" jsonschema:"http or https page to scrape"`
	WaitFor string `json:"wait_for,omitempty" jsonschema:"CSS selector to wait for before reading links, for pages that load content with JavaScript. Defaults to the first link on the page"`
}

type scrapeOutput struct {
	Links []string `json:"links" jsonschema:"absolute URL of every link on the page"`
}

func scrapeLinks(ctx context.Context, _ *mcp.CallToolRequest, input scrapeInput) (*mcp.CallToolResult, scrapeOutput, error) {
	if err := service.ValidateURL(ctx, input.URL); err != nil {
		return nil, scrapeOutput{}, err
	}

	links, err := service.ScrapeLinks(ctx, input.URL, input.WaitFor)
	if err != nil {
		return nil, scrapeOutput{}, err
	}

	return nil, scrapeOutput{Links: links}, nil
}

// New returns the HTTP routes of the server
func New(token string) http.Handler {
	mux := http.NewServeMux()

	mux.HandleFunc("GET /{$}", func(w http.ResponseWriter, r *http.Request) {
		w.Write(indexHTML)
	})

	// Health Check
	mux.HandleFunc("GET /health", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		w.Write([]byte(`{"status":"ok from go. The server has started running"}`))
	})

	// MCP endpoint
	server := mcp.NewServer(&mcp.Implementation{Name: "finance-mcp", Version: "0.1.0"}, nil)
	mcp.AddTool(server, &mcp.Tool{Name: "scrape_links", Description: "Open a page in a browser and return every link on it"}, scrapeLinks)

	handler := mcp.NewStreamableHTTPHandler(func(*http.Request) *mcp.Server { return server }, &mcp.StreamableHTTPOptions{Stateless: true})

	verifier := func(_ context.Context, got string, _ *http.Request) (*auth.TokenInfo, error) {
		if subtle.ConstantTimeCompare([]byte(got), []byte(token)) != 1 {
			return nil, auth.ErrInvalidToken
		}
		return &auth.TokenInfo{}, nil
	}
	mux.Handle("/mcp", auth.RequireBearerToken(verifier, &auth.RequireBearerTokenOptions{AllowMissingExpiration: true})(handler))

	return mux
}
