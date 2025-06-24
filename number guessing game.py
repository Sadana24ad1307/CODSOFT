import { type NextRequest, NextResponse } from "next/server"

// In-memory storage (in production, use a database)
const games = new Map<
  string,
  {
    targetNumber: number
    attempts: number
    maxAttempts: number
    status: "playing" | "won" | "lost"
    minRange: number
    maxRange: number
  }
>()

const playerStats = new Map<
  string,
  {
    totalGames: number
    gamesWon: number
    totalScore: number
    bestStreak: number
    currentStreak: number
  }
>()

export async function POST(request: NextRequest) {
  try {
    const { action, gameId, guess, playerId } = await request.json()

    switch (action) {
      case "start":
        const targetNumber = Math.floor(Math.random() * 100) + 1
        const newGameId = Math.random().toString(36).substring(7)

        games.set(newGameId, {
          targetNumber,
          attempts: 0,
          maxAttempts: 7,
          status: "playing",
          minRange: 1,
          maxRange: 100,
        })

        return NextResponse.json({
          success: true,
          gameId: newGameId,
          message: "New game started! Guess a number between 1 and 100.",
          maxAttempts: 7,
        })

      case "guess":
        const game = games.get(gameId)
        if (!game) {
          return NextResponse.json({ success: false, message: "Game not found" })
        }

        if (game.status !== "playing") {
          return NextResponse.json({ success: false, message: "Game is already finished" })
        }

        const guessNumber = Number.parseInt(guess)
        if (isNaN(guessNumber) || guessNumber < 1 || guessNumber > 100) {
          return NextResponse.json({ success: false, message: "Please enter a valid number between 1 and 100" })
        }

        game.attempts++
        let message = ""
        let gameEnded = false
        let score = 0

        if (guessNumber === game.targetNumber) {
          game.status = "won"
          score = Math.max(100 - (game.attempts - 1) * 10, 10)
          message = `🎉 Congratulations! You guessed it in ${game.attempts} attempt${game.attempts === 1 ? "" : "s"}!`
          gameEnded = true

          // Update player stats
          updatePlayerStats(playerId, true, score)
        } else if (game.attempts >= game.maxAttempts) {
          game.status = "lost"
          message = `😔 Game over! The number was ${game.targetNumber}.`
          gameEnded = true

          // Update player stats
          updatePlayerStats(playerId, false, 0)
        } else {
          const remaining = game.maxAttempts - game.attempts
          if (guessNumber < game.targetNumber) {
            message = `📈 Too low! Try higher. ${remaining} attempt${remaining === 1 ? "" : "s"} remaining.`
          } else {
            message = `📉 Too high! Try lower. ${remaining} attempt${remaining === 1 ? "" : "s"} remaining.`
          }
        }

        return NextResponse.json({
          success: true,
          message,
          attempts: game.attempts,
          maxAttempts: game.maxAttempts,
          status: game.status,
          score,
          gameEnded,
        })

      case "stats":
        const stats = playerStats.get(playerId) || {
          totalGames: 0,
          gamesWon: 0,
          totalScore: 0,
          bestStreak: 0,
          currentStreak: 0,
        }

        return NextResponse.json({
          success: true,
          stats,
        })

      default:
        return NextResponse.json({ success: false, message: "Invalid action" })
    }
  } catch (error) {
    return NextResponse.json({ success: false, message: "Server error" })
  }
}

function updatePlayerStats(playerId: string, won: boolean, score: number) {
  const stats = playerStats.get(playerId) || {
    totalGames: 0,
    gamesWon: 0,
    totalScore: 0,
    bestStreak: 0,
    currentStreak: 0,
  }

  stats.totalGames++
  stats.totalScore += score

  if (won) {
    stats.gamesWon++
    stats.currentStreak++
    stats.bestStreak = Math.max(stats.bestStreak, stats.currentStreak)
  } else {
    stats.currentStreak = 0
  }

  playerStats.set(playerId, stats)
}
import { NextResponse } from "next/server"

// Mock leaderboard data (in production, use a database)
const leaderboard = [
  { id: "1", name: "Alex Champion", score: 2450, gamesWon: 28, winRate: 93 },
  { id: "2", name: "Sarah Genius", score: 2180, gamesWon: 24, winRate: 89 },
  { id: "3", name: "Mike Master", score: 1950, gamesWon: 22, winRate: 85 },
  { id: "4", name: "Lisa Legend", score: 1720, gamesWon: 19, winRate: 82 },
  { id: "5", name: "Tom Tactician", score: 1580, gamesWon: 17, winRate: 78 },
]

