# CLAUDE.md

Behavioral guidelines for the Finance MCP server (Go 1.27, MCP Go SDK over Streamable HTTP, chromedp on an Xvfb display, Docker on Render). Merge with any repo-level instructions.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.
- Check where code belongs (see Project Structure) before creating a file.
- Check the installed API before using it. chromedp v0.21 is generic: `chromedp.Run` returns a value, and `chromedp.Do` runs void actions.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.
- Reuse what exists: `service.ValidateURL`, `config.GetUserAgent`, the SDK's `auth.RequireBearerToken`, and the standard library before adding a dependency or a parallel mechanism.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add a tool" → "It's registered, has a test, and the suite passes"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Verify from the repo root:
- `go build ./...` - everything compiles
- `go vet ./...` - static checks
- `go test ./...` - full suite
- `go test ./internal/service/` - a single package
- `GOOS=linux GOARCH=amd64 go build ./cmd/server` - the deployed target still builds

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

## 5. Project Structure

**Standard Go layout. Handlers stay thin.**

```
cmd/server/       main.go: env vars and server startup only
internal/
├── handler/      mcp.go: tool inputs and outputs, tool handlers, routing, auth
├── service/      business logic: URL validation, browser scraping
└── config/       static configuration such as user agents
deploy/           systemd unit for a Linux VM
Dockerfile        image for Render: Chromium, Xvfb, and the server under xvfb-run
```

- Keep types in the same file as the code that uses them. No separate `types.go`, `models.go`, or `schemas` files or packages.
- Follow Go conventions for files: short lowercase package names, one package per directory, and no `utils` or `helpers` packages.
- Create a new file or package only when the code has a distinct responsibility, not to mirror another language's layout.
- Code used by one package stays in that package. Keep it unexported until another package needs it.
- Put tests in `<file>_test.go` beside the code they cover.
- New MCP tool: define its input and output structs and handler in `internal/handler/mcp.go`, register it with `mcp.AddTool` in `New`, and put the logic in `internal/service`.
- Read env vars in `main` and pass the values down as arguments. Current vars: `MCP_TOKEN` (required) and `PORT` (optional, default 8080).

## 6. Concurrency & Browser

**Pass the context. Bound every browser call.**

- `context.Context` is the first parameter of anything that does I/O. Don't start from `context.Background()` when a caller has a context.
- Every scrape takes a slot from `browserSlots`, runs under a timeout, and closes its browser with `defer cancel()`.
- The browser runs with a visible window through `chromedp.VisibleWindow`, so it needs a display: `xvfb-run` on Linux, never headless.
- Call `service.ValidateURL` before opening any caller-supplied URL. Never let the browser open `file://` or internal addresses.
- Compare secrets with `crypto/subtle`, and never log or return tokens.

## 7. Logging & Errors

**Return errors with context. Log at the top.**

- Wrap errors with `fmt.Errorf("...: %w", err)` and return them. Don't log and return the same error.
- Use the standard `log` package in `cmd/server`.
- Tool errors reach the client, so keep secrets and internal details out of them.

## 8. Tests

- Every new tool and service function gets a test beside the code.
- Use `net/http/httptest` for servers and pages. Tests never hit real services.
- Prefer table-driven tests.
- Tests that need a real browser are not part of the default suite.

## 9. Comments

- One-line `//` comments only, and only where the "why" isn't obvious.
- No multi-line comments.
- No comments in the `Dockerfile`.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.
