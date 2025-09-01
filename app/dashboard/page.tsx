import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Upload, Brain, FileText, ArrowRight, BookOpen, Users, TrendingUp } from "lucide-react"
import Link from "next/link"
import Navbar from "@/components/navbar"
import Leaderboard from "@/components/leaderboard"

export default function DashboardPage() {
  return (
    <div className="min-h-screen bg-background">
      <Navbar />

      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Hero Section */}
        <section className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-foreground mb-4 text-balance">
            Welcome Back to EduAccess
          </h1>
          <p className="text-lg text-muted-foreground mb-8 max-w-2xl mx-auto text-pretty">
            Continue your learning journey. Access notes, generate quizzes, and excel in your studies.
          </p>
          <Button size="lg" className="bg-accent text-accent-foreground hover:bg-accent/90">
            Start Learning
            <ArrowRight className="w-5 h-5 ml-2" />
          </Button>
        </section>

        {/* Stats Cards */}
        <section className="grid md:grid-cols-3 gap-6 mb-12">
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center gap-4">
                <div className="p-3 rounded-full bg-primary/10">
                  <BookOpen className="w-6 h-6 text-primary" />
                </div>
                <div>
                  <p className="text-2xl font-bold text-foreground">1,247</p>
                  <p className="text-sm text-muted-foreground">Notes Available</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center gap-4">
                <div className="p-3 rounded-full bg-secondary/10">
                  <Users className="w-6 h-6 text-secondary" />
                </div>
                <div>
                  <p className="text-2xl font-bold text-foreground">3,892</p>
                  <p className="text-sm text-muted-foreground">Active Students</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center gap-4">
                <div className="p-3 rounded-full bg-chart-4/10">
                  <TrendingUp className="w-6 h-6 text-chart-4" />
                </div>
                <div>
                  <p className="text-2xl font-bold text-foreground">89%</p>
                  <p className="text-sm text-muted-foreground">Success Rate</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </section>

        {/* Features Section */}
        <section className="mb-12">
          <h2 className="text-3xl font-bold text-center mb-8 text-foreground">Choose Your Learning Path</h2>

          <div className="grid md:grid-cols-3 gap-6">
            <Card className="hover:shadow-lg transition-all duration-300 hover:scale-105 cursor-pointer group">
              <CardHeader>
                <div className="p-3 rounded-full bg-secondary/10 w-fit mb-4 group-hover:bg-secondary/20 transition-colors">
                  <Upload className="w-8 h-8 text-secondary" />
                </div>
                <CardTitle>Upload / Paste Notes</CardTitle>
                <CardDescription>
                  Share your study materials and contribute to the community knowledge base.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Button asChild variant="outline" className="w-full bg-transparent">
                  <Link href="/upload">
                    Upload Notes
                    <ArrowRight className="w-4 h-4 ml-2" />
                  </Link>
                </Button>
              </CardContent>
            </Card>

            <Card className="hover:shadow-lg transition-all duration-300 hover:scale-105 cursor-pointer group">
              <CardHeader>
                <div className="p-3 rounded-full bg-primary/10 w-fit mb-4 group-hover:bg-primary/20 transition-colors">
                  <Brain className="w-8 h-8 text-primary" />
                </div>
                <CardTitle>AI Quiz Generator</CardTitle>
                <CardDescription>
                  Generate personalized quizzes from your notes using advanced AI technology.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Button asChild variant="outline" className="w-full bg-transparent">
                  <Link href="/quiz">
                    Generate Quiz
                    <ArrowRight className="w-4 h-4 ml-2" />
                  </Link>
                </Button>
              </CardContent>
            </Card>

            <Card className="hover:shadow-lg transition-all duration-300 hover:scale-105 cursor-pointer group">
              <CardHeader>
                <div className="p-3 rounded-full bg-chart-4/10 w-fit mb-4 group-hover:bg-chart-4/20 transition-colors">
                  <FileText className="w-8 h-8 text-chart-4" />
                </div>
                <CardTitle>Past Questions Bank</CardTitle>
                <CardDescription>
                  Access comprehensive collection of past exam questions and detailed solutions.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Button asChild variant="outline" className="w-full bg-transparent">
                  <Link href="/past-questions">
                    Browse Questions
                    <ArrowRight className="w-4 h-4 ml-2" />
                  </Link>
                </Button>
              </CardContent>
            </Card>
          </div>
        </section>

        {/* Leaderboard Section */}
        <section className="mb-12">
          <div className="grid lg:grid-cols-3 gap-8">
            <div className="lg:col-span-2">
              <h2 className="text-2xl font-bold mb-6 text-foreground">Recent Activity</h2>
              <div className="space-y-4">
                <Card>
                  <CardContent className="p-4">
                    <div className="flex items-center gap-3">
                      <div className="p-2 rounded-full bg-secondary/10">
                        <Upload className="w-4 h-4 text-secondary" />
                      </div>
                      <div>
                        <p className="font-medium text-foreground">New notes uploaded: "Mathematics - Calculus"</p>
                        <p className="text-sm text-muted-foreground">2 hours ago</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardContent className="p-4">
                    <div className="flex items-center gap-3">
                      <div className="p-2 rounded-full bg-primary/10">
                        <Brain className="w-4 h-4 text-primary" />
                      </div>
                      <div>
                        <p className="font-medium text-foreground">Quiz completed: "Physics - Mechanics"</p>
                        <p className="text-sm text-muted-foreground">5 hours ago</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardContent className="p-4">
                    <div className="flex items-center gap-3">
                      <div className="p-2 rounded-full bg-chart-4/10">
                        <FileText className="w-4 h-4 text-chart-4" />
                      </div>
                      <div>
                        <p className="font-medium text-foreground">Past question accessed: "Chemistry 2023"</p>
                        <p className="text-sm text-muted-foreground">1 day ago</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </div>

            <div>
              <Leaderboard />
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="border-t border-border bg-muted/30">
        <div className="max-w-7xl mx-auto px-4 py-8">
          <div className="text-center">
            <div className="flex items-center justify-center gap-2 mb-4">
              <BookOpen className="w-6 h-6 text-primary" />
              <span className="text-xl font-bold text-foreground">EduAccess</span>
            </div>
            <p className="text-muted-foreground">Made for Hackathon – SDG4: Quality Education</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
