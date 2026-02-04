import React from "react";

import UploadPage from "./components/UploadPage";
import Header from "@/app/(presentation-generator)/dashboard/components/Header";
import { Metadata } from "next";


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



const page = () => {
  return (
    <div className="relative">
      <Header />
      <div className="flex flex-col items-center justify-center  py-8">
        <h1 className="text-3xl font-semibold font-instrument_sans">
          Create Presentation{" "}
        </h1>
        {/* <p className='text-sm text-gray-500'>We will generate a presentation for you</p> */}
      </div>

      <UploadPage />
    </div>
  );
};

export default page;
