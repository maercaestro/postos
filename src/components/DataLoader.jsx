import { useState, useEffect } from 'react'
import { AlertCircle, RefreshCw } from 'lucide-react'
import { cleanStationData } from '../utils/dataUtils'

const DataLoader = ({ onDataLoaded }) => {
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [retryCount, setRetryCount] = useState(0)

  const loadData = async () => {
    try {
      setLoading(true)
      setError(null)
      
      const response = await fetch('/raizen_places_cleaned.json')
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      
      if (!Array.isArray(data) || data.length === 0) {
        throw new Error('Invalid or empty data received')
      }
      
      // Clean and validate the data
      const cleanedData = cleanStationData(data)
      
      if (cleanedData.length === 0) {
        throw new Error('No valid station data found after cleaning')
      }
      
      onDataLoaded(cleanedData)
      setLoading(false)
    } catch (err) {
      console.error('Error loading data:', err)
      setError(err.message)
      setLoading(false)
    }
  }

  useEffect(() => {
    loadData()
  }, [retryCount])

  const handleRetry = () => {
    setRetryCount(prev => prev + 1)
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 flex items-center justify-center">
        <div className="bg-white/30 backdrop-blur-xl rounded-3xl p-8 border border-white/20 shadow-2xl text-center">
          <div className="animate-spin w-16 h-16 border-4 border-blue-500 border-t-transparent rounded-full mx-auto mb-6"></div>
          <h2 className="text-2xl font-bold text-gray-800 mb-2">Loading Raizen Analytics</h2>
          <p className="text-gray-600 mb-4">Preparing your gas station intelligence dashboard...</p>
          <div className="bg-blue-100 rounded-xl p-4">
            <p className="text-blue-800 text-sm">
              Loading {retryCount > 0 ? `(Attempt ${retryCount + 1})` : ''} 1,201+ gas stations with reviews
            </p>
          </div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-red-50 via-orange-50 to-yellow-50 flex items-center justify-center">
        <div className="bg-white/30 backdrop-blur-xl rounded-3xl p-8 border border-white/20 shadow-2xl text-center max-w-md">
          <AlertCircle className="w-16 h-16 text-red-500 mx-auto mb-6" />
          <h2 className="text-2xl font-bold text-gray-800 mb-2">Loading Failed</h2>
          <p className="text-gray-600 mb-4">Unable to load the gas station data.</p>
          
          <div className="bg-red-100 rounded-xl p-4 mb-6">
            <p className="text-red-800 text-sm font-medium mb-2">Error Details:</p>
            <p className="text-red-700 text-sm">{error}</p>
          </div>
          
          <button
            onClick={handleRetry}
            className="bg-gradient-to-r from-blue-500 to-purple-600 text-white py-3 px-6 rounded-xl font-medium hover:from-blue-600 hover:to-purple-700 transition-all duration-200 flex items-center space-x-2 mx-auto"
          >
            <RefreshCw className="w-5 h-5" />
            <span>Retry Loading</span>
          </button>
          
          <div className="mt-6 p-4 bg-yellow-100 rounded-xl">
            <p className="text-yellow-800 text-sm">
              <strong>Demo Note:</strong> This is a development version. In production, 
              data would be loaded from a secure API endpoint.
            </p>
          </div>
        </div>
      </div>
    )
  }

  return null
}

export default DataLoader