export async function GET() {
  return NextResponse.json({
    success: true,
    leaderboard: leaderboard.sort((a, b) => b.score - a.score),
  })
}
import type React from "react"
import type { Metadata } from "next"
import { Inter } from "next/font/google"
import "./globals.css"

const inter = Inter({ subsets: ["latin"] })

export const metadata: Metadata = {
  title: "GuessWise - Number Guessing Game",
  description:
    "Challenge your mind with the ultimate number guessing experience! Test your intuition and climb the leaderboard.",
  keywords: ["number guessing game", "puzzle", "brain game", "guessing game"],
  authors: [{ name: "GuessWise Team" }],
  openGraph: {
    title: "GuessWise - Number Guessing Game",
    description: "Challenge your mind with the ultimate number guessing experience!",
    type: "website",
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  )
}
"use client"

import type React from "react"
import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { RefreshCw, Trophy, Target, Zap, TrendingUp, Medal, Award } from "lucide-react"

// Logo Component
function Logo({ size = "md", showText = true }: { size?: "sm" | "md" | "lg"; showText?: boolean }) {
  const sizeClasses = {
    sm: "h-8 w-8",
    md: "h-12 w-12",
    lg: "h-16 w-16",
  }

  const textSizeClasses = {
    sm: "text-lg",
    md: "text-2xl",
    lg: "text-3xl",
  }

  return (
    <div className="flex items-center gap-3">
      <div className="relative">
        <div
          className={`${sizeClasses[size]} bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center shadow-lg`}
        >
          <Target className="h-1/2 w-1/2 text-white" />
        </div>
        <div className="absolute -top-1 -right-1 bg-yellow-400 rounded-full p-1">
          <Zap className="h-3 w-3 text-yellow-800" />
        </div>
      </div>
      {showText && (
        <div className="flex flex-col">
          <h1
            className={`${textSizeClasses[size]} font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent`}
          >
            GuessWise
          </h1>
          <p className="text-xs text-gray-500 -mt-1">Number Guessing Game</p>
        </div>
      )}
    </div>
  )
}

// Leaderboard Component
function Leaderboard() {
  const leaderboard = [
    { id: "1", name: "Alex Champion", score: 2450, gamesWon: 28, winRate: 93 },
    { id: "2", name: "Sarah Genius", score: 2180, gamesWon: 24, winRate: 89 },
    { id: "3", name: "Mike Master", score: 1950, gamesWon: 22, winRate: 85 },
    { id: "4", name: "Lisa Legend", score: 1720, gamesWon: 19, winRate: 82 },
    { id: "5", name: "Tom Tactician", score: 1580, gamesWon: 17, winRate: 78 },
  ]

  const getRankIcon = (index: number) => {
    switch (index) {
      case 0:
        return <Trophy className="h-5 w-5 text-yellow-500" />
      case 1:
        return <Medal className="h-5 w-5 text-gray-400" />
      case 2:
        return <Award className="h-5 w-5 text-amber-600" />
      default:
        return <span className="text-lg font-bold text-gray-500">#{index + 1}</span>
    }
  }

  return (
    <Card className="shadow-xl border-0 bg-white/80 backdrop-blur">
      <CardHeader>
        <CardTitle className="text-lg flex items-center gap-2">
          <Trophy className="h-5 w-5 text-yellow-500" />
          Leaderboard
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        {leaderboard.map((player, index) => (
          <div key={player.id} className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
            <div className="flex-shrink-0">{getRankIcon(index)}</div>
            <div className="flex-1 min-w-0">
              <div className="font-semibold text-gray-800 truncate">{player.name}</div>
              <div className="text-sm text-gray-600">
                {player.gamesWon} wins • {player.winRate}% rate
              </div>
            </div>
            <Badge variant="secondary" className="font-bold">
              {player.score.toLocaleString()}
            </Badge>
          </div>
        ))}
      </CardContent>
    </Card>
  )
}

