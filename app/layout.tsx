import type React from "react"
import type { Metadata } from "next"
import { GeistSans } from "geist/font/sans"
import { GeistMono } from "geist/font/mono"
import { Analytics } from "@vercel/analytics/next"
import { Suspense } from "react"
import "./globals.css"

export const metadata: Metadata = {
  title: "EduAccess - Unlock Learning for Everyone in Africa",
  description:
    "Access affordable notes, quizzes, and past exam questions. Empowering Ghanaian students with quality educational resources.",
  generator: "v0.app",
  keywords: "education, Ghana, students, notes, quizzes, past questions, learning, Africa",
  authors: [{ name: "EduAccess Team" }],
  openGraph: {
    title: "EduAccess - Unlock Learning for Everyone in Africa",
    description:
      "Access affordable notes, quizzes, and past exam questions. Empowering Ghanaian students with quality educational resources.",
    type: "website",
  },
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body className={`font-sans ${GeistSans.variable} ${GeistMono.variable} antialiased`}>
        <Suspense fallback={<div>Loading...</div>}>{children}</Suspense>
        <Analytics />
      </body>
    </html>
  )
}
