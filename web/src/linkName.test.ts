import assert from 'node:assert/strict'
import { test } from 'node:test'
import { linkName } from './linkName.ts'

const cases = [
  [
    'https://a.com/tool/file/21/2025_Annual%20Report?note=Annual%20Report',
    '2025 Annual Report',
  ],
  ['https://a.com/reports/q3-earnings-report.pdf', 'Q3 earnings report'],
  ['https://a.com/en/investor/financial/3', 'Financial 3'],
  ['https://a.com/', 'https://a.com/'],
  ['https://a.com/100%report', 'https://a.com/100%report'],
  ['not a url', 'not a url'],
]

for (const [link, want] of cases) {
  test(link, () => assert.equal(linkName(link), want))
}
