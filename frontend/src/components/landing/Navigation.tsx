import Link from "next/link";
import { Compass as CompassIcon } from "lucide-react";
import { Button } from "@/components/ui/button";
import { NAV_ITEMS } from "@/models/landing.model";

export const Navigation = () => {
  return (
    <nav className="fixed top-0 w-full bg-white/80 dark:bg-[#0A0A0A]/80 backdrop-blur-lg border-b border-slate-200 dark:border-slate-800 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center gap-8">
            <Link
              href="/"
              className="flex items-center gap-2 font-bold text-xl tracking-tight"
            >
              <CompassIcon className="w-6 h-6 text-slate-900 dark:text-white" />
              <span>Compass</span>
            </Link>
            <div className="hidden md:flex items-center gap-6 text-sm font-medium text-slate-600 dark:text-slate-400">
              {NAV_ITEMS.map((item) => (
                <a
                  key={item.label}
                  href={item.href}
                  className="hover:text-slate-900 dark:hover:text-white transition-colors"
                >
                  {item.label}
                </a>
              ))}
            </div>
          </div>
          <div className="flex items-center gap-4">
            <Link href="/login">
              <Button variant="ghost" className="text-sm font-medium">
                Log in
              </Button>
            </Link>
            <Link href="/login">
              <Button className="bg-slate-900 dark:bg-white dark:text-black text-white hover:opacity-90 text-sm font-medium">
                Get Compass free
              </Button>
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
};
