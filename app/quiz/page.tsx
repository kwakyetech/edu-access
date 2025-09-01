"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Slider } from "@/components/ui/slider"
import { Brain, Zap, FileText, Play, Settings } from "lucide-react"
import Navbar from "@/components/navbar"

export default function QuizGeneratorPage() {
  const [quizLength, setQuizLength] = useState([10])
  const [generationMethod, setGenerationMethod] = useState<"upload" | "paste" | "topic">("topic")

  return (
    <div className="min-h-screen bg-background">
      <Navbar />

      <main className="max-w-4xl mx-auto px-4 py-8">
        {/* Hero Section */}
        <div className="text-center mb-8">
          <Brain className="w-16 h-16 mx-auto mb-4 text-primary" />
          <h1 className="text-4xl font-bold text-foreground mb-4 text-balance">AI Quiz Generator</h1>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto text-pretty">
            Generate personalized quizzes from your notes or topics using advanced AI. Perfect for exam preparation and
            knowledge testing.
          </p>
        </div>

        {/* Quiz Generation Options */}
        <div className="grid md:grid-cols-3 gap-4 mb-8">
          <Card
            className={`cursor-pointer transition-all ${generationMethod === "topic" ? "ring-2 ring-primary" : ""}`}
            onClick={() => setGenerationMethod("topic")}
          >
            <CardContent className="p-4 text-center">
              <Zap className="w-8 h-8 mx-auto mb-2 text-primary" />
              <h3 className="font-semibold">From Topic</h3>
              <p className="text-sm text-muted-foreground">Enter a topic and let AI create questions</p>
            </CardContent>
          </Card>

          <Card
            className={`cursor-pointer transition-all ${generationMethod === "paste" ? "ring-2 ring-primary" : ""}`}
            onClick={() => setGenerationMethod("paste")}
          >
            <CardContent className="p-4 text-center">
              <FileText className="w-8 h-8 mx-auto mb-2 text-primary" />
              <h3 className="font-semibold">From Notes</h3>
              <p className="text-sm text-muted-foreground">Paste your notes to generate questions</p>
            </CardContent>
          </Card>

          <Card
            className={`cursor-pointer transition-all ${generationMethod === "upload" ? "ring-2 ring-primary" : ""}`}
            onClick={() => setGenerationMethod("upload")}
          >
            <CardContent className="p-4 text-center">
              <FileText className="w-8 h-8 mx-auto mb-2 text-primary" />
              <h3 className="font-semibold">Upload File</h3>
              <p className="text-sm text-muted-foreground">Upload a document to extract questions</p>
            </CardContent>
          </Card>
        </div>

        {/* Quiz Configuration */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Settings className="w-5 h-5" />
              Quiz Configuration
            </CardTitle>
            <CardDescription>Customize your quiz settings for the best learning experience.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Content Input */}
            {generationMethod === "topic" && (
              <div className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="topic">Topic or Subject *</Label>
                  <Input id="topic" placeholder="e.g., Photosynthesis, Quadratic Equations, World War II" />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="context">Additional Context (Optional)</Label>
                  <Textarea
                    id="context"
                    placeholder="Provide specific areas to focus on or learning objectives..."
                    rows={3}
                  />
                </div>
              </div>
            )}

            {generationMethod === "paste" && (
              <div className="space-y-2">
                <Label htmlFor="notes">Paste Your Notes *</Label>
                <Textarea
                  id="notes"
                  placeholder="Paste your study notes here and AI will generate questions based on the content..."
                  className="min-h-[200px]"
                />
              </div>
            )}

            {generationMethod === "upload" && (
              <div className="space-y-2">
                <Label htmlFor="file">Upload Document *</Label>
                <div className="border-2 border-dashed border-border rounded-lg p-8 text-center">
                  <FileText className="w-12 h-12 mx-auto mb-4 text-muted-foreground" />
                  <p className="text-muted-foreground mb-2">Upload your notes or study materials</p>
                  <p className="text-sm text-muted-foreground">Supports PDF, DOC, DOCX, TXT (Max 10MB)</p>
                  <Input type="file" className="hidden" id="file" accept=".pdf,.doc,.docx,.txt" />
                  <Button
                    variant="outline"
                    className="mt-4 bg-transparent"
                    onClick={() => document.getElementById("file")?.click()}
                  >
                    Choose File
                  </Button>
                </div>
              </div>
            )}

            {/* Quiz Settings */}
            <div className="grid md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="subject">Subject Category</Label>
                <Select>
                  <SelectTrigger>
                    <SelectValue placeholder="Select subject" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="mathematics">Mathematics</SelectItem>
                    <SelectItem value="physics">Physics</SelectItem>
                    <SelectItem value="chemistry">Chemistry</SelectItem>
                    <SelectItem value="biology">Biology</SelectItem>
                    <SelectItem value="english">English</SelectItem>
                    <SelectItem value="history">History</SelectItem>
                    <SelectItem value="geography">Geography</SelectItem>
                    <SelectItem value="economics">Economics</SelectItem>
                    <SelectItem value="other">Other</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="difficulty">Difficulty Level</Label>
                <Select>
                  <SelectTrigger>
                    <SelectValue placeholder="Select difficulty" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="easy">Easy</SelectItem>
                    <SelectItem value="medium">Medium</SelectItem>
                    <SelectItem value="hard">Hard</SelectItem>
                    <SelectItem value="mixed">Mixed</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div className="space-y-2">
              <Label>Number of Questions: {quizLength[0]}</Label>
              <Slider value={quizLength} onValueChange={setQuizLength} max={50} min={5} step={5} className="w-full" />
              <div className="flex justify-between text-sm text-muted-foreground">
                <span>5 questions</span>
                <span>50 questions</span>
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="question-types">Question Types</Label>
              <Select>
                <SelectTrigger>
                  <SelectValue placeholder="Select question type" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="multiple-choice">Multiple Choice Only</SelectItem>
                  <SelectItem value="true-false">True/False Only</SelectItem>
                  <SelectItem value="short-answer">Short Answer Only</SelectItem>
                  <SelectItem value="mixed">Mixed Types</SelectItem>
                </SelectContent>
              </Select>
            </div>

            {/* Generate Button */}
            <div className="flex gap-4 pt-4">
              <Button className="flex-1">
                <Brain className="w-4 h-4 mr-2" />
                Generate Quiz
              </Button>
              <Button variant="outline">Save Settings</Button>
            </div>
          </CardContent>
        </Card>

        {/* Recent Quizzes */}
        <Card className="mt-8">
          <CardHeader>
            <CardTitle>Your Recent Quizzes</CardTitle>
            <CardDescription>Access your previously generated quizzes</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center justify-between p-4 border border-border rounded-lg">
                <div>
                  <h4 className="font-medium">Physics - Wave Motion Quiz</h4>
                  <p className="text-sm text-muted-foreground">15 questions • Created 2 days ago</p>
                </div>
                <div className="flex gap-2">
                  <Button size="sm" variant="outline">
                    <Play className="w-4 h-4 mr-1" />
                    Retake
                  </Button>
                  <Button size="sm">View Results</Button>
                </div>
              </div>

              <div className="flex items-center justify-between p-4 border border-border rounded-lg">
                <div>
                  <h4 className="font-medium">Mathematics - Calculus Quiz</h4>
                  <p className="text-sm text-muted-foreground">20 questions • Created 1 week ago</p>
                </div>
                <div className="flex gap-2">
                  <Button size="sm" variant="outline">
                    <Play className="w-4 h-4 mr-1" />
                    Retake
                  </Button>
                  <Button size="sm">View Results</Button>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </main>
    </div>
  )
}
