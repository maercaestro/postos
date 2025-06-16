import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet'
import { useEffect, useMemo, useState, useCallback } from 'react'
import MarkerClusterGroup from 'react-leaflet-cluster'
import L from 'leaflet'
import { Star, MapPin, Phone, Globe, Navigation } from 'lucide-react'
import { generateUniqueKey, isValidStation } from '../utils/dataUtils'
import 'leaflet/dist/leaflet.css'
import 'leaflet.markercluster/dist/MarkerCluster.css'
import 'leaflet.markercluster/dist/MarkerCluster.Default.css'
import '../styles/map.css'

// Fix for default markers in react-leaflet
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
})

// Custom marker icons based on rating
const createCustomIcon = (rating) => {
  const color = rating >= 4.5 ? '#10b981' : rating >= 3.5 ? '#f59e0b' : '#ef4444'
  
  return L.divIcon({
    className: 'custom-marker',
    html: `
      <div style="
        background: ${color};
        width: 32px;
        height: 32px;
        border-radius: 50% 50% 50% 0;
        transform: rotate(-45deg);
        border: 3px solid white;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
      ">
        <div style="
          transform: rotate(45deg);
          color: white;
          font-weight: bold;
          font-size: 12px;
        ">${rating.toFixed(1)}</div>
      </div>
    `,
    iconSize: [32, 32],
    iconAnchor: [16, 32],
    popupAnchor: [0, -32]
  })
}

