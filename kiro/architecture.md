# System Architecture

SafeRoute AI follows a lightweight, modular architecture designed for rapid development and cross-platform deployment during a hackathon.

---

## 1. Frontend Layer (Mobile-First Web Application)

**Technologies:** HTML5, CSS3, JavaScript (Mobile-Optimized)

- **17-Screen Mobile App**: Complete mobile experience with professional UI/UX
- **No Design Tools Used**: Direct code-to-design approach for rapid development
- **Mobile-First Responsive**: Optimized for smartphones with touch navigation
- **Key Screens Include**:
  - Splash Screen with animated logo
  - 3-screen onboarding flow
  - Login/signup with social options
  - Location permission request
  - Home screen with map interface
  - AI chat assistant
  - Profile and settings
  - Route options with safety scoring
  - Live navigation with Google Maps
  - Emergency SOS with one-tap activation
  - Safety reporting system
  - Working route finder
  - Safety insights and analytics

---

## 2. Navigation & User Experience

**Implementation:** Pure JavaScript with Touch Support

- **Swipe Navigation**: Left/right swipe between screens
- **Button Navigation**: Previous/Next/Home buttons on all screens
- **Keyboard Support**: Arrow keys for desktop testing
- **Screen Transitions**: Smooth animations between 17 screens
- **Mobile Optimized**: Touch-friendly buttons and responsive design

---

## 3. Backend Layer (Flask API)

**Technologies:** Python Flask with CORS Support

- **RESTful API**: Clean endpoints for route finding and safety scoring
- **Safety Algorithm**: Weighted scoring system considering:
  - Time of day factor (40% weight)
  - Area risk level (35% weight)  
  - Crowd density (25% weight)
- **Mock Data**: Comprehensive Delhi NCR area safety database
- **Error Handling**: Proper HTTP status codes and error responses
- **CORS Enabled**: Cross-origin requests for frontend integration

---

## 4. Safety Evaluation & Recommendation Module

**Core Algorithm Implementation:**

```python
def calculate_safety_score(route_areas, time_of_day):
    total_score = 0
    area_count = len(route_areas)
    
    for area in route_areas:
        area_data = AREA_SAFETY_DATA.get(area, {"day_score": 5, "night_score": 3})
        if time_of_day == "night":
            total_score += area_data["night_score"]
        else:
            total_score += area_data["day_score"]
    
    return round(total_score / area_count, 1) if area_count > 0 else 5.0
```

- **Multi-Route Generation**: Creates 3 route options (Safest, Balanced, Fastest)
- **Dynamic Scoring**: Different safety calculations for day vs night
- **Risk Assessment**: Categorizes routes as Safe/Moderate/Risky
- **Feature Detection**: Identifies safety features like lighting, CCTV, police presence

---

## 5. Data Layer

**Type:** Structured Mock Data (Python Dictionaries)

```python
AREA_SAFETY_DATA = {
    "connaught_place": {"day_score": 8, "night_score": 6, "crowd_density": "high", "lighting": "good"},
    "dwarka": {"day_score": 9, "night_score": 8, "crowd_density": "high", "lighting": "excellent"},
    # ... comprehensive Delhi NCR coverage
}
```

- **Realistic Safety Scores**: Based on actual Delhi area characteristics
- **Time-Sensitive Data**: Different day/night safety ratings
- **Comprehensive Coverage**: Major Delhi NCR areas included
- **Future-Ready**: Structure supports real API integration

---

## 6. Maps & Visualization

**Technologies:** Leaflet.js + OpenStreetMap

- **Interactive Maps**: Real-time route visualization
- **Safety Zones**: Color-coded areas (Green/Yellow/Red)
- **Route Paths**: Visual route lines with safety indicators
- **Live Navigation**: Simulated GPS tracking with location markers
- **Responsive Design**: Works on all screen sizes

---

## 7. Deployment & Hosting

- **Frontend:** Netlify (Static hosting for mobile app)
- **Backend:** Can be deployed to Render/Railway/Heroku
- **Development:** Local development with Flask dev server
- **Cross-Platform:** Works on web browsers, mobile devices

---

## 8. Architecture Flow

User Input (Mobile App)
→ 17-Screen Navigation Experience  
→ Route Finder (Screen 16)
→ Flask Backend API  
→ Safety Evaluation Algorithm  
→ Route Recommendations with Safety Scores
→ Interactive Map Display
→ User Selection & Navigation

---

## 9. Key Technical Decisions

**No Design Tools**: Direct HTML/CSS/JS implementation for rapid development
**Mobile-First**: Optimized for smartphone usage patterns
**Standalone Frontend**: 16/17 screens work without backend
**Lightweight Backend**: Simple Flask API for route calculations
**Mock Data Strategy**: Hackathon-friendly approach with realistic scenarios

---

## 10. Scalability & Future Enhancements

- **Real-time APIs**: Google Maps, crime databases, traffic data
- **Community Features**: User-reported incidents and safety updates
- **Machine Learning**: AI-powered safety prediction models
- **Native Apps**: React Native or Flutter for app stores
- **Emergency Integration**: Direct connection to emergency services