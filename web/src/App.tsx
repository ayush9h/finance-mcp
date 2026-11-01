import { useState, type FormEvent } from 'react'
import './App.css'
import { linkName } from './linkName.ts'

const GITHUB_URL = 'https://github.com/ayush9h/finance-mcp'

const SETUP = `git clone ${GITHUB_URL}.git && cd finance-mcp
printf 'MCP_TOKEN=change-me\\nPORT=8080\\n' > .env
go run ./cmd/financemcp &
claude mcp add --transport http finance http://localhost:8080/mcp \\
  --header "Authorization: Bearer change-me"`

type Tool = 'reports' | 'links'

const TOOLS: { value: Tool; label: string }[] = [
  { value: 'reports', label: 'Reports' },
  { value: 'links', label: 'All links' },
]

type Result = { host: string; tool: Tool; links: string[] }

function normalize(value: string) {
  const trimmed = value.trim()
  return /^https?:\/\//i.test(trimmed) ? trimmed : `https://${trimmed}`
}

async function runDemo(url: string, tool: Tool): Promise<string[]> {
  const response = await fetch('/api/mcp', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url, tool }),
  })
  const data = await response.json().catch(() => null)
  if (!response.ok) {
    throw new Error(data?.error ?? 'We could not reach the server.')
  }
  return data.links
}

function Logo() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <circle cx="12" cy="12" r="12" fill="#fff" />
      <path
        d="M12 5v14M15.5 7.5H10.6a2.3 2.3 0 0 0 0 4.5h2.8a2.3 2.3 0 0 1 0 4.5H8"
        fill="none"
        stroke="#0b2a20"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  )
}

function Demo() {
  const [url, setUrl] = useState('')
  const [tool, setTool] = useState<Tool>('reports')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [result, setResult] = useState<Result | null>(null)

  async function submit(event: FormEvent) {
    event.preventDefault()
    if (!url.trim()) {
      setError('Enter a company page URL first.')
      return
    }

    setLoading(true)
    setError('')
    setResult(null)

    try {
      const target = normalize(url)
      const links = await runDemo(target, tool)
      // scraped hrefs are untrusted, so javascript: links must never reach the DOM
      const safe = [...new Set(links)].filter((link) => /^https?:/i.test(link))
      setResult({ host: new URL(target).hostname, tool, links: safe })
    } catch (err) {
      setError(
        err instanceof TypeError
          ? 'We could not reach the server. Try again in a minute.'
          : (err as Error).message,
      )
    } finally {
      setLoading(false)
    }
  }

  const noun = result?.tool === 'reports' ? 'report link' : 'link'

  return (
    <>
      <form className="row try" onSubmit={submit} aria-busy={loading}>
        <fieldset className="toggle">
          <legend className="sr-only">What to find</legend>
          {TOOLS.map((option) => (
            <label key={option.value}>
              <input
                type="radio"
                name="tool"
                value={option.value}
                checked={tool === option.value}
                onChange={() => setTool(option.value)}
              />
              {option.label}
            </label>
          ))}
        </fieldset>

        <label className="sr-only" htmlFor="url">
          Company page URL
        </label>
        <input
          id="url"
          type="text"
          inputMode="url"
          autoComplete="url"
          spellCheck={false}
          placeholder="https://investor.yourcompany.com"
          value={url}
          onChange={(event) => setUrl(event.target.value)}
        />
        <button className="go" type="submit" disabled={loading}>
          {loading ? 'Reading...' : 'Find links'}
        </button>
      </form>

      {loading && (
        <p className="row hint">
          Opening the page in a real browser. This can take 30 seconds.
        </p>
      )}

      <div className="status" aria-live="polite">
        {error && (
          <p className="row error" role="alert">
            {error}
          </p>
        )}
        {result && (
          <section className="result">
            <h2 className="row">
              {result.links.length} {noun}
              {result.links.length === 1 ? '' : 's'} on {result.host}
            </h2>
            {result.links.length === 0 ? (
              <p className="row result-empty">
                Nothing matched here. Try All links, or a page that lists
                reports.
              </p>
            ) : (
              <ol>
                {result.links.map((link) => (
                  <li className="row" key={link}>
                    <a
                      href={link}
                      target="_blank"
                      rel="noopener noreferrer"
                      title={link}
                    >
                      <span>{linkName(link)}</span>
                      <small>{link}</small>
                    </a>
                  </li>
                ))}
              </ol>
            )}
          </section>
        )}
      </div>
    </>
  )
}

function Connect() {
  const [copied, setCopied] = useState(false)

  async function copy() {
    await navigator.clipboard.writeText(SETUP)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <section className="row split" id="connect">
      <div className="split-label">
        <h2>Connect</h2>
        <p>
          Run your own copy with a token you choose, then add it to any MCP
          client.
        </p>
      </div>
      <div className="terminal">
        <pre tabIndex={0}>
          <code>{SETUP}</code>
        </pre>
        <button className="copy" type="button" onClick={copy}>
          {copied ? 'Copied' : 'Copy'}
        </button>
      </div>
    </section>
  )
}

function App() {
  return (
    <div className="page">
      <header className="hero">
        <nav className="row nav" aria-label="Main">
          <a className="brand" href="#top">
            <Logo />
            <span>
              <b>Finance</b>MCP
            </span>
          </a>
          <a className="nav-link nav-end" href="#tools">
            Tools
          </a>
          <a className="nav-link" href="#connect">
            Connect
          </a>
          <a className="nav-link" href={GITHUB_URL}>
            GitHub
          </a>
        </nav>

        <div className="row intro" id="top">
          <h1>Bring company reports into your AI</h1>
          <p className="lead">
            Point FinanceMCP at an investor relations page and get the report
            links back, ready for your AI assistant to read.
          </p>
        </div>

      </header>

      <main>
        <Demo />

        <div className="row spacer" />

        <section className="row split" id="tools">
          <div className="split-label">
            <h2>Tools</h2>
            <p>Two tools your assistant can call.</p>
          </div>
          <ul className="tools">
            <li>
              <code>scrape_reports</code>
              <p>Links whose URL or title mentions a report.</p>
            </li>
            <li>
              <code>scrape_links</code>
              <p>Every link on the page, as absolute URLs.</p>
            </li>
          </ul>
        </section>

        <Connect />
      </main>

      <div className="row spacer" />

      <footer className="row footer">MIT licensed.</footer>
    </div>
  )
}

export default App
