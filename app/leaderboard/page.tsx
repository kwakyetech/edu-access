import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Trophy, Medal, Award, Users, TrendingUp, Star } from "lucide-react"
import Navbar from "@/components/navbar"

const leaderboardData = [
  { rank: 1, name: "Kwame Asante", contributions: 45, points: 2250, badge: "Gold Contributor", icon: Trophy },
  { rank: 2, name: "Ama Osei", contributions: 38, points: 1900, badge: "Silver Contributor", icon: Medal },
  { rank: 3, name: "Kofi Mensah", contributions: 32, points: 1600, badge: "Bronze Contributor", icon: Award },
  { rank: 4, name: "Akosua Boateng", contributions: 28, points: 1400, badge: "Active Learner", icon: null },
  { rank: 5, name: "Yaw Oppong", contributions: 24, points: 1200, badge: "Rising Star", icon: null },
  { rank: 6, name: "Efua Adjei", contributions: 21, points: 1050, badge: "Contributor", icon: null },
  { rank: 7, name: "Kwaku Darko", contributions: 18, points: 900, badge: "Helper", icon: null },
  { rank: 8, name: "Abena Frimpong", contributions: 15, points: 750, badge: "Supporter", icon: null },
  { rank: 9, name: "Kojo Asiedu", contributions: 12, points: 600, badge: "Learner", icon: null },
  { rank: 10, name: "Adwoa Nyong", contributions: 10, points: 500, badge: "Newcomer", icon: null },
]

const stats = [
  { label: "Total Contributors", value: "156", icon: Users },
  { label: "Notes Shared", value: "1,247", icon: TrendingUp },
  { label: "Average Rating", value: "4.8", icon: Star },
]

export default function LeaderboardPage() {
  return (
    <div className="min-h-screen bg-background">
      <Navbar />

      <main className="max-w-6xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-foreground mb-4 text-balance">Community Leaderboard</h1>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto text-pretty">
            Celebrating our top contributors who make learning accessible for everyone in Ghana.
          </p>
        </div>

        {/* Stats Cards */}
        <div className="grid md:grid-cols-3 gap-6 mb-8">
          {stats.map((stat, index) => (
            <Card key={index}>
              <CardContent className="p-6">
                <div className="flex items-center gap-4">
                  <div className="p-3 rounded-full bg-primary/10">
                    <stat.icon className="w-6 h-6 text-primary" />
                  </div>
                  <div>
                    <p className="text-2xl font-bold text-foreground">{stat.value}</p>
                    <p className="text-sm text-muted-foreground">{stat.label}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Leaderboard */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Trophy className="w-6 h-6 text-primary" />
              Top Contributors This Month
            </CardTitle>
            <CardDescription>
              Rankings based on notes uploaded, quizzes created, and community engagement.
            </CardDescription>
          </CardHeader>
          <CardContent>
            {/* Top 3 Podium */}
            <div className="grid md:grid-cols-3 gap-4 mb-8">
              {leaderboardData.slice(0, 3).map((user, index) => (
                <Card
                  key={user.rank}
                  className={`text-center ${
                    index === 0
                      ? "md:order-2 bg-primary/5 border-primary/20"
                      : index === 1
                        ? "md:order-1 bg-secondary/5 border-secondary/20"
                        : "md:order-3 bg-chart-4/5 border-chart-4/20"
                  }`}
                >
                  <CardContent className="p-6">
                    <div className="flex justify-center mb-4">
                      {user.icon && (
                        <user.icon
                          className={`w-12 h-12 ${
                            index === 0 ? "text-primary" : index === 1 ? "text-secondary" : "text-chart-4"
                          }`}
                        />
                      )}
                    </div>
                    <h3 className="font-bold text-lg text-foreground mb-2">{user.name}</h3>
                    <p className="text-sm text-muted-foreground mb-2">{user.badge}</p>
                    <div className="space-y-1">
                      <p className="text-2xl font-bold text-foreground">{user.contributions}</p>
                      <p className="text-xs text-muted-foreground">contributions</p>
                      <p className="text-sm font-semibold text-accent">{user.points} pts</p>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>

            {/* Full Leaderboard Table */}
            <div className="space-y-2">
              <h3 className="text-lg font-semibold text-foreground mb-4">Complete Rankings</h3>

              {/* Desktop Table */}
              <div className="hidden md:block">
                <div className="grid grid-cols-5 gap-4 p-4 bg-muted/30 rounded-lg font-semibold text-sm text-muted-foreground">
                  <div>Rank</div>
                  <div>Name</div>
                  <div>Badge</div>
                  <div>Contributions</div>
                  <div>Points</div>
                </div>

                {leaderboardData.map((user) => (
                  <div
                    key={user.rank}
                    className="grid grid-cols-5 gap-4 p-4 rounded-lg hover:bg-muted/30 transition-colors border-b border-border/50"
                  >
                    <div className="flex items-center gap-2">
                      <div className="flex items-center justify-center w-8 h-8 rounded-full bg-primary/10 text-primary font-semibold text-sm">
                        {user.rank}
                      </div>
                      {user.icon && <user.icon className="w-4 h-4 text-accent" />}
                    </div>
                    <div className="font-medium text-foreground">{user.name}</div>
                    <div className="text-sm text-muted-foreground">{user.badge}</div>
                    <div className="font-semibold text-secondary">{user.contributions}</div>
                    <div className="font-semibold text-accent">{user.points}</div>
                  </div>
                ))}
              </div>

              {/* Mobile Cards */}
              <div className="md:hidden space-y-3">
                {leaderboardData.map((user) => (
                  <Card key={user.rank}>
                    <CardContent className="p-4">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3">
                          <div className="flex items-center justify-center w-10 h-10 rounded-full bg-primary/10 text-primary font-bold">
                            {user.rank}
                          </div>
                          {user.icon && <user.icon className="w-5 h-5 text-accent" />}
                          <div>
                            <p className="font-semibold text-foreground">{user.name}</p>
                            <p className="text-xs text-muted-foreground">{user.badge}</p>
                          </div>
                        </div>
                        <div className="text-right">
                          <p className="font-bold text-secondary">{user.contributions}</p>
                          <p className="text-xs text-muted-foreground">contributions</p>
                          <p className="text-sm font-semibold text-accent">{user.points} pts</p>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Call to Action */}
        <div className="text-center mt-12 p-8 bg-muted/30 rounded-lg">
          <h2 className="text-2xl font-bold text-foreground mb-4">Want to Join the Leaderboard?</h2>
          <p className="text-muted-foreground mb-6 max-w-2xl mx-auto">
            Start contributing to the community by uploading notes, creating quizzes, and helping fellow students
            succeed.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Card className="p-4 bg-background">
              <div className="text-center">
                <Trophy className="w-8 h-8 mx-auto mb-2 text-primary" />
                <p className="font-semibold text-foreground">Upload Notes</p>
                <p className="text-sm text-muted-foreground">+50 points each</p>
              </div>
            </Card>
            <Card className="p-4 bg-background">
              <div className="text-center">
                <Star className="w-8 h-8 mx-auto mb-2 text-secondary" />
                <p className="font-semibold text-foreground">Create Quizzes</p>
                <p className="text-sm text-muted-foreground">+30 points each</p>
              </div>
            </Card>
            <Card className="p-4 bg-background">
              <div className="text-center">
                <Users className="w-8 h-8 mx-auto mb-2 text-chart-4" />
                <p className="font-semibold text-foreground">Help Others</p>
                <p className="text-sm text-muted-foreground">+10 points each</p>
              </div>
            </Card>
          </div>
        </div>
      </main>
    </div>
  )
}
