import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import { useEffect } from 'react';
import { AuthProvider } from './contexts/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import LandingPage from './pages/LandingPage';
import LoginPage from './pages/LoginPage';
import Dashboard from './pages/Dashboard';
import DebugPage from './pages/DebugPage';
import OpenAICaseStudy from './pages/OpenAICaseStudy';

function ScrollToTop() {
  const { pathname } = useLocation();
  useEffect(() => {
    window.scrollTo(0, 0);
  }, [pathname]);
  return null;
}

// Standalone routes rendered without the main app wrapper (dark overlay / grid bg)
const STANDALONE_ROUTES = ['/openaisix'];

function AppContent() {
  const { pathname } = useLocation();
  const isStandalone = STANDALONE_ROUTES.includes(pathname);

  return (
    <>
      <ScrollToTop />
      {isStandalone ? (
        <Routes>
          <Route path="/openaisix" element={<OpenAICaseStudy />} />
        </Routes>
      ) : (
        <div className="min-h-screen bg-[url('/grid-pattern.svg')] bg-fixed bg-cover selection:bg-primary/30">
          <div className="fixed inset-0 bg-background/90 pointer-events-none z-[-1]" />
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/debug" element={<DebugPage />} />
            <Route path="/app" element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            } />
          </Routes>
        </div>
      )}
    </>
  );
}

function App() {
  return (
    <AuthProvider>
      <Router>
        <AppContent />
      </Router>
    </AuthProvider>
  );
}

export default App;
