'use client'

import { useState, useCallback } from 'react'
import { Upload, FileText, AlertCircle } from 'lucide-react'

interface FileUploadProps {
  onFileProcessed: (data: any[]) => void
}

export default function FileUpload({ onFileProcessed }: FileUploadProps) {
  const [isDragOver, setIsDragOver] = useState(false)
  const [isProcessing, setIsProcessing] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const processFile = useCallback(async (file: File) => {
    setIsProcessing(true)
    setError(null)

    try {
      const formData = new FormData()
      formData.append('file', file)

      const response = await fetch('/api/process-portfolio', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error(`Failed to process file: ${response.statusText}`)
      }

      const data = await response.json()
      onFileProcessed(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to process file')
    } finally {
      setIsProcessing(false)
    }
  }, [onFileProcessed])

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragOver(false)

    const files = Array.from(e.dataTransfer.files)
    const file = files[0]

    if (file && (file.name.endsWith('.xlsx') || file.name.endsWith('.xls'))) {
      processFile(file)
    } else {
      setError('Please upload an Excel file (.xlsx or .xls)')
    }
  }, [processFile])

  const handleFileSelect = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      processFile(file)
    }
  }, [processFile])

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragOver(true)
  }, [])

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragOver(false)
  }, [])

  return (
    <div className="max-w-2xl mx-auto">
      <div
        className={`border-2 border-dashed rounded-lg p-12 text-center transition-colors ${
          isDragOver
            ? 'border-blue-500 bg-blue-50'
            : 'border-gray-300 hover:border-gray-400'
        }`}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
      >
        <div className="mb-6">
          {isProcessing ? (
            <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto"></div>
          ) : (
            <Upload className="mx-auto h-16 w-16 text-gray-400" />
          )}
        </div>

        <h3 className="text-xl font-semibold text-gray-900 mb-2">
          {isProcessing ? 'Processing your portfolio...' : 'Upload your portfolio'}
        </h3>

        <p className="text-gray-600 mb-6">
          {isProcessing
            ? 'Analyzing your investments and detecting asset classes...'
            : 'Drag and drop your Excel file here, or click to browse'
          }
        </p>

        {!isProcessing && (
          <label className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 cursor-pointer">
            <FileText className="mr-2 h-5 w-5" />
            Choose Excel File
            <input
              type="file"
              className="hidden"
              accept=".xlsx,.xls"
              onChange={handleFileSelect}
            />
          </label>
        )}

        <p className="text-sm text-gray-500 mt-4">
          Supports .xlsx and .xls files from brokers like Angel One, Zerodha, etc.
        </p>
      </div>

      {error && (
        <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-md">
          <div className="flex">
            <AlertCircle className="h-5 w-5 text-red-400" />
            <div className="ml-3">
              <h3 className="text-sm font-medium text-red-800">Error</h3>
              <div className="mt-1 text-sm text-red-700">{error}</div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}