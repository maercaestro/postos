import { Star, MapPin, Phone, Globe, Users, Calendar, MessageCircle } from 'lucide-react'

const StationCard = ({ station }) => {
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

  const getRatingColor = (rating) => {
    if (rating >= 4.5) return 'text-green-600 bg-green-100'
    if (rating >= 3.5) return 'text-yellow-600 bg-yellow-100'
    return 'text-red-600 bg-red-100'
  }

  const formatDate = (timestamp) => {
    return new Date(timestamp * 1000).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    })
  }

  return (
    <div className="bg-white/20 backdrop-blur-xl rounded-3xl border border-white/30 shadow-2xl overflow-hidden">
      {/* Header */}
      <div className="bg-gradient-to-r from-orange-500 to-red-500 p-6 text-white">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <h2 className="text-2xl font-bold mb-2">{station.name}</h2>
            <div className="flex items-center space-x-1 mb-3">
              {renderStarRating(station.rating)}
              <span className="ml-2 text-orange-100">
                {station.rating.toFixed(1)} • {station.user_ratings_total} reviews
              </span>
            </div>
          </div>
          <div className={`px-4 py-2 rounded-full text-sm font-semibold ${getRatingColor(station.rating)} text-opacity-90`}>
            {station.rating.toFixed(1)}
          </div>
        </div>
        
        <div className="flex items-start space-x-2">
          <MapPin className="w-5 h-5 text-orange-200 mt-0.5 flex-shrink-0" />
          <p className="text-orange-100 leading-relaxed">{station.address}</p>
        </div>
      </div>

      {/* Content */}
      <div className="p-6 space-y-6">
        {/* Contact Information */}
        <div className="space-y-3">
          <h3 className="text-lg font-semibold text-gray-800 flex items-center">
            <Phone className="w-5 h-5 mr-2 text-blue-600" />
            Contact & Info
          </h3>
          
          <div className="grid grid-cols-1 gap-3">
            {station.phone_number && (
              <div className="flex items-center space-x-3 p-3 bg-white/30 rounded-xl">
                <Phone className="w-4 h-4 text-gray-600" />
                <span className="text-gray-700">{station.phone_number}</span>
              </div>
            )}
            
            {station.website && (
              <div className="flex items-center space-x-3 p-3 bg-white/30 rounded-xl">
                <Globe className="w-4 h-4 text-gray-600" />
                <a 
                  href={station.website} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:text-blue-800 truncate"
                >
                  Visit Website
                </a>
              </div>
            )}
            
            <div className="flex items-center space-x-3 p-3 bg-white/30 rounded-xl">
              <Users className="w-4 h-4 text-gray-600" />
              <span className="text-gray-700">
                {station.business_status === 'OPERATIONAL' ? 'Currently Open' : 'Status Unknown'}
              </span>
              {station.business_status === 'OPERATIONAL' && (
                <span className="bg-green-500 w-2 h-2 rounded-full"></span>
              )}
            </div>
            
            {station.price_level && (
              <div className="flex items-center space-x-3 p-3 bg-white/30 rounded-xl">
                <span className="text-gray-600">💰</span>
                <span className="text-gray-700">
                  Price Level: {'$'.repeat(station.price_level)} 
                  <span className="text-gray-500 text-sm ml-1">
                    ({station.price_level === 1 ? 'Budget' : station.price_level === 2 ? 'Moderate' : station.price_level === 3 ? 'Expensive' : 'Premium'})
                  </span>
                </span>
              </div>
            )}
          </div>
        </div>

        {/* Reviews Section */}
        <div>
          <h3 className="text-lg font-semibold text-gray-800 flex items-center mb-4">
            <MessageCircle className="w-5 h-5 mr-2 text-purple-600" />
            Recent Reviews ({station.reviews.length})
          </h3>
          
          {station.reviews.length > 0 ? (
            <div className="space-y-4 max-h-80 overflow-y-auto">
              {station.reviews.slice(0, 5).map((review, index) => (
                <div key={index} className="bg-white/30 rounded-xl p-4 border border-white/20">
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex-1">
                      <div className="flex items-center space-x-2 mb-1">
                        <span className="font-semibold text-gray-800">{review.author_name}</span>
                        <div className="flex items-center space-x-1">
                          {renderStarRating(review.rating)}
                        </div>
                      </div>
                      <div className="flex items-center space-x-2 text-sm text-gray-600">
                        <Calendar className="w-3 h-3" />
                        <span>{review.relative_time_description}</span>
                        {review.time && (
                          <span className="text-gray-500">• {formatDate(review.time)}</span>
                        )}
                      </div>
                    </div>
                    <div className={`px-2 py-1 rounded-full text-xs font-semibold ${getRatingColor(review.rating)}`}>
                      {review.rating}
                    </div>
                  </div>
                  
                  {review.text && (
                    <p className="text-gray-700 text-sm leading-relaxed mt-2">
                      {review.text}
                    </p>
                  )}
                  
                  {review.language && review.language !== 'en' && (
                    <span className="inline-block mt-2 px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">
                      {review.language.toUpperCase()}
                    </span>
                  )}
                </div>
              ))}
              
              {station.reviews.length > 5 && (
                <div className="text-center py-4">
                  <span className="text-gray-600 text-sm">
                    +{station.reviews.length - 5} more reviews available
                  </span>
                </div>
              )}
            </div>
          ) : (
            <div className="text-center py-8 text-gray-600">
              <MessageCircle className="w-12 h-12 text-gray-300 mx-auto mb-2" />
              <p>No reviews available for this station</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default StationCard
