import { BookOpen, Brain, Share2 } from "lucide-react";
import { Card } from "@/components/ui/card";
import { PILLARS } from "@/models/landing.model";

const iconMap = {
  blue: BookOpen,
  purple: Brain,
  green: Share2,
};

const colorMap = {
  blue: {
    bg: "bg-blue-50 dark:bg-blue-900/20",
    text: "text-blue-600",
  },
  purple: {
    bg: "bg-purple-50 dark:bg-purple-900/20",
    text: "text-purple-600",
  },
  green: {
    bg: "bg-green-50 dark:bg-green-900/20",
    text: "text-green-600",
  },
};

export const ThreePillars = () => {
  return (
    <section className="py-24 bg-[#F6F6F3] dark:bg-[#1A1A1A]/50">
      <div className="max-w-6xl mx-auto px-4">
        <h2 className="text-4xl font-bold text-center mb-16">
          The three pillars of mastery.
        </h2>
        <div className="grid md:grid-cols-3 gap-8">
          {PILLARS.map((pillar) => {
            const Icon =
              iconMap[pillar.iconColor as keyof typeof iconMap];
            const colors =
              colorMap[pillar.iconColor as keyof typeof colorMap];

            return (
              <Card
                key={pillar.id}
                className="p-8 bg-white dark:bg-black rounded-xl shadow-md border border-slate-100 dark:border-slate-800 hover:shadow-lg transition-shadow"
              >
                <div
                  className={`w-12 h-12 ${colors.bg} rounded-lg flex items-center justify-center mb-6`}
                >
                  <Icon className={`w-6 h-6 ${colors.text}`} />
                </div>
                <h4 className="text-xl font-bold mb-4">{pillar.title}</h4>
                <p className="text-slate-600 dark:text-slate-400">
                  {pillar.description}
                </p>
              </Card>
            );
          })}
        </div>
      </div>
    </section>
  );
};
