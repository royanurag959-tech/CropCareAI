import React, { useState, useEffect } from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import { useAuth } from '../contexts/AuthContext';
import { api } from '../services/api';
import { Check, Zap, Sparkles, ShieldCheck, ArrowRight, Star } from 'lucide-react';

export function PricingPlans({ onOpenUpgradeModal }) {
  const { t } = useLanguage();
  const { user } = useAuth();
  const [plans, setPlans] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadPlans();
  }, []);

  const loadPlans = async () => {
    try {
      const data = await api.getPricing();
      setPlans(data || []);
    } catch (e) {
      console.warn('Failed to load pricing:', e);
    } finally {
      setLoading(false);
    }
  };

  const currentPlan = user?.subscription_plan || 'free';

  return (
    <div className="max-w-6xl mx-auto px-4 py-8 space-y-12">
      {/* Header */}
      <div className="text-center max-w-2xl mx-auto space-y-3">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800 border border-emerald-300">
          <Sparkles className="w-3.5 h-3.5 text-amber-600" />
          <span>{t('transparent_pricing')}</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-black text-stone-900 tracking-tight">
          {t('pricing_title')}
        </h1>
        <p className="text-xs sm:text-sm text-stone-600">
          {t('pricing_sub')}
        </p>
      </div>

      {/* Pricing Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 items-stretch">
        {/* FREE TIER */}
        <div className="bg-white rounded-3xl border border-stone-200 p-6 flex flex-col justify-between space-y-6 shadow-sm">
          <div className="space-y-4">
            <div className="space-y-1">
              <span className="text-xs font-bold uppercase tracking-wider text-stone-500">{t('essential_access')}</span>
              <h3 className="text-xl font-black text-stone-900">{t('plan_free')}</h3>
              <p className="text-xs text-stone-500">{t('free_plan_desc')}</p>
            </div>

            <div className="py-2">
              <span className="text-4xl font-black text-stone-900">₹0</span>
              <span className="text-xs text-stone-500">{t('per_month')}</span>
            </div>

            <ul className="space-y-2.5 text-xs text-stone-700">
              <li className="flex items-start gap-2">
                <Check className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                <span><strong>5 {t('monthly_scans')}</strong> {t('per_month')}</span>
              </li>
              <li className="flex items-start gap-2">
                <Check className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                <span>{t('free_plan_feat2')}</span>
              </li>
              <li className="flex items-start gap-2">
                <Check className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                <span>{t('free_plan_feat3')}</span>
              </li>
              <li className="flex items-start gap-2">
                <Check className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                <span>{t('free_plan_feat4')}</span>
              </li>
              <li className="flex items-start gap-2">
                <Check className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                <span>{t('free_plan_feat5')}</span>
              </li>
            </ul>
          </div>

          <button
            disabled={currentPlan === 'free'}
            className="w-full py-3 rounded-2xl border border-stone-300 font-bold text-xs text-stone-700 hover:bg-stone-50 disabled:bg-stone-100 disabled:text-stone-400 transition"
          >
            {currentPlan === 'free' ? t('current_tier') : t('downgrade_free')}
          </button>
        </div>

        {/* PLUS TIER (Featured) */}
        <div className="bg-emerald-950 text-white rounded-3xl border-2 border-emerald-500 p-6 flex flex-col justify-between space-y-6 shadow-xl relative overflow-hidden">
          <div className="absolute top-4 right-4 bg-amber-400 text-stone-950 text-[10px] font-black uppercase px-2.5 py-0.5 rounded-full flex items-center gap-1 shadow">
            <Star className="w-3 h-3 fill-stone-950" />
            <span>{t('most_popular')}</span>
          </div>

          <div className="space-y-4">
            <div className="space-y-1">
              <span className="text-xs font-bold uppercase tracking-wider text-emerald-400">
                {language === 'hi' ? 'सक्रिय किसान' : 'Active Grower'}
              </span>
              <h3 className="text-xl font-black text-white">{t('plan_plus')}</h3>
              <p className="text-xs text-emerald-200/80">
                {language === 'hi' ? 'संपूर्ण कारण विश्लेषण व मौसमी रोग ट्रैकिंग।' : 'Complete explainability and seasonal tracking.'}
              </p>
            </div>

            <div className="py-2">
              <span className="text-4xl font-black text-white">₹49</span>
              <span className="text-xs text-emerald-200">{t('per_month')}</span>
            </div>

            <ul className="space-y-2.5 text-xs text-emerald-100">
              <li className="flex items-start gap-2">
                <Check className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                <span><strong>50 {t('monthly_scans')}</strong> {t('per_month')}</span>
              </li>
              <li className="flex items-start gap-2">
                <Check className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                <span>{language === 'hi' ? 'विस्तृत कारण विश्लेषण (Explainable AI)' : 'Detailed Explainable AI'}</span>
              </li>
              <li className="flex items-start gap-2">
                <Check className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                <span>{language === 'hi' ? 'फसल इतिहास व सुरक्षित रिपोर्ट' : 'Persistent Crop History & Saved Reports'}</span>
              </li>
              <li className="flex items-start gap-2">
                <Check className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                <span>{language === 'hi' ? 'PDF रिपोर्ट डाउनलोड व प्रिंट' : 'Exportable PDF diagnostic reports'}</span>
              </li>
            </ul>
          </div>

          <button
            onClick={() => onOpenUpgradeModal('plus')}
            className="w-full py-3.5 rounded-2xl bg-emerald-500 hover:bg-emerald-400 text-emerald-950 font-black text-xs shadow-lg transition hover:scale-[1.02] active:scale-[0.98]"
          >
            {currentPlan === 'plus'
              ? (language === 'hi' ? 'सक्रिय योजना' : 'Active Plan')
              : (language === 'hi' ? 'क्रॉपकेयर प्लस चुनें (₹49)' : 'Get CropCare Plus (₹49)')}
          </button>
        </div>

        {/* PRO TIER */}
        <div className="bg-white rounded-3xl border border-stone-200 p-6 flex flex-col justify-between space-y-6 shadow-sm">
          <div className="space-y-4">
            <div className="space-y-1">
              <span className="text-xs font-bold uppercase tracking-wider text-purple-700">
                {language === 'hi' ? 'व्यावसायिक व CSC' : 'Commercial & CSC'}
              </span>
              <h3 className="text-xl font-black text-stone-900">{t('plan_pro')}</h3>
              <p className="text-xs text-stone-500">
                {language === 'hi' ? 'प्रगतिशील किसानों, कृषि मित्रों व ऑपरेटरों के लिए।' : 'For progressive farmers, Krishi Mitras & operators.'}
              </p>
            </div>

            <div className="py-2">
              <span className="text-4xl font-black text-stone-900">₹99</span>
              <span className="text-xs text-stone-500">{t('per_month')}</span>
            </div>

            <ul className="space-y-2.5 text-xs text-stone-700">
              <li className="flex items-start gap-2">
                <Check className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                <span><strong>500 {t('monthly_scans')}</strong> {t('per_month')}</span>
              </li>
              <li className="flex items-start gap-2">
                <Check className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                <span>{language === 'hi' ? 'कृषि विशेषज्ञ से सीधा परामर्श' : 'Priority 1-on-1 Expert Agronomist triage'}</span>
              </li>
              <li className="flex items-start gap-2">
                <Check className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                <span>{language === 'hi' ? 'कृषि मित्र सहायक जांच टूलकिट' : 'Krishi Mitra assisted diagnosis toolkit'}</span>
              </li>
            </ul>
          </div>

          <button
            onClick={() => onOpenUpgradeModal('pro')}
            className="w-full py-3.5 rounded-2xl bg-stone-900 hover:bg-stone-800 text-white font-black text-xs shadow-md transition hover:scale-[1.02] active:scale-[0.98]"
          >
            {currentPlan === 'pro'
              ? (language === 'hi' ? 'सक्रिय योजना' : 'Active Plan')
              : (language === 'hi' ? 'क्रॉपकेयर प्रो चुनें (₹99)' : 'Get CropCare Pro (₹99)')}
          </button>
        </div>
      </div>

      {/* Sustainable Business Model Architecture Graphic */}
      <div className="p-8 rounded-3xl bg-stone-100 border border-stone-200 space-y-6">
        <h3 className="text-sm font-black text-stone-900 uppercase text-center tracking-wide">
          Sustainable Platform Monetization Architecture
        </h3>

        <div className="max-w-2xl mx-auto p-4 bg-white rounded-2xl border border-stone-200 font-mono text-xs text-stone-800 text-center leading-relaxed">
          <pre className="overflow-x-auto text-[11px] leading-tight">
{`                    🌱 CropCare AI Platform
                               ↓
                      Free Basic Service
                               ↓
                       Farmer Adoption
                               ↓
          ┌────────────────────┼────────────────────┐
          ↓                    ↓                    ↓
      Premium               Expert                 B2B
    Subscription         Consultation         Surveillance
    (₹49 - ₹99/mo)     (Revenue Share)      (FPOs & Input Co)
          ↓                    ↓                    ↓
          └────────────────────┼────────────────────┘
                               ↓
                   Sustainable Reinvestment`}
          </pre>
        </div>
      </div>
    </div>
  );
}
