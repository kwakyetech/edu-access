import { HomeNavbar } from "@/components/home-navbar"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { BookOpen, Users, Upload, Brain, FileText } from "lucide-react"
import Link from "next/link"

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-background">
      <HomeNavbar />

      {/* Hero Section */}
      <section className="px-4 py-12 md:py-20">
        <div className="max-w-4xl mx-auto text-center">
          <div className="mb-8">
            <BookOpen className="w-16 h-16 mx-auto mb-4 text-primary" />
            <h1 className="text-4xl md:text-6xl font-bold text-foreground mb-4 text-balance">
              Unlock Learning for Everyone in Africa
            </h1>
            <p className="text-lg md:text-xl text-muted-foreground max-w-2xl mx-auto text-pretty">
              Access affordable notes, quizzes, and past exam questions. Empowering Ghanaian students with quality
              educational resources.
            </p>
          </div>

          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <Button asChild size="lg" className="w-full sm:w-auto">
              <Link href="/signin">Sign In</Link>
            </Button>
            <Button
              asChild
              variant="outline"
              size="lg"
              className="w-full sm:w-auto bg-accent text-accent-foreground hover:bg-accent/90"
            >
              <Link href="/signup">Get Started</Link>
            </Button>
          </div>
        </div>
      </section>

      {/* Features Preview */}
      <section className="px-4 py-12 bg-muted/30">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-8 text-foreground">Everything You Need to Succeed</h2>

          <div className="grid md:grid-cols-3 gap-6">
            <Card className="hover:shadow-lg transition-shadow duration-300">
              <CardContent className="p-6 text-center">
                <Upload className="w-12 h-12 mx-auto mb-4 text-secondary" />
                <h3 className="text-xl font-semibold mb-2">Upload & Share Notes</h3>
                <p className="text-muted-foreground">
                  Share your study materials and access notes from fellow students across Ghana.
                </p>
              </CardContent>
            </Card>

            <Card className="hover:shadow-lg transition-shadow duration-300">
              <CardContent className="p-6 text-center">
                <Brain className="w-12 h-12 mx-auto mb-4 text-primary" />
                <h3 className="text-xl font-semibold mb-2">AI Quiz Generator</h3>
                <p className="text-muted-foreground">
                  Generate personalized quizzes from your notes using advanced AI technology.
                </p>
              </CardContent>
            </Card>

            <Card className="hover:shadow-lg transition-shadow duration-300">
              <CardContent className="p-6 text-center">
                <FileText className="w-12 h-12 mx-auto mb-4 text-chart-4" />
                <h3 className="text-xl font-semibold mb-2">Past Questions Bank</h3>
                <p className="text-muted-foreground">
                  Access comprehensive collection of past exam questions and solutions.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Community Section */}
      <section className="px-4 py-12">
        <div className="max-w-4xl mx-auto text-center">
          <Users className="w-16 h-16 mx-auto mb-4 text-secondary" />
          <h2 className="text-3xl font-bold mb-4 text-foreground">Join Our Learning Community</h2>
          <p className="text-lg text-muted-foreground mb-8 text-pretty">
            Connect with thousands of students across Ghana. Share knowledge, compete on leaderboards, and achieve
            academic excellence together.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button asChild size="lg" className="w-full sm:w-auto">
              <Link href="/signup">Start Learning Today</Link>
            </Button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="px-4 py-8 border-t border-border">
        <div className="max-w-4xl mx-auto text-center">
          <div className="flex items-center justify-center gap-2 mb-4">
            <BookOpen className="w-6 h-6 text-primary" />
            <span className="text-xl font-bold text-foreground">EduAccess</span>
          </div>
          <p className="text-muted-foreground">Made for Hackathon – SDG4: Quality Education</p>
        </div>
      </footer>
    </div>
  )
}
