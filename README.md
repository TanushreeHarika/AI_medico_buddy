<p align="center">
  <img src="https://img.shields.io/badge/Next.js-16-black?style=for-the-badge&logo=next.js" alt="Next.js" />
  <img src="https://img.shields.io/badge/Tailwind_CSS-v4-38B2AC?style=for-the-badge&logo=tailwind-css" alt="Tailwind CSS" />
  <img src="https://img.shields.io/badge/TypeScript-5-3178C6?style=for-the-badge&logo=typescript" alt="TypeScript" />
  <img src="https://img.shields.io/badge/Flask-3-000?style=for-the-badge&logo=flask" alt="Flask" />
  <img src="https://img.shields.io/badge/Supabase-Database-3ECF8E?style=for-the-badge&logo=supabase" alt="Supabase" />
  <img src="https://img.shields.io/badge/Gemini_AI-Powered-4285F4?style=for-the-badge&logo=google" alt="Gemini AI" />
</p>

# ❤️‍🩹 LifePulse — Medical Emergency Response System

> **Every Second Counts.** A high-performance, AI-powered medical emergency response platform with real-time monitoring, instant first-aid guidance, and autonomous hospital dispatch.

---

## 🌟 Features

| Feature | Description |
|---------|-------------|
| 🗺️ **Real-time Dashboard** | Google Maps integration with browser geolocation, nearby ambulance tracking, and SOS emergency button with countdown |
| 🤖 **AI Assistant** | Gemini-powered chatbot supporting both text and image (Vision) analysis for instant first-aid guidance |
| 📚 **First Aid Library** | 12+ medical conditions with searchable cards, category filters, severity badges, and step-by-step instructions |
| 🚨 **Autonomous Agent** | Automatically detects fatal conditions (heart attack, stroke), simulates emergency calls, and sends patient data to the Hospital Notification table in Supabase |
| 🌙 **Dark Mode** | Sleek dark/light mode toggle with smooth animated transitions |
| 📱 **Mobile Responsive** | Fully responsive design with glassmorphism navbar and hamburger menu |
| 📄 **Terms & Conditions** | Complete medical disclaimer and safety notice |

---

## 🖼️ Screenshots

<details>
<summary>Click to expand</summary>

### Landing Page
Clean hero section with "Every Second Counts" headline, gradient text, animated heartbeat visual, and feature cards.

### Dashboard
Real-time map view with location stats, SOS countdown button, nearby ambulance tracking, and quick emergency actions.

### AI Assistant
Gemini-powered chat interface with suggested prompts, image upload for visual analysis, and smart fallback responses.

### First Aid Library
Searchable grid of 12 medical conditions with category filters and color-coded severity badges (Low → Critical).

### Heart Attack Detail — Autonomous Agent
Emergency agent auto-activates on fatal conditions with hospital notification dispatch and step-by-step CPR instructions.

</details>

---

## 🏗️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Next.js 16, React 19, TypeScript 5, Tailwind CSS v4 |
| **Backend** | Flask 3 (Python) |
| **Database** | Supabase (PostgreSQL) |
| **AI Engine** | Google Gemini 2.0 Flash (Text + Vision) |
| **Animations** | Framer Motion |
| **Auth/DB** | Supabase Client |
| **Icons** | Lucide React |
| **Theming** | next-themes |

---

## 📂 Project Structure

```
lifepulse/
├── frontend/                        # Next.js + Tailwind + TypeScript
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx             # Landing page
│   │   │   ├── dashboard/           # Real-time monitoring + Google Maps
│   │   │   ├── ai-assistant/        # Gemini AI chat + image upload
│   │   │   ├── first-aid/           # Library + [slug] detail pages
│   │   │   └── terms/               # Terms & Conditions
│   │   ├── components/              # Navbar, Footer, ThemeProvider
│   │   └── lib/                     # Supabase client, first-aid data
│   └── package.json
│
├── backend/                         # Flask API
│   ├── app.py                       # Main API server
│   ├── agents/
│   │   └── emergency_agent.py       # Autonomous emergency dispatch
│   ├── supabase_schema.sql          # Database schema
│   └── requirements.txt
│
├── .env.example                     # Environment variable template
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- **Node.js** ≥ 18
- **Python** ≥ 3.9
- **npm** or **yarn**
- A [Supabase](https://supabase.com) account (free tier works)
- A [Google AI Studio](https://aistudio.google.com) API key

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/lifepulse.git
cd lifepulse
```

### 2. Set Up Environment Variables

```bash
# Copy the template
cp .env.example frontend/.env.local
cp .env.example backend/.env
```

Edit both files with your actual keys:

| Variable | Where to get it |
|----------|----------------|
| `NEXT_PUBLIC_SUPABASE_URL` | Supabase → Project Settings → API |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Supabase → Project Settings → API |
| `SUPABASE_SERVICE_KEY` | Supabase → Project Settings → API (service_role) |
| `GEMINI_API_KEY` | [Google AI Studio](https://aistudio.google.com/apikey) |

### 3. Set Up Supabase Database

Run the SQL in `backend/supabase_schema.sql` in your **Supabase SQL Editor** to create the `hospital_notifications` table.

### 4. Install & Run Frontend

```bash
cd frontend
npm install
npm run dev
# → http://localhost:3000
```

### 5. Install & Run Backend

```bash
cd backend
pip install -r requirements.txt
python app.py
# → http://localhost:5000
```

---

## 📋 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/ai/chat` | Send text message → Gemini AI response |
| `POST` | `/api/ai/vision` | Upload image + message → Gemini Vision analysis |
| `POST` | `/api/emergency/trigger` | Trigger autonomous emergency agent |
| `GET` | `/api/health` | Health check with service status |

---

## 🏥 First Aid Conditions Covered

| Condition | Severity | Fatal |
|-----------|----------|-------|
| Low Blood Pressure | 🟢 Low | No |
| Fatigue & Exhaustion | 🟢 Low | No |
| Minor Burns | 🟡 Medium | No |
| Cuts & Bleeding | 🟡 Medium | No |
| Sprains & Fractures | 🟡 Medium | No |
| Choking | 🟠 High | No |
| Allergic Reaction | 🟠 High | No |
| Seizures | 🟠 High | No |
| Heatstroke | 🟠 High | No |
| Hypothermia | 🟠 High | No |
| **Heart Attack** | 🔴 Critical | **Yes** |
| **Stroke** | 🔴 Critical | **Yes** |

> Fatal conditions automatically trigger the **Autonomous Emergency Agent** which simulates emergency dispatch and sends notifications to the hospital database.

---

## ⚠️ Disclaimer

> **LifePulse is for educational and informational purposes only.** It is **NOT** a substitute for professional medical advice, diagnosis, or treatment. The Emergency SOS and Autonomous Agent features are **simulations** and do NOT connect to actual emergency services. In a real emergency, always call your local emergency number (911, 112, 108) directly.

---

## 🛠️ Design Philosophy

- **Apple-esque Editorial Minimalism** — Clean, light-themed default with premium dark mode
- **Gen-Z Aesthetic** — Soft shadows, rounded-3xl corners, gradient accents, fluid animations
- **Glassmorphism** — Frosted glass navbar with backdrop blur
- **Motion Design** — Framer Motion for fade-up, spring, heartbeat, and stagger animations
- **Typography** — Inter font family from Google Fonts

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<p align="center">
  Built with ❤️ for saving lives
</p>
