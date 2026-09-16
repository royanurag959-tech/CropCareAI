import React, { useState } from 'react';
import { LanguageProvider } from './contexts/LanguageContext';
import { AuthProvider } from './contexts/AuthContext';
import { OfflineProvider } from './contexts/OfflineContext';
import { Navbar } from './components/Navbar';
import { Footer } from './components/Footer';
import { UpgradeModal } from './components/UpgradeModal';

// Pages
import { Home } from './pages/Home';
import { DiseaseDetection } from './pages/DiseaseDetection';
import { DetectionResult } from './pages/DetectionResult';
import { DiseaseLibrary } from './pages/DiseaseLibrary';
import { FarmerDashboard } from './pages/FarmerDashboard';
import { AssistedDiagnosis } from './pages/AssistedDiagnosis';
import { TelecomSimulator } from './pages/TelecomSimulator';
import { ExpertHelp } from './pages/ExpertHelp';
import { B2BAnalytics } from './pages/B2BAnalytics';
import { AdminDashboard } from './pages/AdminDashboard';
import { PricingPlans } from './pages/PricingPlans';
import { AuthPage } from './pages/AuthPage';

export function MainLayout() {
  const [currentPage, setCurrentPage] = useState('home');
  const [selectedCrop, setSelectedCrop] = useState('Tomato');
  const [scanResult, setScanResult] = useState(null);
  const [upgradeModalOpen, setUpgradeModalOpen] = useState(false);
  const [selectedPlanForUpgrade, setSelectedPlanForUpgrade] = useState('plus');

  const handleScanComplete = (result) => {
    setScanResult(result);
    setCurrentPage('result');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleResetScan = () => {
    setScanResult(null);
    setCurrentPage('detect');
  };

  const handleRequestExpertFromScan = (result) => {
    setCurrentPage('expert');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleOpenUpgrade = (plan = 'plus') => {
    setSelectedPlanForUpgrade(plan);
    setUpgradeModalOpen(true);
  };

  return (
    <div className="min-h-screen flex flex-col bg-[#f8faf7]">
      <Navbar currentPage={currentPage} setCurrentPage={setCurrentPage} />

      <main className="flex-1 py-4 sm:py-6">
        {currentPage === 'home' && (
          <Home
            setCurrentPage={setCurrentPage}
            setSelectedCrop={setSelectedCrop}
          />
        )}

        {currentPage === 'detect' && (
          <DiseaseDetection
            selectedCrop={selectedCrop}
            setSelectedCrop={setSelectedCrop}
            onScanComplete={handleScanComplete}
          />
        )}

        {currentPage === 'result' && (
          <DetectionResult
            result={scanResult}
            onResetScan={handleResetScan}
            onRequestExpert={handleRequestExpertFromScan}
            onNavigateDashboard={() => setCurrentPage('dashboard')}
          />
        )}

        {currentPage === 'library' && <DiseaseLibrary />}

        {currentPage === 'dashboard' && (
          <FarmerDashboard
            onSelectScan={(scan) => {
              setScanResult(scan);
              setCurrentPage('result');
            }}
            onOpenUpgradeModal={handleOpenUpgrade}
          />
        )}

        {currentPage === 'assisted' && <AssistedDiagnosis />}

        {currentPage === 'telecom' && <TelecomSimulator />}

        {currentPage === 'expert' && <ExpertHelp initialScan={scanResult} />}

        {currentPage === 'b2b' && <B2BAnalytics />}

        {currentPage === 'admin' && <AdminDashboard />}

        {currentPage === 'pricing' && (
          <PricingPlans onOpenUpgradeModal={handleOpenUpgrade} />
        )}

        {currentPage === 'auth' && (
          <AuthPage onAuthSuccess={() => setCurrentPage('dashboard')} />
        )}
      </main>

      <Footer setCurrentPage={setCurrentPage} />

      <UpgradeModal
        isOpen={upgradeModalOpen}
        onClose={() => setUpgradeModalOpen(false)}
        selectedPlan={selectedPlanForUpgrade}
        onUpgradeSuccess={() => setUpgradeModalOpen(false)}
      />
    </div>
  );
}

export default function App() {
  return (
    <LanguageProvider>
      <AuthProvider>
        <OfflineProvider>
          <MainLayout />
        </OfflineProvider>
      </AuthProvider>
    </LanguageProvider>
  );
}
