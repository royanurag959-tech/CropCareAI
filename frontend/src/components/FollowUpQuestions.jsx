import React, { useState } from 'react';
import { ChevronDown, ChevronUp, Sliders, Calendar, CloudRain, Droplet, Clock, MapPin } from 'lucide-react';
import { useLanguage } from '../contexts/LanguageContext';

export function FollowUpQuestions({ contextData, setContextData }) {
  const { t } = useLanguage();
  const [isOpen, setIsOpen] = useState(false);

  const handleChange = (field, value) => {
    setContextData(prev => ({ ...prev, [field]: value }));
  };

  return (
    <div className="rounded-2xl border border-stone-200 bg-white overflow-hidden shadow-sm transition">
      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex items-center justify-between p-4 text-left hover:bg-stone-50 transition"
      >
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg bg-emerald-50 text-emerald-700 flex items-center justify-center font-bold">
            <Sliders className="w-4 h-4" />
          </div>
          <div>
            <span className="text-xs font-bold text-stone-900 block">
              {t('optional_context_title')}
            </span>
            <span className="text-[11px] text-stone-500">
              {t('field_context_sub')}
            </span>
          </div>
        </div>
        <div className="text-stone-400">
          {isOpen ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
        </div>
      </button>

      {isOpen && (
        <div className="p-4 pt-1 border-t border-stone-100 bg-stone-50/50 space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
            {/* Growth Stage */}
            <div>
              <label className="block text-[11px] font-bold text-stone-700 mb-1 flex items-center gap-1">
                <Calendar className="w-3 h-3 text-emerald-600" />
                <span>{t('growth_stage_label')}</span>
              </label>
              <select
                value={contextData.growth_stage}
                onChange={(e) => handleChange('growth_stage', e.target.value)}
                className="w-full rounded-lg border border-stone-300 p-2 text-xs bg-white focus:ring-2 focus:ring-emerald-500 focus:outline-none"
              >
                <option value="Vegetative">{t('growth_vegetative')}</option>
                <option value="Seedling">{t('growth_seedling')}</option>
                <option value="Flowering">{t('growth_flowering')}</option>
                <option value="Fruiting">{t('growth_fruiting')}</option>
                <option value="Near Harvest">{t('growth_harvest')}</option>
              </select>
            </div>

            {/* Rainfall */}
            <div>
              <label className="block text-[11px] font-bold text-stone-700 mb-1 flex items-center gap-1">
                <CloudRain className="w-3 h-3 text-sky-600" />
                <span>{t('rainfall_label')}</span>
              </label>
              <select
                value={contextData.rainfall}
                onChange={(e) => handleChange('rainfall', e.target.value)}
                className="w-full rounded-lg border border-stone-300 p-2 text-xs bg-white focus:ring-2 focus:ring-emerald-500 focus:outline-none"
              >
                <option value="Moderate">{t('rain_moderate')}</option>
                <option value="None">{t('rain_none')}</option>
                <option value="Light">{t('rain_light')}</option>
                <option value="Heavy">{t('rain_heavy')}</option>
              </select>
            </div>

            {/* Irrigation */}
            <div>
              <label className="block text-[11px] font-bold text-stone-700 mb-1 flex items-center gap-1">
                <Droplet className="w-3 h-3 text-teal-600" />
                <span>{t('irrigation_label')}</span>
              </label>
              <select
                value={contextData.irrigation}
                onChange={(e) => handleChange('irrigation', e.target.value)}
                className="w-full rounded-lg border border-stone-300 p-2 text-xs bg-white focus:ring-2 focus:ring-emerald-500 focus:outline-none"
              >
                <option value="Every 2-3 days">{t('irr_23days')}</option>
                <option value="Daily">{t('irr_daily')}</option>
                <option value="Weekly">{t('irr_weekly')}</option>
                <option value="Overhead / Flood">{t('irr_flood')}</option>
              </select>
            </div>

            {/* Duration */}
            <div>
              <label className="block text-[11px] font-bold text-stone-700 mb-1 flex items-center gap-1">
                <Clock className="w-3 h-3 text-amber-600" />
                <span>{t('duration_label')}</span>
              </label>
              <select
                value={contextData.duration}
                onChange={(e) => handleChange('duration', e.target.value)}
                className="w-full rounded-lg border border-stone-300 p-2 text-xs bg-white focus:ring-2 focus:ring-emerald-500 focus:outline-none"
              >
                <option value="4-7 days">{t('dur_medium')}</option>
                <option value="<3 days">{t('dur_fresh')}</option>
                <option value="1-2 weeks">{t('dur_persistent')}</option>
                <option value=">2 weeks">{t('dur_chronic')}</option>
              </select>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
