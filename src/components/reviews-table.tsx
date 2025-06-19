"use client"


import Badge from "./ui/badge"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "./ui/table"
import { Star, TrendingUp, TrendingDown, Minus } from "lucide-react"
import { motion } from "framer-motion"
import { useState } from "react"

interface ReviewData {
  product_name: string
  review_text: string
  rating: number
  sentiment_score: number
  sentiment_label: string
  timestamp: string
}

interface ReviewsTableProps {
  reviews: ReviewData[]
}

export function ReviewsTable({ reviews }: ReviewsTableProps) {
  const [currentPage, setCurrentPage] = useState(1)
  const reviewsPerPage = 10
  const totalPages = Math.ceil(reviews.length / reviewsPerPage)

  const startIndex = (currentPage - 1) * reviewsPerPage
  const endIndex = startIndex + reviewsPerPage
  const currentReviews = reviews.slice(startIndex, endIndex)

  const getSentimentIcon = (label: string) => {
    switch (label) {
      case "Positive":
        return <TrendingUp className="h-4 w-4" />
      case "Negative":
        return <TrendingDown className="h-4 w-4" />
      default:
        return <Minus className="h-4 w-4" />
    }
  }

  const getSentimentColor = (label: string) => {
    switch (label) {
      case "Positive":
        return "bg-green-500/20 text-green-300 border-green-500/30"
      case "Negative":
        return "bg-red-500/20 text-red-300 border-red-500/30"
      default:
        return "bg-yellow-500/20 text-yellow-300 border-yellow-500/30"
    }
  }

  const renderStars = (rating: number) => {
    const validRating = Math.max(0, Math.min(5, Math.floor(rating || 0)))
    return Array.from({ length: 5 }, (_, i) => (
      <Star key={i} className={`h-4 w-4 ${i < validRating ? "text-yellow-400 fill-current" : "text-gray-500"}`} />
    ))
  }

  if (!reviews || reviews.length === 0) {
    return (
      <Card className="bg-white/10 backdrop-blur-md border-white/20 shadow-xl">
        <CardHeader>
          <CardTitle className="text-white">Product Reviews</CardTitle>
          <CardDescription className="text-white/60">No reviews available</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="h-[400px] flex items-center justify-center">
            <p className="text-white/50 text-center">No reviews to display</p>
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}>
      <Card className="bg-white/10 backdrop-blur-md border-white/20 shadow-xl hover:shadow-2xl transition-all duration-300">
        <CardHeader className="pb-4">
          <CardTitle className="text-white text-lg">Product Reviews ({reviews.length})</CardTitle>
          <CardDescription className="text-white/60">
            Scraped reviews with AI-powered sentiment analysis results
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="overflow-hidden rounded-lg border border-white/10">
            <div className="overflow-x-auto">
              <Table>
                <TableHeader>
                  <TableRow className="border-white/10 hover:bg-white/5">
                    <TableHead className="text-white/80 font-semibold min-w-[300px] sm:min-w-[400px]">Review</TableHead>
                    <TableHead className="text-white/80 font-semibold min-w-[120px]">Rating</TableHead>
                    <TableHead className="text-white/80 font-semibold min-w-[120px]">Sentiment</TableHead>
                    <TableHead className="text-white/80 font-semibold min-w-[100px]">Score</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {currentReviews.map((review, index) => (
                    <motion.tr
                      key={startIndex + index}
                      className="border-white/10 hover:bg-white/5 transition-colors duration-200"
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ duration: 0.3, delay: index * 0.05 }}
                    >
                      <TableCell className="py-4">
                        <div className="max-w-md">
                          <p className="text-sm text-white/90 line-clamp-3 leading-relaxed" title={review.review_text}>
                            {review.review_text || "No review text"}
                          </p>
                        </div>
                      </TableCell>
                      <TableCell className="py-4">
                        <div className="flex flex-col gap-2">
                          <div className="flex items-center gap-1">{renderStars(review.rating)}</div>
                          <span className="text-sm text-white/70 font-medium">
                            {review.rating ? review.rating.toFixed(1) : "0.0"}
                          </span>
                        </div>
                      </TableCell>
                      <TableCell className="py-4">
                        <Badge
                          className={`${getSentimentColor(review.sentiment_label)} flex items-center gap-1 w-fit`}
                        >
                          {getSentimentIcon(review.sentiment_label)}
                          <span className="font-medium">{review.sentiment_label || "Neutral"}</span>
                        </Badge>
                      </TableCell>
                      <TableCell className="py-4">
                        <span className="text-sm font-mono text-white/80 bg-white/10 px-2 py-1 rounded">
                          {review.sentiment_score ? review.sentiment_score.toFixed(3) : "0.000"}
                        </span>
                      </TableCell>
                    </motion.tr>
                  ))}
                </TableBody>
              </Table>
            </div>
          </div>

          {/* Pagination */}
          {totalPages > 1 && (
            <div className="flex flex-col sm:flex-row items-center justify-between gap-4 mt-6 pt-4 border-t border-white/10">
              <p className="text-sm text-white/60">
                Showing {startIndex + 1} to {Math.min(endIndex, reviews.length)} of {reviews.length} reviews
              </p>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))}
                  disabled={currentPage === 1}
                  className="px-3 py-1 text-sm bg-white/10 text-white rounded border border-white/20 hover:bg-white/20 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
                >
                  Previous
                </button>
                <span className="px-3 py-1 text-sm text-white/80">
                  Page {currentPage} of {totalPages}
                </span>
                <button
                  onClick={() => setCurrentPage((prev) => Math.min(prev + 1, totalPages))}
                  disabled={currentPage === totalPages}
                  className="px-3 py-1 text-sm bg-white/10 text-white rounded border border-white/20 hover:bg-white/20 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
                >
                  Next
                </button>
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </motion.div>
  )
}
