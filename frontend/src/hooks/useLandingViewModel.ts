import { useState, useCallback } from "react";
import { CALCULATOR_SETTINGS } from "@/models/landing.model";

export const useLandingViewModel = () => {
  const [studyHours, setStudyHours] = useState(
    CALCULATOR_SETTINGS.defaultHours
  );
  const [features, setFeatures] = useState({
    flashcards: true,
    spaceRepetition: true,
    peerReview: true,
  });

  // Calculate saved hours based on study hours and enabled features
  const calculateSavedHours = useCallback(() => {
    const activeFeatures = Object.values(features).filter(Boolean).length;
    const featureMultiplier = activeFeatures / 3; // Normalize to 0-1
    const basePercentage = CALCULATOR_SETTINGS.savingsPercentage;
    const adjustedPercentage = basePercentage * featureMultiplier;
    return Math.round(studyHours * adjustedPercentage);
  }, [studyHours, features]);

  const savedHours = calculateSavedHours();

  const handleStudyHoursChange = useCallback((hours: number) => {
    setStudyHours(hours);
  }, []);

  const handleFeatureToggle = useCallback(
    (feature: keyof typeof features) => {
      setFeatures((prev) => ({
        ...prev,
        [feature]: !prev[feature],
      }));
    },
    []
  );

  return {
    // State
    studyHours,
    savedHours,
    features,

    // Actions
    handleStudyHoursChange,
    handleFeatureToggle,

    // Config
    calculatorSettings: CALCULATOR_SETTINGS,
  };
};
