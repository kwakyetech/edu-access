import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Trophy, Medal, Award } from "lucide-react"

const leaderboardData = [
  { rank: 1, name: "Kwame Asante", contributions: 45, icon: Trophy },
  { rank: 2, name: "Ama Osei", contributions: 38, icon: Medal },
  { rank: 3, name: "Kofi Mensah", contributions: 32, icon: Award },
  { rank: 4, name: "Akosua Boateng", contributions: 28, icon: null },
  { rank: 5, name: "Yaw Oppong", contributions: 24, icon: null },
  { rank: 6, name: "Efua Adjei", contributions: 21, icon: null },
  { rank: 7, name: "Kwaku Darko", contributions: 18, icon: null },
  { rank: 8, name: "Abena Frimpong", contributions: 15, icon: null },
]

export default function Leaderboard() {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Trophy className="w-5 h-5 text-primary" />
          Top Contributors
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          {leaderboardData.map((user) => (
            <div
              key={user.rank}
              className="flex items-center justify-between p-3 rounded-lg bg-muted/30 hover:bg-muted/50 transition-colors"
            >
              <div className="flex items-center gap-3">
                <div className="flex items-center justify-center w-8 h-8 rounded-full bg-primary/10 text-primary font-semibold text-sm">
                  {user.rank}
                </div>
                {user.icon && <user.icon className="w-5 h-5 text-accent" />}
                <span className="font-medium text-foreground">{user.name}</span>
              </div>
              <div className="text-sm text-muted-foreground">
                <span className="font-semibold text-secondary">{user.contributions}</span> contributions
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
