import Link from "next/link";
import { ArrowRight, FileText, Brain, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";

export const HeroSection = () => {
  return (
    <main className="pt-32 pb-20 px-4">
      <div className="max-w-4xl mx-auto text-center">
        {/* Icon Badges */}
        <div className="flex justify-center mb-8">
          <div className="flex -space-x-2">
            <div className="w-12 h-12 rounded-full bg-blue-100 dark:bg-blue-900 flex items-center justify-center border-2 border-white dark:border-black">
              <FileText className="w-5 h-5 text-blue-600" />
            </div>
            <div className="w-12 h-12 rounded-full bg-orange-100 dark:bg-orange-900 flex items-center justify-center border-2 border-white dark:border-black">
              <Brain className="w-5 h-5 text-orange-600" />
            </div>
            <div className="w-12 h-12 rounded-full bg-green-100 dark:bg-green-900 flex items-center justify-center border-2 border-white dark:border-black">
              <Sparkles className="w-5 h-5 text-green-600" />
            </div>
          </div>
        </div>

        {/* Heading */}
        <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight mb-6 leading-[1.1]">
          One workspace.
          <br />
          Zero busywork.
          <br />
          Total mastery.
        </h1>

        {/* Subtitle */}
        <p className="text-xl md:text-2xl text-slate-500 dark:text-slate-400 mb-10 max-w-2xl mx-auto font-medium">
          Compass is where your notes meet AI-powered learning. Capture
          knowledge, generate quizzes, and master anything with spaced
          repetition.
        </p>

        {/* CTAs */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
          <Link href="/login">
            <Button
              size="lg"
              className="bg-slate-900 dark:bg-white dark:text-black text-white hover:opacity-90 text-lg px-8 py-3 font-bold"
            >
              Start learning for free
            </Button>
          </Link>
          <Button
            size="lg"
            variant="ghost"
            className="text-slate-900 dark:text-white text-lg px-8 py-3 font-medium flex items-center gap-2"
          >
            Request a demo <ArrowRight className="w-4 h-4" />
          </Button>
        </div>
      </div>
    </main>
  );
};
