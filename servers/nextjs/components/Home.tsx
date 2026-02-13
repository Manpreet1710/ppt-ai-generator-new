"use client";
import React from 'react';
import Link from 'next/link';
import { ChevronRight, Zap, Image as ImageIcon, FileText, Bot } from 'lucide-react';



// Logo Component
const Logo = () => (
    <Link href="/" aria-label="AI PPT Generator Home">
        <img src="/content-tool-logo.webp" alt="AI PPT Generator Logo" className="h-10 w-auto" />
    </Link>
);

const HomePage = () => {
    return (
        <div className="bg-white text-gray-800 font-sans">
            {/* Header */}
            <header className="fixed top-0 left-0 right-0 bg-white/80 backdrop-blur-md z-50 border-b border-gray-200">
                <div className="container mx-auto px-6 py-4 flex justify-between items-center">
                    <Logo />
                    <nav className="hidden md:flex items-center space-x-8">
                        <Link href="#home" className="text-gray-600 hover:text-blue-600 transition-colors">Home</Link>
                        <Link href="#features" className="text-gray-600 hover:text-blue-600 transition-colors">Features</Link>
                        <Link href="#pricing" className="text-gray-600 hover:text-blue-600 transition-colors">Pricing</Link>
                        <Link href="/login" className="text-gray-600 hover:text-blue-600 transition-colors">Login</Link>
                    </nav>
                    <Link href="/dashboard" className="bg-blue-600 text-white font-semibold px-6 py-2 rounded-lg hover:bg-blue-700 transition-all duration-300 shadow-sm">
                        Dashboard
                    </Link>
                </div>
            </header>

            <main>
                {/* Hero Section */}
                <section id="home" className="pt-32 pb-20 text-center bg-gray-50">
                    <div className="container mx-auto px-6">
                        <h1 className="text-5xl md:text-3xl font-extrabold text-gray-900 leading-tight">
                            Generate Professional Presentations Instantly with AI
                        </h1>
                        
                        <p className="mt-6 max-w-2xl mx-auto text-lg text-gray-500">
                            Say goodbye to tedious slide creation. Our AI-powered tool helps you design, write, and format professional presentations effortlessly, so you can focus on what truly matters: your message.
                        </p>
                        <div className="mt-10 flex justify-center items-center space-x-4">
                            <Link href="/dashboard" className="bg-blue-600 text-white font-bold px-8 py-4 rounded-lg text-lg hover:bg-blue-700 transition-all duration-300 shadow-lg flex items-center">
                                Start Creating <ChevronRight className="w-5 h-5 ml-2" />
                            </Link>
                            <Link href="#pricing" className="bg-white text-blue-600 font-bold px-8 py-4 rounded-lg text-lg border border-gray-300 hover:bg-gray-100 transition-all duration-300 shadow-lg">
                                View Pricing
                            </Link>
                        </div>
                    </div>
                </section>

                {/* Features Section */}
                <section id="features" className="py-20 bg-white">
                    <div className="container mx-auto px-6 text-center">
                        <h2 className="text-4xl font-bold text-gray-900">Features That Set You Apart</h2>
                        <p className="mt-4 text-lg text-gray-600 max-w-3xl mx-auto">
                            Everything you need to create compelling presentations, powered by cutting-edge AI.
                        </p>
                        <div className="mt-16 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-12">
                            <div className="feature-card">
                                <Zap className="w-12 h-12 text-blue-600" />
                                <h3 className="text-xl font-semibold mt-4">AI-Generated Slides</h3>
                                <p className="mt-2 text-gray-500">Generate entire presentations from a single prompt or document.</p>
                            </div>
                            <div className="feature-card">
                                <ImageIcon className="w-12 h-12 text-blue-600" />
                                <h3 className="text-xl font-semibold mt-4">Automatic Image Sourcing</h3>
                                <p className="mt-2 text-gray-500">AI finds and suggests relevant, high-quality images for your slides.</p>
                            </div>
                            <div className="feature-card">
                                <FileText className="w-12 h-12 text-blue-600" />
                                <h3 className="text-xl font-semibold mt-4">Export to PPT/PDF</h3>
                                <p className="mt-2 text-gray-500">Instantly export your work into popular formats with one click.</p>
                            </div>
                            <div className="feature-card">
                                <Bot className="w-12 h-12 text-blue-600" />
                                <h3 className="text-xl font-semibold mt-4">Smart Layouts</h3>
                                <p className="mt-2 text-gray-500">Our AI intelligently designs beautiful and professional slide layouts.</p>
                            </div>
                        </div>
                    </div>
                </section>

                {/* How It Works Section */}
                <section className="py-20 bg-gray-50">
                    <div className="container mx-auto px-6 text-center">
                        <h2 className="text-4xl font-bold text-gray-900">Create in 3 Simple Steps</h2>
                        <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-12">
                            <div className="step-card">
                                <div className="step-number">1</div>
                                <h3 className="text-xl font-semibold mt-4">Provide a Prompt</h3>
                                <p className="mt-2 text-gray-500">Start with a topic, an outline, or an existing document.</p>
                            </div>
                            <div className="step-card">
                                <div className="step-number">2</div>
                                <h3 className="text-xl font-semibold mt-4">Let AI Do the Work</h3>
                                <p className="mt-2 text-gray-500">Our AI generates the content, design, and imagery for you.</p>
                            </div>
                            <div className="step-card">
                                <div className="step-number">3</div>
                                <h3 className="text-xl font-semibold mt-4">Export & Present</h3>
                                <p className="mt-2 text-gray-500">Download your presentation as a PPTX or PDF and impress your audience.</p>
                            </div>
                        </div>
                    </div>
                </section>

                {/* Pricing Section */}
                <section id="pricing" className="py-20 bg-white">
                    <div className="container mx-auto px-6 text-center">
                        <h2 className="text-4xl font-bold text-gray-900">Simple, Transparent Pricing</h2>
                        <p className="mt-4 text-lg text-gray-600 max-w-3xl mx-auto">Choose the plan that's right for you and your team.</p>
                        <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
                            
                            {/* Free Plan */}
                            <div className="pricing-card">
                                <h3 className="text-2xl font-bold text-gray-900">Free</h3>
                                <p className="mt-4 text-5xl font-extrabold text-gray-900">$0<span className="text-lg font-medium text-gray-500">/month</span></p>
                                <p className="mt-2 text-gray-500">For individuals getting started</p>
                                <ul className="mt-8 space-y-4 text-left">
                                    <li className="flex items-center"><Check className="w-5 h-5 text-green-500 mr-3" />5 Presentations/month</li>
                                    <li className="flex items-center"><Check className="w-5 h-5 text-green-500 mr-3" />Basic AI Features</li>
                                    <li className="flex items-center"><Check className="w-5 h-5 text-green-500 mr-3" />PDF Exports</li>
                                    <li className="flex items-center"><Check className="w-5 h-5 text-green-500 mr-3" />Standard Support</li>
                                </ul>
                                <button className="w-full mt-10 bg-white text-blue-600 font-bold py-3 rounded-lg border border-gray-300 hover:bg-gray-100 transition-all duration-300">Get Started Free</button>
                            </div>

                            {/* Pro Plan - Most Popular */}
                            <div className="pricing-card border-blue-600 ring-2 ring-blue-600 relative">
                                <span className="absolute top-0 -translate-y-1/2 bg-blue-600 text-white text-sm font-bold px-4 py-1 rounded-full">MOST POPULAR</span>
                                <h3 className="text-2xl font-bold text-gray-900">Pro</h3>
                                <p className="mt-4 text-5xl font-extrabold text-gray-900">$15<span className="text-lg font-medium text-gray-500">/month</span></p>
                                <p className="mt-2 text-gray-500">For professionals and power users</p>
                                <ul className="mt-8 space-y-4 text-left">
                                    <li className="flex items-center"><Check className="w-5 h-5 text-green-500 mr-3" />Unlimited Presentations</li>
                                    <li className="flex items-center"><Check className="w-5 h-5 text-green-500 mr-3" />Advanced AI Features</li>
                                    <li className="flex items-center"><Check className="w-5 h-5 text-green-500 mr-3" />PPTX & PDF Exports</li>
                                    <li className="flex items-center"><Check className="w-5 h-5 text-green-500 mr-3" />Priority Support</li>
                                </ul>
                                <button className="w-full mt-10 bg-blue-600 text-white font-bold py-3 rounded-lg hover:bg-blue-700 transition-all duration-300">Select Plan</button>
                            </div>

                            {/* Business Plan */}
                            <div className="pricing-card">
                                <h3 className="text-2xl font-bold text-gray-900">Business</h3>
                                <p className="mt-4 text-5xl font-extrabold text-gray-900">$29<span className="text-lg font-medium text-gray-500">/month</span></p>
                                <p className="mt-2 text-gray-500">For teams and enterprises</p>
                                <ul className="mt-8 space-y-4 text-left">
                                    <li className="flex items-center"><Check className="w-5 h-5 text-green-500 mr-3" />Everything in Pro</li>
                                    <li className="flex items-center"><Check className="w-5 h-5 text-green-500 mr-3" />Team Collaboration</li>
                                    <li className="flex items-center"><Check className="w-5 h-5 text-green-500 mr-3" />Custom Branding</li>
                                    <li className="flex items-center"><Check className="w-5 h-5 text-green-500 mr-3" />Dedicated Support</li>
                                </ul>
                                <button className="w-full mt-10 bg-white text-blue-600 font-bold py-3 rounded-lg border border-gray-300 hover:bg-gray-100 transition-all duration-300">Select Plan</button>
                            </div>
                        </div>
                    </div>
                </section>

                {/* FAQ Section */}
                <section className="py-20 bg-gray-50">
                    <div className="container mx-auto px-6 max-w-3xl">
                        <h2 className="text-4xl font-bold text-center text-gray-900">Frequently Asked Questions</h2>
                        <div className="mt-12 space-y-8">
                            <div className="faq-item">
                                <h3 className="text-xl font-semibold">How does the AI generate presentations?</h3>
                                <p className="mt-2 text-gray-600">Our tool uses advanced language models to understand your prompt, structure the content, write the text, and design the slides, all in a cohesive and professional manner.</p>
                            </div>
                            <div className="faq-item">
                                <h3 className="text-xl font-semibold">Can I customize the generated slides?</h3>
                                <p className="mt-2 text-gray-600">Yes! While our AI provides a strong first draft, you have full control to edit text, change images, and adjust layouts before exporting your final presentation.</p>
                            </div>
                             <div className="faq-item">
                                <h3 className="text-xl font-semibold">What formats can I export to?</h3>
                                <p className="mt-2 text-gray-600">You can instantly download your presentations as either a Microsoft PowerPoint file (.pptx) or a PDF, ready for sharing or presenting.</p>
                            </div>
                        </div>
                    </div>
                </section>
            </main>

            {/* Footer */}
            <footer className="bg-gray-800 text-white py-12">
                <div className="container mx-auto px-6 text-center">
                    <Logo />
                    <nav className="mt-8 flex justify-center space-x-8">
                        <Link href="#home" className="hover:text-blue-400">Home</Link>
                        <Link href="#pricing" className="hover:text-blue-400">Pricing</Link>
                        <Link href="/dashboard" className="hover:text-blue-400">Dashboard</Link>
                        <Link href="/privacy" className="hover:text-blue-400">Privacy Policy</Link>
                    </nav>
                    <p className="mt-8 text-gray-400">&copy; 2026 AI PPT Generator. All rights reserved.</p>
                </div>
            </footer>
        </div>
    );
};

// A simple Check icon component to be used in the pricing section
const Check = ({ className }: { className: string }) => (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
        <path d="M20 6 9 17l-5-5"></path>
    </svg>
);

export default HomePage;