// Main Game Component
export default function GuessWiseGame() {
  const [targetNumber, setTargetNumber] = useState<number>(0)
  const [userGuess, setUserGuess] = useState<string>("")
  const [attempts, setAttempts] = useState<number>(0)
  const [maxAttempts] = useState<number>(7)
  const [feedback, setFeedback] = useState<string>("")
  const [gameStatus, setGameStatus] = useState<"playing" | "won" | "lost">("playing")
  const [score, setScore] = useState<number>(0)
  const [stats, setStats] = useState({
    totalGames: 0,
    gamesWon: 0,
    totalScore: 0,
    bestStreak: 0,
    currentStreak: 0,
  })

  // Generate random number between 1 and 100
  const generateRandomNumber = () => {
    return Math.floor(Math.random() * 100) + 1
  }

  // Initialize new game
  const startNewGame = () => {
    const newTarget = generateRandomNumber()
    setTargetNumber(newTarget)
    setUserGuess("")
    setAttempts(0)
    setFeedback("🎯 I'm thinking of a number between 1 and 100. You have 7 attempts to guess it!")
    setGameStatus("playing")
    setScore(0)
  }

  // Handle guess submission
  const makeGuess = () => {
    const guess = Number.parseInt(userGuess)

    if (isNaN(guess) || guess < 1 || guess > 100) {
      setFeedback("⚠️ Please enter a valid number between 1 and 100")
      return
    }

    const newAttempts = attempts + 1
    setAttempts(newAttempts)

    if (guess === targetNumber) {
      // Player won
      setGameStatus("won")
      const roundScore = Math.max(100 - (newAttempts - 1) * 10, 10)
      setScore(roundScore)
      setFeedback(
        `🎉 Congratulations! You guessed it in ${newAttempts} attempt${newAttempts === 1 ? "" : "s"}! (+${roundScore} points)`,
      )

      // Update stats
      setStats((prev) => ({
        totalGames: prev.totalGames + 1,
        gamesWon: prev.gamesWon + 1,
        totalScore: prev.totalScore + roundScore,
        currentStreak: prev.currentStreak + 1,
        bestStreak: Math.max(prev.bestStreak, prev.currentStreak + 1),
      }))
    } else if (newAttempts >= maxAttempts) {
      // Player lost
      setGameStatus("lost")
      setFeedback(`😔 Game over! The number was ${targetNumber}. Better luck next time!`)

      // Update stats
      setStats((prev) => ({
        ...prev,
        totalGames: prev.totalGames + 1,
        currentStreak: 0,
      }))
    } else {
      // Continue playing
      const remaining = maxAttempts - newAttempts
      if (guess < targetNumber) {
        setFeedback(`📈 Too low! Try a higher number. ${remaining} attempt${remaining === 1 ? "" : "s"} remaining.`)
      } else {
        setFeedback(`📉 Too high! Try a lower number. ${remaining} attempt${remaining === 1 ? "" : "s"} remaining.`)
      }
    }

    setUserGuess("")
  }

  // Handle Enter key press
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && gameStatus === "playing") {
      makeGuess()
    }
  }

  // Initialize game on component mount
  useEffect(() => {
    startNewGame()
  }, [])

  const winRate = stats.totalGames > 0 ? Math.round((stats.gamesWon / stats.totalGames) * 100) : 0

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 p-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <Logo size="lg" />
          <p className="text-gray-600 mt-2 max-w-2xl mx-auto">
            Challenge your mind with the ultimate number guessing experience! Test your intuition, improve your
            strategy, and climb the leaderboard.
          </p>
        </div>

        <div className="grid lg:grid-cols-4 gap-8">
          {/* Main Game Area */}
          <div className="lg:col-span-3">
            <div className="grid md:grid-cols-3 gap-6">
              {/* Game Card */}
              <div className="md:col-span-2">
                <Card className="shadow-xl border-0 bg-white/90 backdrop-blur">
                  <CardHeader className="text-center">
                    <CardTitle className="text-xl font-bold text-gray-800 flex items-center justify-center gap-2">
                      <Target className="h-5 w-5 text-blue-600" />
                      Current Game
                    </CardTitle>
                    <CardDescription>Guess the number between 1 and 100</CardDescription>
                  </CardHeader>

                  <CardContent className="space-y-4">
                    {/* Current Game Stats */}
                    <div className="flex justify-between items-center">
                      <Badge variant="outline" className="flex items-center gap-1">
                        <Zap className="h-3 w-3" />
                        Attempts: {attempts}/{maxAttempts}
                      </Badge>
                      {gameStatus === "won" && (
                        <Badge className="bg-green-500 hover:bg-green-600">
                          <Trophy className="h-3 w-3 mr-1" />
                          Winner! +{score} pts
                        </Badge>
                      )}
                      {gameStatus === "lost" && <Badge variant="destructive">Game Over</Badge>}
                    </div>

                    {/* Feedback */}
                    <div className="bg-gradient-to-r from-blue-50 to-purple-50 p-4 rounded-lg text-center text-sm text-gray-700 min-h-[80px] flex items-center justify-center border-2 border-blue-100">
                      <div className="font-medium">{feedback}</div>
                    </div>

                    {/* Input and Guess Button */}
                    {gameStatus === "playing" && (
                      <div className="flex gap-2">
                        <Input
                          type="number"
                          placeholder="Enter your guess (1-100)"
                          value={userGuess}
                          onChange={(e) => setUserGuess(e.target.value)}
                          onKeyPress={handleKeyPress}
                          min={1}
                          max={100}
                          className="flex-1 text-lg"
                        />
                        <Button
                          onClick={makeGuess}
                          disabled={!userGuess.trim()}
                          className="px-8 bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white font-semibold"
                          size="lg"
                        >
                          Guess!
                        </Button>
                      </div>
                    )}

                    {/* Game Over Actions */}
                    {gameStatus !== "playing" && (
                      <div className="flex gap-2 pt-2">
                        <Button
                          onClick={startNewGame}
                          className="flex-1 bg-gradient-to-r from-green-500 to-blue-500 hover:from-green-600 hover:to-blue-600 text-white font-semibold"
                          size="lg"
                        >
                          <RefreshCw className="h-4 w-4 mr-2" />
                          Play Again
                        </Button>
                      </div>
                    )}
                  </CardContent>
                </Card>
              </div>

              {/* Stats Card */}
              <div>
                <Card className="shadow-xl border-0 bg-white/90 backdrop-blur">
                  <CardHeader>
                    <CardTitle className="text-lg flex items-center gap-2">
                      <TrendingUp className="h-5 w-5 text-green-600" />
                      Your Stats
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="grid grid-cols-1 gap-3">
                      <div className="bg-gradient-to-r from-blue-50 to-blue-100 p-3 rounded-lg text-center border border-blue-200">
                        <div className="text-2xl font-bold text-blue-600">{stats.totalScore}</div>
                        <div className="text-xs text-gray-600 font-medium">Total Score</div>
                      </div>
                      <div className="bg-gradient-to-r from-green-50 to-green-100 p-3 rounded-lg text-center border border-green-200">
                        <div className="text-2xl font-bold text-green-600">{winRate}%</div>
                        <div className="text-xs text-gray-600 font-medium">Win Rate</div>
                      </div>
                      <div className="bg-gradient-to-r from-purple-50 to-purple-100 p-3 rounded-lg text-center border border-purple-200">
                        <div className="text-2xl font-bold text-purple-600">{stats.gamesWon}</div>
                        <div className="text-xs text-gray-600 font-medium">Games Won</div>
                      </div>
                      <div className="bg-gradient-to-r from-yellow-50 to-yellow-100 p-3 rounded-lg text-center border border-yellow-200">
                        <div className="text-2xl font-bold text-yellow-600">{stats.bestStreak}</div>
                        <div className="text-xs text-gray-600 font-medium">Best Streak</div>
                      </div>
                    </div>

                    <Separator />

                    <div className="text-center bg-gradient-to-r from-orange-50 to-red-50 p-3 rounded-lg border border-orange-200">
                      <div className="text-sm text-gray-600 font-medium">Current Streak</div>
                      <div className="text-xl font-bold text-orange-600">{stats.currentStreak}</div>
                    </div>

                    <div className="text-center text-xs text-gray-500 pt-2">
                      <div>Games Played: {stats.totalGames}</div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </div>

            {/* How to Play */}
            <Card className="mt-6 shadow-lg border-0 bg-white/80 backdrop-blur">
              <CardHeader>
                <CardTitle className="text-lg">🎮 How to Play</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid md:grid-cols-2 gap-4 text-sm text-gray-600">
                  <div>
                    <h4 className="font-semibold text-gray-800 mb-2">Game Rules:</h4>
                    <ul className="space-y-1">
                      <li>• Guess a number between 1 and 100</li>
                      <li>• You have 7 attempts to find it</li>
                      <li>• Get hints: "too high" or "too low"</li>
                      <li>• Win faster for more points!</li>
                    </ul>
                  </div>
                  <div>
                    <h4 className="font-semibold text-gray-800 mb-2">Scoring:</h4>
                    <ul className="space-y-1">
                      <li>• 1st attempt: 100 points</li>
                      <li>• 2nd attempt: 90 points</li>
                      <li>• 3rd attempt: 80 points</li>
                      <li>• Minimum: 10 points</li>
                    </ul>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Leaderboard */}
          <div className="lg:col-span-1">
            <Leaderboard />
          </div>
        </div>

        {/* Footer */}
        <div className="text-center mt-12 text-gray-500 text-sm">
          <p>© 2024 GuessWise. Challenge your mind, one number at a time.</p>
        </div>
      </div>
    </div>
  )
}
"use client"

