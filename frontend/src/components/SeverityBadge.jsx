import React from 'react';
import { AlertTriangle, CheckCircle2, AlertOctagon } from 'lucide-react';
import { useLanguage } from '../contexts/LanguageContext';

export function SeverityBadge({ severity }) {
  const { t } = useLanguage();
  const sev = (severity || 'Medium').toLowerCase();

  if (sev === 'low' || sev === 'safe') {
    return (
      <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800 border border-emerald-300">
        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
        {t('severity_low')}
      </span>
    );
  }

  if (sev === 'high' || sev === 'severe' || sev === 'danger') {
    return (
      <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-rose-100 text-rose-800 border border-rose-300 animate-pulse">
        <AlertOctagon className="w-3.5 h-3.5 text-rose-600" />
        {t('severity_high')}
      </span>
    );
  }

  return (
    <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-amber-100 text-amber-900 border border-amber-300">
      <AlertTriangle className="w-3.5 h-3.5 text-amber-700" />
      {t('severity_medium')}
    </span>
  );
}
