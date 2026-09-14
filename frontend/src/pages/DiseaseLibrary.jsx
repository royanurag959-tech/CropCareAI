import React, { useState, useEffect } from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import { translateToSelectedLang } from '../services/i18n';
import { api } from '../services/api';
import { SeverityBadge } from '../components/SeverityBadge';
import { Search, Filter, BookOpen, ChevronRight, X, Droplets, ShieldCheck, AlertCircle } from 'lucide-react';

export function DiseaseLibrary() {
  const { t, language } = useLanguage();
  const [diseases, setDiseases] = useState([]);
  const [crops, setCrops] = useState([]);
  const [selectedCrop, setSelectedCrop] = useState('');
  const [selectedSeverity, setSelectedSeverity] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);
  const [selectedDisease, setSelectedDisease] = useState(null);

  const cropHindiMap = {
    Tomato: 'टमाटर',
    Potato: 'आलू',
    Rice: 'धान',
    Apple: 'सेब',
    Corn: 'मक्का',
    Wheat: 'गेहूं',
    Cotton: 'कपास'
  };

  useEffect(() => {
    loadData();
  }, [selectedCrop, selectedSeverity]);

  const loadData = async () => {
    setLoading(true);
    try {
      const [cropsData, diseasesData] = await Promise.all([
        api.getCrops(),
        api.getDiseases({
          crop: selectedCrop || undefined,
          severity: selectedSeverity || undefined
        })
      ]);
      setCrops(cropsData || []);
      setDiseases(diseasesData || []);
    } catch (e) {
      console.warn('Failed to load library:', e);
    } finally {
      setLoading(false);
    }
  };

  const filteredDiseases = diseases.filter(d => {
    if (!searchQuery) return true;
    const q = searchQuery.toLowerCase();
    return (
      d.name.toLowerCase().includes(q) ||
      d.hindi_name.toLowerCase().includes(q) ||
      d.crop_name.toLowerCase().includes(q) ||
      (d.symptoms && d.symptoms.some(s => s.toLowerCase().includes(q)))
    );
  });

  return (
    <div className="max-w-6xl mx-auto px-4 py-6 space-y-6">
      {/* Header */}
      <div className="space-y-1">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800 border border-emerald-300">
          <BookOpen className="w-3.5 h-3.5" />
          <span>{t('pathology_ref')}</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-black text-stone-900 tracking-tight">
          {t('library_title')}
        </h1>
        <p className="text-xs sm:text-sm text-stone-600">
          {t('pathology_sub')}
        </p>
      </div>

      {/* Filter & Search Bar */}
      <div className="bg-white rounded-2xl border border-stone-200 p-4 shadow-sm space-y-3">
        <div className="relative">
          <Search className="w-4 h-4 text-stone-400 absolute left-3.5 top-3.5" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder={t('search_library_placeholder')}
            className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-stone-300 text-xs focus:ring-2 focus:ring-emerald-500 focus:outline-none"
          />
        </div>

        {/* Filter Pills */}
        <div className="flex flex-wrap items-center gap-2 pt-1">
          <span className="text-xs font-bold text-stone-500 flex items-center gap-1">
            <Filter className="w-3 h-3" />
            <span>Crop:</span>
          </span>
          <button
            onClick={() => setSelectedCrop('')}
            className={`px-3 py-1 rounded-xl text-xs font-bold transition ${
              selectedCrop === ''
                ? 'bg-emerald-700 text-white'
                : 'bg-stone-100 text-stone-600 hover:bg-stone-200'
            }`}
          >
            {t('all_crops')}
          </button>
          {crops.map((c) => {
            const cropName = language === 'hi' ? c.hindi_name : c.name;
            return (
              <button
                key={c.id}
                onClick={() => setSelectedCrop(c.name)}
                className={`px-3 py-1 rounded-xl text-xs font-bold transition ${
                  selectedCrop === c.name
                    ? 'bg-emerald-700 text-white'
                    : 'bg-stone-100 text-stone-600 hover:bg-stone-200'
                }`}
              >
                {cropName}
              </button>
            );
          })}
        </div>
      </div>

      {/* Disease Cards Grid */}
      {loading ? (
        <div className="text-center py-12 text-stone-500 text-xs">
          {t('loading_library')}
        </div>
      ) : filteredDiseases.length === 0 ? (
        <div className="text-center py-12 bg-white rounded-3xl border border-stone-200 text-stone-500 text-xs">
          {t('no_matching_diseases')}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredDiseases.map((disease) => {
            const title = language === 'hi' ? disease.hindi_name : disease.name;
            const cropName = language === 'hi' ? (cropHindiMap[disease.crop_name] || disease.crop_name) : disease.crop_name;

            return (
              <div
                key={disease.id}
                onClick={() => setSelectedDisease(disease)}
                className="bg-white rounded-2xl border border-stone-200 p-5 shadow-sm hover:shadow-md hover:border-emerald-500 transition cursor-pointer flex flex-col justify-between space-y-4 group"
              >
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold text-emerald-800 bg-emerald-50 px-2.5 py-0.5 rounded-md">
                      {cropName}
                    </span>
                    <SeverityBadge severity={disease.severity_level} />
                  </div>

                  <h3 className="text-base font-extrabold text-stone-900 group-hover:text-emerald-700 transition leading-tight">
                    {title}
                  </h3>

                  <p className="text-xs text-stone-600 line-clamp-2 leading-relaxed">
                    {disease.description}
                  </p>
                </div>

                <div className="pt-3 border-t border-stone-100 flex items-center justify-between text-xs text-emerald-700 font-bold">
                  <span>{t('view_full_profile')}</span>
                  <ChevronRight className="w-4 h-4 group-hover:translate-x-1 transition" />
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Disease Detail Modal */}
      {selectedDisease && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-in fade-in">
          <div className="bg-white rounded-3xl max-w-2xl w-full max-h-[85vh] overflow-y-auto p-6 shadow-2xl border border-stone-200 space-y-5 relative">
            <button
              onClick={() => setSelectedDisease(null)}
              className="absolute top-4 right-4 p-1.5 rounded-full text-stone-400 hover:text-stone-700 hover:bg-stone-100"
            >
              <X className="w-5 h-5" />
            </button>

            <div className="space-y-1">
              <div className="flex items-center gap-2">
                <span className="text-xs font-bold text-emerald-800 bg-emerald-100 px-2.5 py-0.5 rounded-md">
                  {language === 'hi' ? (cropHindiMap[selectedDisease.crop_name] || selectedDisease.crop_name) : selectedDisease.crop_name}
                </span>
                <SeverityBadge severity={selectedDisease.severity_level} />
              </div>
              <h2 className="text-xl font-black text-stone-900">
                {language === 'hi' ? selectedDisease.hindi_name : selectedDisease.name}
              </h2>
              {selectedDisease.scientific_name && (
                <div className="text-xs text-stone-500 italic">{t('pathogen_label')}: {selectedDisease.scientific_name}</div>
              )}
            </div>

            <p className="text-xs text-stone-700 leading-relaxed bg-stone-50 p-3 rounded-xl border border-stone-200">
              {selectedDisease.description}
            </p>

            {/* Symptoms */}
            <div className="space-y-2">
              <h4 className="text-xs font-black uppercase text-stone-900">{t('observed_symptoms')}:</h4>
              <ul className="space-y-1 text-xs text-stone-700">
                {selectedDisease.symptoms?.map((s, idx) => (
                  <li key={idx} className="flex items-start gap-1.5">
                    <span className="text-amber-500 font-bold">•</span>
                    <span>{translateToSelectedLang(s, language)}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Causes & Conditions */}
            <div className="space-y-2">
              <h4 className="text-xs font-black uppercase text-stone-900">{t('favorable_conditions_causes')}:</h4>
              <ul className="space-y-1 text-xs text-stone-700">
                {selectedDisease.possible_causes?.map((c, idx) => (
                  <li key={idx} className="flex items-start gap-1.5">
                    <Droplets className="w-3.5 h-3.5 text-sky-500 shrink-0 mt-0.5" />
                    <span>{c}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Actions & Prevention */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
              <div className="p-3 bg-emerald-50/70 border border-emerald-200 rounded-xl space-y-1.5">
                <h5 className="text-[11px] font-black uppercase text-emerald-950">{t('immediate_remedies')}:</h5>
                <ul className="space-y-1 text-[11px] text-stone-700">
                  {selectedDisease.immediate_actions?.map((act, idx) => (
                    <li key={idx}>✓ {translateToSelectedLang(act, language)}</li>
                  ))}
                </ul>
              </div>

              <div className="p-3 bg-stone-50 border border-stone-200 rounded-xl space-y-1.5">
                <h5 className="text-[11px] font-black uppercase text-stone-900">{t('prevention_title')}:</h5>
                <ul className="space-y-1 text-[11px] text-stone-700">
                  {selectedDisease.prevention?.map((prev, idx) => (
                    <li key={idx}>• {translateToSelectedLang(prev, language)}</li>
                  ))}
                </ul>
              </div>
            </div>

            <div className="pt-2">
              <button
                onClick={() => setSelectedDisease(null)}
                className="w-full py-2.5 bg-stone-800 text-white rounded-xl font-bold text-xs hover:bg-stone-900 transition"
              >
                {t('close_profile')}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