import type React from "react"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { RefreshCw, Trophy, Target, Zap, TrendingUp } from "lucide-react"
import { Logo } from "./logo"

export default function GameBoard() {
  const [gameId, setGameId] = useState<string>("")
  const [playerId] = useState<string>(() => Math.random().toString(36).substring(7))
  const [userGuess, setUserGuess] = useState<string>("")
  const [attempts, setAttempts] = useState<number>(0)
  const [maxAttempts, setMaxAttempts] = useState<number>(7)
  const [feedback, setFeedback] = useState<string>("")
  const [gameStatus, setGameStatus] = useState<"playing" | "won" | "lost">("playing")
  const [score, setScore] = useState<number>(0)
  const [totalScore, setTotalScore] = useState<number>(0)
  const [stats, setStats] = useState({
    totalGames: 0,
    gamesWon: 0,
    totalScore: 0,
    bestStreak: 0,
    currentStreak: 0,
  })
  const [loading, setLoading] = useState<boolean>(false)

  const startNewGame = async () => {
    setLoading(true)
    try {
      const response = await fetch("/api/game", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ action: "start" }),
      })

      const data = await response.json()
      if (data.success) {
        setGameId(data.gameId)
        setUserGuess("")
        setAttempts(0)
        setMaxAttempts(data.maxAttempts)
        setFeedback(data.message)
        setGameStatus("playing")
        setScore(0)
      }
    } catch (error) {
      setFeedback("Error starting game. Please try again.")
    }
    setLoading(false)
  }

  const makeGuess = async () => {
    if (!userGuess.trim() || loading) return

    setLoading(true)
    try {
      const response = await fetch("/api/game", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          action: "guess",
          gameId,
          guess: userGuess,
          playerId,
        }),
      })

      const data = await response.json()
      if (data.success) {
        setFeedback(data.message)
        setAttempts(data.attempts)
        setGameStatus(data.status)
        if (data.gameEnded) {
          setScore(data.score || 0)
          setTotalScore((prev) => prev + (data.score || 0))
          loadStats()
        }
      } else {
        setFeedback(data.message)
      }
    } catch (error) {
      setFeedback("Error making guess. Please try again.")
    }
    setUserGuess("")
    setLoading(false)
  }

  const loadStats = async () => {
    try {
      const response = await fetch("/api/game", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ action: "stats", playerId }),
      })

      const data = await response.json()
      if (data.success) {
        setStats(data.stats)
      }
    } catch (error) {
      console.error("Error loading stats:", error)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && gameStatus === "playing") {
      makeGuess()
    }
  }

  useEffect(() => {
    startNewGame()
    loadStats()
  }, [])

  const winRate = stats.totalGames > 0 ? Math.round((stats.gamesWon / stats.totalGames) * 100) : 0

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 p-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <Logo size="lg" />
          <p className="text-gray-600 mt-2">Challenge your mind with the ultimate number guessing experience!</p>
        </div>

        <div className="grid md:grid-cols-3 gap-6">
          {/* Game Card */}
          <div className="md:col-span-2">
            <Card className="shadow-xl border-0 bg-white/80 backdrop-blur">
              <CardHeader className="text-center">
                <CardTitle className="text-xl font-bold text-gray-800 flex items-center justify-center gap-2">
                  <Target className="h-5 w-5 text-blue-600" />
                  Current Game
                </CardTitle>
                <CardDescription>Guess the number between 1 and 100</CardDescription>
              </CardHeader>

              <CardContent className="space-y-4">
                {/* Current Game Stats */}
                <div className="flex justify-between items-center">
                  <Badge variant="outline" className="flex items-center gap-1">
                    <Zap className="h-3 w-3" />
                    Attempts: {attempts}/{maxAttempts}
                  </Badge>
                  {gameStatus === "won" && (
                    <Badge className="bg-green-500 hover:bg-green-600">
                      <Trophy className="h-3 w-3 mr-1" />
                      Winner! +{score} pts
                    </Badge>
                  )}
                  {gameStatus === "lost" && <Badge variant="destructive">Game Over</Badge>}
                </div>

                {/* Feedback */}
                <div className="bg-gradient-to-r from-blue-50 to-purple-50 p-4 rounded-lg text-center text-sm text-gray-700 min-h-[60px] flex items-center justify-center border">
                  {feedback}
                </div>

                {/* Input and Guess Button */}
                {gameStatus === "playing" && (
                  <div className="flex gap-2">
                    <Input
                      type="number"
                      placeholder="Enter your guess (1-100)"
                      value={userGuess}
                      onChange={(e) => setUserGuess(e.target.value)}
                      onKeyPress={handleKeyPress}
                      min={1}
                      max={100}
                      className="flex-1"
                      disabled={loading}
                    />
                    <Button
                      onClick={makeGuess}
                      disabled={!userGuess.trim() || loading}
                      className="px-6 bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700"
                    >
                      {loading ? "..." : "Guess"}
                    </Button>
                  </div>
                )}
              </CardContent>

              <CardFooter className="flex gap-2">
                <Button onClick={startNewGame} className="flex-1" variant="default" disabled={loading}>
                  <RefreshCw className="h-4 w-4 mr-2" />
                  New Game
                </Button>
              </CardFooter>
            </Card>
          </div>

          {/* Stats Card */}
          <div className="space-y-6">
            <Card className="shadow-xl border-0 bg-white/80 backdrop-blur">
              <CardHeader>
                <CardTitle className="text-lg flex items-center gap-2">
                  <TrendingUp className="h-5 w-5 text-green-600" />
                  Your Stats
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-3">
                  <div className="bg-blue-50 p-3 rounded-lg text-center">
                    <div className="text-2xl font-bold text-blue-600">{stats.totalScore}</div>
                    <div className="text-xs text-gray-600">Total Score</div>
                  </div>
                  <div className="bg-green-50 p-3 rounded-lg text-center">
                    <div className="text-2xl font-bold text-green-600">{winRate}%</div>
                    <div className="text-xs text-gray-600">Win Rate</div>
                  </div>
                  <div className="bg-purple-50 p-3 rounded-lg text-center">
                    <div className="text-2xl font-bold text-purple-600">{stats.gamesWon}</div>
                    <div className="text-xs text-gray-600">Games Won</div>
                  </div>
                  <div className="bg-yellow-50 p-3 rounded-lg text-center">
                    <div className="text-2xl font-bold text-yellow-600">{stats.bestStreak}</div>
                    <div className="text-xs text-gray-600">Best Streak</div>
                  </div>
                </div>

                <Separator />

                <div className="text-center">
                  <div className="text-sm text-gray-600">Current Streak</div>
                  <div className="text-xl font-bold text-orange-600">{stats.currentStreak}</div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}
