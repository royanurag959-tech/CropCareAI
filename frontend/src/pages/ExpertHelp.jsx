import React, { useState, useEffect } from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import { useAuth } from '../contexts/AuthContext';
import { api } from '../services/api';
import { SeverityBadge } from '../components/SeverityBadge';
import { Headphones, ShieldCheck, CheckCircle2, User, Phone, Calendar, ArrowRight, Loader2 } from 'lucide-react';

export function ExpertHelp({ initialScan }) {
  const { t } = useLanguage();
  const { user } = useAuth();
  const [requests, setRequests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [farmerNotes, setFarmerNotes] = useState('');
  const [farmerPhone, setFarmerPhone] = useState(user?.phone || '9876543210');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [successMsg, setSuccessMsg] = useState(null);

  useEffect(() => {
    loadRequests();
  }, []);

  const loadRequests = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/expert/requests');
      if (res.ok) {
        const data = await res.json();
        setRequests(data || []);
      }
    } catch (e) {
      console.warn('Failed to load expert requests:', e);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateRequest = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    try {
      const res = await api.requestExpert({
        scan_id: initialScan?.scan_id || null,
        farmer_phone: farmerPhone,
        farmer_notes: farmerNotes || 'Farmer requested review on crop foliage spotting.'
      });
      setSuccessMsg(res.message);
      setFarmerNotes('');
      loadRequests();
    } catch (err) {
      alert('Request error: ' + err.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-6 space-y-6">
      {/* Header */}
      <div className="space-y-1 text-center sm:text-left">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-amber-100 text-amber-900 border border-amber-300">
          <Headphones className="w-3.5 h-3.5" />
          <span>Agronomist Consultation Network</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-black text-stone-900 tracking-tight">
          {t('talk_expert_cta')}
        </h1>
        <p className="text-xs sm:text-sm text-stone-600">
          When AI confidence is low or disease severity is elevated, request a 1-on-1 certified agricultural specialist review.
        </p>
      </div>

      {/* Revenue Sharing Banner */}
      <div className="p-4 rounded-2xl bg-stone-100 border border-stone-200 text-xs text-stone-700 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div className="space-y-0.5">
          <span className="font-bold text-stone-900">Fair Expert Revenue Sharing Model:</span>
          <p className="text-[11px] text-stone-500">
            Farmer pays ₹99 consultation fee → Expert receives 80% (₹79.20) • Platform fee: 20% (₹19.80).
          </p>
        </div>
        <span className="font-black text-emerald-800 text-sm shrink-0">₹99 / Consultation</span>
      </div>

      {/* Request Consultation Form */}
      <form onSubmit={handleCreateRequest} className="bg-white rounded-3xl border border-stone-200 p-6 shadow-sm space-y-4">
        <h3 className="text-sm font-black text-stone-900 uppercase">Book an Agronomist Consultation</h3>

        {successMsg && (
          <div className="p-3 bg-emerald-50 border border-emerald-200 text-emerald-900 rounded-xl text-xs flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
            <span>{successMsg}</span>
          </div>
        )}

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-bold text-stone-700 mb-1">Your Mobile Phone:</label>
            <input
              type="tel"
              required
              value={farmerPhone}
              onChange={(e) => setFarmerPhone(e.target.value)}
              className="w-full p-2.5 rounded-xl border border-stone-300 text-xs focus:ring-2 focus:ring-emerald-500 focus:outline-none"
            />
          </div>

          <div>
            <label className="block text-xs font-bold text-stone-700 mb-1">Attached Scan:</label>
            <input
              type="text"
              readOnly
              value={initialScan ? `${initialScan.crop} - ${initialScan.predicted_disease} (#${initialScan.scan_id})` : 'Latest active scan'}
              className="w-full p-2.5 rounded-xl border border-stone-200 bg-stone-50 text-xs text-stone-600"
            />
          </div>
        </div>

        <div>
          <label className="block text-xs font-bold text-stone-700 mb-1">Observation Notes for the Agronomist:</label>
          <textarea
            rows="3"
            value={farmerNotes}
            onChange={(e) => setFarmerNotes(e.target.value)}
            placeholder="Describe field conditions, when you noticed the symptoms, or fertilizers applied..."
            className="w-full p-2.5 rounded-xl border border-stone-300 text-xs focus:ring-2 focus:ring-emerald-500 focus:outline-none"
          ></textarea>
        </div>

        <button
          type="submit"
          disabled={isSubmitting}
          className="w-full py-3.5 bg-emerald-700 hover:bg-emerald-800 disabled:bg-stone-300 text-white font-black text-xs rounded-xl shadow transition flex items-center justify-center gap-2"
        >
          {isSubmitting ? <Loader2 className="w-4 h-4 animate-spin" /> : <Headphones className="w-4 h-4" />}
          <span>Confirm Consultation Request (₹99 Mock Checkout)</span>
        </button>
      </form>

      {/* Existing Requests / Expert Triage Queue */}
      <div className="space-y-3">
        <h3 className="text-xs font-black text-stone-800 uppercase tracking-wide">
          Recent Consultation Cases & Agronomist Responses
        </h3>
        {loading ? (
          <div className="text-center py-6 text-stone-500 text-xs">Loading requests...</div>
        ) : requests.length === 0 ? (
          <div className="p-6 bg-white rounded-2xl border border-stone-200 text-center text-xs text-stone-500">
            No active consultation requests yet.
          </div>
        ) : (
          <div className="space-y-2.5">
            {requests.map((req) => (
              <div
                key={req.id}
                className="p-4 rounded-2xl bg-white border border-stone-200 shadow-sm space-y-2"
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-stone-900">
                    Case #{req.id} • {req.farmer_name} ({req.farmer_phone})
                  </span>
                  <span
                    className={`text-[10px] font-black px-2.5 py-0.5 rounded-full uppercase ${
                      req.status === 'resolved'
                        ? 'bg-emerald-100 text-emerald-800'
                        : 'bg-amber-100 text-amber-800'
                    }`}
                  >
                    {req.status}
                  </span>
                </div>
                <p className="text-xs text-stone-600">Farmer query: "{req.farmer_notes}"</p>
                {req.expert_notes && (
                  <div className="p-2.5 bg-emerald-50 rounded-xl border border-emerald-200 text-xs text-emerald-950">
                    <span className="font-bold block text-[10px] uppercase text-emerald-700">Agronomist Diagnosis & Guidance:</span>
                    {req.expert_notes}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
