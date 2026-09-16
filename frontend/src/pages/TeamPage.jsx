import React from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import {
  Crown,
  Award,
  Download,
  ScanLine,
  ArrowRight,
  Code2,
  Database,
  Sprout,
  Users,
  ShieldCheck
} from 'lucide-react';

export function TeamPage({ setCurrentPage }) {
  const { language } = useLanguage();
  const isHi = language === 'hi';

  const teamMembers = [
    {
      name: 'Ram raghuvir Roy',
      role: isHi ? 'टीम लीडर एवं मुख्य AI डेवलपर' : 'Team Leader & Lead AI Developer',
      badge: isHi ? 'टीम लीडर' : 'Team Leader',
      isLead: true,
      icon: Crown,
      points: [
        isHi ? 'प्रोजेक्ट का संपूर्ण नेतृत्व एवं सिस्टम आर्किटेक्चर' : 'Project leadership and end-to-end system architecture',
        isHi ? 'क्रॉप डिसीज़ विज़न मॉडल ट्रेनिंग एवं ऑप्टिमाइज़ेशन' : 'Crop disease vision model training and optimization',
        isHi ? 'रिएक्ट (React) फ्रंटेंड एवं ऑफलाइन PWA कैचिंग सिस्टम' : 'React frontend and offline-first PWA caching implementation',
        isHi ? 'हैकाथॉन पिच एवं तकनीकी प्रस्तुति की तैयारी' : 'Hackathon pitch deck strategy and live demo orchestration'
      ]
    },
    {
      name: 'Anurag kumar Ray',
      role: isHi ? 'बैकएंड एवं क्लाउड इंफ्रास्ट्रक्चर' : 'Backend & Cloud Infrastructure Lead',
      badge: isHi ? 'टीम मेंबर' : 'Core Member',
      isLead: false,
      icon: Database,
      points: [
        isHi ? 'बैकएंड REST APIs और डेटाबेस स्कीमा का निर्माण' : 'REST API architecture and cloud database schema design',
        isHi ? 'गिटहब एक्शन्स और वर्सेल पर ऑटोमेटेड डेप्लॉयमेंट' : 'Automated CI/CD deployment on GitHub Actions and Vercel',
        isHi ? 'ऑफलाइन डेटा सिंक एवं फील्ड रिकॉर्ड सिंक्रोनाइज़ेशन' : 'Offline data sync protocols for field scan persistence',
        isHi ? 'टेलीकॉम IVR और SMS हेल्पलाइन सिम्युलेटर इंटीग्रेशन' : 'Telecom IVR and SMS helpline simulator integration'
      ]
    },
    {
      name: 'Keshav kumar jha',
      role: isHi ? 'एग्रोनॉमी रिसर्च एवं UI/UX डिजाइन' : 'Agronomy Research & UI/UX Design',
      badge: isHi ? 'टीम मेंबर' : 'Core Member',
      isLead: false,
      icon: Sprout,
      points: [
        isHi ? '14 फसलों के 38+ पादप रोगों का पैथोलॉजिकल डेटा संकलन' : 'Curated pathological datasets across 14 crops and 38+ diseases',
        isHi ? 'जैविक (नीम, बायो-कंट्रोल) एवं रासायनिक उपचार गाइडलाइंस' : 'Formulated organic and chemical treatment recommendation guides',
        isHi ? 'किसानों के अनुकूल द्विभाषी (हिंदी-अंग्रेजी) इंटरफ़ेस डिजाइन' : 'Designed bilingual farmer-friendly UI with high contrast',
        isHi ? 'फील्ड टेस्टिंग और यूजर फीडबैक पर आधारित सुधार' : 'Conducted usability testing and accessibility improvements'
      ]
    }
  ];

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-12">
      {/* Header */}
      <div className="text-center max-w-2xl mx-auto space-y-3">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800 border border-emerald-200">
          <Award className="w-3.5 h-3.5 text-emerald-700" />
          <span>{isHi ? 'हैकाथॉन एवं आइडियाथॉन 2026 प्रोजेक्ट' : 'Hackathon & Ideathon 2026 Project'}</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-stone-900 tracking-tight">
          {isHi ? 'हमारी प्रोजेक्ट टीम' : 'Meet Our Project Team'}
        </h1>
        <p className="text-sm text-stone-600 leading-relaxed">
          {isHi
            ? 'क्रॉपकेयर AI — भारतीय किसानों के लिए सहज, ऑफलाइन-सक्षम और सटीक फसल रोग निदान प्रणाली।'
            : 'CropCare AI — Engineered to provide instant, offline-capable, and accurate crop diagnosis for Indian farmers.'}
        </p>
      </div>

      {/* Team Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {teamMembers.map((member, idx) => {
          const Icon = member.icon;
          return (
            <div
              key={idx}
              className={`rounded-2xl p-6 transition flex flex-col justify-between ${
                member.isLead
                  ? 'bg-gradient-to-b from-stone-900 to-stone-950 text-white shadow-xl border-2 border-emerald-500/60'
                  : 'bg-white border border-stone-200 shadow-sm text-stone-900 hover:shadow-md'
              }`}
            >
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div
                    className={`w-12 h-12 rounded-xl flex items-center justify-center font-bold ${
                      member.isLead
                        ? 'bg-emerald-600 text-white'
                        : 'bg-stone-100 text-stone-800 border border-stone-200'
                    }`}
                  >
                    <Icon className="w-6 h-6" />
                  </div>
                  <span
                    className={`px-2.5 py-1 rounded-full text-[11px] font-bold ${
                      member.isLead
                        ? 'bg-amber-400 text-stone-950'
                        : 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                    }`}
                  >
                    {member.badge}
                  </span>
                </div>

                <div>
                  <h3 className={`text-xl font-bold ${member.isLead ? 'text-white' : 'text-stone-900'}`}>
                    {member.name}
                  </h3>
                  <p className={`text-xs font-semibold mt-0.5 ${member.isLead ? 'text-emerald-300' : 'text-emerald-700'}`}>
                    {member.role}
                  </p>
                </div>

                <div className="pt-2 border-t border-stone-200/20">
                  <div className={`text-[11px] font-bold uppercase tracking-wider mb-2 ${member.isLead ? 'text-stone-400' : 'text-stone-500'}`}>
                    {isHi ? 'मुख्य योगदान:' : 'Key Responsibilities:'}
                  </div>
                  <ul className="space-y-2">
                    {member.points.map((pt, pIdx) => (
                      <li
                        key={pIdx}
                        className={`text-xs leading-relaxed flex items-start gap-1.5 ${
                          member.isLead ? 'text-stone-300' : 'text-stone-600'
                        }`}
                      >
                        <span className={member.isLead ? 'text-emerald-400' : 'text-emerald-600'}>•</span>
                        <span>{pt}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              {member.isLead && (
                <div className="pt-6 mt-4 border-t border-stone-800">
                  <div className="text-[11px] text-amber-300 font-medium">
                    ⭐ {isHi ? 'परियोजना समन्वयक एवं टीम लीडर' : 'Project Coordinator & Team Lead'}
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Project Overview & Download Banner */}
      <div className="p-6 sm:p-8 rounded-2xl bg-stone-100 border border-stone-200 flex flex-col sm:flex-row items-center justify-between gap-6">
        <div className="space-y-1 text-center sm:text-left">
          <h4 className="text-lg font-bold text-stone-900">
            {isHi ? 'आधिकारिक 8-स्लाइड हैकाथॉन प्रेजेंटेशन' : 'Official 8-Slide Hackathon Pitch Deck'}
          </h4>
          <p className="text-xs text-stone-600 max-w-xl">
            {isHi
              ? 'प्रॉब्लम, सॉल्यूशन, टेक स्टैक, वर्किंग डेमो, बिजनेस मॉडल और टीम प्रोफाइल की पूरी जानकारी।'
              : 'Complete breakdown of Problem, Solution, Architecture, Live Demo, Business Model & Team.'}
          </p>
        </div>
        <div className="flex flex-wrap items-center gap-3">
          <a
            href="./CropCare_AI_Hackathon_PitchDeck.pptx"
            download="CropCare_AI_Hackathon_PitchDeck.pptx"
            className="inline-flex items-center gap-2 px-5 py-3 rounded-xl bg-gradient-to-r from-amber-400 to-amber-500 hover:from-amber-300 hover:to-amber-400 text-stone-950 font-extrabold text-xs shadow-md transition"
          >
            <Download className="w-4 h-4" />
            <span>{isHi ? 'डाउनलोड PPT (8 Slides)' : 'Download Pitch Deck (8 Slides)'}</span>
          </a>
          {setCurrentPage && (
            <button
              onClick={() => {
                setCurrentPage('home');
                window.scrollTo({ top: 0, behavior: 'smooth' });
              }}
              className="inline-flex items-center gap-1.5 px-4 py-3 rounded-xl bg-white hover:bg-stone-50 text-stone-800 font-bold text-xs border border-stone-300 transition"
            >
              <span>{isHi ? 'होम पेज' : 'Back to Home'}</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
