import React, { useState } from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import { CameraCapture } from '../components/CameraCapture';
import { api } from '../services/api';
import { SeverityBadge } from '../components/SeverityBadge';
import { translateToSelectedLang } from '../services/i18n';
import { Users, CheckCircle, Printer, MessageSquare, Sparkles, AlertCircle, Loader2 } from 'lucide-react';

export function AssistedDiagnosis() {
  const { t, language } = useLanguage();
  const [farmerName, setFarmerName] = useState('');
  const [farmerPhone, setFarmerPhone] = useState('');
  const [village, setVillage] = useState('');
  const [crop, setCrop] = useState('Tomato');
  const [imageFile, setImageFile] = useState(null);
  const [selectedImage, setSelectedImage] = useState(null);
  const [sampleName, setSampleName] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [receiptResult, setReceiptResult] = useState(null);
  const [error, setError] = useState(null);

  const handleImageSelected = ({ file, previewUrl, sampleName: sName, cropHint }) => {
    setImageFile(file);
    setSelectedImage(previewUrl);
    setSampleName(sName);
    if (cropHint) setCrop(cropHint);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!farmerName || !farmerPhone) {
      setError(language === 'hi' ? 'कृपया किसान का पूरा नाम और मोबाइल नंबर दर्ज करें।' : 'Please provide the farmer’s full name and mobile number.');
      return;
    }
    if (!selectedImage && !sampleName) {
      setError(language === 'hi' ? 'कृपया किसान की फसल की फोटो लें या अपलोड करें।' : 'Please take or upload a crop photo for the farmer.');
      return;
    }

    setIsSubmitting(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('farmer_name', farmerName);
      formData.append('farmer_phone', farmerPhone);
      formData.append('village', village || (language === 'hi' ? 'होशंगाबाद' : 'Hoshangabad'));
      formData.append('crop', crop);
      if (imageFile) formData.append('image', imageFile);
      if (sampleName) formData.append('image_sample_name', sampleName);

      const res = await api.assistedDiagnose(formData);
      setReceiptResult(res);
    } catch (err) {
      setError(err.message || (language === 'hi' ? 'सहायक निदान विफल रहा।' : 'Assisted diagnosis failed.'));
    } finally {
      setIsSubmitting(false);
    }
  };

  const handlePrintReceipt = () => {
    window.print();
  };

  const resetForm = () => {
    setReceiptResult(null);
    setFarmerName('');
    setFarmerPhone('');
    setVillage('');
    setSelectedImage(null);
    setImageFile(null);
    setSampleName(null);
  };

  const cropKey = `crop_${crop.toLowerCase()}`;
  const displayCrop = t(cropKey) !== cropKey ? t(cropKey) : crop;

  return (
    <div className="max-w-4xl mx-auto px-4 py-6 space-y-6">
      {/* Header */}
      <div className="space-y-1 text-center sm:text-left">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-sky-100 text-sky-800 border border-sky-300">
          <Users className="w-3.5 h-3.5" />
          <span>{language === 'hi' ? 'ग्रामीण विस्तार सेवा व CSC ऑपरेटर पोर्टल' : 'Village Extension & CSC Operator Portal'}</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-black text-stone-900 tracking-tight">
          {t('assisted_title')}
        </h1>
        <p className="text-xs sm:text-sm text-stone-600">
          {t('assisted_sub')}
        </p>
      </div>

      {receiptResult ? (
        /* Generated Farmer Receipt Screen */
        <div className="bg-white rounded-3xl border-2 border-emerald-500 p-6 shadow-xl space-y-6 animate-in fade-in">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-stone-200 pb-4">
            <div>
              <span className="text-xs font-bold text-emerald-700 uppercase tracking-wide">
                {t('official_receipt')}
              </span>
              <h2 className="text-xl font-black text-stone-900">
                🌱 {t('farmer_receipt_title')} #{receiptResult.scan_id}
              </h2>
            </div>
            <div className="flex items-center gap-2">
              <button
                onClick={handlePrintReceipt}
                className="inline-flex items-center gap-1.5 px-4 py-2 bg-emerald-700 text-white rounded-xl text-xs font-bold hover:bg-emerald-800 shadow"
              >
                <Printer className="w-4 h-4" />
                <span>{t('print_receipt')}</span>
              </button>
              <button
                onClick={resetForm}
                className="px-4 py-2 bg-stone-100 text-stone-700 rounded-xl text-xs font-bold hover:bg-stone-200"
              >
                {t('new_assisted_scan')}
              </button>
            </div>
          </div>

          {/* Farmer Particulars */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 p-4 rounded-2xl bg-stone-50 border border-stone-200 text-xs">
            <div>
              <span className="text-stone-500 block text-[10px] uppercase font-bold">{t('farmer_name_label')}:</span>
              <span className="font-extrabold text-stone-900">{receiptResult.farmer_name}</span>
            </div>
            <div>
              <span className="text-stone-500 block text-[10px] uppercase font-bold">{t('farmer_phone_label')}:</span>
              <span className="font-extrabold text-stone-900">{receiptResult.farmer_phone}</span>
            </div>
            <div>
              <span className="text-stone-500 block text-[10px] uppercase font-bold">{t('village_label')}:</span>
              <span className="font-extrabold text-stone-900">{receiptResult.village}</span>
            </div>
            <div>
              <span className="text-stone-500 block text-[10px] uppercase font-bold">{language === 'hi' ? 'फसल:' : 'Crop:'}</span>
              <span className="font-extrabold text-emerald-800">
                {language === 'hi' ? (t(`crop_${receiptResult.crop?.toLowerCase()}`) || receiptResult.crop) : receiptResult.crop}
              </span>
            </div>
          </div>

          {/* Diagnosis Result */}
          <div className="p-4 rounded-2xl bg-emerald-50 border border-emerald-200 space-y-2">
            <div className="flex items-center justify-between">
              <div className="text-base font-black text-emerald-950">
                {language === 'hi' ? 'पहचान:' : 'Detected:'} {language === 'hi' && receiptResult.hindi_name ? receiptResult.hindi_name : receiptResult.predicted_disease}
              </div>
              <SeverityBadge severity={receiptResult.severity} />
            </div>
            <div className="text-xs text-stone-700 font-medium">
              {language === 'hi' ? 'सटीकता:' : 'Confidence:'} <span className="font-bold">{receiptResult.confidence_percentage}%</span> • {language === 'hi' ? 'कारण:' : 'Why:'} {language === 'hi' ? (receiptResult.why_did_it_happen?.primary_summary_hi || receiptResult.why_did_it_happen?.primary_summary) : receiptResult.why_did_it_happen?.primary_summary}
            </div>
          </div>

          {/* Immediate Steps to explain to farmer */}
          <div className="space-y-2">
            <h4 className="text-xs font-black uppercase text-stone-900">
              {language === 'hi' ? 'किसान को समझाने हेतु तुरंत किए जाने वाले कदम:' : 'Steps for Krishi Mitra to Explain to Farmer:'}
            </h4>
            <ul className="space-y-1.5 text-xs text-stone-700">
              {receiptResult.immediate_actions?.map((act, idx) => (
                <li key={idx} className="flex items-start gap-2 p-2 bg-stone-50 rounded-lg">
                  <CheckCircle className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                  <span>{translateToSelectedLang(act, language)}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Raw SMS Text */}
          <div className="p-3 bg-stone-900 text-stone-200 rounded-xl text-xs font-mono space-y-1">
            <div className="flex items-center gap-1.5 text-amber-400 font-bold text-[11px]">
              <MessageSquare className="w-3.5 h-3.5" />
              <span>
                {language === 'hi' ? `SMS प्रेषण पूर्वावलोकन (${receiptResult.farmer_phone} पर भेजा गया):` : `SMS Dispatch Preview (Sent to ${receiptResult.farmer_phone}):`}
              </span>
            </div>
            <pre className="whitespace-pre-wrap text-[11px] leading-relaxed">{receiptResult.sms_receipt}</pre>
          </div>
        </div>
      ) : (
        /* Form for Worker */
        <form onSubmit={handleSubmit} className="bg-white rounded-3xl border border-stone-200 p-6 shadow-sm space-y-6">
          {error && (
            <div className="p-3 rounded-xl bg-rose-50 border border-rose-200 text-rose-800 text-xs flex items-center gap-2">
              <AlertCircle className="w-4 h-4 shrink-0" />
              <span>{error}</span>
            </div>
          )}

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div>
              <label className="block text-xs font-bold text-stone-700 mb-1">{t('farmer_name_label')} *</label>
              <input
                type="text"
                required
                value={farmerName}
                onChange={(e) => setFarmerName(e.target.value)}
                placeholder={language === 'hi' ? 'उदा. बाबूलाल पटेल' : 'e.g. Babu Lal Patel'}
                className="w-full p-2.5 rounded-xl border border-stone-300 text-xs focus:ring-2 focus:ring-sky-500 focus:outline-none"
              />
            </div>
            <div>
              <label className="block text-xs font-bold text-stone-700 mb-1">{t('farmer_phone_label')} *</label>
              <input
                type="tel"
                required
                value={farmerPhone}
                onChange={(e) => setFarmerPhone(e.target.value)}
                placeholder="e.g. 9812345678"
                className="w-full p-2.5 rounded-xl border border-stone-300 text-xs focus:ring-2 focus:ring-sky-500 focus:outline-none"
              />
            </div>
            <div>
              <label className="block text-xs font-bold text-stone-700 mb-1">{t('village_label')}</label>
              <input
                type="text"
                value={village}
                onChange={(e) => setVillage(e.target.value)}
                placeholder={language === 'hi' ? 'उदा. होशंगाबाद' : 'e.g. Hoshangabad'}
                className="w-full p-2.5 rounded-xl border border-stone-300 text-xs focus:ring-2 focus:ring-sky-500 focus:outline-none"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-bold text-stone-700 mb-1">{t('select_crop')}</label>
            <select
              value={crop}
              onChange={(e) => setCrop(e.target.value)}
              className="w-full p-2.5 rounded-xl border border-stone-300 text-xs bg-white focus:ring-2 focus:ring-sky-500 focus:outline-none"
            >
              <option value="Tomato">{language === 'hi' ? 'टमाटर' : 'Tomato'}</option>
              <option value="Potato">{language === 'hi' ? 'आलू' : 'Potato'}</option>
              <option value="Rice">{language === 'hi' ? 'धान' : 'Rice'}</option>
              <option value="Apple">{language === 'hi' ? 'सेब' : 'Apple'}</option>
              <option value="Corn">{language === 'hi' ? 'मक्का' : 'Corn'}</option>
              <option value="Wheat">{language === 'hi' ? 'गेहूं' : 'Wheat'}</option>
              <option value="Cotton">{language === 'hi' ? 'कपास' : 'Cotton'}</option>
            </select>
          </div>

          {/* Photo Capture */}
          <div>
            <label className="block text-xs font-bold text-stone-700 mb-2">
              {language === 'hi' ? 'किसान की फसल पत्ती की फोटो लें' : "Capture Farmer's Crop Photo"}
            </label>
            <CameraCapture
              onImageSelected={handleImageSelected}
              selectedImage={selectedImage}
              selectedSampleName={sampleName}
            />
          </div>

          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full py-3.5 bg-sky-700 hover:bg-sky-800 disabled:bg-stone-300 text-white font-black text-sm rounded-xl shadow-md transition flex items-center justify-center gap-2"
          >
            {isSubmitting ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                <span>{language === 'hi' ? 'कृषि मित्र द्वारा फसल जांच चल रही है...' : 'Running Krishi Mitra Diagnostic...'}</span>
              </>
            ) : (
              <>
                <Sparkles className="w-4 h-4" />
                <span>{t('print_sms_receipt_btn')}</span>
              </>
            )}
          </button>
        </form>
      )}
    </div>
  );
}
