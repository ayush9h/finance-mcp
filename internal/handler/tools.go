package handler

import (
	"context"
	"errors"
	"log/slog"
	"time"

	"github.com/ayush9h/finance-mcp/internal/service"
	"github.com/modelcontextprotocol/go-sdk/mcp"
	"golang.org/x/time/rate"
)

var scrapeLimiter = rate.NewLimiter(rate.Every(15*time.Second), 4)
var errBusy = errors.New("server busy, try again in a minute")

// Input schema for ScrapeLinks
type scrapeInput struct {
	URL     string  `json:"url" jsonschema:"http or https page to scrape"`
	WaitFor *string `json:"wait_for,omitempty" jsonschema:"CSS Selector to wait for before reading links"`
}

func (i scrapeInput) waitFor() string {
	if i.WaitFor == nil {
		return ""
	}
	return *i.WaitFor
}

// Output schema for ScrapeLinks
type scrapeOutput struct {
	Links []string `json:"links" jsonschema:"absoulte url of every link on the page"`
}

// Calls the scrape link tool
func scrapeLinks(ctx context.Context, _ *mcp.CallToolRequest, input scrapeInput) (*mcp.CallToolResult, scrapeOutput, error) {
	if err := service.ValidateURL(ctx, input.URL); err != nil {
		slog.LogAttrs(ctx, slog.LevelError, "error in url validation", slog.String("message", err.Error()))
		return nil, scrapeOutput{}, err
	}

	if !scrapeLimiter.Allow() {
		return nil, scrapeOutput{}, errBusy
	}

	links, err := service.ScrapeLinks(ctx, input.URL, input.waitFor())
	if err != nil {
		slog.LogAttrs(ctx, slog.LevelError, "error in link scraping", slog.String("message", err.Error()))
		return nil, scrapeOutput{}, err
	}

	slog.Info("scrape completed")

	return nil, scrapeOutput{Links: links}, nil
}

// ===================================================================

type reportsOutput struct {
	Links []string `json:"links" jsonschema:"absolute url of every link whose URL or title mentions report"`
}

func scrapeReports(ctx context.Context, _ *mcp.CallToolRequest, input scrapeInput) (*mcp.CallToolResult, reportsOutput, error) {
	if err := service.ValidateURL(ctx, input.URL); err != nil {
		slog.LogAttrs(ctx, slog.LevelError, "error in url validation", slog.String("message", err.Error()))
		return nil, reportsOutput{}, err
	}

	if !scrapeLimiter.Allow() {
		return nil, reportsOutput{}, errBusy
	}

	links, err := service.ScrapeReports(ctx, input.URL, input.waitFor())
	if err != nil {
		slog.LogAttrs(ctx, slog.LevelError, "error in report scraping", slog.String("message", err.Error()))
		return nil, reportsOutput{}, err
	}

	slog.Info("scrape completed")

	return nil, reportsOutput{Links: links}, nil
}

// ======================================================================

func registerTools(server *mcp.Server) {
	mcp.AddTool(server, &mcp.Tool{
		Name:        "scrape_links",
		Description: "Opens a page in browser and returns every link on it"}, scrapeLinks)

	mcp.AddTool(server, &mcp.Tool{
		Name:        "scrape_reports",
		Description: "Open a page in a browser and return only the links whose URL or title mentions report"},
		scrapeReports)
}
