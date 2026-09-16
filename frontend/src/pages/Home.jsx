import React from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import {
  ScanLine,
  Search,
  Sparkles,
  ShieldCheck,
  WifiOff,
  PhoneCall,
  Users,
  CheckCircle2,
  ArrowRight,
  TrendingUp,
  Award,
  Crown,
  HelpCircle,
  Download,
  FileText
} from 'lucide-react';

export function Home({ setCurrentPage, setSelectedCrop }) {
  const { t, language } = useLanguage();

  const handleStartScan = (cropName = 'Tomato') => {
    if (setSelectedCrop) setSelectedCrop(cropName);
    setCurrentPage('detect');
  };

  const cropQuickLinks = [
    { name: 'Tomato', hindi: 'टमाटर', icon: '🍅' },
    { name: 'Potato', hindi: 'आलू', icon: '🥔' },
    { name: 'Rice', hindi: 'धान', icon: '🌾' },
    { name: 'Apple', hindi: 'सेब', icon: '🍎' },
    { name: 'Corn', hindi: 'मक्का', icon: '🌽' },
    { name: 'Wheat', hindi: 'गेहूं', icon: '🌾' },
    { name: 'Cotton', hindi: 'कपास', icon: '☁️' }
  ];

  return (
    <div className="space-y-16 pb-16">
      {/* HERO SECTION */}
      <section className="relative overflow-hidden pt-8 pb-12 sm:pt-14 sm:pb-18 bg-gradient-to-b from-emerald-900 via-emerald-800 to-emerald-950 text-white rounded-3xl mx-4 sm:mx-6 lg:mx-8 px-6 sm:px-12 shadow-xl">
        {/* Background ambient elements */}
        <div className="absolute -right-16 -top-16 w-96 h-96 rounded-full bg-emerald-500/10 blur-3xl pointer-events-none"></div>
        <div className="absolute -left-16 -bottom-16 w-96 h-96 rounded-full bg-emerald-400/10 blur-3xl pointer-events-none"></div>

        <div className="relative z-10 max-w-3xl space-y-6">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full text-xs font-bold bg-emerald-700/80 text-emerald-200 border border-emerald-600 shadow-sm backdrop-blur">
            <Sparkles className="w-3.5 h-3.5 text-amber-300" />
            <span>{t('ai_platform_badge')}</span>
          </div>

          <h1 className="text-3xl sm:text-5xl font-extrabold tracking-tight leading-[1.15]">
            {t('tagline')}
          </h1>

          <p className="text-sm sm:text-base text-emerald-100/90 leading-relaxed font-normal">
            {t('hero_desc')}
          </p>

          {/* Primary Action Buttons */}
          <div className="flex flex-wrap items-center gap-4 pt-2">
            <button
              onClick={() => handleStartScan('Tomato')}
              className="inline-flex items-center gap-2.5 px-6 py-4 rounded-2xl bg-white text-emerald-900 font-extrabold text-sm hover:bg-emerald-50 shadow-lg hover:shadow-xl transition hover:scale-105 active:scale-95"
            >
              <ScanLine className="w-5 h-5 text-emerald-700" />
              <span>{t('nav_detect')} ({t('demo_scan_btn')})</span>
            </button>

            <a
              href="./CropCare_AI_Hackathon_PitchDeck.pptx"
              download="CropCare_AI_Hackathon_PitchDeck.pptx"
              className="inline-flex items-center gap-2 px-5 py-4 rounded-2xl bg-gradient-to-r from-amber-400 to-amber-500 hover:from-amber-300 hover:to-amber-400 text-stone-950 font-black text-sm shadow-xl hover:shadow-2xl transition hover:scale-105 active:scale-95 border border-amber-300"
            >
              <Award className="w-5 h-5 text-stone-950" />
              <span>{language === 'hi' ? '🏆 हैकाथॉन PPT (8 Slides)' : '🏆 Hackathon Pitch Deck (8 Slides)'}</span>
            </a>

            <button
              onClick={() => setCurrentPage('library')}
              className="inline-flex items-center gap-2 px-5 py-4 rounded-2xl bg-emerald-800/80 hover:bg-emerald-700 text-white font-bold text-sm border border-emerald-600/80 transition"
            >
              <Search className="w-4 h-4" />
              <span>{t('nav_library')}</span>
            </button>

            <button
              onClick={() => setCurrentPage('telecom')}
              className="inline-flex items-center gap-2 px-4 py-4 rounded-2xl bg-stone-900/60 hover:bg-stone-900 text-amber-300 font-bold text-xs border border-stone-700 transition"
            >
              <PhoneCall className="w-4 h-4 text-amber-400" />
              <span>{t('basic_phone_ivr')}</span>
            </button>
          </div>

          {/* Hackathon Pitch Deck Highlight Banner */}
          <div className="flex items-center justify-between flex-wrap gap-3 p-3.5 rounded-2xl bg-amber-400/10 border border-amber-400/30 text-amber-200 text-xs">
            <div className="flex items-center gap-2.5">
              <span className="text-xl">📊</span>
              <div>
                <span className="font-extrabold text-amber-300">
                  {language === 'hi' ? 'आधिकारिक हैकाथॉन प्रेजेंटेशन (8 स्लाइड्स):' : 'Official Hackathon Pitch Deck (8 Slides):'}
                </span>
                <span className="ml-1.5 text-emerald-100 hidden sm:inline">
                  {language === 'hi' ? 'प्रॉब्लम, सॉल्यूशन, टेक स्टैक, लाइव डेमो, बिज़नेस मॉडल एवं टीम प्रोफाइल।' : 'Problem, Solution, Architecture, Live Demo, Business Model & Team.'}
                </span>
              </div>
            </div>
            <a
              href="./CropCare_AI_Hackathon_PitchDeck.pptx"
              download="CropCare_AI_Hackathon_PitchDeck.pptx"
              className="px-3 py-1.5 rounded-xl bg-amber-400 hover:bg-amber-300 text-stone-950 font-bold text-xs transition flex items-center gap-1.5 shadow-sm"
            >
              <Download className="w-3.5 h-3.5" />
              <span>{language === 'hi' ? 'डाउनलोड PPT (8 Slides)' : 'Download PPT (8 Slides)'}</span>
            </a>
          </div>

          {/* Quick Crop Selector Pills */}
          <div className="pt-4 border-t border-emerald-700/60">
            <div className="text-xs font-semibold text-emerald-200 mb-2">
              {t('quick_scan_by_crop')}
            </div>
            <div className="flex flex-wrap gap-2">
              {cropQuickLinks.map((c) => {
                const displayName = language === 'hi' ? c.hindi : c.name;
                return (
                  <button
                    key={c.name}
                    onClick={() => handleStartScan(c.name)}
                    className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-emerald-700/50 hover:bg-emerald-600 text-xs font-bold text-white border border-emerald-500/40 transition hover:scale-105"
                  >
                    <span>{c.icon}</span>
                    <span>{displayName}</span>
                  </button>
                );
              })}
            </div>
          </div>
        </div>
      </section>

      {/* CORE PHILOSOPHY SECTION */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-2xl mx-auto space-y-2 mb-10">
          <h2 className="text-2xl sm:text-3xl font-black text-stone-900 tracking-tight">
            {t('philosophy_title')}
          </h2>
          <p className="text-xs sm:text-sm text-stone-600 leading-relaxed">
            {t('philosophy_sub')}
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {/* Step 1: Detect */}
          <div className="bg-white p-6 rounded-3xl border border-stone-200 shadow-sm hover:shadow-md transition space-y-3 relative overflow-hidden group">
            <div className="w-12 h-12 rounded-2xl bg-emerald-100 text-emerald-800 flex items-center justify-center font-black text-lg group-hover:scale-110 transition">
              1
            </div>
            <h3 className="text-base font-extrabold text-stone-900">{t('step_detect')}</h3>
            <p className="text-xs text-stone-600 leading-relaxed">{t('step_detect_desc')}</p>
            <div className="pt-2 text-[11px] font-bold text-emerald-700 flex items-center gap-1">
              <span>{t('accuracy_baseline')}</span>
              <CheckCircle2 className="w-3.5 h-3.5" />
            </div>
          </div>

          {/* Step 2: Explain */}
          <div className="bg-white p-6 rounded-3xl border border-stone-200 shadow-sm hover:shadow-md transition space-y-3 relative overflow-hidden group">
            <div className="w-12 h-12 rounded-2xl bg-sky-100 text-sky-800 flex items-center justify-center font-black text-lg group-hover:scale-110 transition">
              2
            </div>
            <h3 className="text-base font-extrabold text-stone-900">{t('step_explain')}</h3>
            <p className="text-xs text-stone-600 leading-relaxed">{t('step_explain_desc')}</p>
            <div className="pt-2 text-[11px] font-bold text-sky-700 flex items-center gap-1">
              <span>{t('explainable_ai_engine')}</span>
              <Sparkles className="w-3.5 h-3.5" />
            </div>
          </div>

          {/* Step 3: Solve */}
          <div className="bg-white p-6 rounded-3xl border border-stone-200 shadow-sm hover:shadow-md transition space-y-3 relative overflow-hidden group">
            <div className="w-12 h-12 rounded-2xl bg-amber-100 text-amber-800 flex items-center justify-center font-black text-lg group-hover:scale-110 transition">
              3
            </div>
            <h3 className="text-base font-extrabold text-stone-900">{t('step_solve')}</h3>
            <p className="text-xs text-stone-600 leading-relaxed">{t('step_solve_desc')}</p>
            <div className="pt-2 text-[11px] font-bold text-amber-700 flex items-center gap-1">
              <span>{t('safe_guidelines')}</span>
              <ShieldCheck className="w-3.5 h-3.5" />
            </div>
          </div>

          {/* Step 4: Prevent */}
          <div className="bg-white p-6 rounded-3xl border border-stone-200 shadow-sm hover:shadow-md transition space-y-3 relative overflow-hidden group">
            <div className="w-12 h-12 rounded-2xl bg-emerald-900 text-white flex items-center justify-center font-black text-lg group-hover:scale-110 transition">
              4
            </div>
            <h3 className="text-base font-extrabold text-stone-900">{t('step_prevent')}</h3>
            <p className="text-xs text-stone-600 leading-relaxed">{t('step_prevent_desc')}</p>
            <div className="pt-2 text-[11px] font-bold text-emerald-800 flex items-center gap-1">
              <span>{t('next_season_security')}</span>
              <Award className="w-3.5 h-3.5" />
            </div>
          </div>
        </div>
      </section>

      {/* RURAL ACCESSIBILITY PILLARS */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="p-8 sm:p-10 rounded-3xl bg-stone-100 border border-stone-200">
          <div className="max-w-2xl mb-8 space-y-2">
            <div className="text-xs font-bold text-emerald-700 uppercase tracking-wide">
              {t('universal_inclusion')}
            </div>
            <h3 className="text-2xl font-black text-stone-900">
              {t('built_for_rural')}
            </h3>
            <p className="text-xs sm:text-sm text-stone-600">
              {t('rural_desc')}
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Pillar 1: Offline PWA */}
            <div className="bg-white p-6 rounded-2xl border border-stone-200 space-y-3 shadow-sm">
              <div className="w-10 h-10 rounded-xl bg-amber-100 text-amber-800 flex items-center justify-center">
                <WifiOff className="w-5 h-5" />
              </div>
              <h4 className="text-sm font-bold text-stone-900">{t('offline_pwa_title')}</h4>
              <p className="text-xs text-stone-600 leading-relaxed">
                {t('offline_pwa_desc')}
              </p>
              <div className="text-[11px] font-bold text-amber-700">🟢 {t('offline_aware')}</div>
            </div>

            {/* Pillar 2: Feature Phone IVR & SMS */}
            <div className="bg-white p-6 rounded-2xl border border-stone-200 space-y-3 shadow-sm">
              <div className="w-10 h-10 rounded-xl bg-emerald-100 text-emerald-800 flex items-center justify-center">
                <PhoneCall className="w-5 h-5" />
              </div>
              <h4 className="text-sm font-bold text-stone-900">{t('ivr_helpline_title')}</h4>
              <p className="text-xs text-stone-600 leading-relaxed">
                {t('ivr_helpline_desc')}
              </p>
              <button
                onClick={() => setCurrentPage('telecom')}
                className="text-[11px] font-bold text-emerald-700 hover:underline flex items-center gap-1"
              >
                <span>{t('launch_simulator')}</span>
                <ArrowRight className="w-3 h-3" />
              </button>
            </div>

            {/* Pillar 3: Krishi Mitra Assisted Diagnosis */}
            <div className="bg-white p-6 rounded-2xl border border-stone-200 space-y-3 shadow-sm">
              <div className="w-10 h-10 rounded-xl bg-sky-100 text-sky-800 flex items-center justify-center">
                <Users className="w-5 h-5" />
              </div>
              <h4 className="text-sm font-bold text-stone-900">{t('extension_portal_title')}</h4>
              <p className="text-xs text-stone-600 leading-relaxed">
                {t('extension_portal_desc')}
              </p>
              <button
                onClick={() => setCurrentPage('assisted')}
                className="text-[11px] font-bold text-sky-700 hover:underline flex items-center gap-1"
              >
                <span>{t('open_extension')}</span>
                <ArrowRight className="w-3 h-3" />
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* PROJECT TEAM & LEADERSHIP */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="p-8 sm:p-10 rounded-3xl bg-white border border-stone-200 shadow-sm space-y-6">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800 mb-2">
                <Award className="w-3.5 h-3.5 text-emerald-700" />
                <span>{language === 'hi' ? 'हैकाथॉन प्रोजेक्ट टीम' : 'Hackathon Project Team'}</span>
              </div>
              <h3 className="text-2xl font-black text-stone-900">
                {language === 'hi' ? 'प्रोजेक्ट टीम एवं नेतृत्व' : 'Project Team & Leadership'}
              </h3>
              <p className="text-xs sm:text-sm text-stone-600 mt-1">
                {language === 'hi'
                  ? 'क्रॉपकेयर AI — जमीनी स्तर पर भारतीय किसानों को सशक्त बनाने वाली इनोवेटर टीम'
                  : 'The innovator team engineering CropCare AI for Indian agriculture'}
              </p>
            </div>
            <div className="flex items-center gap-3">
              <a
                href="./CropCare_AI_Hackathon_PitchDeck.pptx"
                download="CropCare_AI_Hackathon_PitchDeck.pptx"
                className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-amber-400 hover:bg-amber-300 text-stone-950 font-bold text-xs shadow-sm transition"
              >
                <Download className="w-4 h-4" />
                <span>{language === 'hi' ? 'डाउनलोड PPT (8 Slides)' : 'Download Pitch Deck (8 Slides)'}</span>
              </a>
              <button
                onClick={() => {
                  setCurrentPage('team');
                  window.scrollTo({ top: 0, behavior: 'smooth' });
                }}
                className="inline-flex items-center gap-1.5 px-4 py-2.5 rounded-xl bg-stone-900 hover:bg-stone-800 text-white font-bold text-xs transition"
              >
                <span>{language === 'hi' ? 'पूरी टीम देखें' : 'View Team Page'}</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-2">
            {/* Team Leader */}
            <div className="p-6 rounded-2xl bg-stone-900 text-white space-y-3 relative overflow-hidden border-2 border-emerald-500/80 shadow-md flex flex-col justify-between">
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="px-2.5 py-1 rounded-full bg-amber-400 text-stone-950 text-[11px] font-black flex items-center gap-1">
                    <Crown className="w-3 h-3" />
                    <span>{language === 'hi' ? 'टीम लीडर' : 'Team Leader'}</span>
                  </span>
                  <span className="text-xs text-emerald-400 font-bold">Project Lead</span>
                </div>
                <div>
                  <h4 className="text-lg font-extrabold text-white">Ram raghuvir Roy</h4>
                  <div className="text-xs text-emerald-300 font-medium mt-0.5">
                    {language === 'hi' ? 'AI सिस्टम आर्किटेक्चर एवं फुल स्टैक' : 'AI System Architecture & Full Stack'}
                  </div>
                </div>
                <p className="text-xs text-stone-300 leading-relaxed">
                  {language === 'hi'
                    ? 'क्रॉप डिसीज़ विज़न मॉडल, रिएक्ट वेब ऐप और ऑफलाइन PWA सिस्टम का समग्र नेतृत्व व निर्माण।'
                    : 'Led overall project architecture, disease detection model, React frontend, and offline PWA integration.'}
                </p>
              </div>
              <div className="pt-3 border-t border-stone-800 text-[11px] text-amber-300 font-semibold">
                ⭐ {language === 'hi' ? 'परियोजना समन्वयक' : 'Project Coordinator'}
              </div>
            </div>

            {/* Team Mate 1 */}
            <div className="p-6 rounded-2xl bg-stone-50 border border-stone-200 space-y-3 flex flex-col justify-between">
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="px-2.5 py-1 rounded-full bg-stone-200 text-stone-800 text-[11px] font-bold">
                    {language === 'hi' ? 'टीम मेंबर' : 'Team Member'}
                  </span>
                  <span className="text-xs text-stone-500 font-medium">Core Member</span>
                </div>
                <div>
                  <h4 className="text-lg font-bold text-stone-900">Anurag kumar Ray</h4>
                  <div className="text-xs text-emerald-700 font-semibold mt-0.5">
                    {language === 'hi' ? 'क्लाउड, डेटाबेस एवं बैकएंड' : 'Cloud, Database & Backend Lead'}
                  </div>
                </div>
                <p className="text-xs text-stone-600 leading-relaxed">
                  {language === 'hi'
                    ? 'डेटाबेस स्कीमा, क्लाउड डेप्लॉयमेंट, फील्ड डेटा सिंक और टेलीकॉम IVR/SMS इंटीग्रेशन।'
                    : 'Engineered backend APIs, cloud database, deployment automation, and telecom IVR/SMS simulation.'}
                </p>
              </div>
              <div className="pt-3 border-t border-stone-200 text-[11px] text-stone-500 font-medium">
                🌱 {language === 'hi' ? 'बैकएंड इंफ्रास्ट्रक्चर' : 'Backend Infrastructure'}
              </div>
            </div>

            {/* Team Mate 2 */}
            <div className="p-6 rounded-2xl bg-stone-50 border border-stone-200 space-y-3 flex flex-col justify-between">
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="px-2.5 py-1 rounded-full bg-stone-200 text-stone-800 text-[11px] font-bold">
                    {language === 'hi' ? 'टीम मेंबर' : 'Team Member'}
                  </span>
                  <span className="text-xs text-stone-500 font-medium">Core Member</span>
                </div>
                <div>
                  <h4 className="text-lg font-bold text-stone-900">Keshav kumar jha</h4>
                  <div className="text-xs text-emerald-700 font-semibold mt-0.5">
                    {language === 'hi' ? 'पादप रोग रिसर्च एवं UX' : 'Agronomy Research & UX Design'}
                  </div>
                </div>
                <p className="text-xs text-stone-600 leading-relaxed">
                  {language === 'hi'
                    ? '14 फसलों के रोग लक्षण व जैविक/रासायनिक उपचार संकलन और ग्रामीण किसान-अनुकूल इंटरफ़ेस।'
                    : 'Curated plant disease dataset, localized remedies (organic + chemical), and farmer-friendly UI/UX.'}
                </p>
              </div>
              <div className="pt-3 border-t border-stone-200 text-[11px] text-stone-500 font-medium">
                🌾 {language === 'hi' ? 'एग्रोनॉमी एवं किसान UX' : 'Agronomy & Farmer UX'}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* PLATFORM STATISTICS */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="p-5 rounded-2xl bg-white border border-stone-200 text-center space-y-1">
            <div className="text-3xl font-black text-emerald-700">94%</div>
            <div className="text-xs font-bold text-stone-800">{t('stat_accuracy')}</div>
            <div className="text-[10px] text-stone-500">{t('stat_accuracy_sub')}</div>
          </div>
          <div className="p-5 rounded-2xl bg-white border border-stone-200 text-center space-y-1">
            <div className="text-3xl font-black text-stone-900">5,320+</div>
            <div className="text-xs font-bold text-stone-800">{t('stat_scanned')}</div>
            <div className="text-[10px] text-stone-500">{t('stat_scanned_sub')}</div>
          </div>
          <div className="p-5 rounded-2xl bg-white border border-stone-200 text-center space-y-1">
            <div className="text-3xl font-black text-stone-900">1,420+</div>
            <div className="text-xs font-bold text-stone-800">{t('stat_farmers')}</div>
            <div className="text-[10px] text-stone-500">{t('stat_farmers_sub')}</div>
          </div>
          <div className="p-5 rounded-2xl bg-white border border-stone-200 text-center space-y-1">
            <div className="text-3xl font-black text-emerald-700">100%</div>
            <div className="text-xs font-bold text-stone-800">{t('stat_offline')}</div>
            <div className="text-[10px] text-stone-500">{t('stat_offline_sub')}</div>
          </div>
        </div>
      </section>
    </div>
  );
}
