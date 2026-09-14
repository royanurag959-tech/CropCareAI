import React, { useState, useEffect } from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import { api } from '../services/api';
import {
  BarChart3,
  TrendingUp,
  TrendingDown,
  ShieldCheck,
  Building2,
  FileDown,
  MapPin,
  AlertTriangle,
  Layers
} from 'lucide-react';

export function B2BAnalytics() {
  const { t } = useLanguage();
  const [analyticsData, setAnalyticsData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAnalytics();
  }, []);

  const loadAnalytics = async () => {
    setLoading(true);
    try {
      const data = await api.getRegionalAnalytics();
      setAnalyticsData(data);
    } catch (e) {
      console.warn('Could not load regional analytics:', e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto px-4 py-6 space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="space-y-1">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-purple-100 text-purple-900 border border-purple-300">
            <Building2 className="w-3.5 h-3.5" />
            <span>FPO & Enterprise Disease Surveillance</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-black text-stone-900 tracking-tight">
            Regional Crop Health & Epidemiology Analytics
          </h1>
          <p className="text-xs sm:text-sm text-stone-600">
            Aggregated crop health surveillance for Farmer Producer Organizations, agricultural cooperatives, and input suppliers.
          </p>
        </div>

        <button
          onClick={() => alert('Exporting aggregated regional disease epidemiology report (CSV)...')}
          className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-white border border-stone-300 text-xs font-bold text-stone-800 hover:bg-stone-50 shadow-sm transition"
        >
          <FileDown className="w-4 h-4 text-emerald-700" />
          <span>Export Analytics Report</span>
        </button>
      </div>

      {/* Privacy Protection Banner */}
      <div className="p-4 rounded-2xl bg-emerald-50 border border-emerald-200 text-xs text-emerald-950 flex items-start gap-2.5">
        <ShieldCheck className="w-5 h-5 text-emerald-700 shrink-0 mt-0.5" />
        <div className="leading-relaxed">
          <span className="font-bold block">Privacy-First Data Governance:</span>
          Under our B2B charter, all surveillance insights are 100% anonymized and aggregated at district clusters. Individual farmer mobile numbers, GPS pins, and private field coordinates are strictly isolated and never commercialized.
        </div>
      </div>

      {/* District Surveillance Cards */}
      <div className="space-y-3">
        <h3 className="text-xs font-black text-stone-800 uppercase tracking-wide flex items-center gap-1.5">
          <MapPin className="w-4 h-4 text-emerald-600" />
          <span>Active District Crop-Disease Clusters</span>
        </h3>

        {loading ? (
          <div className="text-center py-12 text-stone-500 text-xs">
            Aggregating district disease reports...
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {analyticsData?.districts?.map((d, idx) => (
              <div
                key={idx}
                className="bg-white rounded-2xl border border-stone-200 p-5 shadow-sm space-y-3 hover:shadow-md transition"
              >
                <div className="flex items-center justify-between">
                  <div>
                    <h4 className="text-sm font-black text-stone-900">{d.district}</h4>
                    <span className="text-[10px] text-stone-500">{d.state}</span>
                  </div>
                  <span
                    className={`text-[9px] font-black px-2 py-0.5 rounded-full uppercase ${
                      d.alert_level === 'High Alert'
                        ? 'bg-rose-100 text-rose-800 border border-rose-200'
                        : d.alert_level === 'Elevated'
                        ? 'bg-amber-100 text-amber-800 border border-amber-200'
                        : 'bg-emerald-100 text-emerald-800 border border-emerald-200'
                    }`}
                  >
                    {d.alert_level}
                  </span>
                </div>

                <div className="p-3 bg-stone-50 rounded-xl space-y-1 text-xs">
                  <div className="flex justify-between">
                    <span className="text-stone-500">Most Reported Crop:</span>
                    <span className="font-bold text-stone-900">{d.most_reported_crop}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-stone-500">Primary Disease:</span>
                    <span className="font-bold text-emerald-800">{d.primary_disease}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-stone-500">Reports (30 Days):</span>
                    <span className="font-bold text-stone-900">{d.cases_reported_30d} scans</span>
                  </div>
                </div>

                <div className="flex items-center justify-between text-xs pt-1">
                  <span className="text-stone-500">Weekly Trajectory:</span>
                  <span
                    className={`font-black flex items-center gap-1 ${
                      d.trend_direction === 'increasing' ? 'text-rose-600' : 'text-emerald-600'
                    }`}
                  >
                    {d.trend_direction === 'increasing' ? (
                      <TrendingUp className="w-3.5 h-3.5" />
                    ) : (
                      <TrendingDown className="w-3.5 h-3.5" />
                    )}
                    <span>{d.trend}</span>
                  </span>
                </div>

                <div className="text-[11px] text-stone-600 pt-2 border-t border-stone-100 leading-snug">
                  <span className="font-bold text-stone-700">Contributing Weather: </span>
                  {d.contributing_weather}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
