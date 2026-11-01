import assert from 'node:assert/strict'
import { afterEach, test } from 'node:test'
import { POST } from './mcp.ts'

const realFetch = globalThis.fetch

afterEach(() => {
  globalThis.fetch = realFetch
})

function call(body: string) {
  return POST(new Request('http://test/api/mcp', { method: 'POST', body }))
}

function serve(sse: string) {
  const seen: RequestInit[] = []
  process.env.MCP_URL = 'http://mcp.test/mcp'
  process.env.MCP_TOKEN = 'secret'
  globalThis.fetch = async (_url, init) => {
    seen.push(init!)
    return new Response(sse)
  }
  return seen
}

test('calls the tool with the token and returns its links', async () => {
  const seen = serve(
    'event: message\ndata: {"result":{"structuredContent":{"links":["https://a.com/r"]}}}\n\n',
  )

  const response = await call('{"url":"https://a.com","tool":"links"}')

  assert.deepEqual(await response.json(), { links: ['https://a.com/r'] })
  const headers = seen[0].headers as Record<string, string>
  assert.equal(headers.Authorization, 'Bearer secret')
  assert.equal(JSON.parse(seen[0].body as string).params.name, 'scrape_links')
})

test('tells the visitor when the server is rate limited', async () => {
  serve(
    'data: {"result":{"isError":true,"content":[{"text":"server busy, try again in a minute"}]}}\n',
  )

  const response = await call('{"url":"https://a.com"}')

  assert.equal(response.status, 429)
})

test('hides tool errors and bad requests from the visitor', async () => {
  serve(
    'data: {"result":{"isError":true,"content":[{"text":"internal detail"}]}}\n',
  )

  for (const body of ['{"url":"file:///etc/passwd"}', '{']) {
    const response = await call(body)
    assert.equal(response.status, 502)
    assert.doesNotMatch(await response.text(), /internal detail/)
  }
})
