"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Upload, FileText, Plus, X } from "lucide-react"
import Navbar from "@/components/navbar"

export default function UploadNotesPage() {
  const [uploadMethod, setUploadMethod] = useState<"file" | "paste">("file")
  const [tags, setTags] = useState<string[]>([])
  const [newTag, setNewTag] = useState("")

  const addTag = () => {
    if (newTag.trim() && !tags.includes(newTag.trim())) {
      setTags([...tags, newTag.trim()])
      setNewTag("")
    }
  }

  const removeTag = (tagToRemove: string) => {
    setTags(tags.filter((tag) => tag !== tagToRemove))
  }

  return (
    <div className="min-h-screen bg-background">
      <Navbar />

      <main className="max-w-4xl mx-auto px-4 py-8">
        {/* Hero Section */}
        <div className="text-center mb-8">
          <Upload className="w-16 h-16 mx-auto mb-4 text-secondary" />
          <h1 className="text-4xl font-bold text-foreground mb-4 text-balance">Upload & Share Notes</h1>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto text-pretty">
            Share your study materials with the community and help fellow students succeed. Upload files or paste your
            notes directly.
          </p>
        </div>

        {/* Upload Form */}
        <Card>
          <CardHeader>
            <CardTitle>Add New Notes</CardTitle>
            <CardDescription>Choose how you'd like to share your notes with the community.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Upload Method Selection */}
            <div className="grid md:grid-cols-2 gap-4">
              <Card
                className={`cursor-pointer transition-all ${uploadMethod === "file" ? "ring-2 ring-secondary" : ""}`}
                onClick={() => setUploadMethod("file")}
              >
                <CardContent className="p-4 text-center">
                  <Upload className="w-8 h-8 mx-auto mb-2 text-secondary" />
                  <h3 className="font-semibold">Upload File</h3>
                  <p className="text-sm text-muted-foreground">Upload PDF, DOC, or image files</p>
                </CardContent>
              </Card>

              <Card
                className={`cursor-pointer transition-all ${uploadMethod === "paste" ? "ring-2 ring-secondary" : ""}`}
                onClick={() => setUploadMethod("paste")}
              >
                <CardContent className="p-4 text-center">
                  <FileText className="w-8 h-8 mx-auto mb-2 text-secondary" />
                  <h3 className="font-semibold">Paste Text</h3>
                  <p className="text-sm text-muted-foreground">Type or paste your notes directly</p>
                </CardContent>
              </Card>
            </div>

            {/* Note Details */}
            <div className="grid md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="title">Note Title *</Label>
                <Input id="title" placeholder="e.g., Mathematics - Calculus Basics" />
              </div>

              <div className="space-y-2">
                <Label htmlFor="subject">Subject *</Label>
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
            </div>

            <div className="grid md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="level">Academic Level *</Label>
                <Select>
                  <SelectTrigger>
                    <SelectValue placeholder="Select level" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="jhs">Junior High School</SelectItem>
                    <SelectItem value="shs">Senior High School</SelectItem>
                    <SelectItem value="university">University</SelectItem>
                    <SelectItem value="professional">Professional</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="year">Year/Grade</Label>
                <Input id="year" placeholder="e.g., Form 2, Year 1" />
              </div>
            </div>

            {/* Content Upload */}
            {uploadMethod === "file" ? (
              <div className="space-y-2">
                <Label htmlFor="file">Upload File *</Label>
                <div className="border-2 border-dashed border-border rounded-lg p-8 text-center">
                  <Upload className="w-12 h-12 mx-auto mb-4 text-muted-foreground" />
                  <p className="text-muted-foreground mb-2">Drag and drop your file here, or click to browse</p>
                  <p className="text-sm text-muted-foreground">Supports PDF, DOC, DOCX, JPG, PNG (Max 10MB)</p>
                  <Input type="file" className="hidden" id="file" accept=".pdf,.doc,.docx,.jpg,.jpeg,.png" />
                  <Button
                    variant="outline"
                    className="mt-4 bg-transparent"
                    onClick={() => document.getElementById("file")?.click()}
                  >
                    Choose File
                  </Button>
                </div>
              </div>
            ) : (
              <div className="space-y-2">
                <Label htmlFor="content">Note Content *</Label>
                <Textarea id="content" placeholder="Paste or type your notes here..." className="min-h-[200px]" />
              </div>
            )}

            {/* Tags */}
            <div className="space-y-2">
              <Label>Tags (Optional)</Label>
              <div className="flex gap-2 mb-2">
                <Input
                  placeholder="Add a tag..."
                  value={newTag}
                  onChange={(e) => setNewTag(e.target.value)}
                  onKeyPress={(e) => e.key === "Enter" && addTag()}
                />
                <Button onClick={addTag} size="sm">
                  <Plus className="w-4 h-4" />
                </Button>
              </div>
              {tags.length > 0 && (
                <div className="flex flex-wrap gap-2">
                  {tags.map((tag) => (
                    <span
                      key={tag}
                      className="bg-secondary/20 text-secondary px-2 py-1 rounded-md text-sm flex items-center gap-1"
                    >
                      {tag}
                      <button onClick={() => removeTag(tag)} className="hover:text-destructive">
                        <X className="w-3 h-3" />
                      </button>
                    </span>
                  ))}
                </div>
              )}
            </div>

            {/* Description */}
            <div className="space-y-2">
              <Label htmlFor="description">Description (Optional)</Label>
              <Textarea id="description" placeholder="Brief description of what these notes cover..." rows={3} />
            </div>

            {/* Submit Button */}
            <div className="flex gap-4 pt-4">
              <Button className="flex-1">
                <Upload className="w-4 h-4 mr-2" />
                Upload Notes
              </Button>
              <Button variant="outline">Save as Draft</Button>
            </div>
          </CardContent>
        </Card>

        {/* Recent Uploads */}
        <Card className="mt-8">
          <CardHeader>
            <CardTitle>Your Recent Uploads</CardTitle>
            <CardDescription>Track your contributions to the community</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center justify-between p-4 border border-border rounded-lg">
                <div>
                  <h4 className="font-medium">Physics - Wave Motion</h4>
                  <p className="text-sm text-muted-foreground">Uploaded 2 days ago • 15 downloads</p>
                </div>
                <div className="text-right">
                  <p className="text-sm font-medium text-accent">+50 points</p>
                  <p className="text-xs text-muted-foreground">Approved</p>
                </div>
              </div>

              <div className="flex items-center justify-between p-4 border border-border rounded-lg">
                <div>
                  <h4 className="font-medium">Mathematics - Trigonometry</h4>
                  <p className="text-sm text-muted-foreground">Uploaded 1 week ago • 32 downloads</p>
                </div>
                <div className="text-right">
                  <p className="text-sm font-medium text-accent">+50 points</p>
                  <p className="text-xs text-muted-foreground">Approved</p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </main>
    </div>
  )
}
