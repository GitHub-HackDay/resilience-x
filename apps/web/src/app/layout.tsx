import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Resilience-X",
  description: "AI-powered Q&A with multi-hop reasoning for crisis recovery",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
