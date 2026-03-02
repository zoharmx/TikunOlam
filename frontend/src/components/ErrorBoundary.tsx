import React, { Component, ReactNode } from 'react';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
  errorInfo: React.ErrorInfo | null;
}

class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null
    };
  }

  static getDerivedStateFromError(_error: Error): Partial<State> {
    return { hasError: true };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('❌ CRITICAL ERROR IN COMPONENT:', error);
    console.error('Component stack:', errorInfo.componentStack);
    this.setState({
      error,
      errorInfo
    });
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="p-8 bg-red-900/20 border border-red-500 rounded-xl">
          <h2 className="text-2xl font-bold text-red-400 mb-4">
            ❌ Component Error
          </h2>
          <div className="space-y-4">
            <div>
              <h3 className="font-bold text-red-300">Error:</h3>
              <pre className="text-sm bg-black/50 p-4 rounded overflow-auto">
                {this.state.error?.toString()}
              </pre>
            </div>
            <div>
              <h3 className="font-bold text-red-300">Stack:</h3>
              <pre className="text-xs bg-black/50 p-4 rounded overflow-auto max-h-96">
                {this.state.errorInfo?.componentStack}
              </pre>
            </div>
            <button
              onClick={() => window.location.reload()}
              className="px-4 py-2 bg-red-600 hover:bg-red-700 rounded text-white"
            >
              Reload Page
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
