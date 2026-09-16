import React from 'react';
import { Sprout, Phone, ShieldCheck, HeartHandshake, CloudLightning } from 'lucide-react';
import { useLanguage } from '../contexts/LanguageContext';

export function Footer({ setCurrentPage }) {
  const { t } = useLanguage();

  return (
    <footer className="bg-stone-900 text-stone-300 pt-12 pb-8 border-t border-stone-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          {/* Brand Col */}
          <div className="space-y-3">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-emerald-600 flex items-center justify-center text-white">
                <Sprout className="w-5 h-5" />
              </div>
              <span className="font-black text-lg text-white tracking-tight">{t('brand')}</span>
            </div>
            <p className="text-xs text-stone-400 leading-relaxed">
              {t('footer_tagline')}
            </p>
            <div className="flex items-center gap-2 text-xs text-emerald-400 font-semibold">
              <CloudLightning className="w-4 h-4" />
              <span>{t('footer_status')}</span>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-white mb-3">{t('core_modules')}</h4>
            <ul className="space-y-2 text-xs text-stone-400">
              <li>
                <button onClick={() => setCurrentPage('detect')} className="hover:text-emerald-400 transition">
                  {t('nav_detect')}
                </button>
              </li>
              <li>
                <button onClick={() => setCurrentPage('library')} className="hover:text-emerald-400 transition">
                  {t('nav_library')}
                </button>
              </li>
              <li>
                <button onClick={() => setCurrentPage('assisted')} className="hover:text-emerald-400 transition">
                  {t('nav_assisted')}
                </button>
              </li>
              <li>
                <button onClick={() => setCurrentPage('telecom')} className="hover:text-emerald-400 transition">
                  {t('nav_telecom')}
                </button>
              </li>
            </ul>
          </div>

          {/* Monetization & Enterprise */}
          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-white mb-3">{t('platform_b2b')}</h4>
            <ul className="space-y-2 text-xs text-stone-400">
              <li>
                <button onClick={() => setCurrentPage('pricing')} className="hover:text-emerald-400 transition">
                  {t('nav_pricing')}
                </button>
              </li>
              <li>
                <button onClick={() => setCurrentPage('b2b')} className="hover:text-emerald-400 transition">
                  {t('nav_b2b')}
                </button>
              </li>
              <li>
                <button onClick={() => setCurrentPage('expert')} className="hover:text-emerald-400 transition">
                  {t('nav_expert')}
                </button>
              </li>
              <li>
                <button onClick={() => setCurrentPage('admin')} className="hover:text-emerald-400 transition">
                  {t('nav_admin')}
                </button>
              </li>
            </ul>
          </div>

          {/* Emergency & Extension helpline */}
          <div className="bg-stone-800/80 p-4 rounded-xl border border-stone-700 space-y-2">
            <div className="flex items-center gap-2 text-amber-400 font-bold text-xs">
              <Phone className="w-4 h-4" />
              <span>{t('national_call_centre')}</span>
            </div>
            <div className="text-lg font-black text-white">1800-180-1551</div>
            <p className="text-[11px] text-stone-400">
              {t('call_centre_desc')}
            </p>
          </div>
        </div>

        {/* Disclaimer Bar */}
        <div className="pt-6 border-t border-stone-800 text-[11px] text-stone-400 text-center leading-relaxed">
          <p className="max-w-4xl mx-auto mb-2">
            {t('safety_disclaimer')}
          </p>
          <p className="text-stone-400">
            {t('footer_copyright')}
          </p>
        </div>
      </div>
    </footer>
  );
}
