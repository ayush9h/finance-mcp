const FAILED = 'We could not read links from that page.'
const BUSY = 'The server is busy. Try again in a minute.'

// runs on Vercel so MCP_TOKEN stays on the server and out of the browser bundle
export async function POST(request: Request) {
  try {
    const { url, tool } = await request.json()

    const response = await fetch(process.env.MCP_URL!, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${process.env.MCP_TOKEN}`,
        'Content-Type': 'application/json',
        Accept: 'application/json, text/event-stream',
      },
      body: JSON.stringify({
        jsonrpc: '2.0',
        id: 1,
        method: 'tools/call',
        params: {
          name: tool === 'links' ? 'scrape_links' : 'scrape_reports',
          arguments: { url },
        },
      }),
    })

    const event = (await response.text())
      .split('\n')
      .find((line) => line.startsWith('data:'))
    const result = event && JSON.parse(event.slice(5)).result

    if (result?.content?.[0]?.text?.includes('server busy')) {
      return Response.json({ error: BUSY }, { status: 429 })
    }
    if (!result?.structuredContent || result.isError) {
      return Response.json({ error: FAILED }, { status: 502 })
    }
    return Response.json({ links: result.structuredContent.links ?? [] })
  } catch {
    return Response.json({ error: FAILED }, { status: 502 })
  }
}
