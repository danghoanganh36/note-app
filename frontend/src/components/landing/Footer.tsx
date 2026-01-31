import { Compass as CompassIcon, Globe, Terminal, MessageSquare } from "lucide-react";
import { FOOTER_SECTIONS } from "@/models/landing.model";

export const Footer = () => {
  return (
    <footer className="bg-white dark:bg-[#0A0A0A] border-t border-slate-100 dark:border-slate-900 py-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-12">
          <div className="col-span-2 lg:col-span-1">
            <a href="#" className="flex items-center gap-2 font-bold text-xl mb-6">
              <CompassIcon className="w-6 h-6" />
              <span>Compass</span>
            </a>
            <div className="flex gap-4 opacity-60 mb-6">
              <Globe className="w-5 h-5" />
              <Terminal className="w-5 h-5" />
              <MessageSquare className="w-5 h-5" />
            </div>
          </div>

          {FOOTER_SECTIONS.map((section) => (
            <div key={section.title}>
              <h5 className="font-bold text-sm mb-4">{section.title}</h5>
              <ul className="space-y-2 text-sm text-slate-500 dark:text-slate-400">
                {section.links.map((link) => (
                  <li key={link.label}>
                    <a
                      href={link.href}
                      className="hover:text-slate-900 dark:hover:text-white transition-colors"
                    >
                      {link.label}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <div className="mt-16 pt-8 border-t border-slate-100 dark:border-slate-900 flex flex-col md:flex-row justify-between items-center gap-4 text-xs text-slate-400">
          <p>&copy; 2026 Compass Technologies Inc. All rights reserved.</p>
          <div className="flex gap-6">
            <a
              href="#"
              className="hover:text-slate-900 dark:hover:text-white transition-colors"
            >
              Terms of Service
            </a>
            <a
              href="#"
              className="hover:text-slate-900 dark:hover:text-white transition-colors"
            >
              Cookie Settings
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
};
