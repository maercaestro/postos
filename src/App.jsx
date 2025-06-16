import { useState, useEffect } from 'react'
import MapComponent from './components/MapComponent'
import StationCard from './components/StationCard'
import StatsPanel from './components/StatsPanel'
import SearchBar from './components/SearchBar'
import DataLoader from './components/DataLoader'
import { calculateStats } from './utils/dataUtils'
import { MapPin, BarChart3, Star, Users } from 'lucide-react'

function App() {
  const [stations, setStations] = useState([])
  const [selectedStation, setSelectedStation] = useState(null)
  const [filteredStations, setFilteredStations] = useState([])
  const [searchTerm, setSearchTerm] = useState('')
  const [dataLoaded, setDataLoaded] = useState(false)

  const handleDataLoaded = (data) => {
    setStations(data)
    setFilteredStations(data)
    setDataLoaded(true)
  }

  useEffect(() => {
    if (searchTerm) {
      const filtered = stations.filter(station =>
        station.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        station.address.toLowerCase().includes(searchTerm.toLowerCase())
      )
      setFilteredStations(filtered)
    } else {
      setFilteredStations(stations)
    }
  }, [searchTerm, stations])

  if (!dataLoaded) {
    return <DataLoader onDataLoaded={handleDataLoaded} />
  }

  const totalStations = stations.length
  const stats = calculateStats(stations)
  const { averageRating, totalReviews } = stats

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      {/* Demo Banner */}
      <div className="bg-gradient-to-r from-orange-500 to-red-500 text-white py-3 px-6 text-center">
        <div className="container mx-auto">
          <p className="text-sm font-medium">
            🚀 <strong>DEMO VERSION</strong> - Raizen Analytics Prototype | 
            <span className="ml-2">1,201 unique stations • 3,500+ reviews • Real-time insights</span>
          </p>
        </div>
      </div>

      {/* Header */}
      <header className="sticky top-0 z-50 bg-white/10 backdrop-blur-xl border-b border-white/20">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-12 h-12 bg-gradient-to-r from-orange-500 to-red-500 rounded-2xl flex items-center justify-center">
                <MapPin className="w-7 h-7 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-800">Raizen Analytics</h1>
                <p className="text-sm text-gray-600">Gas Station Intelligence Platform</p>
              </div>
            </div>
            <SearchBar searchTerm={searchTerm} setSearchTerm={setSearchTerm} />
          </div>
        </div>
      </header>

      {/* Stats Panel */}
      <div className="container mx-auto px-6 py-6">
        <StatsPanel 
          totalStations={totalStations}
          averageRating={averageRating}
          totalReviews={totalReviews}
        />
      </div>

      {/* Main Content */}
      <div className="container mx-auto px-6 pb-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Map Section */}
          <div className="lg:col-span-2">
            <div className="bg-white/20 backdrop-blur-xl rounded-3xl border border-white/30 shadow-2xl overflow-hidden">
              <div className="p-6 border-b border-white/20">
                <h2 className="text-xl font-bold text-gray-800 flex items-center">
                  <MapPin className="w-5 h-5 mr-2 text-blue-600" />
                  Station Locations
                </h2>
                <p className="text-sm text-gray-600 mt-1">
                  {filteredStations.length} stations found
                </p>
              </div>
              <div className="h-[500px]">
                <MapComponent 
                  stations={filteredStations} 
                  selectedStation={selectedStation}
                  setSelectedStation={setSelectedStation}
                />
              </div>
            </div>
          </div>

          {/* Station Details */}
          <div className="space-y-6">
            {selectedStation ? (
              <StationCard station={selectedStation} />
            ) : (
              <div className="bg-white/20 backdrop-blur-xl rounded-3xl border border-white/30 shadow-2xl p-8 text-center">
                <MapPin className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-semibold text-gray-700 mb-2">Select a Station</h3>
                <p className="text-gray-600">Click on any marker on the map to view detailed information about that gas station.</p>
              </div>
            )}

            {/* Quick Stats */}
            <div className="bg-white/20 backdrop-blur-xl rounded-3xl border border-white/30 shadow-2xl p-6">
              <h3 className="text-lg font-bold text-gray-800 mb-4 flex items-center">
                <BarChart3 className="w-5 h-5 mr-2 text-purple-600" />
                Quick Insights
              </h3>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Top Rated</span>
                  <span className="font-semibold text-green-600">
                    {Math.max(...stations.map(s => s.rating)).toFixed(1)}★
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Most Reviews</span>
                  <span className="font-semibold text-blue-600">
                    {Math.max(...stations.map(s => s.reviews.length))}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Coverage</span>
                  <span className="font-semibold text-purple-600">Brazil Wide</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
