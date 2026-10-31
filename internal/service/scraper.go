package service

import (
	"context"
	"fmt"
	"time"

	"github.com/ayush9h/finance-mcp/internal/config"
	"github.com/chromedp/chromedp"
)

func ScrapeTitle(url string) (string, error) {
	// defining proxy settings
	options := append(chromedp.DefaultExecAllocatorOptions[:], chromedp.UserAgent(config.GetUserAgent()))

	// Parent context with proxy settings
	ctx, cancel := chromedp.NewExecAllocator(context.Background(), options...)
	defer cancel()

	ctx, cancel = chromedp.NewContext(ctx)
	defer cancel()

	// context declaration with timeout
	tctx, cancel := context.WithTimeout(ctx, 10*time.Second)
	defer cancel()

	if err := chromedp.Do(tctx, chromedp.Navigate(url)); err != nil {
		return "", fmt.Errorf("scrape %s %w", url, err)
	}

	title, err := chromedp.Run(ctx, chromedp.Title())
	if err != nil {
		return "", fmt.Errorf("scrape %s: %w", url, err)
	}

	fmt.Printf("title scraped: %s", title)

	return title, nil
}
