import { useState } from 'react';
import { Link, Navigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { LogIn, Shield, ArrowLeft, GitBranch } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

const LoginPage = () => {
  const { user, signInWithGoogle } = useAuth();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // If already logged in, redirect to app
  if (user) {
    return <Navigate to="/app" replace />;
  }

  const handleGoogleSignIn = async () => {
    try {
      setLoading(true);
      setError(null);
      await signInWithGoogle();
    } catch (err: any) {
      setError(err.message || 'Failed to sign in');
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-background p-4 relative">
      {/* Back link */}
      <Link
        to="/"
        className="absolute top-6 left-6 flex items-center gap-1.5 text-sm text-slate-400 hover:text-slate-200 transition-colors"
      >
        <ArrowLeft size={15} />
        tikun.pro
      </Link>
      {/* Background effects */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary/10 rounded-full blur-[120px]" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-secondary/10 rounded-full blur-[120px]" />
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="relative glass-panel p-8 sm:p-12 rounded-2xl max-w-md w-full"
      >
        {/* Logo */}
        <div className="flex justify-center mb-8">
          <div className="w-16 h-16 rounded-full bg-gradient-to-tr from-secondary to-primary flex items-center justify-center font-bold text-white text-3xl">
            ת
          </div>
        </div>

        {/* Title */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">
            Welcome to Tikun<span className="text-primary">Olam</span>
          </h1>
          <p className="text-slate-400 text-sm">
            Multi-civilizational ethical reasoning powered by AI
          </p>
        </div>

        {/* Error message */}
        {error && (
          <div className="mb-6 p-4 bg-red-500/10 border border-red-500/20 rounded-lg text-red-200 text-sm">
            {error}
          </div>
        )}

        {/* Google Sign In Button */}
        <button
          onClick={handleGoogleSignIn}
          disabled={loading}
          className="w-full flex items-center justify-center gap-3 px-6 py-4 bg-white hover:bg-gray-100 disabled:bg-gray-300 text-gray-800 font-semibold rounded-lg transition-all shadow-lg hover:shadow-xl disabled:cursor-not-allowed"
        >
          {loading ? (
            <div className="w-5 h-5 border-2 border-gray-400 border-t-gray-800 rounded-full animate-spin" />
          ) : (
            <>
              <svg className="w-5 h-5" viewBox="0 0 24 24">
                <path
                  fill="#4285F4"
                  d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                />
                <path
                  fill="#34A853"
                  d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                />
                <path
                  fill="#FBBC05"
                  d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                />
                <path
                  fill="#EA4335"
                  d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                />
              </svg>
              Sign in with Google
            </>
          )}
        </button>

        {/* Divider */}
        <div className="my-8 flex items-center gap-4">
          <div className="flex-1 border-t border-white/10" />
          <span className="text-slate-500 text-sm">or</span>
          <div className="flex-1 border-t border-white/10" />
        </div>

        {/* Features */}
        <div className="space-y-3 text-sm text-slate-400">
          <div className="flex items-start gap-3">
            <Shield className="w-4 h-4 text-primary mt-0.5 flex-shrink-0" />
            <p>Secure authentication — no stored credentials</p>
          </div>
          <div className="flex items-start gap-3">
            <GitBranch className="w-4 h-4 text-accent mt-0.5 flex-shrink-0" />
            <p>6 AI providers analyze your dilemma independently</p>
          </div>
          <div className="flex items-start gap-3">
            <LogIn className="w-4 h-4 text-secondary mt-0.5 flex-shrink-0" />
            <p>Full audit trail — every step attributed to its AI model</p>
          </div>
        </div>

        {/* Footer */}
        <div className="mt-8 pt-6 border-t border-white/10 text-center text-xs text-slate-500">
          By signing in, you agree to our Terms of Service and Privacy Policy
        </div>
      </motion.div>
    </div>
  );
};

export default LoginPage;
