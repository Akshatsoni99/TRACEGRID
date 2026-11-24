import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'TRACEGRID | Financial Crime Analytics & Investigation Platform',
  description: 'Team CyboShield | Rajasthan Police Hackathon 2026 - PS05 | Connecting Financial Evidence. Revealing Hidden Relationships.',
  icons: {
    icon: '/favicon.ico',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="bg-tg-bg text-tg-text antialiased font-sans select-none overflow-hidden">
        {children}
      </body>
    </html>
  );
}

