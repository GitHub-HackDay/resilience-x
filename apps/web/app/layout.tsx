import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Resilience-X",
  description: "AI-powered Q&A for post-disaster recovery planning",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased font-sans">
        {children}
      </body>
    </html>
  );
}
