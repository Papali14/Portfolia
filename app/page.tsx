'use client'

import { useState } from 'react'
import FileUpload from '@/components/FileUpload'
import PortfolioAnalysis from '@/components/PortfolioAnalysis'

export default function Home() {
  const [portfolioData, setPortfolioData] = useState<any[]>([])

  const handleFileProcessed = (data: any[]) => {
    setPortfolioData(data)
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Portfolio Analyzer
          </h1>
          <p className="text-xl text-gray-600">
            Upload your investment portfolio and get AI-powered insights
          </p>
        </div>

        {!portfolioData.length ? (
          <FileUpload onFileProcessed={handleFileProcessed} />
        ) : (
          <PortfolioAnalysis data={portfolioData} />
        )}
      </div>
    </main>
  )
}