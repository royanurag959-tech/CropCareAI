import React, { useState, useEffect } from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import { useAuth } from '../contexts/AuthContext';
import { api } from '../services/api';
import { SeverityBadge } from '../components/SeverityBadge';
import { History, Bookmark, Zap, Calendar, MapPin, ChevronRight, Eye, RefreshCw, X } from 'lucide-react';

export function FarmerDashboard({ onSelectScan, onOpenUpgradeModal }) {
  const { t, language } = useLanguage();
  const { user } = useAuth();
  const [scans, setScans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('scans'); // 'scans' or 'saved'
  const [selectedScanDetail, setSelectedScanDetail] = useState(null);

  useEffect(() => {
    loadScans();
  }, []);

  const loadScans = async () => {
    setLoading(true);
    try {
      const data = await api.getScans();
      setScans(data || []);
    } catch (e) {
      console.warn('Could not load scans:', e);
    } finally {
      setLoading(false);
    }
  };

  const planLimit = user?.subscription_plan === 'pro' ? 500 : (user?.subscription_plan === 'plus' ? 50 : 5);
  const scanCount = user?.scan_count_month || scans.length;
  const remainingScans = Math.max(0, planLimit - scanCount);

  return (
    <div className="max-w-5xl mx-auto px-4 py-6 space-y-6">
      {/* User Header & Quota Card */}
      <div className="bg-white rounded-3xl border border-stone-200 p-6 shadow-sm flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div className="space-y-1.5">
          <div className="flex items-center gap-2">
            <span className="text-xs font-bold px-2.5 py-0.5 rounded-full bg-emerald-100 text-emerald-800 uppercase tracking-wide">
              {user?.role ? (language === 'hi' ? (user.role === 'admin' ? 'व्यवस्थापक' : 'किसान खाता') : `${user.role} Account`) : t('farmer_account')}
            </span>
            <span className="text-xs font-bold px-2.5 py-0.5 rounded-full bg-stone-100 text-stone-700 uppercase">
              {user?.subscription_plan || 'free'} {t('tier_label')}
            </span>
          </div>
          <h1 className="text-2xl font-black text-stone-900 tracking-tight">
            {user?.name || (language === 'hi' ? 'रमेश कुमार (किसान)' : 'Ramesh Kumar (Demo Farmer)')}
          </h1>
          <div className="text-xs text-stone-500 flex items-center gap-3">
            <span>📞 {user?.phone || '9876543210'}</span>
            <span>•</span>
            <span>📍 {language === 'hi' ? 'पुणे जिला, महाराष्ट्र' : 'Pune District, Maharashtra'}</span>
          </div>
        </div>

        {/* Scan Usage Card */}
        <div className="w-full md:w-64 p-4 rounded-2xl bg-stone-50 border border-stone-200 space-y-2">
          <div className="flex justify-between items-center text-xs font-bold">
            <span className="text-stone-600">{t('monthly_scans')}</span>
            <span className="text-emerald-700">{scanCount} / {planLimit} {t('scans_used')}</span>
          </div>
          <div className="w-full h-2.5 rounded-full bg-stone-200 overflow-hidden">
            <div
              className="h-full bg-emerald-600 rounded-full"
              style={{ width: `${Math.min(100, (scanCount / planLimit) * 100)}%` }}
            ></div>
          </div>
          <div className="flex items-center justify-between pt-1">
            <span className="text-[11px] text-stone-500">{remainingScans} {t('scans_left')}</span>
            <button
              onClick={() => onOpenUpgradeModal(user?.subscription_plan === 'plus' ? 'pro' : 'plus')}
              className="inline-flex items-center gap-1 text-[11px] font-black text-emerald-700 hover:underline"
            >
              <Zap className="w-3 h-3 text-amber-500 fill-amber-500" />
              <span>{t('upgrade_btn')}</span>
            </button>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex items-center justify-between border-b border-stone-200 pb-2">
        <div className="flex items-center gap-2">
          <button
            onClick={() => setActiveTab('scans')}
            className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-bold transition ${
              activeTab === 'scans'
                ? 'bg-emerald-700 text-white shadow-sm'
                : 'bg-white text-stone-600 hover:bg-stone-100'
            }`}
          >
            <History className="w-3.5 h-3.5" />
            <span>{t('scan_history')} ({scans.length})</span>
          </button>
        </div>

        <button
          onClick={loadScans}
          className="p-2 rounded-xl text-stone-500 hover:text-stone-900 hover:bg-stone-100 transition"
          title={language === 'hi' ? 'स्कैन सूची रीफ्रेश करें' : 'Refresh Scans'}
        >
          <RefreshCw className="w-4 h-4" />
        </button>
      </div>

      {/* Scans List */}
      {loading ? (
        <div className="text-center py-12 text-stone-500 text-xs">
          {language === 'hi' ? 'स्कैन रिकॉर्ड लोड हो रहे हैं...' : 'Loading scan records...'}
        </div>
      ) : scans.length === 0 ? (
        <div className="text-center py-12 bg-white rounded-3xl border border-stone-200 text-stone-500 text-xs">
          {language === 'hi'
            ? 'अभी तक कोई स्कैन रिकॉर्ड नहीं मिला। पहली पत्ती की जांच के लिए फसल जांचें पर जाएं!'
            : 'No crop scans recorded yet. Go to Scan Crop to analyze your first leaf!'}
        </div>
      ) : (
        <div className="space-y-3">
          {scans.map((scan) => {
            const cropKey = `crop_${scan.crop?.toLowerCase()}`;
            const displayCrop = t(cropKey) !== cropKey ? t(cropKey) : scan.crop;
            const displayDisease = language === 'hi' && scan.hindi_name ? scan.hindi_name : scan.predicted_disease;

            return (
              <div
                key={scan.id}
                className="bg-white rounded-2xl border border-stone-200 p-4 shadow-sm hover:shadow-md transition flex flex-col sm:flex-row sm:items-center justify-between gap-4"
              >
                <div className="flex items-center gap-4">
                  <img
                    src={scan.image_url || '/sample_leaves/sample_tomato_blight.jpg'}
                    alt={displayCrop}
                    className="w-16 h-16 rounded-xl object-cover border border-stone-200 bg-stone-100 shrink-0"
                  />
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-bold text-emerald-800 bg-emerald-50 px-2 py-0.5 rounded-md">
                        {displayCrop}
                      </span>
                      <SeverityBadge severity={scan.severity} />
                    </div>
                    <h3 className="text-sm font-extrabold text-stone-900 leading-tight">
                      {displayDisease}
                    </h3>
                    <div className="text-[11px] text-stone-500 flex items-center gap-3">
                      <span className="flex items-center gap-1">
                        <Calendar className="w-3 h-3 text-stone-400" />
                        {scan.created_at ? new Date(scan.created_at).toLocaleDateString() : (language === 'hi' ? 'आज' : 'Today')}
                      </span>
                      <span>•</span>
                      <span className="font-semibold text-emerald-700">
                        {Math.round(scan.confidence * 100)}% {language === 'hi' ? 'सटीकता' : 'Confidence'}
                      </span>
                      {scan.farmer_name && (
                        <>
                          <span>•</span>
                          <span>{scan.farmer_name}</span>
                        </>
                      )}
                    </div>
                  </div>
                </div>

                <button
                  onClick={() => setSelectedScanDetail(scan)}
                  className="inline-flex items-center justify-center gap-1.5 px-4 py-2 bg-stone-50 hover:bg-emerald-50 text-stone-700 hover:text-emerald-800 border border-stone-200 hover:border-emerald-300 rounded-xl text-xs font-bold transition self-end sm:self-center"
                >
                  <Eye className="w-3.5 h-3.5" />
                  <span>{language === 'hi' ? 'पूरी सलाह देखें' : 'View Full Advisory'}</span>
                </button>
              </div>
            );
          })}
        </div>
      )}

      {/* Modal View for Scan Details */}
      {selectedScanDetail && (() => {
        const cropKey = `crop_${selectedScanDetail.crop?.toLowerCase()}`;
        const modalCrop = t(cropKey) !== cropKey ? t(cropKey) : selectedScanDetail.crop;
        const modalDisease = language === 'hi' && selectedScanDetail.hindi_name
          ? selectedScanDetail.hindi_name
          : selectedScanDetail.predicted_disease;

        return (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-in fade-in">
            <div className="bg-white rounded-3xl max-w-lg w-full max-h-[85vh] overflow-y-auto p-6 shadow-2xl border border-stone-200 space-y-4 relative">
              <button
                onClick={() => setSelectedScanDetail(null)}
                className="absolute top-4 right-4 p-1.5 rounded-full text-stone-400 hover:text-stone-700 hover:bg-stone-100"
              >
                <X className="w-5 h-5" />
              </button>

              <div className="space-y-1">
                <span className="text-xs font-bold text-emerald-800 bg-emerald-100 px-2 py-0.5 rounded-md">
                  {modalCrop}
                </span>
                <h3 className="text-lg font-black text-stone-900">{modalDisease}</h3>
                <div className="text-xs text-stone-500">
                  {language === 'hi' ? 'सटीकता' : 'Confidence'}: {Math.round(selectedScanDetail.confidence * 100)}% • {language === 'hi' ? 'गंभीरता' : 'Severity'}: {selectedScanDetail.severity}
                </div>
              </div>

              {selectedScanDetail.image_url && (
                <img
                  src={selectedScanDetail.image_url}
                  alt={modalCrop}
                  className="w-full h-48 object-cover rounded-xl border border-stone-200"
                />
              )}

              {selectedScanDetail.generated_explanation && (
                <div className="p-3 bg-emerald-50 rounded-xl border border-emerald-200 text-xs text-stone-800">
                  <span className="font-bold text-emerald-900 block mb-1">
                    {language === 'hi' ? 'यह रोग क्यों हुआ?' : 'Why Did This Happen?'}
                  </span>
                  {selectedScanDetail.generated_explanation}
                </div>
              )}

              <button
                onClick={() => setSelectedScanDetail(null)}
                className="w-full py-2.5 bg-stone-800 text-white rounded-xl text-xs font-bold hover:bg-stone-900 transition"
              >
                {language === 'hi' ? 'बंद करें' : 'Close Record'}
              </button>
            </div>
          </div>
        );
      })()}
    </div>
  );
}
