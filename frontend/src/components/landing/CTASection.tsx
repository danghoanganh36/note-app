import Link from "next/link";
import { Button } from "@/components/ui/button";

export const CTASection = () => {
  return (
    <section className="py-24 text-center">
      <div className="max-w-2xl mx-auto px-4">
        <h2 className="text-5xl font-extrabold mb-8">Try for free.</h2>
        <p className="text-xl text-slate-500 dark:text-slate-400 mb-10">
          Join 100,000+ lifelong learners and teams building their knowledge OS
          on Compass.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link href="/login">
            <Button
              size="lg"
              className="bg-slate-900 dark:bg-white dark:text-black text-white hover:opacity-90 text-lg px-8 py-3 font-bold"
            >
              Get started now
            </Button>
          </Link>
          <Button
            size="lg"
            variant="outline"
            className="border border-slate-200 dark:border-slate-800 text-lg px-8 py-3 font-medium hover:bg-slate-50 dark:hover:bg-[#1A1A1A]"
          >
            Talk to sales
          </Button>
        </div>
        <p className="mt-8 text-sm text-slate-400">
          No credit card required. Free forever for individuals.
        </p>
      </div>
    </section>
  );
};
