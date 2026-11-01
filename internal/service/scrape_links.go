package service

import (
	"context"
	"fmt"
	"net"
	neturl "net/url"
	"time"

	"github.com/ayush9h/finance-mcp/internal/config"
	"github.com/chromedp/chromedp"
)

var browserSlots = make(chan struct{}, 2)

func ValidateURL(ctx context.Context, rawURL string) error {
	u, err := neturl.Parse(rawURL)
	if err != nil {
		return fmt.Errorf("invalid url: %w", err)
	}
	if (u.Scheme != "http" && u.Scheme != "https") || u.Hostname() == "" {
		return fmt.Errorf("url must be http or https: %s", rawURL)
	}

	addrs, err := net.DefaultResolver.LookupIPAddr(ctx, u.Hostname())
	if err != nil {
		return fmt.Errorf("resolve %s: %w", u.Hostname(), err)
	}
	for _, addr := range addrs {
		if !addr.IP.IsGlobalUnicast() || addr.IP.IsPrivate() {
			return fmt.Errorf("url must not point to an internal address: %s", rawURL)
		}
	}
	return nil
}

// ScrapeLinks returns every link on the page as an absolute URL
func ScrapeLinks(ctx context.Context, url, waitFor string) ([]string, error) {
	return evaluateLinks[string](ctx, url, waitFor, `Array.from(document.links, a => a.href)`)
}

// evaluateLinks opens the page in a browser and decodes the result of expression into a slice of T
func evaluateLinks[T any](ctx context.Context, url, waitFor, expression string) ([]T, error) {
	select {
	case browserSlots <- struct{}{}:
		defer func() { <-browserSlots }()
	case <-ctx.Done():
		return nil, fmt.Errorf("scrape %s: %w", url, ctx.Err())
	}

	if waitFor == "" {
		waitFor = "a[href]"
	}

	// defining browser settings
	options := append(chromedp.DefaultExecAllocatorOptions[:], chromedp.VisibleWindow, chromedp.UserAgent(config.GetUserAgent()))

	// Parent context with browser settings
	ctx, cancel := chromedp.NewExecAllocator(ctx, options...)
	defer cancel()

	ctx, cancel = chromedp.NewContext(ctx)
	defer cancel()

	// context declaration with timeout
	tctx, cancel := context.WithTimeout(ctx, 30*time.Second)
	defer cancel()

	if err := chromedp.Do(tctx, chromedp.Navigate(url), chromedp.WaitReady(chromedp.CSS(waitFor))); err != nil {
		return nil, fmt.Errorf("scrape %s: %w", url, err)
	}

	//location.href
	finalURL, err := chromedp.Run(tctx, chromedp.Evaluate[string](`location.href`))
	if err != nil {
		return nil, fmt.Errorf("scrape %s: %w", url, err)
	}
	if err := ValidateURL(tctx, finalURL); err != nil {
		return nil, fmt.Errorf("scrape %s: %w", url, err)
	}

	// a tags href are found
	links, err := chromedp.Run(tctx, chromedp.Evaluate[[]T](expression))
	if err != nil {
		return nil, fmt.Errorf("scrape %s: %w", url, err)
	}

	return links, nil
}
