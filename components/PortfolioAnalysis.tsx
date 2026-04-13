'use client'

import { useMemo } from 'react'
import { PieChart, Pie, Cell, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts'
import { TrendingUp, PieChart as PieChartIcon, BarChart3, Download } from 'lucide-react'

interface PortfolioData {
  symbol: string
  asset_class: string
  market_value: number
}

interface PortfolioAnalysisProps {
  data: PortfolioData[]
}

const COLORS = {
  equity: '#3B82F6',
  debt: '#10B981',
  gold: '#F59E0B',
  cash: '#6B7280',
  unknown: '#EF4444'
}

export default function PortfolioAnalysis({ data }: PortfolioAnalysisProps) {
  const analysis = useMemo(() => {
    const totalValue = data.reduce((sum, item) => sum + item.market_value, 0)

    const assetClassBreakdown = data.reduce((acc, item) => {
      const assetClass = item.asset_class
      if (!acc[assetClass]) {
        acc[assetClass] = { value: 0, count: 0 }
      }
      acc[assetClass].value += item.market_value
      acc[assetClass].count += 1
      return acc
    }, {} as Record<string, { value: number; count: number }>)

    const pieData = Object.entries(assetClassBreakdown).map(([assetClass, { value, count }]) => ({
      name: assetClass.charAt(0).toUpperCase() + assetClass.slice(1),
      value,
      percentage: ((value / totalValue) * 100).toFixed(1),
      count
    }))

    const topHoldings = data
      .sort((a, b) => b.market_value - a.market_value)
      .slice(0, 10)

    return {
      totalValue,
      assetClassBreakdown,
      pieData,
      topHoldings
    }
  }, [data])

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value)
  }

  return (
    <div className="space-y-8">
      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <TrendingUp className="h-8 w-8 text-blue-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Portfolio Value</p>
              <p className="text-2xl font-bold text-gray-900">{formatCurrency(analysis.totalValue)}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <PieChartIcon className="h-8 w-8 text-green-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Asset Classes</p>
              <p className="text-2xl font-bold text-gray-900">{Object.keys(analysis.assetClassBreakdown).length}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <BarChart3 className="h-8 w-8 text-purple-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Holdings</p>
              <p className="text-2xl font-bold text-gray-900">{data.length}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Asset Allocation Pie Chart */}
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Asset Allocation</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={analysis.pieData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percentage }) => `${name}: ${percentage}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {analysis.pieData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[entry.name.toLowerCase() as keyof typeof COLORS] || '#8884d8'} />
                ))}
              </Pie>
              <Tooltip formatter={(value: number) => formatCurrency(value)} />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Top Holdings Bar Chart */}
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Top 10 Holdings</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={analysis.topHoldings}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis
                dataKey="symbol"
                angle={-45}
                textAnchor="end"
                height={80}
                fontSize={12}
              />
              <YAxis tickFormatter={formatCurrency} />
              <Tooltip formatter={(value: number) => formatCurrency(value)} />
              <Bar dataKey="market_value" fill="#3B82F6" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Holdings Table */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-200">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold text-gray-900">All Holdings</h3>
            <button className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50">
              <Download className="mr-2 h-4 w-4" />
              Export CSV
            </button>
          </div>
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Symbol
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Asset Class
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Market Value
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  % of Portfolio
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {data.map((holding, index) => (
                <tr key={index} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {holding.symbol}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                      holding.asset_class === 'equity' ? 'bg-blue-100 text-blue-800' :
                      holding.asset_class === 'debt' ? 'bg-green-100 text-green-800' :
                      holding.asset_class === 'gold' ? 'bg-yellow-100 text-yellow-800' :
                      holding.asset_class === 'cash' ? 'bg-gray-100 text-gray-800' :
                      'bg-red-100 text-red-800'
                    }`}>
                      {holding.asset_class}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {formatCurrency(holding.market_value)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {((holding.market_value / analysis.totalValue) * 100).toFixed(2)}%
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}