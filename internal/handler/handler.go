package handler

import (
	"net/http"

	"github.com/modelcontextprotocol/go-sdk/auth"
	"github.com/modelcontextprotocol/go-sdk/mcp"
)

const (
	serverName    = "finance-mcp"
	serverVersion = "0.1.0"
	description   = "MCP server to fetch links and reports from company's investor relations page"
)

func New(token string) http.Handler {
	mux := http.NewServeMux()

	registerHealthRoute(mux)

	server := mcp.NewServer(
		&mcp.Implementation{
			Name:        serverName,
			Version:     serverVersion,
			Description: description,
		},
		nil,
	)

	registerTools(server)

	mcpHandler := mcp.NewStreamableHTTPHandler(
		func(*http.Request) *mcp.Server {
			return server
		},
		&mcp.StreamableHTTPOptions{
			Stateless:                  true,
			DisableLocalhostProtection: true,
		},
	)

	mux.Handle(
		"/mcp",
		auth.RequireBearerToken(
			TokenVerifier(token),
			&auth.RequireBearerTokenOptions{
				AllowMissingExpiration: true,
			},
		)(mcpHandler),
	)

	return mux
}
