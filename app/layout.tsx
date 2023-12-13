import './globals.css'
import { Inter } from 'next/font/google'
import Providers from '@/utils/Providers'

const inter = Inter({ subsets: ['latin'] })

export const metadata = {
  title: 'LearnAI',
  description: 'An adaptive math tutor for math problems',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}><Providers>{children}</Providers></body>
    </html>
  )
}
