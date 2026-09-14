import React, { useState } from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import { api } from '../services/api';
import {
  PhoneCall,
  MessageSquare,
  Volume2,
  VolumeX,
  PhoneForwarded,
  Send,
  Sparkles,
  CheckCircle2,
  CornerDownLeft,
  Smartphone
} from 'lucide-react';

export function TelecomSimulator() {
  const { t, language } = useLanguage();
  const [activeTab, setActiveTab] = useState('ivr'); // 'ivr' or 'sms'

  // IVR State
  const [ivrStep, setIvrStep] = useState('idle'); // 'idle', 'in_call', 'ended'
  const [ivrLang, setIvrLang] = useState(language || 'hi');
  const [ivrCrop, setIvrCrop] = useState('Tomato');
  const [ivrSymptom, setIvrSymptom] = useState('spots');
  const [callLog, setCallLog] = useState([]);
  const [spokenText, setSpokenText] = useState('');
  const [isSpeaking, setIsSpeaking] = useState(false);

  // SMS State
  const [smsQuery, setSmsQuery] = useState(language === 'hi' ? 'टमाटर धब्बे' : 'TOMATO LEAF SPOTS');
  const [smsConversation, setSmsConversation] = useState([
    {
      sender: 'system',
      text: language === 'hi'
        ? '🌱 क्रॉपकेयर AI SMS हेल्पलाइन (51969) में आपका स्वागत है। अपनी फसल और लक्षण लिखकर भेजें, उदा. "टमाटर धब्बे" या "धान झोंका"।'
        : '🌱 Welcome to CropCare AI SMS Helpline (51969). Send [CROP] [SYMPTOM], e.g. "TOMATO LEAF SPOTS" or "धान झोंका".'
    }
  ]);
  const [isSendingSMS, setIsSendingSMS] = useState(false);

  // Speak via Web Speech Synthesis API
  const speakText = (text, langCode = 'hi-IN') => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = langCode;
      utterance.rate = 0.95;
      utterance.onstart = () => setIsSpeaking(true);
      utterance.onend = () => setIsSpeaking(false);
      utterance.onerror = () => setIsSpeaking(false);
      window.speechSynthesis.speak(utterance);
    }
  };

  const stopSpeaking = () => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
    }
    setIsSpeaking(false);
  };

  // IVR Workflow
  const handleDialHelpline = () => {
    setIvrStep('step1_lang');
    const welcome = language === 'hi'
      ? "नमस्ते। क्रॉपकेयर एआई किसान हेल्पलाइन में आपका स्वागत है। हिंदी के लिए 1 दबाएं, For English press 2."
      : "Welcome to CropCare AI Kisan Helpline. For English press 1, हिंदी के लिए 2 दबाएं.";
    setSpokenText(welcome);
    setCallLog([{ prompt: welcome }]);
    speakText(welcome, language === 'hi' ? 'hi-IN' : 'en-US');
  };

  const handleKeypadPress = async (digit) => {
    if (ivrStep === 'step1_lang') {
      const selectedLang = digit === '2' ? (language === 'hi' ? 'en' : 'hi') : (language === 'hi' ? 'hi' : 'en');
      setIvrLang(selectedLang);
      setIvrStep('step2_crop');

      const cropPrompt = selectedLang === 'hi'
        ? "फसल चुनने के लिए: टमाटर के लिए 1 दबाएं, आलू के लिए 2, धान के लिए 3, गेहूं के लिए 4 दबाएं।"
        : "To select crop: Press 1 for Tomato, 2 for Potato, 3 for Rice, 4 for Wheat.";
      setSpokenText(cropPrompt);
      setCallLog(prev => [...prev, { user: digit }, { prompt: cropPrompt }]);
      speakText(cropPrompt, selectedLang === 'hi' ? 'hi-IN' : 'en-US');
    } else if (ivrStep === 'step2_crop') {
      const cropMap = { '1': 'Tomato', '2': 'Potato', '3': 'Rice', '4': 'Wheat' };
      const selectedCrop = cropMap[digit] || 'Tomato';
      setIvrCrop(selectedCrop);
      setIvrStep('step3_symptoms');

      const cropHindiMap = { 'Tomato': 'टमाटर', 'Potato': 'आलू', 'Rice': 'धान', 'Wheat': 'गेहूं' };
      const displayCropName = ivrLang === 'hi' ? cropHindiMap[selectedCrop] : selectedCrop;

      const symPrompt = ivrLang === 'hi'
        ? `आपने ${displayCropName} चुना। पत्तियों पर धब्बे या झुलसन के लिए 1 दबाएं, पत्ती मरोड़ या पीलापन के लिए 2 दबाएं।`
        : `You selected ${selectedCrop}. For leaf spots or blight press 1, for leaf curl or yellowing press 2.`;
      setSpokenText(symPrompt);
      setCallLog(prev => [...prev, { user: digit }, { prompt: symPrompt }]);
      speakText(symPrompt, ivrLang === 'hi' ? 'hi-IN' : 'en-US');
    } else if (ivrStep === 'step3_symptoms') {
      const symKey = digit === '2' ? 'curl' : 'spots';
      setIvrSymptom(symKey);
      setIvrStep('advisory_speaking');

      // Call Backend IVR API
      const res = await api.triggerIVR({
        caller_phone: '9876543210',
        language: ivrLang,
        crop: ivrCrop,
        symptoms_key: symKey
      });

      const advice = res.voice_script;
      setSpokenText(advice);
      setCallLog(prev => [...prev, { user: digit }, { prompt: advice, isFinal: true }]);
      speakText(advice, ivrLang === 'hi' ? 'hi-IN' : 'en-US');
    }
  };

  const handleEndCall = () => {
    stopSpeaking();
    setIvrStep('idle');
    setSpokenText('');
  };

  // SMS Workflow
  const handleSendSMS = async (e) => {
    e.preventDefault();
    if (!smsQuery.trim() || isSendingSMS) return;

    const query = smsQuery.trim();
    setSmsConversation(prev => [...prev, { sender: 'user', text: query }]);
    setSmsQuery('');
    setIsSendingSMS(true);

    try {
      const res = await api.sendSMS({
        sender_phone: '9876543210',
        message: query
      });
      setSmsConversation(prev => [...prev, { sender: 'system', text: res.sms_response }]);
    } catch (err) {
      setSmsConversation(prev => [...prev, {
        sender: 'system',
        text: language === 'hi' ? 'क्रॉपकेयर त्रुटि: सेवा अनुपलब्ध है।' : 'CropCare Error: Service unavailable.'
      }]);
    } finally {
      setIsSendingSMS(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-6 space-y-6">
      {/* Header */}
      <div className="space-y-1 text-center sm:text-left">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-amber-100 text-amber-900 border border-amber-300">
          <PhoneCall className="w-3.5 h-3.5" />
          <span>{language === 'hi' ? 'साधारण फोन टेलीकॉम सिम्युलेटर' : 'Feature Phone Telecom Simulator'}</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-black text-stone-900 tracking-tight">
          {t('telecom_title')}
        </h1>
        <p className="text-xs sm:text-sm text-stone-600">
          {t('telecom_sub')}
        </p>
      </div>

      {/* Tabs */}
      <div className="flex items-center gap-2 border-b border-stone-200 pb-2">
        <button
          onClick={() => {
            stopSpeaking();
            setActiveTab('ivr');
          }}
          className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-xs font-bold transition ${
            activeTab === 'ivr'
              ? 'bg-emerald-700 text-white shadow'
              : 'bg-white text-stone-700 hover:bg-stone-100'
          }`}
        >
          <PhoneCall className="w-4 h-4" />
          <span>{t('ivr_tab')}</span>
        </button>

        <button
          onClick={() => {
            stopSpeaking();
            setActiveTab('sms');
          }}
          className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-xs font-bold transition ${
            activeTab === 'sms'
              ? 'bg-emerald-700 text-white shadow'
              : 'bg-white text-stone-700 hover:bg-stone-100'
          }`}
        >
          <MessageSquare className="w-4 h-4" />
          <span>{t('sms_tab')}</span>
        </button>
      </div>

      {activeTab === 'ivr' ? (
        /* IVR SIMULATOR */
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Keypad Phone Frame */}
          <div className="bg-stone-900 rounded-3xl p-6 text-white shadow-2xl border-4 border-stone-800 space-y-4 max-w-sm mx-auto w-full">
            {/* Phone Screen */}
            <div className="bg-emerald-950/80 border-2 border-emerald-800 rounded-2xl p-4 min-h-[140px] flex flex-col justify-between font-mono text-emerald-300 shadow-inner">
              <div className="flex justify-between items-center text-[10px] text-emerald-400">
                <span>📶 2G GSM BSNL</span>
                <span>{ivrStep !== 'idle' ? (language === 'hi' ? 'कॉल जारी है' : 'CALL ACTIVE') : (language === 'hi' ? 'तैयार' : 'STANDBY')}</span>
              </div>
              <div className="text-center py-2">
                {ivrStep === 'idle' ? (
                  <div className="space-y-1">
                    <div className="text-sm font-bold text-white">{language === 'hi' ? 'टोल-फ्री हेल्पलाइन' : 'Toll-Free Helpline'}</div>
                    <div className="text-lg font-black text-amber-400">1800-180-1551</div>
                  </div>
                ) : (
                  <div className="space-y-1">
                    <div className="text-xs text-white animate-pulse">● {language === 'hi' ? 'IVR वॉइस संदेश:' : 'IVR Spoken Response:'}</div>
                    <div className="text-[11px] text-emerald-200 line-clamp-3 leading-snug">
                      "{spokenText}"
                    </div>
                  </div>
                )}
              </div>
              <div className="flex justify-between items-center text-[10px] text-emerald-400">
                <span>{isSpeaking ? (language === 'hi' ? '🔊 बोल रहा है...' : '🔊 Speaking...') : (language === 'hi' ? '🔇 शांत' : '🔇 Ready')}</span>
                <span>{language === 'hi' ? 'भाषा' : 'Language'}: {ivrLang.toUpperCase()}</span>
              </div>
            </div>

            {/* Call Control Buttons */}
            {ivrStep === 'idle' ? (
              <button
                onClick={handleDialHelpline}
                className="w-full py-3 bg-emerald-600 hover:bg-emerald-500 text-white rounded-2xl font-black text-xs shadow-lg flex items-center justify-center gap-2 transition"
              >
                <PhoneCall className="w-4 h-4" />
                <span>{language === 'hi' ? '1800-180-1551 पर कॉल करें' : 'Dial 1800-180-1551 (Call)'}</span>
              </button>
            ) : (
              <button
                onClick={handleEndCall}
                className="w-full py-3 bg-rose-600 hover:bg-rose-500 text-white rounded-2xl font-black text-xs shadow-lg flex items-center justify-center gap-2 transition"
              >
                <VolumeX className="w-4 h-4" />
                <span>{language === 'hi' ? 'कॉल समाप्त करें (काटें)' : 'End Call (Hang Up)'}</span>
              </button>
            )}

            {/* DTMF Keypad Grid */}
            <div className="grid grid-cols-3 gap-2 pt-2">
              {['1', '2', '3', '4', '5', '6', '7', '8', '9', '*', '0', '#'].map((key) => (
                <button
                  key={key}
                  disabled={ivrStep === 'idle'}
                  onClick={() => handleKeypadPress(key)}
                  className="py-3 rounded-xl bg-stone-800 hover:bg-stone-700 disabled:opacity-40 disabled:hover:bg-stone-800 text-white font-black text-base shadow active:scale-95 transition flex flex-col items-center justify-center"
                >
                  <span>{key}</span>
                  <span className="text-[8px] text-stone-400 font-normal">
                    {key === '1' && (language === 'hi' ? 'हिं/टमाटर' : 'HI/TOM')}
                    {key === '2' && (language === 'hi' ? 'EN/आलू' : 'EN/POT')}
                    {key === '3' && (language === 'hi' ? 'धान' : 'RICE')}
                    {key === '4' && (language === 'hi' ? 'गेहूं' : 'WHEAT')}
                  </span>
                </button>
              ))}
            </div>
          </div>

          {/* Transcript Log & Flow Description */}
          <div className="bg-white rounded-3xl border border-stone-200 p-6 shadow-sm space-y-4">
            <div className="space-y-1">
              <h3 className="text-sm font-black text-stone-900 uppercase">
                {language === 'hi' ? 'IVR हेल्पलाइन कॉल वार्तालाप' : 'IVR Helpline Call Transcript'}
              </h3>
              <p className="text-xs text-stone-500">{t('ivr_desc')}</p>
            </div>

            <div className="p-4 rounded-2xl bg-stone-50 border border-stone-200 min-h-[220px] max-h-[280px] overflow-y-auto space-y-2.5 text-xs">
              {callLog.length === 0 ? (
                <div className="text-stone-400 text-center py-12">
                  {language === 'hi' ? 'कॉल शुरू करने के लिए कीपैड पर "कॉल करें" दबाएं।' : 'Press "Dial 1800-180-1551" on the keypad to begin interactive voice call.'}
                </div>
              ) : (
                callLog.map((log, idx) => (
                  <div key={idx}>
                    {log.prompt && (
                      <div className="p-2.5 rounded-xl bg-emerald-50 text-emerald-950 border border-emerald-200">
                        <span className="font-bold text-[10px] uppercase text-emerald-700 block">
                          📞 {language === 'hi' ? 'IVR स्वचालित आवाज़:' : 'IVR Automated Voice:'}
                        </span>
                        {log.prompt}
                      </div>
                    )}
                    {log.user && (
                      <div className="text-right py-1 text-stone-600 font-mono text-xs">
                        {language === 'hi' ? 'किसान द्वारा दबाया गया बटन:' : 'Farmer Pressed Key:'} <span className="font-black text-stone-900 bg-stone-200 px-2 py-0.5 rounded">[{log.user}]</span>
                      </div>
                    )}
                  </div>
                ))
              )}
            </div>

            <div className="text-[11px] text-stone-500 bg-stone-100 p-3 rounded-xl">
              💡 <strong>{language === 'hi' ? 'सुलभ तकनीक' : 'Accessible Engineering'}</strong>: {language === 'hi'
                ? 'मानक DTMF ऑडियो आवृत्तियों द्वारा बिना स्मार्टफोन वाले कीपैड फोन से भी पूरी कृषि सलाह सुलभ।'
                : 'Integrates with Asterisk / FreeSWITCH / Exotel telecom gateways using standard DTMF audio frequencies.'}
            </div>
          </div>
        </div>
      ) : (
        /* SMS SHORT-CODE SIMULATOR */
        <div className="max-w-xl mx-auto bg-white rounded-3xl border border-stone-200 p-6 shadow-sm space-y-4">
          <div className="space-y-1">
            <h3 className="text-sm font-black text-stone-900 uppercase">
              {language === 'hi' ? 'शॉर्ट-कोड SMS सलाह (51969)' : 'Short-Code SMS Guidance (51969)'}
            </h3>
            <p className="text-xs text-stone-500">{t('sms_desc')}</p>
          </div>

          {/* Message Thread */}
          <div className="p-4 rounded-2xl bg-stone-100 min-h-[280px] max-h-[340px] overflow-y-auto space-y-3">
            {smsConversation.map((msg, idx) => (
              <div
                key={idx}
                className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[85%] p-3 rounded-2xl text-xs leading-relaxed ${
                    msg.sender === 'user'
                      ? 'bg-emerald-700 text-white rounded-br-none'
                      : 'bg-white text-stone-900 border border-stone-200 rounded-bl-none shadow-sm font-mono'
                  }`}
                >
                  {msg.text}
                </div>
              </div>
            ))}
          </div>

          {/* SMS Input Form */}
          <form onSubmit={handleSendSMS} className="flex gap-2">
            <input
              type="text"
              value={smsQuery}
              onChange={(e) => setSmsQuery(e.target.value)}
              placeholder={language === 'hi' ? 'उदा. टमाटर धब्बे या धान झोंका' : 'e.g. TOMATO LEAF SPOTS or धान झोंका'}
              className="flex-1 p-3 rounded-xl border border-stone-300 text-xs focus:ring-2 focus:ring-emerald-500 focus:outline-none"
            />
            <button
              type="submit"
              disabled={isSendingSMS}
              className="px-5 py-3 bg-emerald-700 hover:bg-emerald-800 disabled:bg-stone-300 text-white rounded-xl font-bold text-xs shadow flex items-center gap-1.5 transition"
            >
              <Send className="w-3.5 h-3.5" />
              <span>{language === 'hi' ? 'भेजें' : 'Send'}</span>
            </button>
          </form>

          {/* Quick Click Query Chips */}
          <div className="pt-1 flex flex-wrap gap-1.5 text-[11px]">
            <span className="text-stone-400 self-center">{language === 'hi' ? 'उदाहरण:' : 'Try:'}</span>
            {(language === 'hi'
              ? ['टमाटर धब्बे', 'आलू झुलसा', 'धान झोंका', 'टमाटर मरोड़', 'गेहूं रतुआ']
              : ['TOMATO LEAF SPOTS', 'POTATO BLIGHT', 'RICE BLAST', 'TOMATO CURL', 'WHEAT RUST']
            ).map((chip) => (
              <button
                key={chip}
                type="button"
                onClick={() => setSmsQuery(chip)}
                className="px-2.5 py-1 rounded-lg bg-stone-100 hover:bg-stone-200 text-stone-700 font-mono text-[10px]"
              >
                {chip}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
