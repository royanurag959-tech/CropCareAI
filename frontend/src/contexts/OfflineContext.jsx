import React, { createContext, useContext, useState, useEffect } from 'react';
import { api } from '../services/api';
import { offlineStorage } from '../services/offlineStorage';

const OfflineContext = createContext();

export function OfflineProvider({ children }) {
  const [isOnline, setIsOnline] = useState(navigator.onLine);
  const [queuedCount, setQueuedCount] = useState(0);
  const [isSyncing, setIsSyncing] = useState(false);

  const refreshQueueCount = async () => {
    const queue = await offlineStorage.getQueuedScans();
    setQueuedCount(queue.length);
  };

  const triggerManualSync = async () => {
    if (!navigator.onLine || isSyncing) return;
    setIsSyncing(true);
    try {
      const res = await api.syncOfflineQueue();
      if (res.success) {
        await refreshQueueCount();
      }
    } finally {
      setIsSyncing(false);
    }
  };

  useEffect(() => {
    const handleOnline = () => {
      setIsOnline(true);
      triggerManualSync();
    };
    const handleOffline = () => {
      setIsOnline(false);
    };

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);
    refreshQueueCount();
    if (navigator.onLine) {
      triggerManualSync();
    }

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  return (
    <OfflineContext.Provider value={{ isOnline, queuedCount, isSyncing, refreshQueueCount, triggerManualSync }}>
      {children}
    </OfflineContext.Provider>
  );
}

export function useOffline() {
  return useContext(OfflineContext);
}
