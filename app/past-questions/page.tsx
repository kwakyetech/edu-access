"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"
import { FileText, Search, Download, Eye, Filter, Calendar, BookOpen } from "lucide-react"
import Navbar from "@/components/navbar"

const pastQuestions = [
  {
    id: 1,
    title: "WASSCE Mathematics 2023",
    subject: "Mathematics",
    year: "2023",
    exam: "WASSCE",
    level: "SHS",
    questions: 50,
    downloads: 1234,
    rating: 4.8,
    hasAnswers: true,
  },
  {
    id: 2,
    title: "BECE Science 2023",
    subject: "Science",
    year: "2023",
    exam: "BECE",
    level: "JHS",
    questions: 40,
    downloads: 892,
    rating: 4.6,
    hasAnswers: true,
  },
  {
    id: 3,
    title: "University of Ghana Physics 2022",
    subject: "Physics",
    year: "2022",
    exam: "University",
    level: "University",
    questions: 30,
    downloads: 567,
    rating: 4.9,
    hasAnswers: false,
  },
  {
    id: 4,
    title: "WASSCE Chemistry 2022",
    subject: "Chemistry",
    year: "2022",
    exam: "WASSCE",
    level: "SHS",
    questions: 45,
    downloads: 1089,
    rating: 4.7,
    hasAnswers: true,
  },
  {
    id: 5,
    title: "BECE Mathematics 2022",
    subject: "Mathematics",
    year: "2022",
    exam: "BECE",
    level: "JHS",
    questions: 40,
    downloads: 756,
    rating: 4.5,
    hasAnswers: true,
  },
  {
    id: 6,
    title: "KNUST Engineering Mathematics 2023",
    subject: "Mathematics",
    year: "2023",
    exam: "University",
    level: "University",
    questions: 25,
    downloads: 423,
    rating: 4.8,
    hasAnswers: false,
  },
]

