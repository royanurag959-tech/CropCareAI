import React, { useState } from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import { useAuth } from '../contexts/AuthContext';
import { UserCheck, Lock, Smartphone, Mail, UserPlus, Sparkles, AlertCircle, Loader2 } from 'lucide-react';

export function AuthPage({ onAuthSuccess }) {
  const { t } = useLanguage();
  const { login, register, loading } = useAuth();
  const [isRegister, setIsRegister] = useState(false);
  const [identifier, setIdentifier] = useState('farmer@cropcare.ai');
  const [password, setPassword] = useState('password123');
  const [name, setName] = useState('');
  const [phone, setPhone] = useState('');
  const [role, setRole] = useState('farmer');
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    try {
      if (isRegister) {
        await register(name, phone, identifier.includes('@') ? identifier : undefined, password, role);
      } else {
        await login(identifier, password);
      }
      if (onAuthSuccess) onAuthSuccess();
    } catch (err) {
      setError(err.message || 'Authentication failed');
    }
  };

  const handleQuickDemoLogin = (userEmail, userPass) => {
    setIsRegister(false);
    setIdentifier(userEmail);
    setPassword(userPass);
    setError(null);
  };

  return (
    <div className="max-w-md mx-auto px-4 py-8 space-y-6">
      <div className="text-center space-y-1">
        <h1 className="text-2xl font-black text-stone-900">
          {isRegister ? 'Create CropCare Account' : 'Welcome to CropCare AI'}
        </h1>
        <p className="text-xs text-stone-500">
          {isRegister ? 'Join our community of protected farms.' : 'Sign in to access saved scans & farm records.'}
        </p>
      </div>

      {error && (
        <div className="p-3 bg-rose-50 border border-rose-200 text-rose-800 text-xs rounded-xl flex items-center gap-2">
          <AlertCircle className="w-4 h-4 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Auth Card */}
      <form onSubmit={handleSubmit} className="bg-white rounded-3xl border border-stone-200 p-6 shadow-sm space-y-4">
        {isRegister && (
          <>
            <div>
              <label className="block text-xs font-bold text-stone-700 mb-1">Full Name *</label>
              <input
                type="text"
                required
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Ramesh Kumar"
                className="w-full p-2.5 rounded-xl border border-stone-300 text-xs focus:ring-2 focus:ring-emerald-500 focus:outline-none"
              />
            </div>

            <div>
              <label className="block text-xs font-bold text-stone-700 mb-1">Mobile Phone *</label>
              <input
                type="tel"
                required
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                placeholder="9876543210"
                className="w-full p-2.5 rounded-xl border border-stone-300 text-xs focus:ring-2 focus:ring-emerald-500 focus:outline-none"
              />
            </div>

            <div>
              <label className="block text-xs font-bold text-stone-700 mb-1">Account Role *</label>
              <select
                value={role}
                onChange={(e) => setRole(e.target.value)}
                className="w-full p-2.5 rounded-xl border border-stone-300 text-xs bg-white focus:ring-2 focus:ring-emerald-500 focus:outline-none"
              >
                <option value="farmer">Farmer (Smallholder / Grower)</option>
                <option value="worker">Krishi Mitra / Extension Worker</option>
                <option value="expert">Certified Agronomist / Expert</option>
                <option value="b2b_org">FPO / Cooperative / Agribusiness</option>
                <option value="admin">Platform Administrator</option>
              </select>
            </div>
          </>
        )}

        <div>
          <label className="block text-xs font-bold text-stone-700 mb-1">
            {isRegister ? 'Email Address' : 'Mobile Number or Email'} *
          </label>
          <input
            type="text"
            required
            value={identifier}
            onChange={(e) => setIdentifier(e.target.value)}
            placeholder="farmer@cropcare.ai or 9876543210"
            className="w-full p-2.5 rounded-xl border border-stone-300 text-xs focus:ring-2 focus:ring-emerald-500 focus:outline-none"
          />
        </div>

        <div>
          <label className="block text-xs font-bold text-stone-700 mb-1">Password *</label>
          <input
            type="password"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="••••••••"
            className="w-full p-2.5 rounded-xl border border-stone-300 text-xs focus:ring-2 focus:ring-emerald-500 focus:outline-none"
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full py-3 bg-emerald-700 hover:bg-emerald-800 disabled:bg-stone-300 text-white rounded-xl font-bold text-xs shadow transition flex items-center justify-center gap-2"
        >
          {loading ? (
            <Loader2 className="w-4 h-4 animate-spin" />
          ) : isRegister ? (
            <>
              <UserPlus className="w-4 h-4" />
              <span>Create Account</span>
            </>
          ) : (
            <>
              <UserCheck className="w-4 h-4" />
              <span>Sign In</span>
            </>
          )}
        </button>

        <div className="pt-2 text-center text-xs text-stone-500">
          {isRegister ? 'Already registered?' : "Don't have an account?"}{' '}
          <button
            type="button"
            onClick={() => setIsRegister(!isRegister)}
            className="font-bold text-emerald-700 hover:underline"
          >
            {isRegister ? 'Sign In Here' : 'Register as Farmer'}
          </button>
        </div>
      </form>

      {/* Quick 1-Click Demo Accounts */}
      <div className="p-4 rounded-2xl bg-stone-100 border border-stone-200 space-y-2.5">
        <div className="flex items-center gap-1.5 text-xs font-bold text-stone-800">
          <Sparkles className="w-3.5 h-3.5 text-amber-600" />
          <span>1-Click Hackathon Demo Logins:</span>
        </div>
        <div className="grid grid-cols-2 gap-1.5 text-[11px]">
          <button
            type="button"
            onClick={() => handleQuickDemoLogin('farmer@cropcare.ai', 'password123')}
            className="p-2 rounded-lg bg-white border border-stone-200 hover:border-emerald-500 text-left font-semibold text-stone-800"
          >
            🌾 Farmer
          </button>
          <button
            type="button"
            onClick={() => handleQuickDemoLogin('mitra@cropcare.ai', 'password123')}
            className="p-2 rounded-lg bg-white border border-stone-200 hover:border-emerald-500 text-left font-semibold text-stone-800"
          >
            🤝 Krishi Mitra
          </button>
          <button
            type="button"
            onClick={() => handleQuickDemoLogin('expert@cropcare.ai', 'password123')}
            className="p-2 rounded-lg bg-white border border-stone-200 hover:border-emerald-500 text-left font-semibold text-stone-800"
          >
            🔬 Agronomist
          </button>
          <button
            type="button"
            onClick={() => handleQuickDemoLogin('admin@cropcare.ai', 'admin123')}
            className="p-2 rounded-lg bg-white border border-stone-200 hover:border-emerald-500 text-left font-semibold text-stone-800"
          >
            🛡️ Admin
          </button>
        </div>
      </div>
    </div>
  );
}