"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Trophy, Medal, Award } from "lucide-react"

interface LeaderboardEntry {
  id: string
  name: string
  score: number
  gamesWon: number
  winRate: number
}

export function Leaderboard() {
  const [leaderboard, setLeaderboard] = useState<LeaderboardEntry[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchLeaderboard = async () => {
      try {
        const response = await fetch("/api/leaderboard")
        const data = await response.json()
        if (data.success) {
          setLeaderboard(data.leaderboard)
        }
      } catch (error) {
        console.error("Error fetching leaderboard:", error)
      }
      setLoading(false)
    }

    fetchLeaderboard()
  }, [])

  const getRankIcon = (index: number) => {
    switch (index) {
      case 0:
        return <Trophy className="h-5 w-5 text-yellow-500" />
      case 1:
        return <Medal className="h-5 w-5 text-gray-400" />
      case 2:
        return <Award className="h-5 w-5 text-amber-600" />
      default:
        return <span className="text-lg font-bold text-gray-500">#{index + 1}</span>
    }
  }

  if (loading) {
    return (
      <Card className="shadow-xl border-0 bg-white/80 backdrop-blur">
        <CardHeader>
          <CardTitle className="text-lg flex items-center gap-2">
            <Trophy className="h-5 w-5 text-yellow-500" />
            Leaderboard
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center text-gray-500">Loading...</div>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card className="shadow-xl border-0 bg-white/80 backdrop-blur">
      <CardHeader>
        <CardTitle className="text-lg flex items-center gap-2">
          <Trophy className="h-5 w-5 text-yellow-500" />
          Leaderboard
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        {leaderboard.map((player, index) => (
          <div key={player.id} className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
            <div className="flex-shrink-0">{getRankIcon(index)}</div>
            <div className="flex-1 min-w-0">
              <div className="font-semibold text-gray-800 truncate">{player.name}</div>
              <div className="text-sm text-gray-600">
                {player.gamesWon} wins • {player.winRate}% rate
              </div>
            </div>
            <Badge variant="secondary" className="font-bold">
              {player.score.toLocaleString()}
            </Badge>
          </div>
        ))}
      </CardContent>
    </Card>
  )
}
"use client"

