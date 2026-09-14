import React from 'react';
import { useOffline } from '../contexts/OfflineContext';
import { useLanguage } from '../contexts/LanguageContext';
import { Wifi, WifiOff, RefreshCw } from 'lucide-react';

export function NetworkStatus() {
  const { isOnline, queuedCount, isSyncing, triggerManualSync } = useOffline();
  const { t } = useLanguage();

  return (
    <div className="flex items-center gap-2">
      {isOnline ? (
        <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800 border border-emerald-300 shadow-sm">
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <Wifi className="w-3.5 h-3.5 text-emerald-600" />
          <span>🟢 {t('status_online')}</span>
        </span>
      ) : (
        <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-amber-100 text-amber-900 border border-amber-300 shadow-sm">
          <span className="w-2 h-2 rounded-full bg-amber-500"></span>
          <WifiOff className="w-3.5 h-3.5 text-amber-700" />
          <span>🔴 {t('status_offline')}</span>
        </span>
      )}

      {queuedCount > 0 && (
        <button
          onClick={triggerManualSync}
          disabled={!isOnline || isSyncing}
          className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800 border border-blue-300 hover:bg-blue-200 transition"
          title="Click to sync queued scans to cloud"
        >
          <RefreshCw className={`w-3 h-3 ${isSyncing ? 'animate-spin' : ''}`} />
          <span>{queuedCount} {queuedCount === 1 ? 'scan queued' : 'scans queued'}</span>
        </button>
      )}
    </div>
  );
}
