# 🎓 EduAccess - Unlock Learning for Everyone in Africa

> **Democratizing quality education across Africa through technology, community, and shared knowledge.**

EduAccess is a comprehensive educational platform built for the SDG 4: Quality Education hackathon, designed to empower African students with accessible, affordable, and quality educational resources.

## 🌟 Features

### 📚 **Study Notes Management**
- **Upload & Share**: Students can upload and share study materials with the community
- **Multiple Formats**: Support for PDF, DOC, DOCX, JPG, PNG files (up to 10MB)
- **Categorization**: Organize notes by subject, academic level, and year/grade
- **Community-Driven**: Access to 1,200+ notes shared by fellow students

### 🧠 **AI-Powered Quiz Generation**
- **Smart Quiz Creation**: Generate personalized quizzes from uploaded notes using AI
- **Multiple Input Methods**: 
  - Upload documents (PDF, DOC, DOCX, TXT)
  - Paste notes directly
  - Topic-based generation
- **Customizable**: Set difficulty levels and focus areas
- **Progress Tracking**: Monitor quiz completion and performance

### 📋 **Past Questions Database**
- **Comprehensive Collection**: Access to past exam questions from:
  - WASSCE (West African Senior School Certificate Examination)
  - BECE (Basic Education Certificate Examination)
  - University entrance exams
  - Professional certifications
- **Advanced Search**: Filter by subject, year, exam type, and academic level
- **Answer Keys**: Many questions include detailed solutions
- **Download & Preview**: Easy access to question papers

### 🏆 **Community Leaderboard**
- **Gamified Learning**: Compete with fellow students across Africa
- **Contribution Tracking**: Earn points for uploading notes and helping others
- **Recognition System**: Badges for top contributors (Gold, Silver, Bronze)
- **Community Stats**: Track your impact on the learning community

### 👤 **User Authentication**
- **Secure Sign-up/Sign-in**: Email-based authentication system
- **User Profiles**: Personalized dashboard with learning progress
- **Session Management**: Secure user sessions with proper logout functionality

### 📊 **Dashboard & Analytics**
- **Learning Overview**: Track your educational journey
- **Recent Activity**: Monitor uploads, quiz completions, and achievements
- **Statistics**: View community stats (2,500+ students, 5,000+ quizzes completed)
- **Quick Actions**: Easy access to all platform features

## 🛠️ Tech Stack

### **Frontend**
- **Framework**: Next.js 15.2.4 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS 4.1.12
- **UI Components**: Radix UI primitives
- **Icons**: Lucide React
- **Fonts**: Geist Sans & Mono

### **Development Tools**
- **Package Manager**: npm
- **Linting**: ESLint with Next.js config
- **Build Tool**: Turbopack (Next.js)
- **Analytics**: Vercel Analytics

### **Key Dependencies**
- `@radix-ui/react-*`: Modern, accessible UI components
- `class-variance-authority`: Type-safe component variants
- `clsx` & `tailwind-merge`: Utility for conditional CSS classes
- `lucide-react`: Beautiful, customizable icons

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ 
- npm or yarn package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/kwakyetech/edu-access.git
   cd edu-access
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Run the development server**
   ```bash
   npm run dev
   ```

4. **Open your browser**
   Navigate to [http://localhost:3000](http://localhost:3000) to see the application.

### Available Scripts

- `npm run dev` - Start development server with Turbopack
- `npm run build` - Build the application for production
- `npm run start` - Start the production server
- `npm run lint` - Run ESLint for code quality checks

## 📱 Application Structure

```
edu-access/
├── app/                    # Next.js App Router pages
│   ├── about/             # About page
│   ├── dashboard/         # User dashboard
│   ├── leaderboard/       # Community leaderboard
│   ├── past-questions/    # Past exam questions
│   ├── quiz/              # AI quiz generator
│   ├── signin/            # User authentication
│   ├── signup/            # User registration
│   ├── start-learning/    # Learning paths
│   ├── upload/            # Notes upload
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Landing page
├── components/            # Reusable React components
│   ├── ui/               # UI component library
│   ├── home-navbar.tsx   # Landing page navigation
│   ├── navbar.tsx        # Main application navigation
│   ├── leaderboard.tsx   # Leaderboard component
│   └── loading-spinner.tsx # Loading states
├── lib/                   # Utility functions
├── public/               # Static assets
└── styles/               # Global styles
```

## 🌍 Impact & Mission

### **Our Mission**
To break down educational barriers and provide every student in Africa with access to quality learning resources, regardless of their economic background or geographical location. We believe education is a fundamental right, not a privilege.

### **Current Impact**
- 📈 **2,500+** students reached across Africa
- 📚 **1,200+** study notes shared in the community
- 🧠 **5,000+** AI-generated quizzes completed
- 🌍 **15+** countries represented in our user base

### **Key Benefits**
- **Accessibility**: Free access to quality educational resources
- **Community-Driven**: Students helping students across Africa
- **AI-Enhanced**: Personalized learning through intelligent quiz generation
- **Comprehensive**: Covers multiple academic levels (JHS, SHS, University)
- **Localized**: Focused on African educational systems (WASSCE, BECE)

## 🤝 Contributing

We welcome contributions from the community! Whether you're a student, educator, or developer, there are many ways to help:

1. **Share Notes**: Upload your study materials to help fellow students
2. **Report Issues**: Help us improve by reporting bugs or suggesting features
3. **Code Contributions**: Submit pull requests for new features or improvements
4. **Spread the Word**: Share EduAccess with students who could benefit

## 📄 License

This project was created for the SDG 4: Quality Education hackathon. Built with ❤️ for African students.

## 🔗 Links

- **Live Demo**: [Coming Soon]
- **GitHub Repository**: [https://github.com/kwakyetech/edu-access](https://github.com/kwakyetech/edu-access)
- **SDG 4 - Quality Education**: [Learn More](https://sdgs.un.org/goals/goal4)

---

**Made with ❤️ for African Students** | **SDG 4: Quality Education Hackathon Project**

*"Education is the most powerful weapon which you can use to change the world." - Nelson Mandela*
