import React from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import { Languages } from 'lucide-react';

export function LanguageSwitcher() {
  const { language, setLanguage } = useLanguage();

  return (
    <div className="inline-flex items-center rounded-lg bg-stone-100 p-0.5 border border-stone-300">
      <button
        type="button"
        onClick={() => setLanguage('en')}
        className={`px-2.5 py-1 text-xs font-semibold rounded-md transition ${
          language === 'en'
            ? 'bg-emerald-700 text-white shadow-sm'
            : 'text-stone-600 hover:text-stone-900'
        }`}
      >
        English
      </button>
      <button
        type="button"
        onClick={() => setLanguage('hi')}
        className={`px-2.5 py-1 text-xs font-semibold rounded-md transition ${
          language === 'hi'
            ? 'bg-emerald-700 text-white shadow-sm'
            : 'text-stone-600 hover:text-stone-900'
        }`}
      >
        हिंदी
      </button>
    </div>
  );
}
