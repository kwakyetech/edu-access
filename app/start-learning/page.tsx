import { Navbar } from "@/components/navbar"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { BookOpen, Brain, FileText, Users, Trophy, Clock } from "lucide-react"
import Link from "next/link"

export default function StartLearningPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-green-50">
      <Navbar />

      <main className="container mx-auto px-4 pt-24 pb-12">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">Start Your Learning Journey</h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto mb-8">
            Choose your path to academic excellence. Access notes, practice with AI quizzes, and explore past questions.
          </p>
        </div>

        {/* Learning Paths */}
        <div className="grid md:grid-cols-3 gap-6 mb-12">
          <Card className="hover:shadow-lg transition-shadow cursor-pointer group">
            <CardHeader className="text-center">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4 group-hover:bg-blue-200 transition-colors">
                <BookOpen className="w-8 h-8 text-blue-600" />
              </div>
              <CardTitle className="text-xl">Study Notes</CardTitle>
              <CardDescription>Access comprehensive notes uploaded by students and educators</CardDescription>
            </CardHeader>
            <CardContent className="text-center">
              <Link href="/upload">
                <Button className="w-full bg-blue-600 hover:bg-blue-700">Browse Notes</Button>
              </Link>
            </CardContent>
          </Card>

          <Card className="hover:shadow-lg transition-shadow cursor-pointer group">
            <CardHeader className="text-center">
              <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4 group-hover:bg-green-200 transition-colors">
                <Brain className="w-8 h-8 text-green-600" />
              </div>
              <CardTitle className="text-xl">AI Quiz Practice</CardTitle>
              <CardDescription>Generate personalized quizzes from your study materials</CardDescription>
            </CardHeader>
            <CardContent className="text-center">
              <Link href="/quiz">
                <Button className="w-full bg-green-600 hover:bg-green-700">Start Quiz</Button>
              </Link>
            </CardContent>
          </Card>

          <Card className="hover:shadow-lg transition-shadow cursor-pointer group">
            <CardHeader className="text-center">
              <div className="w-16 h-16 bg-yellow-100 rounded-full flex items-center justify-center mx-auto mb-4 group-hover:bg-yellow-200 transition-colors">
                <FileText className="w-8 h-8 text-yellow-600" />
              </div>
              <CardTitle className="text-xl">Past Questions</CardTitle>
              <CardDescription>Practice with real exam questions from previous years</CardDescription>
            </CardHeader>
            <CardContent className="text-center">
              <Link href="/past-questions">
                <Button className="w-full bg-yellow-600 hover:bg-yellow-700">Browse Questions</Button>
              </Link>
            </CardContent>
          </Card>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-12">
          <div className="text-center p-4 bg-white rounded-lg shadow-sm">
            <Users className="w-8 h-8 text-blue-600 mx-auto mb-2" />
            <div className="text-2xl font-bold text-gray-900">2,500+</div>
            <div className="text-sm text-gray-600">Active Students</div>
          </div>
          <div className="text-center p-4 bg-white rounded-lg shadow-sm">
            <BookOpen className="w-8 h-8 text-green-600 mx-auto mb-2" />
            <div className="text-2xl font-bold text-gray-900">1,200+</div>
            <div className="text-sm text-gray-600">Study Notes</div>
          </div>
          <div className="text-center p-4 bg-white rounded-lg shadow-sm">
            <Brain className="w-8 h-8 text-yellow-600 mx-auto mb-2" />
            <div className="text-2xl font-bold text-gray-900">5,000+</div>
            <div className="text-sm text-gray-600">Quizzes Generated</div>
          </div>
          <div className="text-center p-4 bg-white rounded-lg shadow-sm">
            <Trophy className="w-8 h-8 text-purple-600 mx-auto mb-2" />
            <div className="text-2xl font-bold text-gray-900">98%</div>
            <div className="text-sm text-gray-600">Success Rate</div>
          </div>
        </div>

        {/* Recent Activity */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Clock className="w-5 h-5" />
              Continue Where You Left Off
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div>
                  <h4 className="font-medium">Mathematics - Calculus Notes</h4>
                  <p className="text-sm text-gray-600">Last accessed 2 hours ago</p>
                </div>
                <Button variant="outline" size="sm">
                  Continue
                </Button>
              </div>
              <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div>
                  <h4 className="font-medium">Physics Quiz - Mechanics</h4>
                  <p className="text-sm text-gray-600">Score: 85% (3 days ago)</p>
                </div>
                <Button variant="outline" size="sm">
                  Retake
                </Button>
              </div>
              <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div>
                  <h4 className="font-medium">Chemistry Past Questions 2023</h4>
                  <p className="text-sm text-gray-600">Completed 15/20 questions</p>
                </div>
                <Button variant="outline" size="sm">
                  Resume
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      </main>
    </div>
  )
}
