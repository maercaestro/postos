import { MapPin, Star, Users, BarChart3 } from 'lucide-react'

const StatsPanel = ({ totalStations, averageRating, totalReviews }) => {
  const stats = [
    {
      icon: MapPin,
      label: 'Total Stations',
      value: totalStations.toLocaleString(),
      color: 'from-blue-500 to-cyan-500',
      bgColor: 'bg-blue-50',
      iconColor: 'text-blue-600'
    },
    {
      icon: Star,
      label: 'Avg Rating',
      value: averageRating.toFixed(2),
      suffix: '/5.0',
      color: 'from-yellow-500 to-orange-500',
      bgColor: 'bg-yellow-50',
      iconColor: 'text-yellow-600'
    },
    {
      icon: Users,
      label: 'Total Reviews',
      value: totalReviews.toLocaleString(),
      color: 'from-green-500 to-emerald-500',
      bgColor: 'bg-green-50',
      iconColor: 'text-green-600'
    },
    {
      icon: BarChart3,
      label: 'Coverage',
      value: 'Brazil',
      subtitle: 'Nationwide',
      color: 'from-purple-500 to-indigo-500',
      bgColor: 'bg-purple-50',
      iconColor: 'text-purple-600'
    }
  ]

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {stats.map((stat, index) => (
        <div 
          key={index}
          className="bg-white/20 backdrop-blur-xl rounded-3xl border border-white/30 shadow-2xl p-6 hover:shadow-3xl transition-all duration-300 hover:scale-105"
        >
          <div className="flex items-center justify-between">
            <div className="flex-1">
              <div className={`w-12 h-12 rounded-2xl ${stat.bgColor} flex items-center justify-center mb-4`}>
                <stat.icon className={`w-6 h-6 ${stat.iconColor}`} />
              </div>
              
              <div className="space-y-1">
                <p className="text-sm font-medium text-gray-600">{stat.label}</p>
                <div className="flex items-baseline space-x-1">
                  <span className={`text-2xl font-bold bg-gradient-to-r ${stat.color} bg-clip-text text-transparent`}>
                    {stat.value}
                  </span>
                  {stat.suffix && (
                    <span className="text-sm text-gray-500">{stat.suffix}</span>
                  )}
                </div>
                {stat.subtitle && (
                  <p className="text-xs text-gray-500">{stat.subtitle}</p>
                )}
              </div>
            </div>
            
            <div className={`w-16 h-16 rounded-2xl bg-gradient-to-r ${stat.color} opacity-10`}></div>
          </div>
        </div>
      ))}
    </div>
  )
}

export default StatsPanel
