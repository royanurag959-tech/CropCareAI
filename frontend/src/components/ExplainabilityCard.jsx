import React from 'react';
import { HelpCircle, Droplets, Wind, Thermometer, ShieldAlert, CheckCircle, Info } from 'lucide-react';
import { useLanguage } from '../contexts/LanguageContext';

export function ExplainabilityCard({ explainability }) {
  const { t, language } = useLanguage();

  if (!explainability) return null;

  const {
    primary_summary,
    primary_summary_hi,
    contributing_factors = [],
    context_insights = []
  } = explainability;

  const getFactorIcon = (category = '') => {
    const cat = category.toLowerCase();
    if (cat.includes('moisture') || cat.includes('rain') || cat.includes('irrigation') || cat.includes('नमी') || cat.includes('बारिश')) {
      return <Droplets className="w-4 h-4 text-sky-500" />;
    }
    if (cat.includes('canopy') || cat.includes('air') || cat.includes('wind') || cat.includes('हवा')) {
      return <Wind className="w-4 h-4 text-teal-500" />;
    }
    if (cat.includes('weather') || cat.includes('temp') || cat.includes('मौसम') || cat.includes('तापमान')) {
      return <Thermometer className="w-4 h-4 text-amber-500" />;
    }
    return <Info className="w-4 h-4 text-emerald-500" />;
  };

  const getImpactBadge = (level = 'Medium') => {
    const lvl = level.toLowerCase();
    if (lvl.includes('high') || lvl.includes('गंभीर')) {
      return {
        label: language === 'hi' ? t('impact_high') : 'High Impact',
        className: 'bg-rose-100 text-rose-800 border border-rose-200'
      };
    }
    if (lvl.includes('low') || lvl.includes('कम') || lvl.includes('सामान्य')) {
      return {
        label: language === 'hi' ? t('impact_low') : 'Low Impact',
        className: 'bg-emerald-100 text-emerald-800 border border-emerald-200'
      };
    }
    return {
      label: language === 'hi' ? t('impact_medium') : 'Medium Impact',
      className: 'bg-amber-100 text-amber-800 border border-amber-200'
    };
  };

  const translateInsight = (insight) => {
    if (language !== 'hi' || !insight) return insight;
    return insight
      .replace('Growth phase:', 'फसल अवस्था:')
      .replace('Recent rainfall:', 'हालिया बारिश:')
      .replace('Irrigation schedule:', 'सिंचाई चक्र:')
      .replace('Symptom duration:', 'लक्षण अवधि:')
      .replace('Vegetative', 'वानस्पतिक वृद्धि')
      .replace('Seedling', 'अंकुरण')
      .replace('Flowering', 'फूल आने की अवस्था')
      .replace('Fruiting', 'फल लगने की अवस्था')
      .replace('Near Harvest', 'कटाई के नजदीक')
      .replace('Moderate', 'मध्यम')
      .replace('None', 'कोई बारिश नहीं')
      .replace('Light', 'हल्की बारिश')
      .replace('Heavy', 'भारी बारिश')
      .replace('Every 2-3 days', 'हर 2-3 दिन')
      .replace('Daily', 'रोजाना')
      .replace('Weekly', 'साप्ताहिक')
      .replace('Overhead / Flood', 'ऊपर से फव्वारा')
      .replace('4-7 days', '4-7 दिन')
      .replace('<3 days', '3 दिन से कम')
      .replace('1-2 weeks', '1-2 सप्ताह')
      .replace('>2 weeks', '2 सप्ताह से अधिक');
  };

  const displaySummary = language === 'hi' && primary_summary_hi ? primary_summary_hi : primary_summary;

  return (
    <div className="bg-white rounded-2xl border border-stone-200 p-5 shadow-sm space-y-4">
      <div className="flex items-center gap-2 border-b border-stone-100 pb-3">
        <div className="w-8 h-8 rounded-lg bg-emerald-100 text-emerald-800 flex items-center justify-center font-bold">
          <HelpCircle className="w-5 h-5" />
        </div>
        <div>
          <h3 className="text-sm font-black text-stone-900 uppercase tracking-wide">
            {t('section_why')}
          </h3>
          <p className="text-[11px] text-stone-500">
            {t('causal_explanation_sub')}
          </p>
        </div>
      </div>

      {/* Primary Narrative Summary */}
      <div className="p-3.5 rounded-xl bg-emerald-50/70 border border-emerald-200 text-xs text-stone-800 leading-relaxed font-medium">
        <span className="font-bold text-emerald-900 block mb-1">
          🌿 {t('diagnostic_assessment_title')}
        </span>
        {displaySummary}
      </div>

      {/* Contributing Factors Cards */}
      <div className="space-y-2.5">
        <div className="text-xs font-bold text-stone-700">
          {t('contributing_causal_title')}
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-2.5">
          {contributing_factors.map((f, idx) => {
            const factorTitle = language === 'hi' && f.factor_hi ? f.factor_hi : f.factor;
            const factorDesc = language === 'hi' && f.scientific_rationale_hi ? f.scientific_rationale_hi : f.scientific_rationale;
            const badge = getImpactBadge(f.impact_level);

            return (
              <div
                key={idx}
                className="p-3 rounded-xl border border-stone-100 bg-stone-50/70 hover:bg-white hover:border-stone-200 transition space-y-1.5"
              >
                <div className="flex items-center justify-between gap-2">
                  <div className="flex items-center gap-1.5">
                    {getFactorIcon(f.category)}
                    <span className="text-[11px] font-bold text-stone-900">{factorTitle}</span>
                  </div>
                  <span
                    className={`text-[9px] font-extrabold px-2 py-0.5 rounded-full uppercase tracking-wider shrink-0 ${badge.className}`}
                  >
                    {badge.label}
                  </span>
                </div>
                <p className="text-[11px] text-stone-600 leading-normal">
                  {factorDesc}
                </p>
              </div>
            );
          })}
        </div>
      </div>

      {/* Field Context Insights if available */}
      {context_insights.length > 0 && (
        <div className="pt-2 border-t border-stone-100">
          <div className="text-[11px] font-bold text-stone-700 mb-1.5 flex items-center gap-1">
            <CheckCircle className="w-3.5 h-3.5 text-emerald-600" />
            <span>{t('field_observations_factored')}</span>
          </div>
          <ul className="space-y-1">
            {context_insights.map((insight, idx) => (
              <li key={idx} className="text-[11px] text-stone-600 flex items-start gap-1.5">
                <span className="text-emerald-500 font-bold">•</span>
                <span>{translateInsight(insight)}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
