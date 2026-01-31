// Landing Page Models

export interface NavItem {
  label: string;
  href: string;
}

export interface Feature {
  id: string;
  title: string;
  description: string;
  icon: string;
  color: string;
}

export interface Pillar {
  id: string;
  title: string;
  description: string;
  iconColor: string;
}

export interface Company {
  name: string;
  style: string;
}

export interface FooterSection {
  title: string;
  links: Array<{
    label: string;
    href: string;
  }>;
}

export interface CalculatorSettings {
  minHours: number;
  maxHours: number;
  defaultHours: number;
  savingsPercentage: number;
}

// Static data
export const NAV_ITEMS: NavItem[] = [
  { label: "Product", href: "#" },
  { label: "Solutions", href: "#" },
  { label: "Resources", href: "#" },
  { label: "Pricing", href: "#" },
];

export const FEATURES: Feature[] = [
  {
    id: "editor",
    title: "Documentation built for learning.",
    description:
      "Write your notes, import PDFs, or sync from web pages. Our editor automatically identifies key concepts.",
    icon: "FileText",
    color: "slate",
  },
  {
    id: "quiz",
    title: "Instant mastery check.",
    description:
      "With one click, turn your documentation into dynamic quizzes and active recall flashcards.",
    icon: "Sparkles",
    color: "blue",
  },
];

export const PILLARS: Pillar[] = [
  {
    id: "document",
    title: "Document",
    description:
      "Structured markdown editor with real-time collaboration. The home for all your knowledge assets.",
    iconColor: "blue",
  },
  {
    id: "learn",
    title: "Learn",
    description:
      "Adaptive learning algorithms that schedule reviews based on your individual memory curve.",
    iconColor: "purple",
  },
  {
    id: "share",
    title: "Share",
    description:
      "Publish your handbooks, share flashcard decks with your team, and track group progress.",
    iconColor: "green",
  },
];

export const COMPANIES: Company[] = [
  { name: "Figma", style: "text-xl font-black" },
  { name: "OpenAI", style: "text-xl font-black italic" },
  { name: "ramp", style: "text-xl font-black tracking-tighter" },
  { name: "▲ Vercel", style: "text-xl font-black italic" },
  { name: "NVIDIA", style: "text-xl font-black" },
];

export const FOOTER_SECTIONS: FooterSection[] = [
  {
    title: "Product",
    links: [
      { label: "Features", href: "#" },
      { label: "AI Tools", href: "#" },
      { label: "Mobile App", href: "#" },
      { label: "Web Clipper", href: "#" },
    ],
  },
  {
    title: "Resources",
    links: [
      { label: "Documentation", href: "#" },
      { label: "Learning Center", href: "#" },
      { label: "Community", href: "#" },
      { label: "Integrations", href: "#" },
    ],
  },
  {
    title: "Company",
    links: [
      { label: "About us", href: "#" },
      { label: "Careers", href: "#" },
      { label: "Privacy Policy", href: "#" },
      { label: "Contact", href: "#" },
    ],
  },
  {
    title: "Solutions",
    links: [
      { label: "Enterprise", href: "#" },
      { label: "Startups", href: "#" },
      { label: "Education", href: "#" },
      { label: "Personal", href: "#" },
    ],
  },
];

export const CALCULATOR_SETTINGS: CalculatorSettings = {
  minHours: 10,
  maxHours: 200,
  defaultHours: 40,
  savingsPercentage: 0.3,
};