const MapComponent = ({ stations, selectedStation, setSelectedStation }) => {
  // Center map on Brazil
  const center = [-14.2350, -51.9253]
  const zoom = 5
  const [mapLoaded, setMapLoaded] = useState(false)

  // Memoize filtered and validated stations
  const validStations = useMemo(() => {
    if (!stations || !Array.isArray(stations)) return []
    return stations.filter(isValidStation)
  }, [stations])

  // Handle map load
  const handleMapLoad = useCallback(() => {
    setMapLoaded(true)
  }, [])

  // Show loading state for large datasets
  const showLoading = !mapLoaded && validStations.length > 500

  // Memoize marker creation function
  const createOptimizedIcon = useCallback((rating) => {
    const color = rating >= 4.5 ? '#10b981' : rating >= 3.5 ? '#f59e0b' : '#ef4444'
    
    return L.divIcon({
      className: 'custom-marker-optimized',
      html: `
        <div style="
          background: ${color};
          width: 24px;
          height: 24px;
          border-radius: 50% 50% 50% 0;
          transform: rotate(-45deg);
          border: 2px solid white;
          box-shadow: 0 2px 6px rgba(0,0,0,0.3);
          display: flex;
          align-items: center;
          justify-content: center;
        ">
          <span style="
            transform: rotate(45deg);
            color: white;
            font-weight: bold;
            font-size: 10px;
          ">${rating >= 4.5 ? '★' : rating >= 3.5 ? '●' : '▲'}</span>
        </div>
      `,
      iconSize: [24, 24],
      iconAnchor: [12, 24],
      popupAnchor: [0, -24]
    })
  }, [])

  // Custom cluster icon
  const createClusterCustomIcon = useCallback((cluster) => {
    const count = cluster.getChildCount()
    const size = count < 10 ? 'small' : count < 100 ? 'medium' : 'large'
    const dimensions = { small: 30, medium: 40, large: 50 }
    
    return L.divIcon({
      html: `
        <div style="
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          width: ${dimensions[size]}px;
          height: ${dimensions[size]}px;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          color: white;
          font-weight: bold;
          font-size: ${size === 'small' ? '12' : size === 'medium' ? '14' : '16'}px;
          border: 3px solid white;
          box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        ">${count}</div>
      `,
      className: 'marker-cluster-custom',
      iconSize: [dimensions[size], dimensions[size]],
      iconAnchor: [dimensions[size] / 2, dimensions[size] / 2]
    })
  }, [])

  const renderStarRating = (rating) => {
    const stars = []
    const fullStars = Math.floor(rating)
    const hasHalfStar = rating % 1 >= 0.5

    for (let i = 0; i < fullStars; i++) {
      stars.push(<Star key={i} className="w-4 h-4 fill-yellow-400 text-yellow-400" />)
    }
    
    if (hasHalfStar) {
      stars.push(<Star key="half" className="w-4 h-4 fill-yellow-400/50 text-yellow-400" />)
    }
    
    const emptyStars = 5 - Math.ceil(rating)
    for (let i = 0; i < emptyStars; i++) {
      stars.push(<Star key={`empty-${i}`} className="w-4 h-4 text-gray-300" />)
    }
    
    return stars
  }

  return (
    <div className={`relative h-full w-full ${showLoading ? 'map-loading' : ''}`}>
      {showLoading && (
        <div className="absolute inset-0 bg-white bg-opacity-80 flex items-center justify-center z-50 rounded-b-3xl">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-600 font-medium">Loading {validStations.length} gas stations...</p>
          </div>
        </div>
      )}
      <MapContainer
        center={center}
        zoom={zoom}
        style={{ height: '100%', width: '100%' }}
        className="rounded-b-3xl"
        whenReady={handleMapLoad}
      >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      
      <MarkerClusterGroup 
        chunkedLoading
        iconCreateFunction={createClusterCustomIcon}
        maxClusterRadius={50}
        spiderfyOnMaxZoom={true}
        showCoverageOnHover={false}
        zoomToBoundsOnClick={true}
        animate={true}
        animateAddingMarkers={true}
        removeOutsideVisibleBounds={true}
        disableClusteringAtZoom={18}
      >
        {validStations.map((station, index) => (
          <Marker
            key={generateUniqueKey(station, index)}
            position={[station.latitude, station.longitude]}
            icon={createOptimizedIcon(station.rating)}
            eventHandlers={{
              click: () => setSelectedStation(station)
            }}
          >
            <Popup className="custom-popup" maxWidth={350}>
              <div className="bg-white rounded-2xl p-4 max-w-sm">
                {/* Header */}
                <div className="flex items-start justify-between mb-3">
                  <div className="flex-1">
                    <h3 className="font-bold text-gray-800 text-lg leading-tight">
                      {station.name}
                    </h3>
                    <div className="flex items-center mt-1 space-x-1">
                      {renderStarRating(station.rating)}
                      <span className="text-sm text-gray-600 ml-1">
                        ({station.user_ratings_total})
                      </span>
                    </div>
                  </div>
                  <div className="bg-gradient-to-r from-orange-500 to-red-500 text-white px-3 py-1 rounded-full text-sm font-semibold">
                    {station.rating.toFixed(1)}
                  </div>
                </div>

                {/* Address */}
                <div className="flex items-start space-x-2 mb-3">
                  <MapPin className="w-4 h-4 text-gray-500 mt-0.5 flex-shrink-0" />
                  <p className="text-sm text-gray-600 leading-relaxed">
                    {station.address}
                  </p>
                </div>

                {/* Contact Info */}
                <div className="space-y-2 mb-4">
                  {station.phone_number && (
                    <div className="flex items-center space-x-2">
                      <Phone className="w-4 h-4 text-gray-500" />
                      <span className="text-sm text-gray-600">{station.phone_number}</span>
                    </div>
                  )}
                  {station.website && (
                    <div className="flex items-center space-x-2">
                      <Globe className="w-4 h-4 text-gray-500" />
                      <a 
                        href={station.website} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="text-sm text-blue-600 hover:text-blue-800 truncate"
                      >
                        Visit Website
                      </a>
                    </div>
                  )}
                </div>

                {/* Reviews Summary */}
                <div className="bg-gray-50 rounded-xl p-3">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-semibold text-gray-700">
                      Reviews ({station.reviews.length})
                    </span>
                    {station.business_status === 'OPERATIONAL' && (
                      <span className="bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs font-medium">
                        Open
                      </span>
                    )}
                  </div>
                  
                  {station.reviews.length > 0 && (
                    <div className="space-y-2">
                      {station.reviews.slice(0, 2).map((review, index) => (
                        <div key={index} className="text-xs text-gray-600 bg-white rounded-lg p-2">
                          <div className="flex items-center space-x-1 mb-1">
                            {renderStarRating(review.rating).slice(0, review.rating)}
                            <span className="font-medium text-gray-700">
                              {review.author_name}
                            </span>
                          </div>
                          <p className="line-clamp-2">
                            {review.text.length > 100 
                              ? review.text.substring(0, 100) + '...' 
                              : review.text
                            }
                          </p>
                        </div>
                      ))}
                    </div>
                  )}
                </div>

                {/* Action Button */}
                <button
                  onClick={() => setSelectedStation(station)}
                  className="w-full mt-4 bg-gradient-to-r from-blue-500 to-purple-600 text-white py-2 px-4 rounded-xl font-medium text-sm hover:from-blue-600 hover:to-purple-700 transition-all duration-200 flex items-center justify-center space-x-2"
                >
                  <Navigation className="w-4 h-4" />
                  <span>View Details</span>
                </button>
              </div>
            </Popup>
          </Marker>
        ))}
      </MarkerClusterGroup>
    </MapContainer>
    </div>
  )
}

export default MapComponent
