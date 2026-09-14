import React, { useState, useRef, useEffect } from 'react';
import { Camera, Upload, RefreshCw, CheckCircle2, Sparkles, X, SwitchCamera } from 'lucide-react';
import { useLanguage } from '../contexts/LanguageContext';

export function CameraCapture({ onImageSelected, selectedImage, selectedSampleName }) {
  const { t, language } = useLanguage();
  const [isCameraActive, setIsCameraActive] = useState(false);
  const [cameraError, setCameraError] = useState(null);
  const [facingMode, setFacingMode] = useState('environment'); // 'environment' or 'user'
  const videoRef = useRef(null);
  const streamRef = useRef(null);
  const fileInputRef = useRef(null);

  const sampleLeaves = [
    {
      name: 'sample_tomato_blight.jpg',
      labelEn: 'Tomato Blight (Demo)',
      labelHi: 'टमाटर झुलसा (डेमो)',
      cropEn: 'Tomato',
      cropHi: 'टमाटर',
      crop: 'Tomato',
      severity: 'Medium'
    },
    {
      name: 'sample_potato_blight.jpg',
      labelEn: 'Potato Early Blight',
      labelHi: 'आलू अगेती झुलसा',
      cropEn: 'Potato',
      cropHi: 'आलू',
      crop: 'Potato',
      severity: 'Medium'
    },
    {
      name: 'sample_rice_blast.jpg',
      labelEn: 'Rice Blast',
      labelHi: 'धान का झोंका',
      cropEn: 'Rice',
      cropHi: 'धान',
      crop: 'Rice',
      severity: 'High'
    },
    {
      name: 'sample_apple_scab.jpg',
      labelEn: 'Apple Scab',
      labelHi: 'सेब का पपड़ी रोग',
      cropEn: 'Apple',
      cropHi: 'सेब',
      crop: 'Apple',
      severity: 'Medium'
    },
    {
      name: 'sample_corn_spot.jpg',
      labelEn: 'Corn Leaf Spot',
      labelHi: 'मक्के का पत्ती झुलसा',
      cropEn: 'Corn',
      cropHi: 'मक्का',
      crop: 'Corn',
      severity: 'Medium'
    },
    {
      name: 'sample_tomato_healthy.jpg',
      labelEn: 'Tomato Healthy',
      labelHi: 'स्वस्थ टमाटर',
      cropEn: 'Tomato',
      cropHi: 'टमाटर',
      crop: 'Tomato',
      severity: 'Low'
    },
    {
      name: 'sample_unclear_leaf.jpg',
      labelEn: 'Blurry Leaf (Low Conf)',
      labelHi: 'अस्पष्ट पत्ती (कम विश्वास)',
      cropEn: 'Tomato',
      cropHi: 'टमाटर',
      crop: 'Tomato',
      severity: 'Uncertain'
    }
  ];

  // Stop camera when unmounting
  useEffect(() => {
    return () => {
      stopCamera();
    };
  }, []);

  // When camera becomes active and video element is mounted in DOM, attach media stream
  useEffect(() => {
    if (isCameraActive && videoRef.current && streamRef.current) {
      videoRef.current.srcObject = streamRef.current;
      videoRef.current.play().catch((err) => {
        console.warn('Video autoPlay prevented:', err);
      });
    }
  }, [isCameraActive]);

  const startCamera = async (mode = facingMode) => {
    setCameraError(null);
    stopCamera();

    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      setCameraError(t('camera_not_supported'));
      return;
    }

    try {
      const constraints = {
        video: {
          facingMode: { ideal: mode },
          width: { ideal: 1280 },
          height: { ideal: 720 }
        },
        audio: false
      };
      const stream = await navigator.mediaDevices.getUserMedia(constraints);
      streamRef.current = stream;
      setIsCameraActive(true);

      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        videoRef.current.play().catch(console.warn);
      }
    } catch (err) {
      console.warn('Primary camera constraints failed, attempting fallback { video: true }:', err);
      try {
        const fallbackStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
        streamRef.current = fallbackStream;
        setIsCameraActive(true);
        if (videoRef.current) {
          videoRef.current.srcObject = fallbackStream;
          videoRef.current.play().catch(console.warn);
        }
      } catch (fallbackErr) {
        console.error('Camera access failed completely:', fallbackErr);
        if (fallbackErr.name === 'NotAllowedError' || fallbackErr.name === 'PermissionDeniedError') {
          setCameraError(t('camera_permission_denied'));
        } else if (fallbackErr.name === 'NotFoundError' || fallbackErr.name === 'DevicesNotFoundError') {
          setCameraError(t('camera_not_found'));
        } else {
          setCameraError(t('camera_error_msg'));
        }
        setIsCameraActive(false);
      }
    }
  };

  const stopCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    }
    setIsCameraActive(false);
  };

  const toggleCameraFacing = async () => {
    const newMode = facingMode === 'environment' ? 'user' : 'environment';
    setFacingMode(newMode);
    await startCamera(newMode);
  };

  const capturePhoto = () => {
    if (!videoRef.current) return;
    const video = videoRef.current;
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth || 640;
    canvas.height = video.videoHeight || 480;
    const ctx = canvas.getContext('2d');

    if (facingMode === 'user') {
      ctx.translate(canvas.width, 0);
      ctx.scale(-1, 1);
    }
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob((blob) => {
      if (blob) {
        const file = new File([blob], `cropcare_capture_${Date.now()}.jpg`, { type: 'image/jpeg' });
        const previewUrl = URL.createObjectURL(blob);
        onImageSelected({ file, previewUrl, sampleName: null, cropHint: null });
        stopCamera();
      }
    }, 'image/jpeg', 0.92);
  };

  const handleFileChange = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      const previewUrl = URL.createObjectURL(file);
      onImageSelected({ file, previewUrl, sampleName: null, cropHint: null });
    }
  };

  const handleSelectSample = (sample) => {
    stopCamera();
    onImageSelected({
      file: null,
      previewUrl: `/sample_leaves/${sample.name}`,
      sampleName: sample.name,
      cropHint: sample.crop
    });
  };

  const clearSelection = () => {
    stopCamera();
    onImageSelected({ file: null, previewUrl: null, sampleName: null, cropHint: null });
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  return (
    <div className="space-y-4">
      {/* Active Preview */}
      {selectedImage ? (
        <div className="relative rounded-2xl overflow-hidden border-2 border-emerald-500 bg-stone-900 shadow-md">
          <img
            src={selectedImage}
            alt="Selected leaf scan"
            className="w-full h-64 object-cover object-center"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-transparent to-black/20 flex flex-col justify-between p-4">
            <div className="flex justify-between items-center">
              <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-emerald-500 text-white shadow">
                <CheckCircle2 className="w-3.5 h-3.5" />
                <span>{t('image_ready')}</span>
              </span>
              <button
                type="button"
                onClick={clearSelection}
                className="p-1.5 rounded-full bg-black/60 text-white hover:bg-rose-600 transition"
                title={t('remove_photo')}
              >
                <X className="w-4 h-4" />
              </button>
            </div>
            <div className="text-white text-xs font-medium">
              {selectedSampleName
                ? `${t('sample_test_leaf_label')}: ${selectedSampleName}`
                : t('custom_uploaded_photo_label')}
            </div>
          </div>
        </div>
      ) : isCameraActive ? (
        /* Live Camera Viewfinder */
        <div className="relative rounded-2xl overflow-hidden bg-black aspect-video flex items-center justify-center border-2 border-emerald-600 shadow-lg">
          <video
            ref={videoRef}
            autoPlay
            playsInline
            muted
            className={`w-full h-full object-cover ${facingMode === 'user' ? '-scale-x-100' : ''}`}
          />
          {/* Target Reticle */}
          <div className="absolute inset-8 border-2 border-dashed border-emerald-400/70 rounded-xl pointer-events-none flex items-center justify-center">
            <span className="text-[11px] text-white bg-black/70 px-3 py-1 rounded-full shadow">
              {t('reticle_instruction')}
            </span>
          </div>

          {/* Controls Bar */}
          <div className="absolute bottom-4 inset-x-0 flex justify-center items-center gap-4 z-10 px-4">
            <button
              type="button"
              onClick={stopCamera}
              className="px-4 py-2 text-xs font-bold text-white bg-stone-800/90 rounded-xl hover:bg-stone-900 shadow transition"
            >
              {t('camera_cancel')}
            </button>

            {/* Shutter Button */}
            <button
              type="button"
              onClick={capturePhoto}
              title={t('take_photo')}
              className="w-16 h-16 rounded-full bg-white border-4 border-emerald-500 shadow-xl flex items-center justify-center hover:scale-105 active:scale-95 transition"
            >
              <div className="w-11 h-11 rounded-full bg-emerald-600"></div>
            </button>

            {/* Flip Camera Button */}
            <button
              type="button"
              onClick={toggleCameraFacing}
              title={t('flip_camera')}
              className="p-2.5 rounded-xl bg-stone-800/90 text-white hover:bg-stone-900 shadow transition flex items-center gap-1 text-xs font-semibold"
            >
              <SwitchCamera className="w-4 h-4 text-emerald-400" />
            </button>
          </div>
        </div>
      ) : (
        /* Action Options */
        <div className="space-y-3">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {/* Camera Button */}
            <button
              type="button"
              onClick={() => startCamera(facingMode)}
              className="flex items-center justify-center gap-3 p-4 rounded-xl border-2 border-dashed border-emerald-300 bg-emerald-50/50 hover:bg-emerald-50 text-emerald-800 font-bold text-sm transition group"
            >
              <div className="w-10 h-10 rounded-lg bg-emerald-600 text-white flex items-center justify-center shadow group-hover:scale-110 transition">
                <Camera className="w-5 h-5" />
              </div>
              <div className="text-left">
                <div>{t('camera_btn')}</div>
                <div className="text-[11px] text-stone-500 font-normal">{t('use_mobile_webcam')}</div>
              </div>
            </button>

            {/* File Upload Button */}
            <button
              type="button"
              onClick={() => fileInputRef.current?.click()}
              className="flex items-center justify-center gap-3 p-4 rounded-xl border-2 border-dashed border-stone-300 bg-stone-50 hover:bg-stone-100 text-stone-800 font-bold text-sm transition group"
            >
              <div className="w-10 h-10 rounded-lg bg-stone-700 text-white flex items-center justify-center shadow group-hover:scale-110 transition">
                <Upload className="w-5 h-5" />
              </div>
              <div className="text-left">
                <div>{t('upload_file_btn')}</div>
                <div className="text-[11px] text-stone-500 font-normal">{t('file_types_hint')}</div>
              </div>
            </button>
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              onChange={handleFileChange}
              className="hidden"
            />
          </div>

          {cameraError && (
            <div className="p-3 rounded-xl bg-amber-50 border border-amber-300 text-amber-900 text-xs flex items-center gap-2">
              <span className="font-bold">⚠️</span>
              <span>{cameraError}</span>
            </div>
          )}

          {/* Quick Demo Sample Picker */}
          <div className="pt-2 border-t border-stone-200">
            <div className="flex items-center gap-1.5 text-xs font-bold text-stone-700 mb-2">
              <Sparkles className="w-3.5 h-3.5 text-emerald-600" />
              <span>{t('sample_images_btn')}:</span>
            </div>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
              {sampleLeaves.map((sample) => {
                const label = language === 'hi' ? sample.labelHi : sample.labelEn;
                const cropName = language === 'hi' ? sample.cropHi : sample.cropEn;
                return (
                  <button
                    key={sample.name}
                    type="button"
                    onClick={() => handleSelectSample(sample)}
                    className="flex items-center gap-2 p-2 rounded-lg border border-stone-200 bg-white hover:border-emerald-500 hover:bg-emerald-50/40 text-left transition shadow-sm"
                  >
                    <img
                      src={`/sample_leaves/${sample.name}`}
                      alt={label}
                      className="w-8 h-8 rounded-md object-cover bg-stone-100 border border-stone-200 shrink-0"
                    />
                    <div className="overflow-hidden">
                      <div className="text-[11px] font-bold text-stone-800 truncate">{label}</div>
                      <div className="text-[10px] text-stone-500">{cropName}</div>
                    </div>
                  </button>
                );
              })}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
