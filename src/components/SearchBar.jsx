import { Search, X } from 'lucide-react'

const SearchBar = ({ searchTerm, setSearchTerm }) => {
  return (
    <div className="relative">
      <div className="relative flex items-center">
        <Search className="absolute left-3 w-5 h-5 text-gray-400" />
        <input
          type="text"
          placeholder="Search stations by name or location..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="pl-10 pr-10 py-3 w-80 bg-white/20 backdrop-blur-xl border border-white/30 rounded-2xl text-gray-800 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50 transition-all duration-200"
        />
        {searchTerm && (
          <button
            onClick={() => setSearchTerm('')}
            className="absolute right-3 p-1 hover:bg-gray-200/50 rounded-full transition-colors duration-200"
          >
            <X className="w-4 h-4 text-gray-400" />
          </button>
        )}
      </div>
      
      {searchTerm && (
        <div className="absolute top-full left-0 right-0 mt-2 bg-white/90 backdrop-blur-xl border border-white/30 rounded-2xl shadow-xl z-10">
          <div className="p-3">
            <p className="text-sm text-gray-600">
              Searching for: <span className="font-semibold text-gray-800">"{searchTerm}"</span>
            </p>
          </div>
        </div>
      )}
    </div>
  )
}

export default SearchBar
