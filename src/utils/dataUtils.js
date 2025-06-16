/**
 * Data utility functions for the Raizen Analytics app
 */

/**
 * Remove duplicate stations based on place_id
 * @param {Array} stations - Array of station objects
 * @returns {Array} - Array of unique stations
 */
export const removeDuplicateStations = (stations) => {
  if (!Array.isArray(stations)) return []
  
  const uniqueStations = stations.filter((station, index, self) =>
    index === self.findIndex(s => s.place_id === station.place_id)
  )
  
  if (uniqueStations.length !== stations.length) {
    console.warn(`Removed ${stations.length - uniqueStations.length} duplicate stations`)
  }
  
  return uniqueStations
}

/**
 * Validate station data structure
 * @param {Object} station - Station object to validate
 * @returns {boolean} - Whether the station is valid
 */
export const isValidStation = (station) => {
  return (
    station &&
    typeof station === 'object' &&
    station.place_id &&
    station.name &&
    typeof station.latitude === 'number' &&
    typeof station.longitude === 'number' &&
    !isNaN(station.latitude) &&
    !isNaN(station.longitude) &&
    station.latitude >= -90 &&
    station.latitude <= 90 &&
    station.longitude >= -180 &&
    station.longitude <= 180
  )
}

/**
 * Filter and clean station data
 * @param {Array} stations - Array of station objects
 * @returns {Array} - Array of cleaned and validated stations
 */
export const cleanStationData = (stations) => {
  if (!Array.isArray(stations)) return []
  
  const validStations = stations.filter(isValidStation)
  const uniqueStations = removeDuplicateStations(validStations)
  
  console.log(`Data cleaning results:
    Original: ${stations.length}
    Valid: ${validStations.length}
    Unique: ${uniqueStations.length}
    Removed: ${stations.length - uniqueStations.length}
  `)
  
  return uniqueStations
}

/**
 * Generate a unique key for React components
 * @param {Object} station - Station object
 * @param {number} index - Index in array
 * @returns {string} - Unique key
 */
export const generateUniqueKey = (station, index) => {
  return `${station.place_id || 'unknown'}-${index}-${Date.now()}`
}

/**
 * Calculate statistics from station data
 * @param {Array} stations - Array of station objects
 * @returns {Object} - Statistics object
 */
export const calculateStats = (stations) => {
  if (!Array.isArray(stations) || stations.length === 0) {
    return {
      totalStations: 0,
      averageRating: 0,
      totalReviews: 0,
      stationsWithReviews: 0
    }
  }
  
  const stationsWithRatings = stations.filter(s => s.rating && s.rating > 0)
  const averageRating = stationsWithRatings.length > 0
    ? stationsWithRatings.reduce((sum, station) => sum + station.rating, 0) / stationsWithRatings.length
    : 0
  
  const totalReviews = stations.reduce((sum, station) => 
    sum + (Array.isArray(station.reviews) ? station.reviews.length : 0), 0
  )
  
  const stationsWithReviews = stations.filter(s => 
    Array.isArray(s.reviews) && s.reviews.length > 0
  ).length
  
  return {
    totalStations: stations.length,
    averageRating: Math.round(averageRating * 100) / 100,
    totalReviews,
    stationsWithReviews
  }
}
