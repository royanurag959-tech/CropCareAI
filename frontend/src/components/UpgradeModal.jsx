import React, { useState } from 'react';
import { X, Check, Zap, ShieldCheck, CreditCard, Smartphone } from 'lucide-react';
import { api } from '../services/api';
import { useAuth } from '../contexts/AuthContext';

export function UpgradeModal({ isOpen, onClose, selectedPlan = 'plus', onUpgradeSuccess }) {
  const { user, refreshProfile } = useAuth();
  const [paymentMethod, setPaymentMethod] = useState('upi');
  const [upiId, setUpiId] = useState('farmer@oksbi');
  const [isProcessing, setIsProcessing] = useState(false);
  const [paymentResult, setPaymentResult] = useState(null);

  if (!isOpen) return null;

  const planPrice = selectedPlan === 'pro' ? 99 : 49;
  const planTitle = selectedPlan === 'pro' ? 'CropCare Pro' : 'CropCare Plus';

  const handlePay = async () => {
    setIsProcessing(true);
    try {
      const res = await api.upgradePlan(selectedPlan, paymentMethod === 'upi' ? `UPI: ${upiId}` : 'Mock Debit Card');
      setPaymentResult(res);
      await refreshProfile();
      if (onUpgradeSuccess) onUpgradeSuccess(res);
    } catch (err) {
      alert('Mock payment error: ' + err.message);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-in fade-in">
      <div className="bg-white rounded-3xl max-w-md w-full p-6 shadow-2xl border border-stone-200 relative">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 p-1.5 rounded-full text-stone-400 hover:text-stone-700 hover:bg-stone-100"
        >
          <X className="w-5 h-5" />
        </button>

        {paymentResult ? (
          /* Payment Success State */
          <div className="text-center py-6 space-y-4">
            <div className="w-16 h-16 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center mx-auto shadow-inner">
              <Check className="w-8 h-8" />
            </div>
            <div>
              <h3 className="text-lg font-black text-stone-900">Subscription Activated!</h3>
              <p className="text-xs text-stone-500 mt-1">{paymentResult.message}</p>
            </div>
            <div className="p-3 bg-stone-50 rounded-xl text-left text-xs space-y-1 font-mono text-stone-700 border border-stone-200">
              <div>Ref: <span className="font-bold">{paymentResult.transaction_reference}</span></div>
              <div>Plan: <span className="font-bold text-emerald-700 uppercase">{paymentResult.plan}</span></div>
              <div>Amount: <span className="font-bold">₹{paymentResult.amount_paid_inr}</span></div>
              <div>Status: <span className="text-emerald-600 font-bold">PAID (Active)</span></div>
            </div>
            <button
              onClick={() => {
                setPaymentResult(null);
                onClose();
              }}
              className="w-full py-3 bg-emerald-700 hover:bg-emerald-800 text-white rounded-xl font-bold text-xs shadow-md transition"
            >
              Back to App
            </button>
          </div>
        ) : (
          /* Payment Form */
          <div className="space-y-5">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 rounded-2xl bg-amber-100 text-amber-800 flex items-center justify-center font-black shadow-sm">
                <Zap className="w-6 h-6" />
              </div>
              <div>
                <h3 className="text-base font-black text-stone-900">Upgrade to {planTitle}</h3>
                <p className="text-xs text-stone-500">Instant monthly subscription activation</p>
              </div>
            </div>

            {/* Price Badge */}
            <div className="p-4 rounded-2xl bg-emerald-50 border border-emerald-200 flex items-baseline justify-between">
              <span className="text-xs font-bold text-emerald-900">Total Subscription Fee</span>
              <div>
                <span className="text-2xl font-black text-emerald-700">₹{planPrice}</span>
                <span className="text-xs text-stone-500"> / month</span>
              </div>
            </div>

            {/* Payment Method Selector */}
            <div className="space-y-2">
              <label className="block text-xs font-bold text-stone-700">Select Payment Method (Mock):</label>
              <div className="grid grid-cols-2 gap-2">
                <button
                  type="button"
                  onClick={() => setPaymentMethod('upi')}
                  className={`p-3 rounded-xl border flex items-center gap-2 text-xs font-bold transition ${
                    paymentMethod === 'upi'
                      ? 'border-emerald-600 bg-emerald-50 text-emerald-900'
                      : 'border-stone-200 hover:bg-stone-50 text-stone-600'
                  }`}
                >
                  <Smartphone className="w-4 h-4" />
                  <span>UPI / QR</span>
                </button>
                <button
                  type="button"
                  onClick={() => setPaymentMethod('card')}
                  className={`p-3 rounded-xl border flex items-center gap-2 text-xs font-bold transition ${
                    paymentMethod === 'card'
                      ? 'border-emerald-600 bg-emerald-50 text-emerald-900'
                      : 'border-stone-200 hover:bg-stone-50 text-stone-600'
                  }`}
                >
                  <CreditCard className="w-4 h-4" />
                  <span>Debit / Card</span>
                </button>
              </div>
            </div>

            {paymentMethod === 'upi' ? (
              <div>
                <label className="block text-[11px] font-semibold text-stone-600 mb-1">UPI ID or VPA:</label>
                <input
                  type="text"
                  value={upiId}
                  onChange={(e) => setUpiId(e.target.value)}
                  className="w-full p-2.5 rounded-xl border border-stone-300 text-xs focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                  placeholder="e.g. yourname@upi"
                />
              </div>
            ) : (
              <div className="p-3 bg-stone-50 rounded-xl border border-stone-200 text-xs text-stone-600">
                Mock Card Payment: Test card 4111 •••• •••• 1111 pre-filled for evaluation.
              </div>
            )}

            <div className="flex items-center gap-1.5 text-[11px] text-stone-500">
              <ShieldCheck className="w-4 h-4 text-emerald-600 shrink-0" />
              <span>Hackathon Safe Sandbox Mode — No real money is charged.</span>
            </div>

            <button
              type="button"
              disabled={isProcessing}
              onClick={handlePay}
              className="w-full py-3.5 bg-emerald-700 hover:bg-emerald-800 disabled:bg-stone-300 text-white rounded-xl font-black text-sm shadow-md transition"
            >
              {isProcessing ? 'Processing Mock Payment...' : `Confirm & Pay ₹${planPrice}`}
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
