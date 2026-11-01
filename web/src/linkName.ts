const tidy = (part: string) =>
  decodeURIComponent(part)
    .replace(/\.[a-z0-9]{2,5}$/i, '')
    .replace(/[_-]+/g, ' ')
    .trim()

export function linkName(link: string) {
  try {
    const parts = new URL(link).pathname.split('/').filter(Boolean).map(tidy)
    const last = parts.at(-1) ?? ''
    // numbered pages like /financial/3 need their parent to mean anything
    const name = /[a-z]/i.test(last) ? last : parts.slice(-2).join(' ')
    return name ? name[0].toUpperCase() + name.slice(1) : link
  } catch {
    return link
  }
}
