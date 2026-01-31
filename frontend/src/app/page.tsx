"use client";

import { useLandingViewModel } from "@/hooks/useLandingViewModel";
import {
  Navigation,
  HeroSection,
  FeatureCards,
  ThreePillars,
  Calculator,
  TrustSection,
  CTASection,
  Footer,
} from "@/components/landing";

export default function Home() {
  // ViewModel
  const {
    studyHours,
    savedHours,
    features,
    handleStudyHoursChange,
    handleFeatureToggle,
    calculatorSettings,
  } = useLandingViewModel();

  // View
  return (
    <div className="min-h-screen bg-white dark:bg-[#0A0A0A] text-slate-900 dark:text-slate-100 transition-colors">
      <Navigation />
      <HeroSection />
      <FeatureCards />
      <ThreePillars />
      <Calculator
        studyHours={studyHours}
        savedHours={savedHours}
        features={features}
        calculatorSettings={calculatorSettings}
        onStudyHoursChange={handleStudyHoursChange}
        onFeatureToggle={handleFeatureToggle}
      />
      <TrustSection />
      <CTASection />
      <Footer />
    </div>
  );
}

