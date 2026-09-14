// IndexedDB Wrapper for Offline Storage & Sync Queue
const DB_NAME = 'CropCareOfflineDB';
const DB_VERSION = 1;

function openDB() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open(DB_NAME, DB_VERSION);

    request.onupgradeneeded = (event) => {
      const db = event.target.result;
      if (!db.objectStoreNames.contains('cached_diseases')) {
        db.createObjectStore('cached_diseases', { keyPath: 'id' });
      }
      if (!db.objectStoreNames.contains('offline_queue')) {
        db.createObjectStore('offline_queue', { keyPath: 'client_id', autoIncrement: true });
      }
      if (!db.objectStoreNames.contains('saved_reports')) {
        db.createObjectStore('saved_reports', { keyPath: 'id' });
      }
    };

    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
  });
}

export const offlineStorage = {
  // Cache diseases
  async cacheDiseases(diseases) {
    try {
      const db = await openDB();
      const tx = db.transaction('cached_diseases', 'readwrite');
      const store = tx.objectStore('cached_diseases');
      diseases.forEach(d => store.put(d));
      return tx.complete;
    } catch (e) {
      console.warn('Could not cache diseases to IndexedDB:', e);
    }
  },

  async getCachedDiseases() {
    try {
      const db = await openDB();
      return new Promise((resolve) => {
        const tx = db.transaction('cached_diseases', 'readonly');
        const store = tx.objectStore('cached_diseases');
        const req = store.getAll();
        req.onsuccess = () => resolve(req.result || []);
        req.onerror = () => resolve([]);
      });
    } catch (e) {
      return [];
    }
  },

  // Queue offline scans
  async queueScan(scanData) {
    try {
      const db = await openDB();
      return new Promise((resolve, reject) => {
        const tx = db.transaction('offline_queue', 'readwrite');
        const store = tx.objectStore('offline_queue');
        const record = {
          ...scanData,
          client_timestamp: new Date().toISOString(),
          synced: false
        };
        const req = store.add(record);
        req.onsuccess = () => resolve(req.result);
        req.onerror = () => reject(req.error);
      });
    } catch (e) {
      // Fallback to localStorage if IndexedDB is blocked
      const queue = JSON.parse(localStorage.getItem('cropcare_offline_queue') || '[]');
      queue.push(scanData);
      localStorage.setItem('cropcare_offline_queue', JSON.stringify(queue));
      return queue.length;
    }
  },

  async getQueuedScans() {
    try {
      const db = await openDB();
      return new Promise((resolve) => {
        const tx = db.transaction('offline_queue', 'readonly');
        const store = tx.objectStore('offline_queue');
        const req = store.getAll();
        req.onsuccess = () => resolve(req.result || []);
        req.onerror = () => resolve([]);
      });
    } catch (e) {
      return JSON.parse(localStorage.getItem('cropcare_offline_queue') || '[]');
    }
  },

  async clearQueuedScans() {
    try {
      const db = await openDB();
      const tx = db.transaction('offline_queue', 'readwrite');
      tx.objectStore('offline_queue').clear();
      localStorage.removeItem('cropcare_offline_queue');
      return true;
    } catch (e) {
      localStorage.removeItem('cropcare_offline_queue');
      return true;
    }
  },

  // Save reports
  async saveReportLocally(report) {
    try {
      const db = await openDB();
      const tx = db.transaction('saved_reports', 'readwrite');
      tx.objectStore('saved_reports').put(report);
      return true;
    } catch (e) {
      const reports = JSON.parse(localStorage.getItem('cropcare_saved_reports') || '[]');
      reports.unshift(report);
      localStorage.setItem('cropcare_saved_reports', JSON.stringify(reports));
      return true;
    }
  },

  async getSavedReports() {
    try {
      const db = await openDB();
      return new Promise((resolve) => {
        const tx = db.transaction('saved_reports', 'readonly');
        const req = tx.objectStore('saved_reports').getAll();
        req.onsuccess = () => resolve(req.result || []);
        req.onerror = () => resolve([]);
      });
    } catch (e) {
      return JSON.parse(localStorage.getItem('cropcare_saved_reports') || '[]');
    }
  }
};
