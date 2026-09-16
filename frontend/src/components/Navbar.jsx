import React, { useState } from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import { useAuth } from '../contexts/AuthContext';
import { NetworkStatus } from './NetworkStatus';
import { LanguageSwitcher } from './LanguageSwitcher';
import {
  Sprout,
  ScanLine,
  BookOpen,
  History,
  Users,
  PhoneCall,
  BarChart3,
  CreditCard,
  UserCheck,
  Menu,
  X,
  LogOut,
  ShieldAlert
} from 'lucide-react';

export function Navbar({ currentPage, setCurrentPage }) {
  const { t } = useLanguage();
  const { user, logout } = useAuth();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const navItems = [
    { id: 'home', label: t('nav_home'), icon: Sprout },
    { id: 'detect', label: t('nav_detect'), icon: ScanLine, highlight: true },
    { id: 'library', label: t('nav_library'), icon: BookOpen },
    { id: 'dashboard', label: t('nav_dashboard'), icon: History },
    { id: 'assisted', label: t('nav_assisted'), icon: Users },
    { id: 'telecom', label: t('nav_telecom'), icon: PhoneCall },
    { id: 'pricing', label: t('nav_pricing'), icon: CreditCard },
    { id: 'b2b', label: t('nav_b2b'), icon: BarChart3 },
    { id: 'admin', label: t('nav_admin'), icon: ShieldAlert, adminOnly: true }
  ];

  const handleNavClick = (id) => {
    setCurrentPage(id);
    setMobileMenuOpen(false);
  };

  return (
    <header className="sticky top-0 z-50 bg-white/95 backdrop-blur-md border-b border-stone-200 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Brand Logo */}
          <div
            onClick={() => handleNavClick('home')}
            className="flex items-center gap-2.5 cursor-pointer select-none group"
          >
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-600 to-emerald-800 flex items-center justify-center text-white shadow-md shadow-emerald-700/20 group-hover:scale-105 transition">
              <Sprout className="w-6 h-6 text-emerald-100" />
            </div>
            <div>
              <span className="font-extrabold text-xl tracking-tight text-stone-900 flex items-center gap-1">
                {t('brand')}
              </span>
              <span className="hidden sm:block text-[10px] text-stone-500 font-medium tracking-wide uppercase">
                {t('navbar_detect_tagline')}
              </span>
            </div>
          </div>

          {/* Desktop Navigation Links */}
          <nav className="hidden xl:flex items-center gap-1">
            {navItems.map((item) => {
              if (item.adminOnly && (!user || user.role !== 'admin')) return null;
              const Icon = item.icon;
              const active = currentPage === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => handleNavClick(item.id)}
                  className={`flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold rounded-lg transition ${
                    active
                      ? 'bg-emerald-50 text-emerald-800 border border-emerald-200 font-bold'
                      : item.highlight
                      ? 'bg-emerald-600 text-white hover:bg-emerald-700 shadow-sm'
                      : 'text-stone-600 hover:text-stone-900 hover:bg-stone-100'
                  }`}
                >
                  <Icon className="w-3.5 h-3.5" />
                  <span>{item.label}</span>
                </button>
              );
            })}
          </nav>

          {/* Controls: Online Status, i18n, Auth */}
          <div className="hidden sm:flex items-center gap-3">
            <NetworkStatus />
            <LanguageSwitcher />

            {user ? (
              <div className="flex items-center gap-2 pl-2 border-l border-stone-200">
                <div
                  onClick={() => handleNavClick('dashboard')}
                  className="cursor-pointer text-right"
                  title={t('view_profile_dash')}
                >
                  <div className="text-xs font-bold text-stone-800 leading-tight truncate max-w-[120px]">
                    {user.name}
                  </div>
                  <div className="text-[10px] uppercase tracking-wider font-semibold text-emerald-700">
                    {user.subscription_plan} {t('plan_label')}
                  </div>
                </div>
                <button
                  onClick={logout}
                  className="p-1.5 text-stone-400 hover:text-stone-700 rounded-lg hover:bg-stone-100 transition"
                  title={t('nav_logout')}
                >
                  <LogOut className="w-4 h-4" />
                </button>
              </div>
            ) : (
              <button
                onClick={() => handleNavClick('auth')}
                className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-bold text-emerald-700 hover:bg-emerald-50 border border-emerald-300 transition"
              >
                <UserCheck className="w-3.5 h-3.5" />
                <span>{t('nav_login')}</span>
              </button>
            )}
          </div>

          {/* Mobile Menu Button */}
          <div className="flex xl:hidden items-center gap-2">
            <NetworkStatus />
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 rounded-lg text-stone-600 hover:bg-stone-100 focus:outline-none"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Drawer */}
      {mobileMenuOpen && (
        <div className="xl:hidden bg-white border-b border-stone-200 px-4 pt-2 pb-6 space-y-2">
          <div className="flex items-center justify-between pb-3 border-b border-stone-100">
            <LanguageSwitcher />
            {user ? (
              <div className="flex items-center gap-2 text-xs font-bold text-stone-800">
                <span>{user.name} ({user.subscription_plan})</span>
                <button onClick={logout} className="text-red-600 hover:underline">
                  {t('nav_logout')}
                </button>
              </div>
            ) : (
              <button
                onClick={() => handleNavClick('auth')}
                className="text-xs font-bold text-emerald-700 underline"
              >
                {t('nav_login')}
              </button>
            )}
          </div>

          <div className="grid grid-cols-2 gap-1.5 pt-2">
            {navItems.map((item) => {
              if (item.adminOnly && (!user || user.role !== 'admin')) return null;
              const Icon = item.icon;
              const active = currentPage === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => handleNavClick(item.id)}
                  className={`flex items-center gap-2 px-3 py-2.5 rounded-xl text-xs font-bold transition text-left ${
                    active
                      ? 'bg-emerald-700 text-white'
                      : item.highlight
                      ? 'bg-emerald-100 text-emerald-900 border border-emerald-300'
                      : 'bg-stone-50 text-stone-700 hover:bg-stone-100'
                  }`}
                >
                  <Icon className="w-4 h-4 shrink-0" />
                  <span className="truncate">{item.label}</span>
                </button>
              );
            })}
          </div>
        </div>
      )}
    </header>
  );
}
