import { Card } from "@/components/ui/card";

interface FeatureState {
  flashcards: boolean;
  spaceRepetition: boolean;
  peerReview: boolean;
}

interface CalculatorProps {
  studyHours: number;
  savedHours: number;
  features: FeatureState;
  calculatorSettings: {
    minHours: number;
    maxHours: number;
  };
  onStudyHoursChange: (hours: number) => void;
  onFeatureToggle: (feature: keyof FeatureState) => void;
}

export const Calculator = ({
  studyHours,
  savedHours,
  features,
  calculatorSettings,
  onStudyHoursChange,
  onFeatureToggle,
}: CalculatorProps) => {
  return (
    <section className="py-24">
      <div className="max-w-4xl mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold mb-4">
            Calculate your efficiency gains
          </h2>
          <p className="text-slate-500 dark:text-slate-400">
            See how much time you save with Compass AI
          </p>
        </div>
        <Card className="bg-white dark:bg-[#1A1A1A] border border-slate-200 dark:border-slate-800 rounded-2xl p-8 shadow-lg">
          <div className="grid md:grid-cols-2 gap-12">
            <div className="space-y-8">
              <div>
                <label className="block text-sm font-bold mb-4 flex justify-between">
                  <span>Monthly hours spent studying</span>
                  <span className="text-blue-600">{studyHours} hrs</span>
                </label>
                <input
                  type="range"
                  min={calculatorSettings.minHours}
                  max={calculatorSettings.maxHours}
                  value={studyHours}
                  onChange={(e) => onStudyHoursChange(Number(e.target.value))}
                  className="w-full h-2 bg-slate-200 dark:bg-slate-700 rounded-lg appearance-none cursor-pointer accent-slate-900 dark:accent-white"
                />
              </div>
              <div className="space-y-3">
                <label className="flex items-center gap-3">
                  <input
                    type="checkbox"
                    checked={features.flashcards}
                    onChange={() => onFeatureToggle("flashcards")}
                    className="rounded border-slate-300 text-slate-900 focus:ring-slate-900"
                  />
                  <span className="text-sm">AI Flashcard Generation</span>
                </label>
                <label className="flex items-center gap-3">
                  <input
                    type="checkbox"
                    checked={features.spaceRepetition}
                    onChange={() => onFeatureToggle("spaceRepetition")}
                    className="rounded border-slate-300 text-slate-900 focus:ring-slate-900"
                  />
                  <span className="text-sm">Spaced Repetition Scheduling</span>
                </label>
                <label className="flex items-center gap-3">
                  <input
                    type="checkbox"
                    checked={features.peerReview}
                    onChange={() => onFeatureToggle("peerReview")}
                    className="rounded border-slate-300 text-slate-900 focus:ring-slate-900"
                  />
                  <span className="text-sm">Collaborative Peer Review</span>
                </label>
              </div>
            </div>
            <div className="bg-slate-50 dark:bg-black/40 rounded-xl p-8 flex flex-col justify-center items-center text-center">
              <span className="text-sm font-bold text-slate-400 uppercase tracking-widest mb-2">
                Estimated time saved
              </span>
              <div className="text-6xl font-black text-slate-900 dark:text-white mb-2">
                {savedHours} hrs
              </div>
              <p className="text-slate-500 text-sm">per month, per learner</p>
              <hr className="w-full my-6 border-slate-200 dark:border-slate-800" />
              <div className="text-2xl font-bold text-green-600">
                30% faster mastery
              </div>
            </div>
          </div>
        </Card>
      </div>
    </section>
  );
};
