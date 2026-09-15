import React, { useState } from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import { translateToSelectedLang } from '../services/i18n';
import { SeverityBadge } from '../components/SeverityBadge';
import { ExplainabilityCard } from '../components/ExplainabilityCard';
import { offlineStorage } from '../services/offlineStorage';
import {
  CheckCircle2,
  AlertTriangle,
  Bookmark,
  Printer,
  Headphones,
  RotateCcw,
  ShieldCheck,
  Calendar,
  Sparkles,
  Info
} from 'lucide-react';

export function DetectionResult({ result, onResetScan, onRequestExpert, onNavigateDashboard }) {
  const { t, language } = useLanguage();
  const [isSaved, setIsSaved] = useState(false);

  if (!result) return null;

  const {
    crop,
    predicted_disease,
    hindi_name,
    scientific_name,
    confidence_percentage,
    severity,
    is_uncertain,
    uncertainty_message,
    why_did_it_happen,
    symptoms = [],
    immediate_actions = [],
    general_management = [],
    prevention = [],
    when_to_contact_expert,
    image_url,
    disclaimer
  } = result;

  const cropHindiMap = {
    Tomato: 'टमाटर',
    Potato: 'आलू',
    Rice: 'धान',
    Apple: 'सेब',
    Corn: 'मक्का',
    Wheat: 'गेहूं',
    Cotton: 'कपास'
  };

  const displayCrop = language === 'hi' ? (cropHindiMap[crop] || crop) : crop;
  const displayTitle = language === 'hi' ? (hindi_name || predicted_disease) : predicted_disease;

  const localizedSymptoms = (language === 'hi' && result.symptoms_hi && result.symptoms_hi.length > 0)
    ? result.symptoms_hi
    : symptoms;
  const localizedImmediateActions = (language === 'hi' && result.immediate_actions_hi && result.immediate_actions_hi.length > 0)
    ? result.immediate_actions_hi
    : immediate_actions;
  const localizedGeneralManagement = (language === 'hi' && result.general_management_hi && result.general_management_hi.length > 0)
    ? result.general_management_hi
    : general_management;
  const localizedPrevention = (language === 'hi' && result.prevention_hi && result.prevention_hi.length > 0)
    ? result.prevention_hi
    : prevention;

  const handleSaveLocally = async () => {
    await offlineStorage.saveReportLocally({
      ...result,
      saved_at: new Date().toISOString()
    });
    setIsSaved(true);
    setTimeout(() => setIsSaved(false), 3000);
  };

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-6 space-y-6">
      {/* Action Bar */}
      <div className="flex flex-wrap items-center justify-between gap-3 pb-2 border-b border-stone-200">
        <button
          onClick={onResetScan}
          className="inline-flex items-center gap-1.5 text-xs font-bold text-stone-600 hover:text-emerald-700 transition"
        >
          <RotateCcw className="w-4 h-4" />
          <span>{t('scan_another_crop')}</span>
        </button>

        <div className="flex items-center gap-2">
          <button
            onClick={handleSaveLocally}
            className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold transition border ${
              isSaved
                ? 'bg-emerald-100 text-emerald-800 border-emerald-300'
                : 'bg-white text-stone-700 hover:bg-stone-50 border-stone-300'
            }`}
          >
            <Bookmark className="w-3.5 h-3.5" />
            <span>{isSaved ? t('saved_to_dashboard') : t('save_report_btn')}</span>
          </button>

          <button
            onClick={handlePrint}
            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold bg-white text-stone-700 hover:bg-stone-50 border border-stone-300 transition"
          >
            <Printer className="w-3.5 h-3.5" />
            <span>{t('print_report_btn')}</span>
          </button>
        </div>
      </div>

      {/* Uncertainty Warning Banner */}
      {is_uncertain && (
        <div className="p-4 rounded-2xl bg-amber-50 border-2 border-amber-300 text-amber-900 space-y-2">
          <div className="flex items-center gap-2 font-black text-sm">
            <AlertTriangle className="w-5 h-5 text-amber-600 shrink-0" />
            <span>{t('uncertain_warning_title')}</span>
          </div>
          <p className="text-xs leading-relaxed">
            {uncertainty_message || t('uncertain_warning_msg')}
          </p>
          <div className="pt-1">
            <button
              onClick={() => onRequestExpert(result)}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-amber-700 text-white rounded-xl text-xs font-bold hover:bg-amber-800 transition shadow-sm"
            >
              <Headphones className="w-3.5 h-3.5" />
              <span>{t('talk_expert_cta')}</span>
            </button>
          </div>
        </div>
      )}

      {/* Main Diagnostic Header Card */}
      <div className="bg-white rounded-3xl border border-stone-200 p-6 shadow-sm space-y-5">
        <div className="flex flex-col sm:flex-row gap-6 items-start sm:items-center justify-between">
          <div className="space-y-1.5">
            <div className="inline-flex items-center gap-2 text-xs font-bold text-emerald-700 uppercase tracking-wider">
              <span>{displayCrop} {t('crop_analysis_title')}</span>
              <span>•</span>
              <SeverityBadge severity={severity} />
            </div>

            <h1 className="text-2xl sm:text-3xl font-black text-stone-900 tracking-tight">
              {displayTitle}
            </h1>

            {scientific_name && (
              <div className="text-xs text-stone-500 italic">
                {t('pathogen_label')}: {scientific_name}
              </div>
            )}
          </div>

          {/* Confidence Meter Card */}
          <div className="w-full sm:w-56 p-4 rounded-2xl bg-stone-50 border border-stone-200 text-center space-y-2 shrink-0">
            <div className="flex justify-between items-center text-xs font-bold text-stone-600">
              <span>{t('confidence_label')}</span>
              <span className="text-emerald-700 text-sm font-black">{confidence_percentage}%</span>
            </div>
            {/* Progress bar */}
            <div className="w-full h-3 rounded-full bg-stone-200 overflow-hidden">
              <div
                className={`h-full rounded-full transition-all duration-1000 ${
                  confidence_percentage >= 80 ? 'bg-emerald-600' : 'bg-amber-500'
                }`}
                style={{ width: `${confidence_percentage}%` }}
              ></div>
            </div>
            <div className="text-[10px] text-stone-500">
              {confidence_percentage >= 85 ? t('high_pattern_confidence') : t('moderate_visual_match')}
            </div>
          </div>
        </div>

        {image_url && (
          <div className="rounded-2xl overflow-hidden border border-stone-200 max-h-56">
            <img
              src={image_url}
              alt="Analyzed leaf"
              className="w-full h-56 object-cover object-center"
            />
          </div>
        )}
      </div>

      {/* EXPLAINABLE AI COMPONENT ("Why did this happen?") */}
      <ExplainabilityCard explainability={why_did_it_happen} />

      {/* Observed Symptoms */}
      <div className="bg-white rounded-2xl border border-stone-200 p-5 shadow-sm space-y-3">
        <h3 className="text-sm font-black text-stone-900 uppercase tracking-wide flex items-center gap-2">
          <span className="w-2.5 h-2.5 rounded-full bg-amber-500"></span>
          <span>{t('section_symptoms')}</span>
        </h3>
        <ul className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs text-stone-700">
          {localizedSymptoms.map((s, idx) => (
            <li key={idx} className="flex items-start gap-2 p-2.5 rounded-xl bg-stone-50 border border-stone-100">
              <span className="text-amber-600 font-bold">•</span>
              <span>{s}</span>
            </li>
          ))}
        </ul>
      </div>

      {/* Two Column Grid: Immediate Actions & General Management */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Immediate Actions (What to do now) */}
        <div className="bg-white rounded-2xl border border-emerald-200 p-5 shadow-sm space-y-3">
          <div className="flex items-center gap-2">
            <div className="w-7 h-7 rounded-lg bg-emerald-100 text-emerald-800 flex items-center justify-center font-bold text-xs">
              ⚡
            </div>
            <h3 className="text-xs font-black text-emerald-900 uppercase tracking-wide">
              {t('section_immediate')}
            </h3>
          </div>
          <ul className="space-y-2 text-xs text-stone-700">
            {localizedImmediateActions.map((act, idx) => (
              <li key={idx} className="flex items-start gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                <span>{act}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* General Crop Management */}
        <div className="bg-white rounded-2xl border border-stone-200 p-5 shadow-sm space-y-3">
          <div className="flex items-center gap-2">
            <div className="w-7 h-7 rounded-lg bg-stone-100 text-stone-700 flex items-center justify-center font-bold text-xs">
              📋
            </div>
            <h3 className="text-xs font-black text-stone-900 uppercase tracking-wide">
              {t('section_management')}
            </h3>
          </div>
          <ul className="space-y-2 text-xs text-stone-700">
            {localizedGeneralManagement.map((gm, idx) => (
              <li key={idx} className="flex items-start gap-2">
                <span className="text-emerald-700 font-bold">•</span>
                <span>{gm}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Prevention Guide (Next Season) */}
      <div className="bg-white rounded-2xl border border-stone-200 p-5 shadow-sm space-y-3">
        <h3 className="text-sm font-black text-stone-900 uppercase tracking-wide flex items-center gap-2">
          <ShieldCheck className="w-4 h-4 text-emerald-600" />
          <span>{t('section_prevention')}</span>
        </h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5 text-xs text-stone-700">
          {localizedPrevention.map((prev, idx) => (
            <div key={idx} className="p-3 rounded-xl bg-stone-50 border border-stone-100 space-y-1">
              <div className="font-bold text-emerald-900">
                {t('prevention_method_label')} {idx + 1}:
              </div>
              <p>{prev}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Talk to Expert Banner CTA */}
      <div className="p-6 rounded-3xl bg-gradient-to-r from-emerald-800 to-emerald-950 text-white flex flex-col sm:flex-row items-center justify-between gap-4 shadow-lg">
        <div className="space-y-1 text-center sm:text-left">
          <div className="flex items-center justify-center sm:justify-start gap-2 text-amber-300 text-xs font-bold uppercase">
            <Headphones className="w-4 h-4" />
            <span>{t('agronomist_support')}</span>
          </div>
          <h4 className="text-lg font-black">{t('talk_expert_cta')}</h4>
          <p className="text-xs text-emerald-200/90 max-w-md">
            {t('expert_persist_msg')}
          </p>
        </div>
        <button
          onClick={() => onRequestExpert(result)}
          className="px-6 py-3.5 bg-amber-400 hover:bg-amber-300 text-stone-950 font-black text-xs rounded-xl shadow-md transition hover:scale-105 active:scale-95 shrink-0"
        >
          {t('request_expert_btn')}
        </button>
      </div>

      {/* Legal & Safety Disclaimer */}
      <div className="p-4 rounded-2xl bg-stone-100 border border-stone-200 text-[11px] text-stone-600 leading-relaxed">
        <span className="font-bold text-stone-800 block mb-0.5">
          ⚠️ {t('disclaimer_title')}
        </span>
        {disclaimer || t('safety_disclaimer')}
      </div>
    </div>
  );
}
