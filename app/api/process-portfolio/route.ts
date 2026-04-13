import { NextRequest, NextResponse } from 'next/server'
import * as XLSX from 'xlsx'
import Papa from 'papaparse'

interface PortfolioHolding {
  symbol: string
  asset_class: string
  market_value: number
}

// Asset class inference logic (converted from Python)
function inferAssetClass(fundName: string): string {
  const name = fundName.toLowerCase()

  // Equity patterns
  if (name.includes('nifty') || name.includes('sensex') || name.includes('equity') ||
      name.includes('large cap') || name.includes('mid cap') || name.includes('small cap') ||
      name.includes('multi asset') || name.includes('aggressive') || name.includes('balanced')) {
    return 'equity'
  }

  // Debt patterns
  if (name.includes('debt') || name.includes('bond') || name.includes(' gilt') ||
      name.includes('corporate bond') || name.includes('short term') || name.includes('liquid') ||
      name.includes('ultra short') || name.includes('dynamic bond') || name.includes('conservative')) {
    return 'debt'
  }

  // Gold patterns
  if (name.includes('gold') || name.includes('commodity') || name.includes('gold etf')) {
    return 'gold'
  }

  // Cash patterns
  if (name.includes('liquid') || name.includes('overnight') || name.includes('money market') ||
      name.includes('cash') || name.includes('treasury') || name.includes('savings')) {
    return 'cash'
  }

  return 'unknown'
}

function processExcelData(buffer: ArrayBuffer): PortfolioHolding[] {
  const workbook = XLSX.read(buffer, { type: 'array' })
  const sheetName = workbook.SheetNames[0]
  const worksheet = workbook.Sheets[sheetName]

  // Convert to JSON
  const jsonData = XLSX.utils.sheet_to_json(worksheet, { header: 1 }) as any[][]

  if (jsonData.length < 2) {
    throw new Error('Excel file must contain at least a header row and one data row')
  }

  // Find relevant columns
  const headers = jsonData[0].map(h => h?.toString().toLowerCase().trim() || '')
  const dataRows = jsonData.slice(1)

  // Map column indices
  const symbolIndex = headers.findIndex(h =>
    h.includes('scheme') || h.includes('fund') || h.includes('name') || h.includes('symbol')
  )
  const valueIndex = headers.findIndex(h =>
    h.includes('value') && h.includes('on') ||
    h.includes('market value') || h.includes('current value') ||
    h.includes('invested value')
  )
  const navIndex = headers.findIndex(h =>
    h.includes('nav') && h.includes('on') ||
    h.includes('nav as on')
  )

  if (symbolIndex === -1 || valueIndex === -1) {
    throw new Error('Could not find required columns: symbol/fund name and market value')
  }

  const holdings: PortfolioHolding[] = []

  for (const row of dataRows) {
    if (!row[symbolIndex] || !row[valueIndex]) continue

    const fundName = row[symbolIndex].toString().trim()
    const marketValue = parseFloat(row[valueIndex].toString().replace(/,/g, '')) || 0

    if (marketValue <= 0) continue

    const assetClass = inferAssetClass(fundName)

    holdings.push({
      symbol: fundName,
      asset_class: assetClass,
      market_value: marketValue
    })
  }

  return holdings
}

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData()
    const file = formData.get('file') as File

    if (!file) {
      return NextResponse.json({ error: 'No file uploaded' }, { status: 400 })
    }

    // Check file type
    if (!file.name.endsWith('.xlsx') && !file.name.endsWith('.xls')) {
      return NextResponse.json({ error: 'Only Excel files (.xlsx, .xls) are supported' }, { status: 400 })
    }

    // Convert file to buffer
    const buffer = await file.arrayBuffer()

    // Process the Excel data
    const holdings = processExcelData(buffer)

    if (holdings.length === 0) {
      return NextResponse.json({ error: 'No valid holdings found in the file' }, { status: 400 })
    }

    return NextResponse.json(holdings)

  } catch (error) {
    console.error('Error processing portfolio:', error)
    return NextResponse.json({
      error: error instanceof Error ? error.message : 'Failed to process portfolio file'
    }, { status: 500 })
  }
}