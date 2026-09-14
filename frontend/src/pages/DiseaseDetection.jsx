import React, { useState } from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import { CameraCapture } from '../components/CameraCapture';
import { FollowUpQuestions } from '../components/FollowUpQuestions';
import { api } from '../services/api';
import { ScanLine, Sparkles, Loader2, AlertCircle } from 'lucide-react';

export function DiseaseDetection({ selectedCrop, setSelectedCrop, onScanComplete }) {
  const { t, language } = useLanguage();
  const [selectedImage, setSelectedImage] = useState(null);
  const [imageFile, setImageFile] = useState(null);
  const [sampleName, setSampleName] = useState(null);
  const [contextData, setContextData] = useState({
    growth_stage: 'Fruiting',
    rainfall: 'Moderate',
    irrigation: 'Every 2-3 days',
    duration: '4-7 days',
    affected_area: '10-30%'
  });
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisStep, setAnalysisStep] = useState(0);
  const [error, setError] = useState(null);

  const crops = [
    { id: 'Tomato', name: 'Tomato', hindi: 'टमाटर', icon: '🍅' },
    { id: 'Potato', name: 'Potato', hindi: 'आलू', icon: '🥔' },
    { id: 'Rice', name: 'Rice', hindi: 'धान', icon: '🌾' },
    { id: 'Apple', name: 'Apple', hindi: 'सेब', icon: '🍎' },
    { id: 'Corn', name: 'Corn', hindi: 'मक्का', icon: '🌽' },
    { id: 'Wheat', name: 'Wheat', hindi: 'गेहूं', icon: '🌾' },
    { id: 'Cotton', name: 'Cotton', hindi: 'कपास', icon: '☁️' },
  ];

  const handleImageSelected = ({ file, previewUrl, sampleName: sName, cropHint }) => {
    setImageFile(file);
    setSelectedImage(previewUrl);
    setSampleName(sName);
    setError(null);
    if (cropHint && setSelectedCrop) {
      setSelectedCrop(cropHint);
    }
  };

  const handleRunAnalysis = async () => {
    if (!selectedCrop) {
      setError(t('please_select_crop'));
      return;
    }
    if (!selectedImage && !sampleName) {
      setError(t('please_select_image'));
      return;
    }

    setIsAnalyzing(true);
    setError(null);
    setAnalysisStep(1);

    // Simulated progress steps for engaging UX
    const t1 = setTimeout(() => setAnalysisStep(2), 500);
    const t2 = setTimeout(() => setAnalysisStep(3), 1000);

    try {
      const formData = new FormData();
      formData.append('crop', selectedCrop);
      if (imageFile) {
        formData.append('image', imageFile);
      }
      if (sampleName) {
        formData.append('image_sample_name', sampleName);
      }
      formData.append('growth_stage', contextData.growth_stage);
      formData.append('rainfall', contextData.rainfall);
      formData.append('irrigation', contextData.irrigation);
      formData.append('duration', contextData.duration);
      formData.append('affected_area', contextData.affected_area);

      const result = await api.detectCropDisease(formData);
      clearTimeout(t1);
      clearTimeout(t2);
      onScanComplete(result);
    } catch (err) {
      clearTimeout(t1);
      clearTimeout(t2);
      setError(err.message || t('detection_failed'));
    } finally {
      setIsAnalyzing(false);
      setAnalysisStep(0);
    }
  };

  return (
    <div className="max-w-3xl mx-auto px-4 py-6 space-y-6">
      {/* Header */}
      <div className="space-y-1 text-center sm:text-left">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800 border border-emerald-300">
          <ScanLine className="w-3.5 h-3.5" />
          <span>{t('ai_diagnostic_station')}</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-black text-stone-900 tracking-tight">
          {t('title_detect')}
        </h1>
        <p className="text-xs sm:text-sm text-stone-600">
          {t('subtitle_detect')}
        </p>
      </div>

      {error && (
        <div className="p-4 rounded-2xl bg-rose-50 border border-rose-200 text-rose-800 text-xs flex items-center gap-2">
          <AlertCircle className="w-4 h-4 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Step 1: Crop Selection */}
      <div className="bg-white rounded-3xl border border-stone-200 p-5 shadow-sm space-y-3">
        <label className="block text-xs font-extrabold text-stone-900 uppercase tracking-wider">
          {t('select_crop')}
        </label>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
          {crops.map((c) => {
            const isSelected = selectedCrop === c.name;
            const displayName = language === 'hi' ? c.hindi : c.name;
            return (
              <button
                key={c.id}
                type="button"
                onClick={() => {
                  setSelectedCrop(c.name);
                  setError(null);
                }}
                className={`p-3 rounded-2xl border text-left transition flex items-center gap-2.5 ${
                  isSelected
                    ? 'border-emerald-600 bg-emerald-50 text-emerald-950 ring-2 ring-emerald-500 shadow-sm'
                    : 'border-stone-200 hover:border-stone-300 bg-stone-50/50 hover:bg-stone-50 text-stone-700'
                }`}
              >
                <span className="text-xl shrink-0">{c.icon}</span>
                <div>
                  <div className="text-xs font-bold leading-tight">{displayName}</div>
                </div>
              </button>
            );
          })}
        </div>
      </div>

      {/* Step 2: Camera / Upload */}
      <div className="bg-white rounded-3xl border border-stone-200 p-5 shadow-sm space-y-3">
        <label className="block text-xs font-extrabold text-stone-900 uppercase tracking-wider">
          {t('upload_photo')}
        </label>
        <CameraCapture
          onImageSelected={handleImageSelected}
          selectedImage={selectedImage}
          selectedSampleName={sampleName}
        />
      </div>

      {/* Step 3: Optional Field Context Form */}
      <FollowUpQuestions
        contextData={contextData}
        setContextData={setContextData}
      />

      {/* Step 4: Run Diagnosis Button */}
      <div className="pt-2">
        <button
          type="button"
          disabled={isAnalyzing}
          onClick={handleRunAnalysis}
          className="w-full py-4 rounded-2xl bg-emerald-700 hover:bg-emerald-800 disabled:bg-stone-300 text-white font-black text-sm sm:text-base shadow-xl hover:shadow-2xl transition hover:scale-[1.01] active:scale-[0.99] flex items-center justify-center gap-3 relative overflow-hidden"
        >
          {isAnalyzing ? (
            <div className="flex items-center gap-3">
              <Loader2 className="w-5 h-5 animate-spin" />
              <span>
                {analysisStep === 1 && t('extracting_features')}
                {analysisStep === 2 && t('comparing_pathogen')}
                {analysisStep === 3 && t('synthesizing_ai')}
                {analysisStep === 0 && t('analyzing_text')}
              </span>
            </div>
          ) : (
            <div className="flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-amber-300" />
              <span>{t('analyze_btn')}</span>
            </div>
          )}
        </button>
      </div>
    </div>
  );
}
