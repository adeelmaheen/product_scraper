"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./ui/card"
import { PieChart, Pie, Cell, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip } from "recharts"
import { motion } from "framer-motion"

interface ReviewData {
  product_name: string
  review_text: string
  rating: number
  sentiment_score: number
  sentiment_label: string
  timestamp: string
}

interface SentimentChartProps {
  data: ReviewData[]
}

export function SentimentChart({ data }: SentimentChartProps) {
  if (!data || data.length === 0) {
    return (
      <Card className="bg-white/10 backdrop-blur-md border-white/20 shadow-xl">
        <CardHeader>
          <CardTitle className="text-white">Sentiment Distribution</CardTitle>
          <CardDescription className="text-white/60">No data available</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="h-[300px] flex items-center justify-center">
            <p className="text-white/50 text-center">No sentiment data to display</p>
          </div>
        </CardContent>
      </Card>
    )
  }

  const sentimentData = data.reduce(
    (acc, review) => {
      const sentiment = review.sentiment_label || "Neutral"
      const existing = acc.find((item) => item.sentiment === sentiment)
      if (existing) {
        existing.count += 1
      } else {
        acc.push({
          sentiment: sentiment,
          count: 1,
          color: sentiment === "Positive" ? "#10b981" : sentiment === "Negative" ? "#ef4444" : "#f59e0b",
        })
      }
      return acc
    },
    [] as Array<{ sentiment: string; count: number; color: string }>,
  )

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-black/80 backdrop-blur-md p-3 border border-white/20 rounded-lg shadow-xl">
          <p className="font-medium text-white">{payload[0].payload.sentiment || label}</p>
          <p className="text-sm text-white/70">Count: {payload[0].value}</p>
          <p className="text-sm text-white/70">Percentage: {((payload[0].value / data.length) * 100).toFixed(1)}%</p>
        </div>
      )
    }
    return null
  }

  return (
    <div className="space-y-6">
      {/* Pie Chart */}
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
      >
        <Card className="bg-white/10 backdrop-blur-md border-white/20 shadow-xl hover:shadow-2xl transition-all duration-300">
          <CardHeader className="pb-4">
            <CardTitle className="text-white text-lg">Sentiment Distribution</CardTitle>
            <CardDescription className="text-white/60">
              Overall sentiment breakdown of {data.length} reviews
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-[280px] sm:h-[320px]">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={sentimentData}
                    cx="50%"
                    cy="50%"
                    outerRadius="80%"
                    dataKey="count"
                    nameKey="sentiment"
                    label={({ sentiment, count, percent }) => `${sentiment}: ${count} (${(percent * 100).toFixed(1)}%)`}
                    labelLine={false}
                    fontSize={12}
                    fill="#ffffff"
                  >
                    {sentimentData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip content={<CustomTooltip />} />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>
      </motion.div>

      {/* Bar Chart */}
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5, delay: 0.2 }}
      >
        <Card className="bg-white/10 backdrop-blur-md border-white/20 shadow-xl hover:shadow-2xl transition-all duration-300">
          <CardHeader className="pb-4">
            <CardTitle className="text-white text-lg">Sentiment Count</CardTitle>
            <CardDescription className="text-white/60">Number of reviews by sentiment</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-[200px] sm:h-[240px]">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={sentimentData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                  <XAxis dataKey="sentiment" stroke="rgba(255,255,255,0.7)" fontSize={12} />
                  <YAxis stroke="rgba(255,255,255,0.7)" fontSize={12} />
                  <Tooltip content={<CustomTooltip />} />
                  <Bar dataKey="count" fill="url(#barGradient)" radius={[4, 4, 0, 0]} />
                  <defs>
                    <linearGradient id="barGradient" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="#8b5cf6" />
                      <stop offset="100%" stopColor="#3b82f6" />
                    </linearGradient>
                  </defs>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  )
}
