"use client"

import { useState } from "react"
import LoginPage from "@/components/login-page"
import GradeCalculator from "@/components/grade-calculator"

export default function Home() {
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [user, setUser] = useState("")

  const handleLogin = (username: string) => {
    setIsLoggedIn(true)
    setUser(username)
  }

  const handleLogout = () => {
    setIsLoggedIn(false)
    setUser("")
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {!isLoggedIn ? <LoginPage onLogin={handleLogin} /> : <GradeCalculator user={user} onLogout={handleLogout} />}
    </div>
  )
}
"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { LogOut, Plus, Trash2, Calculator, Award } from "lucide-react"

interface Subject {
  id: number
  name: string
  marks: number
}

interface GradeCalculatorProps {
  user: string
  onLogout: () => void
}

export default function GradeCalculator({ user, onLogout }: GradeCalculatorProps) {
  const [subjects, setSubjects] = useState<Subject[]>([
    { id: 1, name: "Mathematics", marks: 0 },
    { id: 2, name: "Science", marks: 0 },
    { id: 3, name: "English", marks: 0 },
  ])
  const [newSubjectName, setNewSubjectName] = useState("")
  const [results, setResults] = useState<{
    totalMarks: number
    averagePercentage: number
    grade: string
    gradeColor: string
  } | null>(null)

  const addSubject = () => {
    if (newSubjectName.trim()) {
      const newSubject: Subject = {
        id: Date.now(),
        name: newSubjectName.trim(),
        marks: 0,
      }
      setSubjects([...subjects, newSubject])
      setNewSubjectName("")
    }
  }

  const removeSubject = (id: number) => {
    if (subjects.length > 1) {
      setSubjects(subjects.filter((subject) => subject.id !== id))
    }
  }

  const updateMarks = (id: number, marks: number) => {
    if (marks >= 0 && marks <= 100) {
      setSubjects(subjects.map((subject) => (subject.id === id ? { ...subject, marks } : subject)))
    }
  }

  const calculateGrade = (percentage: number): { grade: string; color: string } => {
    if (percentage >= 90) return { grade: "A+", color: "bg-green-500" }
    if (percentage >= 80) return { grade: "A", color: "bg-green-400" }
    if (percentage >= 70) return { grade: "B+", color: "bg-blue-500" }
    if (percentage >= 60) return { grade: "B", color: "bg-blue-400" }
    if (percentage >= 50) return { grade: "C", color: "bg-yellow-500" }
    return { grade: "F", color: "bg-red-500" }
  }

  const calculateResults = () => {
    const totalMarks = subjects.reduce((sum, subject) => sum + subject.marks, 0)
    const averagePercentage = totalMarks / subjects.length
    const { grade, color } = calculateGrade(averagePercentage)

    setResults({
      totalMarks,
      averagePercentage: Math.round(averagePercentage * 100) / 100,
      grade,
      gradeColor: color,
    })
  }

  const resetCalculator = () => {
    setSubjects(subjects.map((subject) => ({ ...subject, marks: 0 })))
    setResults(null)
  }

  return (
    <div className="min-h-screen p-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="flex justify-between items-center mb-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-800">Grade Calculator</h1>
            <p className="text-gray-600">Welcome back, {user}!</p>
          </div>
          <Button variant="outline" onClick={onLogout}>
            <LogOut className="h-4 w-4 mr-2" />
            Logout
          </Button>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          {/* Input Section */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Calculator className="h-5 w-5 mr-2" />
                Enter Marks
              </CardTitle>
              <CardDescription>Enter marks for each subject (out of 100)</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Add New Subject */}
              <div className="flex gap-2">
                <Input
                  placeholder="Subject name"
                  value={newSubjectName}
                  onChange={(e) => setNewSubjectName(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && addSubject()}
                />
                <Button onClick={addSubject} size="sm">
                  <Plus className="h-4 w-4" />
                </Button>
              </div>

              {/* Subjects List */}
              <div className="space-y-3">
                {subjects.map((subject) => (
                  <div key={subject.id} className="flex items-center gap-2">
                    <div className="flex-1">
                      <Label className="text-sm font-medium">{subject.name}</Label>
                      <Input
                        type="number"
                        min="0"
                        max="100"
                        value={subject.marks || ""}
                        onChange={(e) => updateMarks(subject.id, Number.parseInt(e.target.value) || 0)}
                        placeholder="0-100"
                        className="mt-1"
                      />
                    </div>
                    {subjects.length > 1 && (
                      <Button variant="outline" size="sm" onClick={() => removeSubject(subject.id)} className="mt-6">
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    )}
                  </div>
                ))}
              </div>

              {/* Action Buttons */}
              <div className="flex gap-2 pt-4">
                <Button onClick={calculateResults} className="flex-1">
                  Calculate Grade
                </Button>
                <Button variant="outline" onClick={resetCalculator}>
                  Reset
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Results Section */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Award className="h-5 w-5 mr-2" />
                Results
              </CardTitle>
              <CardDescription>Your calculated grades and performance</CardDescription>
            </CardHeader>
            <CardContent>
              {results ? (
                <div className="space-y-6">
                  {/* Summary Cards */}
                  <div className="grid grid-cols-2 gap-4">
                    <div className="bg-blue-50 p-4 rounded-lg">
                      <p className="text-sm text-blue-600 font-medium">Total Marks</p>
                      <p className="text-2xl font-bold text-blue-800">
                        {results.totalMarks}/{subjects.length * 100}
                      </p>
                    </div>
                    <div className="bg-purple-50 p-4 rounded-lg">
                      <p className="text-sm text-purple-600 font-medium">Average %</p>
                      <p className="text-2xl font-bold text-purple-800">{results.averagePercentage}%</p>
                    </div>
                  </div>

                  {/* Grade Badge */}
                  <div className="text-center">
                    <p className="text-sm text-gray-600 mb-2">Your Grade</p>
                    <Badge className={`${results.gradeColor} text-white text-2xl px-6 py-2`}>{results.grade}</Badge>
                  </div>

                  {/* Subject Breakdown */}
                  <div>
                    <h4 className="font-semibold mb-3">Subject Breakdown</h4>
                    <div className="space-y-2">
                      {subjects.map((subject) => (
                        <div key={subject.id} className="flex justify-between items-center p-2 bg-gray-50 rounded">
                          <span className="font-medium">{subject.name}</span>
                          <span className="text-lg font-bold">{subject.marks}/100</span>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Grade Scale */}
                  <div>
                    <h4 className="font-semibold mb-3">Grade Scale</h4>
                    <div className="text-sm space-y-1">
                      <div className="flex justify-between">
                        <span>A+ (90-100%)</span>
                        <span>Excellent</span>
                      </div>
                      <div className="flex justify-between">
                        <span>A (80-89%)</span>
                        <span>Very Good</span>
                      </div>
                      <div className="flex justify-between">
                        <span>B+ (70-79%)</span>
                        <span>Good</span>
                      </div>
                      <div className="flex justify-between">
                        <span>B (60-69%)</span>
                        <span>Satisfactory</span>
                      </div>
                      <div className="flex justify-between">
                        <span>C (50-59%)</span>
                        <span>Pass</span>
                      </div>
                      <div className="flex justify-between">
                        <span>F (Below 50%)</span>
                        <span>Fail</span>
                      </div>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="text-center py-12">
                  <Calculator className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-500">Enter marks and click "Calculate Grade" to see results</p>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { GraduationCap, User, Lock } from "lucide-react"

interface LoginPageProps {
  onLogin: (username: string) => void
}

export default function LoginPage({ onLogin }: LoginPageProps) {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState("")

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()

    if (!username.trim()) {
      setError("Please enter a username")
      return
    }

    if (!password.trim()) {
      setError("Please enter a password")
      return
    }

    // Simple validation - in real app, this would be proper authentication
    if (password.length < 4) {
      setError("Password must be at least 4 characters")
      return
    }

    setError("")
    onLogin(username)
  }

  return (
    <div className="flex items-center justify-center min-h-screen p-4">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          <div className="flex justify-center mb-4">
            <div className="p-3 bg-blue-100 rounded-full">
              <GraduationCap className="h-8 w-8 text-blue-600" />
            </div>
          </div>
          <CardTitle className="text-2xl font-bold">Grade Calculator</CardTitle>
          <CardDescription>Enter your credentials to access the grade calculation system</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="username">Username</Label>
              <div className="relative">
                <User className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                <Input
                  id="username"
                  type="text"
                  placeholder="Enter your username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="pl-10"
                />
              </div>
            </div>
            <div className="space-y-2">
              <Label htmlFor="password">Password</Label>
              <div className="relative">
                <Lock className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                <Input
                  id="password"
                  type="password"
                  placeholder="Enter your password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="pl-10"
                />
              </div>
            </div>
            {error && <div className="text-sm text-red-600 bg-red-50 p-2 rounded">{error}</div>}
            <Button type="submit" className="w-full">
              Login
            </Button>
          </form>
          <div className="mt-4 text-center text-sm text-gray-600">
            <p>Demo credentials: Any username with password length ≥ 4</p>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
