import { FileText, Sparkles, ArrowDown } from "lucide-react";
import { Card } from "@/components/ui/card";

export const FeatureCards = () => {
  return (
    <div className="max-w-6xl mx-auto mt-24 px-4">
      <Card className="bg-white dark:bg-[#1A1A1A] rounded-xl shadow-lg border border-slate-200 dark:border-slate-800 overflow-hidden">
        <div className="flex flex-col lg:flex-row min-h-[500px]">
          {/* Left: Smart Editor */}
          <div className="flex-1 p-8 border-b lg:border-b-0 lg:border-r border-slate-100 dark:border-slate-800">
            <div className="flex items-center gap-2 mb-6">
              <FileText className="w-5 h-5 text-slate-400" />
              <span className="font-semibold text-sm uppercase tracking-wider text-slate-400">
                Smart Editor
              </span>
            </div>
            <h3 className="text-2xl font-bold mb-4">
              Documentation built for learning.
            </h3>
            <p className="text-slate-600 dark:text-slate-400 mb-8">
              Write your notes, import PDFs, or sync from web pages. Our editor
              automatically identifies key concepts.
            </p>
            <div className="bg-slate-50 dark:bg-black/40 rounded-lg p-6 font-mono text-sm border border-slate-100 dark:border-slate-800">
              <div className="flex items-center gap-2 mb-4">
                <div className="w-3 h-3 rounded-full bg-red-400"></div>
                <div className="w-3 h-3 rounded-full bg-yellow-400"></div>
                <div className="w-3 h-3 rounded-full bg-green-400"></div>
              </div>
              <div className="space-y-2 opacity-80">
                <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-3/4"></div>
                <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-full"></div>
                <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-5/6"></div>
                <div className="h-8 bg-blue-100 dark:bg-blue-900/30 border-l-4 border-blue-500 rounded-sm w-full"></div>
                <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-2/3"></div>
              </div>
            </div>
          </div>

          {/* Right: AI Quiz Generator */}
          <div className="flex-1 p-8 bg-slate-50/50 dark:bg-slate-900/20">
            <div className="flex items-center gap-2 mb-6">
              <Sparkles className="w-5 h-5 text-blue-500" />
              <span className="font-semibold text-sm uppercase tracking-wider text-blue-500">
                AI Quiz Generator
              </span>
            </div>
            <h3 className="text-2xl font-bold mb-4">Instant mastery check.</h3>
            <p className="text-slate-600 dark:text-slate-400 mb-8">
              With one click, turn your documentation into dynamic quizzes and
              active recall flashcards.
            </p>
            <div className="space-y-4">
              <Card className="bg-white dark:bg-black p-4 border border-slate-200 dark:border-slate-800">
                <p className="text-sm font-medium mb-3">
                  Q: Explain the principle of Spaced Repetition.
                </p>
                <div className="grid grid-cols-1 gap-2">
                  <div className="p-3 border rounded-md text-xs border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800 cursor-pointer">
                    A) Cramming information into one session
                  </div>
                  <div className="p-3 border rounded-md text-xs bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-800 cursor-pointer">
                    B) Increasing intervals between review sessions
                  </div>
                </div>
              </Card>
              <div className="flex justify-center">
                <ArrowDown className="w-5 h-5 text-blue-500 animate-bounce" />
              </div>
              <Card className="bg-white dark:bg-black p-3 border border-slate-200 dark:border-slate-800 flex items-center justify-between">
                <span className="text-xs font-medium text-slate-500">
                  Next review: In 3 days
                </span>
                <span className="px-2 py-1 bg-green-100 dark:bg-green-900/40 text-green-700 dark:text-green-300 text-[10px] rounded uppercase font-bold">
                  Mastered
                </span>
              </Card>
            </div>
          </div>
        </div>
      </Card>
    </div>
  );
};
