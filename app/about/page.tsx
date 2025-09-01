import { Navbar } from "@/components/navbar"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { BookOpen, Users, Target, Heart, Award, Globe } from "lucide-react"

export default function AboutPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-green-50">
      <Navbar />

      <main className="container mx-auto px-4 pt-24 pb-12">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">About EduAccess</h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto mb-8">
            Democratizing quality education across Africa through technology, community, and shared knowledge.
          </p>
        </div>

        {/* Mission Section */}
        <div className="grid md:grid-cols-2 gap-8 mb-12">
          <Card className="h-full">
            <CardHeader>
              <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mb-4">
                <Target className="w-6 h-6 text-blue-600" />
              </div>
              <CardTitle className="text-2xl">Our Mission</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-600 leading-relaxed">
                To break down educational barriers and provide every student in Africa with access to quality learning
                resources, regardless of their economic background or geographical location. We believe education is a
                fundamental right, not a privilege.
              </p>
            </CardContent>
          </Card>

          <Card className="h-full">
            <CardHeader>
              <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mb-4">
                <Heart className="w-6 h-6 text-green-600" />
              </div>
              <CardTitle className="text-2xl">Our Vision</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-600 leading-relaxed">
                A future where every African student has the tools and resources needed to excel academically,
                contribute to their communities, and drive sustainable development across the continent through quality
                education and knowledge sharing.
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Features Section */}
        <div className="mb-12">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-8">What We Offer</h2>
          <div className="grid md:grid-cols-3 gap-6">
            <Card className="text-center hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <BookOpen className="w-8 h-8 text-blue-600" />
                </div>
                <CardTitle>Collaborative Notes</CardTitle>
                <CardDescription>Students and educators share comprehensive study materials</CardDescription>
              </CardHeader>
            </Card>

            <Card className="text-center hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Award className="w-8 h-8 text-green-600" />
                </div>
                <CardTitle>AI-Powered Learning</CardTitle>
                <CardDescription>
                  Personalized quizzes and assessments generated from your study materials
                </CardDescription>
              </CardHeader>
            </Card>

            <Card className="text-center hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="w-16 h-16 bg-yellow-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Globe className="w-8 h-8 text-yellow-600" />
                </div>
                <CardTitle>Past Questions Bank</CardTitle>
                <CardDescription>
                  Extensive collection of previous exam questions for effective preparation
                </CardDescription>
              </CardHeader>
            </Card>
          </div>
        </div>

        {/* Impact Section */}
        <Card className="mb-12">
          <CardHeader className="text-center">
            <CardTitle className="text-3xl">Our Impact</CardTitle>
            <CardDescription className="text-lg">Supporting SDG 4: Quality Education across Africa</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
              <div>
                <div className="text-3xl font-bold text-blue-600 mb-2">2,500+</div>
                <div className="text-gray-600">Students Reached</div>
              </div>
              <div>
                <div className="text-3xl font-bold text-green-600 mb-2">1,200+</div>
                <div className="text-gray-600">Notes Shared</div>
              </div>
              <div>
                <div className="text-3xl font-bold text-yellow-600 mb-2">5,000+</div>
                <div className="text-gray-600">Quizzes Completed</div>
              </div>
              <div>
                <div className="text-3xl font-bold text-purple-600 mb-2">15+</div>
                <div className="text-gray-600">Countries</div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Team Section */}
        <div className="text-center">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">Built for Hackathon</h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto mb-8">
            EduAccess was created as part of a hackathon focused on achieving SDG 4: Quality Education. Our team is
            passionate about leveraging technology to solve real-world educational challenges in Africa.
          </p>
          <div className="bg-white rounded-lg p-6 shadow-sm">
            <div className="flex items-center justify-center gap-2 text-gray-600">
              <Users className="w-5 h-5" />
              <span className="font-medium">Made with ❤️ for African Students</span>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