export default function PastQuestionsPage() {
  const [searchTerm, setSearchTerm] = useState("")
  const [selectedSubject, setSelectedSubject] = useState("all")
  const [selectedYear, setSelectedYear] = useState("all")
  const [selectedLevel, setSelectedLevel] = useState("all")

  const filteredQuestions = pastQuestions.filter((question) => {
    const matchesSearch =
      question.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      question.subject.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesSubject = selectedSubject === "all" || question.subject.toLowerCase() === selectedSubject
    const matchesYear = selectedYear === "all" || question.year === selectedYear
    const matchesLevel = selectedLevel === "all" || question.level.toLowerCase() === selectedLevel.toLowerCase()

    return matchesSearch && matchesSubject && matchesYear && matchesLevel
  })

  return (
    <div className="min-h-screen bg-background">
      <Navbar />

      <main className="max-w-6xl mx-auto px-4 py-8">
        {/* Hero Section */}
        <div className="text-center mb-8">
          <FileText className="w-16 h-16 mx-auto mb-4 text-chart-4" />
          <h1 className="text-4xl font-bold text-foreground mb-4 text-balance">Past Questions Bank</h1>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto text-pretty">
            Access comprehensive collection of past exam questions from WASSCE, BECE, and university exams. Practice
            with real questions and detailed solutions.
          </p>
        </div>

        {/* Search and Filters */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Filter className="w-5 h-5" />
              Search & Filter
            </CardTitle>
            <CardDescription>Find the exact past questions you need for your exam preparation.</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-2 lg:grid-cols-5 gap-4">
              <div className="lg:col-span-2">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground w-4 h-4" />
                  <Input
                    placeholder="Search questions, subjects, or exams..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="pl-10"
                  />
                </div>
              </div>

              <Select value={selectedSubject} onValueChange={setSelectedSubject}>
                <SelectTrigger>
                  <SelectValue placeholder="Subject" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Subjects</SelectItem>
                  <SelectItem value="mathematics">Mathematics</SelectItem>
                  <SelectItem value="physics">Physics</SelectItem>
                  <SelectItem value="chemistry">Chemistry</SelectItem>
                  <SelectItem value="biology">Biology</SelectItem>
                  <SelectItem value="english">English</SelectItem>
                  <SelectItem value="science">Science</SelectItem>
                </SelectContent>
              </Select>

              <Select value={selectedYear} onValueChange={setSelectedYear}>
                <SelectTrigger>
                  <SelectValue placeholder="Year" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Years</SelectItem>
                  <SelectItem value="2023">2023</SelectItem>
                  <SelectItem value="2022">2022</SelectItem>
                  <SelectItem value="2021">2021</SelectItem>
                  <SelectItem value="2020">2020</SelectItem>
                  <SelectItem value="2019">2019</SelectItem>
                </SelectContent>
              </Select>

              <Select value={selectedLevel} onValueChange={setSelectedLevel}>
                <SelectTrigger>
                  <SelectValue placeholder="Level" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Levels</SelectItem>
                  <SelectItem value="jhs">Junior High School</SelectItem>
                  <SelectItem value="shs">Senior High School</SelectItem>
                  <SelectItem value="university">University</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </CardContent>
        </Card>

        {/* Results Summary */}
        <div className="flex items-center justify-between mb-6">
          <p className="text-muted-foreground">
            Showing {filteredQuestions.length} of {pastQuestions.length} past questions
          </p>
          <Select defaultValue="newest">
            <SelectTrigger className="w-48">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="newest">Newest First</SelectItem>
              <SelectItem value="oldest">Oldest First</SelectItem>
              <SelectItem value="popular">Most Downloaded</SelectItem>
              <SelectItem value="rating">Highest Rated</SelectItem>
            </SelectContent>
          </Select>
        </div>

        {/* Questions Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredQuestions.map((question) => (
            <Card key={question.id} className="hover:shadow-lg transition-all duration-300">
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <CardTitle className="text-lg mb-2">{question.title}</CardTitle>
                    <div className="flex flex-wrap gap-2 mb-3">
                      <Badge variant="secondary">{question.exam}</Badge>
                      <Badge variant="outline">{question.level}</Badge>
                      {question.hasAnswers && <Badge className="bg-accent text-accent-foreground">With Answers</Badge>}
                    </div>
                  </div>
                </div>

                <div className="space-y-2 text-sm text-muted-foreground">
                  <div className="flex items-center gap-2">
                    <BookOpen className="w-4 h-4" />
                    <span>{question.subject}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Calendar className="w-4 h-4" />
                    <span>{question.year}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <FileText className="w-4 h-4" />
                    <span>{question.questions} questions</span>
                  </div>
                </div>
              </CardHeader>

              <CardContent>
                <div className="flex items-center justify-between mb-4 text-sm text-muted-foreground">
                  <span>{question.downloads.toLocaleString()} downloads</span>
                  <div className="flex items-center gap-1">
                    <span>★</span>
                    <span>{question.rating}</span>
                  </div>
                </div>

                <div className="flex gap-2">
                  <Button size="sm" variant="outline" className="flex-1 bg-transparent">
                    <Eye className="w-4 h-4 mr-1" />
                    Preview
                  </Button>
                  <Button size="sm" className="flex-1">
                    <Download className="w-4 h-4 mr-1" />
                    Download
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Popular Categories */}
        <Card className="mt-12">
          <CardHeader>
            <CardTitle>Popular Categories</CardTitle>
            <CardDescription>Browse past questions by popular exam categories</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
              <Card className="p-4 text-center hover:shadow-md transition-shadow cursor-pointer">
                <h3 className="font-semibold mb-2">WASSCE</h3>
                <p className="text-2xl font-bold text-primary mb-1">124</p>
                <p className="text-sm text-muted-foreground">Past Questions</p>
              </Card>

              <Card className="p-4 text-center hover:shadow-md transition-shadow cursor-pointer">
                <h3 className="font-semibold mb-2">BECE</h3>
                <p className="text-2xl font-bold text-secondary mb-1">89</p>
                <p className="text-sm text-muted-foreground">Past Questions</p>
              </Card>

              <Card className="p-4 text-center hover:shadow-md transition-shadow cursor-pointer">
                <h3 className="font-semibold mb-2">University</h3>
                <p className="text-2xl font-bold text-chart-4 mb-1">67</p>
                <p className="text-sm text-muted-foreground">Past Questions</p>
              </Card>

              <Card className="p-4 text-center hover:shadow-md transition-shadow cursor-pointer">
                <h3 className="font-semibold mb-2">Professional</h3>
                <p className="text-2xl font-bold text-accent mb-1">34</p>
                <p className="text-sm text-muted-foreground">Past Questions</p>
              </Card>
            </div>
          </CardContent>
        </Card>
      </main>
    </div>
  )
}
