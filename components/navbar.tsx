"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { BookOpen, Menu, X, Home, Upload, FileText, Trophy, Info, LogOut } from "lucide-react"
import Link from "next/link"
import { useRouter } from "next/navigation"

export default function Navbar() {
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const router = useRouter()

  const navItems = [
    { href: "/dashboard", label: "Home", icon: Home },
    { href: "/upload", label: "Upload Notes", icon: Upload },
    { href: "/past-questions", label: "Past Questions", icon: FileText },
    { href: "/leaderboard", label: "Leaderboard", icon: Trophy },
    { href: "/about", label: "About", icon: Info },
  ]

  const handleLogout = () => {
    // Clear any stored user data (localStorage, sessionStorage, etc.)
    localStorage.removeItem("user")
    sessionStorage.removeItem("authToken")

    // Redirect to homepage
    router.push("/")
  }

  return (
    <nav className="bg-background border-b border-border sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/dashboard" className="flex items-center gap-2">
            <BookOpen className="w-8 h-8 text-primary" />
            <span className="text-xl font-bold text-foreground">EduAccess</span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-6">
            {navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className="flex items-center gap-2 text-muted-foreground hover:text-foreground transition-colors"
              >
                <item.icon className="w-4 h-4" />
                {item.label}
              </Link>
            ))}
            <Button
              variant="ghost"
              size="sm"
              className="text-destructive hover:text-destructive"
              onClick={handleLogout}
            >
              <LogOut className="w-4 h-4 mr-2" />
              Logout
            </Button>
          </div>

          {/* Mobile Menu Button */}
          <Button variant="ghost" size="sm" className="md:hidden" onClick={() => setIsMenuOpen(!isMenuOpen)}>
            {isMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </Button>
        </div>

        {/* Mobile Navigation */}
        {isMenuOpen && (
          <div className="md:hidden py-4 border-t border-border">
            <div className="flex flex-col gap-4">
              {navItems.map((item) => (
                <Link
                  key={item.href}
                  href={item.href}
                  className="flex items-center gap-3 text-muted-foreground hover:text-foreground transition-colors py-2"
                  onClick={() => setIsMenuOpen(false)}
                >
                  <item.icon className="w-5 h-5" />
                  {item.label}
                </Link>
              ))}
              <Button
                variant="ghost"
                size="sm"
                className="text-destructive hover:text-destructive justify-start p-0"
                onClick={handleLogout}
              >
                <LogOut className="w-5 h-5 mr-3" />
                Logout
              </Button>
            </div>
          </div>
        )}
      </div>
    </nav>
  )
}
