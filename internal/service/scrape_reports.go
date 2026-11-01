package service

import (
	"context"
	"strings"
)

type pageLink struct {
	Href  string `json:"href"`
	Title string `json:"title"`
}

// ScrapeReports returns the links on the page whose URL or title mentions "report"
func ScrapeReports(ctx context.Context, url, waitFor string) ([]string, error) {
	links, err := evaluateLinks[pageLink](ctx, url, waitFor, `Array.from(document.links, a => ({href: a.href, title: a.textContent + ' ' + a.title}))`)
	if err != nil {
		return nil, err
	}
	return filterReports(links), nil
}

func filterReports(links []pageLink) []string {
	reports := []string{}
	for _, link := range links {
		if strings.Contains(strings.ToLower(link.Href+" "+link.Title), "report") {
			reports = append(reports, link.Href)
		}
	}
	return reports
}
