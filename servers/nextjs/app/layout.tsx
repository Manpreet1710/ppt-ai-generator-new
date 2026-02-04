import type { Metadata } from "next";
import localFont from "next/font/local";
import { Roboto, Instrument_Sans } from "next/font/google";
import "./globals.css";
import { Providers } from "./providers";
import MixpanelInitializer from "./MixpanelInitializer";
import { LayoutProvider } from "./(presentation-generator)/context/LayoutContext";
import { Toaster } from "@/components/ui/sonner";
const inter = localFont({
  src: [
    {
      path: "./fonts/Inter.ttf",
      weight: "400",
      style: "normal",
    },
  ],
  variable: "--font-inter",
});

const instrument_sans = Instrument_Sans({
  subsets: ["latin"],
  weight: ["400"],
  variable: "--font-instrument-sans",
});

const roboto = Roboto({
  subsets: ["latin"],
  weight: ["400"],
  variable: "--font-roboto",
});


export const metadata: Metadata = {
  metadataBase: new URL("https://contenttool.io"),

  title: "AI Presentation Generator | Create Professional Slides with AI",
  description:
    "Presenton is an AI-powered presentation generator that helps you create professional slides in seconds. Supports OpenAI, Gemini & Ollama with smart layouts, data storytelling, and instant PDF/PPTX export.",

  keywords: [
    "AI presentation generator",
    "Presenton AI",
    "AI slides creator",
    "AI powerpoint maker",
    "presentation maker AI",
    "data storytelling presentations",
    "automatic slide generator",
    "Gamma alternative",
    "professional presentation tool",
  ],

  openGraph: {
    title: "Presenton – AI Presentation Generator",
    description:
      "Create stunning presentations using AI. Multi-model support, smart layouts, and instant PPTX/PDF export for professional slides.",
    url: "https://contenttool.io",
    siteName: "Presenton",
    images: [
      {
        url: "https://contenttool.io/favicon.svg",
        width: 1200,
        height: 630,
        alt: "Presenton AI Presentation Generator",
      },
    ],
    type: "website",
    locale: "en_US",
  },

  alternates: {
    canonical: "https://contenttool.io",
  },

  twitter: {
    card: "summary_large_image",
    title: "Presenton – AI Presentation Generator",
    description:
      "Generate professional AI presentations with smart layouts and multi-model support. Export slides to PPTX or PDF instantly.",
    images: ["https://contenttool.io/favicon.svg"],
  },
};


export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {

  return (
    <html lang="en">
      <body
        className={`${inter.variable} ${roboto.variable} ${instrument_sans.variable} antialiased`}
      >
        <Providers>
          <MixpanelInitializer>
            <LayoutProvider>
              {children}
            </LayoutProvider>
          </MixpanelInitializer>
        </Providers>
        <Toaster position="top-center" />
      </body>
    </html>
  );
}
