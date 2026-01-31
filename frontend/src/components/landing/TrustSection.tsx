import { COMPANIES } from "@/models/landing.model";

export const TrustSection = () => {
  return (
    <section className="py-12 border-y border-slate-100 dark:border-slate-800">
      <div className="max-w-7xl mx-auto px-4">
        <p className="text-center text-xs font-bold text-slate-400 uppercase tracking-widest mb-8">
          Empowering teams at the world&apos;s most innovative companies
        </p>
        <div className="flex flex-wrap justify-center items-center gap-12 opacity-50 grayscale hover:grayscale-0 transition-all duration-500">
          {COMPANIES.map((company) => (
            <span key={company.name} className={company.style}>
              {company.name}
            </span>
          ))}
        </div>
      </div>
    </section>
  );
};
