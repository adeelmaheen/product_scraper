"use client"

import { useState } from "react"
import { Button } from "../components/ui/button"
import { Input } from "../components/ui/input"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card"
import {
  Loader2,
  Search,
  TrendingUp,
  TrendingDown,
  Minus,
  AlertCircle,
  ExternalLink,
  CheckCircle,
  Sparkles,
  BarChart3,
  Database,
} from "lucide-react"
import { ReviewsTable } from "../components/reviews-table"
import { SentimentChart } from "../components/sentiment-chart"
import { Alert, AlertDescription } from "../components/ui/alert"
import  {Badge}  from "../components/ui/badge"
import { motion, AnimatePresence } from "framer-motion"

interface ReviewData {
  product_name: string
  review_text: string
  rating: number
  sentiment_score: number
  sentiment_label: string
  timestamp: string
}

interface ScrapeResponse {
  success: boolean
  data: ReviewData[]
  message: string
  total_reviews: number
  google_sheets_saved: boolean
  sheet_url?: string
}

export default function Home() {
  const [productUrl, setProductUrl] = useState("https://www.daraz.pk/products/sample-product")
  const [reviews, setReviews] = useState<ReviewData[]>([])
  const [loading, setLoading] = useState(false)
  const [hasData, setHasData] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [googleSheetsStatus, setGoogleSheetsStatus] = useState<{
    saved: boolean
    url?: string
  } | null>(null)

  // Animation variants
  const containerVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.6,
        staggerChildren: 0.1,
      },
    },
  }

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.5 },
    },
  }

  const cardHoverVariants = {
    hover: {
      scale: 1.02,
      rotateX: 5,
      rotateY: 5,
      transition: {
        duration: 0.3,
        ease: "easeOut",
      },
    },
  }

  const handleScrape = async () => {
    if (!productUrl.trim()) {
      setError("Please enter a product URL")
      return
    }

    setLoading(true)
    setError(null)
    setGoogleSheetsStatus(null)

    try {
      const response = await fetch("http://localhost:8000/scrape", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ product_url: productUrl }),
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: "Unknown error occurred" }))
        throw new Error(errorData.detail || `HTTP ${response.status}`)
      }

      const data: ScrapeResponse = await response.json()

      if (!data.success || !data.data || data.data.length === 0) {
        throw new Error("No reviews found or invalid response")
      }

      setReviews(data.data)
      setHasData(true)
      setError(null)

      setGoogleSheetsStatus({
        saved: data.google_sheets_saved,
        url: data.sheet_url,
      })
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : "Failed to scrape reviews"
      setError(errorMessage)
      console.error("Scraping error:", error)
    } finally {
      setLoading(false)
    }
  }

  const getSentimentStats = () => {
    if (!reviews || reviews.length === 0) {
      return { positive: 0, negative: 0, neutral: 0, total: 0 }
    }

    const stats = reviews.reduce(
      (acc, review) => {
        const label = review.sentiment_label || "Neutral"
        acc[label] = (acc[label] || 0) + 1
        return acc
      },
      {} as Record<string, number>,
    )

    return {
      positive: stats.Positive || 0,
      negative: stats.Negative || 0,
      neutral: stats.Neutral || 0,
      total: reviews.length,
    }
  }

  const sentimentStats = getSentimentStats()

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 relative overflow-hidden">
      {/* Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-purple-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-blue-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-2000"></div>
        <div className="absolute top-40 left-40 w-80 h-80 bg-pink-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-4000"></div>
      </div>

      {/* Grid Pattern Overlay */}
      <div className="absolute inset-0 bg-[url('data:image/svg+xml,%3Csvg width=&quot;60&quot; height=&quot;60&quot; viewBox=&quot;0 0 60 60&quot; xmlns=&quot;http://www.w3.org/2000/svg&quot;%3E%3Cg fill=&quot;none&quot; fillRule=&quot;evenodd&quot;%3E%3Cg fill=&quot;%239C92AC&quot; fillOpacity=&quot;0.05&quot;%3E%3Ccircle cx=&quot;30&quot; cy=&quot;30&quot; r=&quot;1&quot;/%3E%3C/g%3E%3C/g%3E%3C/svg%3E')] opacity-40"></div>

      <motion.div
        className="relative z-10 max-w-7xl mx-auto p-4 sm:p-6 lg:p-8 space-y-8"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        {/* Header */}
        <motion.div className="text-center space-y-4" variants={itemVariants}>
          <motion.div
            className="inline-flex items-center gap-2 px-4 py-2 bg-white/10 backdrop-blur-sm rounded-full border border-white/20 mb-4"
            whileHover={{ scale: 1.05 }}
            transition={{ duration: 0.2 }}
          >
            <Sparkles className="h-4 w-4 text-yellow-400" />
            <span className="text-sm text-white/80 font-medium">AI-Powered Sentiment Analysis</span>
          </motion.div>

          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold bg-gradient-to-r from-white via-purple-200 to-blue-200 bg-clip-text text-transparent leading-tight">
            Product Review
            <br />
            <span className="bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
              Sentiment Scraper
            </span>
          </h1>
          <p className="text-lg sm:text-xl text-white/70 max-w-2xl mx-auto leading-relaxed">
            Harness the power of AI to scrape, analyze, and visualize product reviews with advanced sentiment analysis
          </p>
        </motion.div>

        {/* Input Section */}
        <motion.div variants={itemVariants}>
          <Card className="bg-white/10 backdrop-blur-md border-white/20 shadow-2xl">
            <CardHeader className="pb-4">
              <CardTitle className="flex items-center gap-3 text-white text-xl">
                <div className="p-2 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg">
                  <Search className="h-5 w-5 text-white" />
                </div>
                Scrape Product Reviews
              </CardTitle>
              <CardDescription className="text-white/60 text-base">
                Enter a product URL to scrape and analyze reviews with AI-powered sentiment analysis
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex flex-col sm:flex-row gap-4">
                <Input
                  placeholder="https://www.daraz.pk/products/..."
                  value={productUrl}
                  onChange={(e) => setProductUrl(e.target.value)}
                  className="flex-1 bg-white/10 border-white/20 text-white placeholder:text-white/50 focus:border-purple-400 focus:ring-purple-400/20 h-12 text-base"
                  disabled={loading}
                />
                <Button
                  onClick={handleScrape}
                  disabled={loading}
                  className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white border-0 h-12 px-8 font-semibold shadow-lg hover:shadow-xl transition-all duration-300 min-w-[140px]"
                >
                  {loading ? (
                    <>
                      <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                      Analyzing...
                    </>
                  ) : (
                    <>
                      <BarChart3 className="mr-2 h-5 w-5" />
                      Scrape Reviews
                    </>
                  )}
                </Button>
              </div>

              <AnimatePresence>
                {error && (
                  <motion.div
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -10 }}
                    transition={{ duration: 0.3 }}
                  >
                    <Alert variant="destructive" className="bg-red-500/20 border-red-500/30 backdrop-blur-sm">
                      <AlertCircle className="h-4 w-4" />
                      <AlertDescription className="text-red-200">{error}</AlertDescription>
                    </Alert>
                  </motion.div>
                )}

                {googleSheetsStatus && (
                  <motion.div
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.3 }}
                  >
                    <Alert className="bg-green-500/20 border-green-500/30 backdrop-blur-sm">
                      <CheckCircle className="h-4 w-4 text-green-400" />
                      <AlertDescription className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 text-green-200">
                        <span>
                          {googleSheetsStatus.saved
                            ? "✅ Data saved to Google Sheets successfully!"
                            : "⚠️ Data processed but not saved to Google Sheets"}
                        </span>
                        {googleSheetsStatus.url && (
                          <Button
                            variant="outline"
                            size="sm"
                            asChild
                            className="bg-white/10 border-white/20 text-white hover:bg-white/20"
                          >
                            <a href={googleSheetsStatus.url} target="_blank" rel="noopener noreferrer">
                              <ExternalLink className="h-4 w-4 mr-2" />
                              View Sheet
                            </a>
                          </Button>
                        )}
                      </AlertDescription>
                    </Alert>
                  </motion.div>
                )}
              </AnimatePresence>
            </CardContent>
          </Card>
        </motion.div>

        {/* Stats Cards */}
        <AnimatePresence>
          {hasData && (
            <motion.div
              className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6"
              variants={containerVariants}
              initial="hidden"
              animate="visible"
            >
              {[
                {
                  title: "Total Reviews",
                  value: sentimentStats.total,
                  icon: Database,
                  color: "from-blue-500 to-cyan-500",
                  bgColor: "bg-blue-500/20",
                },
                {
                  title: "Positive",
                  value: sentimentStats.positive,
                  icon: TrendingUp,
                  color: "from-green-500 to-emerald-500",
                  bgColor: "bg-green-500/20",
                },
                {
                  title: "Negative",
                  value: sentimentStats.negative,
                  icon: TrendingDown,
                  color: "from-red-500 to-pink-500",
                  bgColor: "bg-red-500/20",
                },
                {
                  title: "Neutral",
                  value: sentimentStats.neutral,
                  icon: Minus,
                  color: "from-yellow-500 to-orange-500",
                  bgColor: "bg-yellow-500/20",
                },
              ].map((stat, index) => (
                <motion.div key={stat.title} variants={itemVariants} whileHover="hover" style={{ perspective: 1000 }}>
                  <motion.div variants={cardHoverVariants}>
                    <Card className="bg-white/10 backdrop-blur-md border-white/20 shadow-xl hover:shadow-2xl transition-all duration-300">
                      <CardContent className="p-6">
                        <div className="flex items-center justify-between">
                          <div className="space-y-2">
                            <p className="text-sm font-medium text-white/70">{stat.title}</p>
                            <p className="text-3xl font-bold text-white">{stat.value}</p>
                            {stat.title === "Neutral" && googleSheetsStatus && (
                              <Badge
                                variant={googleSheetsStatus.saved ? "default" : "secondary"}
                                className={`${googleSheetsStatus.saved ? "bg-green-500/20 text-green-300" : "bg-gray-500/20 text-gray-300"} border-0`}
                              >
                                {googleSheetsStatus.saved ? "Sheets Saved" : "Not Saved"}
                              </Badge>
                            )}
                          </div>
                          <div className={`p-3 rounded-xl ${stat.bgColor} backdrop-blur-sm`}>
                            <stat.icon
                              className={`h-8 w-8 bg-gradient-to-r ${stat.color} bg-clip-text text-transparent`}
                            />
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  </motion.div>
                </motion.div>
              ))}
            </motion.div>
          )}
        </AnimatePresence>

        {/* Charts and Table */}
        <AnimatePresence>
          {hasData && reviews.length > 0 && (
            <motion.div
              className="grid grid-cols-1 xl:grid-cols-3 gap-6 lg:gap-8"
              variants={containerVariants}
              initial="hidden"
              animate="visible"
            >
              <motion.div
                className="xl:col-span-1"
                variants={itemVariants}
                whileHover="hover"
                style={{ perspective: 1000 }}
              >
                <motion.div variants={cardHoverVariants}>
                  <SentimentChart data={reviews} />
                </motion.div>
              </motion.div>
              <motion.div
                className="xl:col-span-2"
                variants={itemVariants}
                whileHover="hover"
                style={{ perspective: 1000 }}
              >
                <motion.div variants={cardHoverVariants}>
                  <ReviewsTable reviews={reviews} />
                </motion.div>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>

      <style jsx>{`
        @keyframes blob {
          0% {
            transform: translate(0px, 0px) scale(1);
          }
          33% {
            transform: translate(30px, -50px) scale(1.1);
          }
          66% {
            transform: translate(-20px, 20px) scale(0.9);
          }
          100% {
            transform: translate(0px, 0px) scale(1);
          }
        }
        .animate-blob {
          animation: blob 7s infinite;
        }
        .animation-delay-2000 {
          animation-delay: 2s;
        }
        .animation-delay-4000 {
          animation-delay: 4s;
        }
      `}</style>
    </div>
  )
}
