import React from 'react'
import { AlertTriangle, RefreshCw } from 'lucide-react'

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false, error: null, errorInfo: null }
  }

  static getDerivedStateFromError(error) {
    return { hasError: true }
  }

  componentDidCatch(error, errorInfo) {
    this.setState({
      error: error,
      errorInfo: errorInfo
    })
    console.error('Error Boundary caught an error:', error, errorInfo)
  }

  handleReset = () => {
    this.setState({ hasError: false, error: null, errorInfo: null })
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-gradient-to-br from-red-50 via-orange-50 to-yellow-50 flex items-center justify-center p-6">
          <div className="bg-white/30 backdrop-blur-xl rounded-3xl p-8 border border-white/20 shadow-2xl text-center max-w-lg">
            <AlertTriangle className="w-16 h-16 text-red-500 mx-auto mb-6" />
            <h2 className="text-2xl font-bold text-gray-800 mb-4">Something went wrong</h2>
            <p className="text-gray-600 mb-6">
              We're sorry, but there was an error loading the Raizen Analytics dashboard.
            </p>
            
            {this.props.showDetails && this.state.error && (
              <div className="bg-red-100 rounded-xl p-4 mb-6 text-left">
                <p className="text-red-800 text-sm font-medium mb-2">Error Details:</p>
                <p className="text-red-700 text-xs font-mono break-all">
                  {this.state.error.toString()}
                </p>
              </div>
            )}
            
            <div className="space-y-4">
              <button
                onClick={this.handleReset}
                className="bg-gradient-to-r from-blue-500 to-purple-600 text-white py-3 px-6 rounded-xl font-medium hover:from-blue-600 hover:to-purple-700 transition-all duration-200 flex items-center space-x-2 mx-auto"
              >
                <RefreshCw className="w-5 h-5" />
                <span>Try Again</span>
              </button>
              
              <button
                onClick={() => window.location.reload()}
                className="bg-gray-500 text-white py-2 px-4 rounded-xl font-medium hover:bg-gray-600 transition-all duration-200 block mx-auto"
              >
                Reload Page
              </button>
            </div>
            
            <div className="mt-6 p-4 bg-blue-100 rounded-xl">
              <p className="text-blue-800 text-sm">
                <strong>Demo Note:</strong> This is a development version. 
                In production, errors would be logged and handled more gracefully.
              </p>
            </div>
          </div>
        </div>
      )
    }

    return this.props.children
  }
}

export default ErrorBoundary