import { Target, Zap } from "lucide-react"

interface LogoProps {
  size?: "sm" | "md" | "lg"
  showText?: boolean
}

export function Logo({ size = "md", showText = true }: LogoProps) {
  const sizeClasses = {
    sm: "h-8 w-8",
    md: "h-12 w-12",
    lg: "h-16 w-16",
  }

  const textSizeClasses = {
    sm: "text-lg",
    md: "text-2xl",
    lg: "text-3xl",
  }

  return (
    <div className="flex items-center gap-3">
      <div className="relative">
        <div
          className={`${sizeClasses[size]} bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center shadow-lg`}
        >
          <Target className="h-1/2 w-1/2 text-white" />
        </div>
        <div className="absolute -top-1 -right-1 bg-yellow-400 rounded-full p-1">
          <Zap className="h-3 w-3 text-yellow-800" />
        </div>
      </div>
      {showText && (
        <div className="flex flex-col">
          <h1
            className={`${textSizeClasses[size]} font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent`}
          >
            GuessWise
          </h1>
          <p className="text-xs text-gray-500 -mt-1">Number Guessing Game</p>
        </div>
      )}
    </div>
  )
}
-- Create database schema for GuessWise
CREATE TABLE IF NOT EXISTS players (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS games (
    id VARCHAR(36) PRIMARY KEY,
    player_id VARCHAR(36),
    target_number INTEGER NOT NULL,
    attempts INTEGER DEFAULT 0,
    max_attempts INTEGER DEFAULT 7,
    status ENUM('playing', 'won', 'lost') DEFAULT 'playing',
    score INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP NULL,
    FOREIGN KEY (player_id) REFERENCES players(id)
);

CREATE TABLE IF NOT EXISTS player_stats (
    player_id VARCHAR(36) PRIMARY KEY,
    total_games INTEGER DEFAULT 0,
    games_won INTEGER DEFAULT 0,
    total_score INTEGER DEFAULT 0,
    best_streak INTEGER DEFAULT 0,
    current_streak INTEGER DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (player_id) REFERENCES players(id)
);

CREATE TABLE IF NOT EXISTS leaderboard (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    player_id VARCHAR(36),
    player_name VARCHAR(100),
    total_score INTEGER,
    games_won INTEGER,
    win_rate DECIMAL(5,2),
    rank_position INTEGER,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (player_id) REFERENCES players(id)
);

-- Insert sample leaderboard data
INSERT INTO leaderboard (player_id, player_name, total_score, games_won, win_rate, rank_position) VALUES
('sample1', 'Alex Champion', 2450, 28, 93.33, 1),
('sample2', 'Sarah Genius', 2180, 24, 88.89, 2),
('sample3', 'Mike Master', 1950, 22, 84.62, 3),
('sample4', 'Lisa Legend', 1720, 19, 82.61, 4),
('sample5', 'Tom Tactician', 1580, 17, 77.27, 5);
"use client"

import type React from "react"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { RefreshCw, Trophy, Target, Zap } from "lucide-react"

export default function NumberGuessingGame() {
  const [targetNumber, setTargetNumber] = useState<number>(0)
  const [userGuess, setUserGuess] = useState<string>("")
  const [attempts, setAttempts] = useState<number>(0)
  const [maxAttempts] = useState<number>(7)
  const [feedback, setFeedback] = useState<string>("")
  const [gameStatus, setGameStatus] = useState<"playing" | "won" | "lost">("playing")
  const [roundsPlayed, setRoundsPlayed] = useState<number>(0)
  const [roundsWon, setRoundsWon] = useState<number>(0)
  const [score, setScore] = useState<number>(0)
  const [minRange] = useState<number>(1)
  const [maxRange] = useState<number>(100)

  // Generate random number between min and max range
  const generateRandomNumber = () => {
    return Math.floor(Math.random() * (maxRange - minRange + 1)) + minRange
  }

  // Initialize game
  const initializeGame = () => {
    setTargetNumber(generateRandomNumber())
    setUserGuess("")
    setAttempts(0)
    setFeedback(`I'm thinking of a number between ${minRange} and ${maxRange}. You have ${maxAttempts} attempts!`)
    setGameStatus("playing")
  }

  // Start new round
  const startNewRound = () => {
    initializeGame()
    setRoundsPlayed((prev) => prev + 1)
  }

  // Reset entire game
  const resetGame = () => {
    initializeGame()
    setRoundsPlayed(0)
    setRoundsWon(0)
    setScore(0)
  }

  // Handle guess submission
  const handleGuess = () => {
    const guess = Number.parseInt(userGuess)

    if (isNaN(guess) || guess < minRange || guess > maxRange) {
      setFeedback(`Please enter a valid number between ${minRange} and ${maxRange}`)
      return
    }

    const newAttempts = attempts + 1
    setAttempts(newAttempts)

    if (guess === targetNumber) {
      setGameStatus("won")
      setRoundsWon((prev) => prev + 1)
      const roundScore = Math.max(100 - (newAttempts - 1) * 10, 10)
      setScore((prev) => prev + roundScore)
      setFeedback(
        `🎉 Congratulations! You guessed it in ${newAttempts} attempt${newAttempts === 1 ? "" : "s"}! (+${roundScore} points)`,
      )
    } else if (newAttempts >= maxAttempts) {
      setGameStatus("lost")
      setFeedback(`😔 Game over! The number was ${targetNumber}. Better luck next time!`)
    } else {
      const remainingAttempts = maxAttempts - newAttempts
      if (guess < targetNumber) {
        setFeedback(
          `📈 Too low! Try a higher number. ${remainingAttempts} attempt${remainingAttempts === 1 ? "" : "s"} remaining.`,
        )
      } else {
        setFeedback(
          `📉 Too high! Try a lower number. ${remainingAttempts} attempt${remainingAttempts === 1 ? "" : "s"} remaining.`,
        )
      }
    }

    setUserGuess("")
  }

  // Handle Enter key press
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && gameStatus === "playing") {
      handleGuess()
    }
  }

  // Initialize game on component mount
  useEffect(() => {
    initializeGame()
  }, [])

  const winRate = roundsPlayed > 0 ? Math.round((roundsWon / roundsPlayed) * 100) : 0

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4 flex items-center justify-center">
      <Card className="w-full max-w-md shadow-xl">
        <CardHeader className="text-center">
          <CardTitle className="text-2xl font-bold text-gray-800 flex items-center justify-center gap-2">
            <Target className="h-6 w-6 text-blue-600" />
            Number Guessing Game
          </CardTitle>
          <CardDescription>
            Guess the number between {minRange} and {maxRange}
          </CardDescription>
        </CardHeader>

        <CardContent className="space-y-4">
          {/* Game Stats */}
          <div className="grid grid-cols-3 gap-2 text-center">
            <div className="bg-blue-50 p-2 rounded-lg">
              <div className="text-lg font-bold text-blue-600">{score}</div>
              <div className="text-xs text-gray-600">Score</div>
            </div>
            <div className="bg-green-50 p-2 rounded-lg">
              <div className="text-lg font-bold text-green-600">
                {roundsWon}/{roundsPlayed}
              </div>
              <div className="text-xs text-gray-600">Won</div>
            </div>
            <div className="bg-purple-50 p-2 rounded-lg">
              <div className="text-lg font-bold text-purple-600">{winRate}%</div>
              <div className="text-xs text-gray-600">Win Rate</div>
            </div>
          </div>

          <Separator />

          {/* Current Game Info */}
          <div className="flex justify-between items-center">
            <Badge variant="outline" className="flex items-center gap-1">
              <Zap className="h-3 w-3" />
              Attempts: {attempts}/{maxAttempts}
            </Badge>
            {gameStatus === "won" && (
              <Badge className="bg-green-500 hover:bg-green-600">
                <Trophy className="h-3 w-3 mr-1" />
                Winner!
              </Badge>
            )}
            {gameStatus === "lost" && <Badge variant="destructive">Game Over</Badge>}
          </div>

          {/* Feedback */}
          <div className="bg-gray-50 p-3 rounded-lg text-center text-sm text-gray-700 min-h-[60px] flex items-center justify-center">
            {feedback}
          </div>

          {/* Input and Guess Button */}
          {gameStatus === "playing" && (
            <div className="flex gap-2">
              <Input
                type="number"
                placeholder="Enter your guess"
                value={userGuess}
                onChange={(e) => setUserGuess(e.target.value)}
                onKeyPress={handleKeyPress}
                min={minRange}
                max={maxRange}
                className="flex-1"
              />
              <Button onClick={handleGuess} disabled={!userGuess.trim()} className="px-6">
                Guess
              </Button>
            </div>
          )}
        </CardContent>

        <CardFooter className="flex gap-2">
          {gameStatus !== "playing" && (
            <Button onClick={startNewRound} className="flex-1" variant="default">
              <RefreshCw className="h-4 w-4 mr-2" />
              New Round
            </Button>
          )}
          <Button onClick={resetGame} variant="outline" className="flex-1">
            Reset Game
          </Button>
        </CardFooter>
      </Card>
    </div>
  )
}
