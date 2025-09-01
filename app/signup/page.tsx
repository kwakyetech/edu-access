"use client"

import type React from "react"
import LoadingSpinner from "@/components/loading-spinner"
import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { BookOpen, Eye, EyeOff, CheckCircle, XCircle } from "lucide-react"
import Link from "next/link"

export default function SignUpPage() {
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    confirmPassword: "",
  })

  const passwordsMatch = formData.password === formData.confirmPassword && formData.confirmPassword !== ""
  const passwordValid = formData.password.length >= 8

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!passwordsMatch || !passwordValid) {
      return
    }

    setIsLoading(true)

    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 2000))

    // TODO: Implement actual sign up logic
    console.log("Sign up attempt:", formData)

    // Redirect to dashboard on success
    window.location.href = "/dashboard"
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }))
  }

  return (
    <div className="min-h-screen bg-background flex items-center justify-center px-4 py-8 relative">
      {/* Back to Home Link */}
      <Link 
        href="/" 
        className="absolute top-4 left-4 flex items-center gap-2 text-muted-foreground hover:text-foreground transition-colors"
      >
        <BookOpen className="w-5 h-5" />
        <span className="text-sm font-medium">Back to Home</span>
      </Link>
      
      <div className="w-full max-w-md">
        {/* Header */}
        <div className="text-center mb-8">
          <Link href="/" className="inline-flex items-center gap-2 mb-4 hover:opacity-80 transition-opacity">
            <BookOpen className="w-8 h-8 text-primary" />
            <span className="text-2xl font-bold text-foreground">EduAccess</span>
          </Link>
          <h1 className="text-3xl font-bold text-foreground mb-2">Join EduAccess</h1>
          <p className="text-muted-foreground">Create your account and start learning today</p>
        </div>

        {/* Sign Up Form */}
        <Card className="shadow-lg">
          <CardHeader>
            <CardTitle>Create Account</CardTitle>
            <CardDescription>Fill in your details to get started</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="name">Full Name</Label>
                <Input
                  id="name"
                  name="name"
                  type="text"
                  placeholder="Enter your full name"
                  value={formData.name}
                  onChange={handleInputChange}
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  name="email"
                  type="email"
                  placeholder="Enter your email"
                  value={formData.email}
                  onChange={handleInputChange}
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="password">Password</Label>
                <div className="relative">
                  <Input
                    id="password"
                    name="password"
                    type={showPassword ? "text" : "password"}
                    placeholder="Create a password"
                    value={formData.password}
                    onChange={handleInputChange}
                    required
                  />
                  <Button
                    type="button"
                    variant="ghost"
                    size="sm"
                    className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent"
                    onClick={() => setShowPassword(!showPassword)}
                  >
                    {showPassword ? (
                      <EyeOff className="h-4 w-4 text-muted-foreground" />
                    ) : (
                      <Eye className="h-4 w-4 text-muted-foreground" />
                    )}
                  </Button>
                </div>
                {formData.password && (
                  <div className="flex items-center gap-2 text-sm">
                    {passwordValid ? (
                      <CheckCircle className="w-4 h-4 text-secondary" />
                    ) : (
                      <XCircle className="w-4 h-4 text-destructive" />
                    )}
                    <span className={passwordValid ? "text-secondary" : "text-destructive"}>At least 8 characters</span>
                  </div>
                )}
              </div>

              <div className="space-y-2">
                <Label htmlFor="confirmPassword">Confirm Password</Label>
                <div className="relative">
                  <Input
                    id="confirmPassword"
                    name="confirmPassword"
                    type={showConfirmPassword ? "text" : "password"}
                    placeholder="Confirm your password"
                    value={formData.confirmPassword}
                    onChange={handleInputChange}
                    required
                  />
                  <Button
                    type="button"
                    variant="ghost"
                    size="sm"
                    className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent"
                    onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                  >
                    {showConfirmPassword ? (
                      <EyeOff className="h-4 w-4 text-muted-foreground" />
                    ) : (
                      <Eye className="h-4 w-4 text-muted-foreground" />
                    )}
                  </Button>
                </div>
                {formData.confirmPassword && (
                  <div className="flex items-center gap-2 text-sm">
                    {passwordsMatch ? (
                      <CheckCircle className="w-4 h-4 text-secondary" />
                    ) : (
                      <XCircle className="w-4 h-4 text-destructive" />
                    )}
                    <span className={passwordsMatch ? "text-secondary" : "text-destructive"}>Passwords match</span>
                  </div>
                )}
              </div>

              <Button
                type="submit"
                className="w-full"
                size="lg"
                disabled={!passwordsMatch || !passwordValid || isLoading}
              >
                {isLoading ? (
                  <>
                    <LoadingSpinner size="sm" />
                    <span className="ml-2">Creating Account...</span>
                  </>
                ) : (
                  "Create Account"
                )}
              </Button>
            </form>

            <div className="mt-6 text-center">
              <p className="text-sm text-muted-foreground">
                Already have an account?{" "}
                <Link href="/signin" className="text-primary hover:underline font-medium transition-colors">
                  Sign in here
                </Link>
              </p>
            </div>
          </CardContent>
        </Card>


      </div>
    </div>
  )
}
