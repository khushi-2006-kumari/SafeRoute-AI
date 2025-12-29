from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Mock safety data for different areas
AREA_SAFETY_DATA = {
    "connaught_place": {"day_score": 8, "night_score": 6, "crowd_density": "high", "lighting": "good"},
    "karol_bagh": {"day_score": 7, "night_score": 5, "crowd_density": "medium", "lighting": "moderate"},
    "lajpat_nagar": {"day_score": 7, "night_score": 4, "crowd_density": "medium", "lighting": "poor"},
    "nehru_place": {"day_score": 6, "night_score": 3, "crowd_density": "low", "lighting": "poor"},
    "rajouri_garden": {"day_score": 8, "night_score": 7, "crowd_density": "high", "lighting": "good"},
    "dwarka": {"day_score": 9, "night_score": 8, "crowd_density": "high", "lighting": "excellent"},
    "gurgaon": {"day_score": 8, "night_score": 6, "crowd_density": "medium", "lighting": "good"},
    "noida": {"day_score": 7, "night_score": 5, "crowd_density": "medium", "lighting": "moderate"}
}

def calculate_safety_score(route_areas, time_of_day):
    """Calculate safety score based on areas and time of day"""
    total_score = 0
    area_count = len(route_areas)
    
    for area in route_areas:
        area_data = AREA_SAFETY_DATA.get(area, {"day_score": 5, "night_score": 3})
        if time_of_day == "night":
            total_score += area_data["night_score"]
        else:
            total_score += area_data["day_score"]
    
    return round(total_score / area_count, 1) if area_count > 0 else 5.0

def get_safety_features(route_areas, time_of_day):
    """Get safety features for the route"""
    features = []
    
    # Check lighting
    good_lighting_count = sum(1 for area in route_areas 
                             if AREA_SAFETY_DATA.get(area, {}).get("lighting") in ["good", "excellent"])
    if good_lighting_count > len(route_areas) / 2:
        features.append("Well-lit streets")
    
    # Check crowd density
    high_crowd_count = sum(1 for area in route_areas 
                          if AREA_SAFETY_DATA.get(area, {}).get("crowd_density") == "high")
    if high_crowd_count > 0:
        features.append("Crowded areas")
    
    # Time-based features
    if time_of_day == "day":
        features.append("Daytime travel")
    else:
        features.append("Night travel - extra caution")
    
    # Add some default safety features
    features.extend(["Main roads", "Police patrol areas"])
    
    return features

def get_risk_level(safety_score):
    """Get risk level based on safety score"""
    if safety_score >= 7:
        return "Low"
    elif safety_score >= 4:
        return "Medium"
    else:
        return "High"

@app.route('/')
def home():
    return jsonify({
        "message": "SafeRoute AI Backend API",
        "status": "running",
        "version": "1.0.0"
    })

@app.route('/find-routes', methods=['POST'])
def find_routes():
    try:
        data = request.get_json()
        
        source = data.get('source', '').lower()
        destination = data.get('destination', '').lower()
        time_of_day = data.get('time_of_day', 'day')
        
        if not source or not destination:
            return jsonify({"error": "Source and destination are required"}), 400
        
        # Generate mock routes based on source and destination
        routes = generate_mock_routes(source, destination, time_of_day)
        
        # Sort routes by safety score (highest first)
        routes.sort(key=lambda x: x['safety_score'], reverse=True)
        
        return jsonify({
            "routes": routes,
            "total_routes": len(routes),
            "time_of_day": time_of_day,
            "message": f"Found {len(routes)} routes from {source} to {destination}"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def generate_mock_routes(source, destination, time_of_day):
    """Generate mock routes with different safety characteristics"""
    
    # Base coordinates (Delhi area)
    base_coords = {
        "start": {"lat": 28.6139, "lng": 77.2090},
        "end": {"lat": 28.6304, "lng": 77.2177}
    }
    
    routes = []
    
    # Route 1: Safest route (via main roads)
    route1_areas = ["connaught_place", "rajouri_garden", "dwarka"]
    safety_score1 = calculate_safety_score(route1_areas, time_of_day)
    
    routes.append({
        "name": "Main Road Route",
        "distance": "12.5 km",
        "duration": "25 mins",
        "safety_score": safety_score1,
        "risk_level": get_risk_level(safety_score1),
        "safety_features": get_safety_features(route1_areas, time_of_day),
        "coordinates": {
            "start": base_coords["start"],
            "end": base_coords["end"],
            "path": [
                [28.6139, 77.2090],
                [28.6200, 77.2120],
                [28.6250, 77.2150],
                [28.6304, 77.2177]
            ]
        }
    })
    
    # Route 2: Moderate safety route
    route2_areas = ["karol_bagh", "lajpat_nagar"]
    safety_score2 = calculate_safety_score(route2_areas, time_of_day)
    
    routes.append({
        "name": "Alternative Route",
        "distance": "10.8 km",
        "duration": "22 mins",
        "safety_score": safety_score2,
        "risk_level": get_risk_level(safety_score2),
        "safety_features": get_safety_features(route2_areas, time_of_day),
        "coordinates": {
            "start": base_coords["start"],
            "end": base_coords["end"],
            "path": [
                [28.6139, 77.2090],
                [28.6180, 77.2100],
                [28.6220, 77.2130],
                [28.6280, 77.2160],
                [28.6304, 77.2177]
            ]
        }
    })
    
    # Route 3: Fastest but less safe route
    route3_areas = ["nehru_place", "lajpat_nagar"]
    safety_score3 = calculate_safety_score(route3_areas, time_of_day)
    
    routes.append({
        "name": "Fastest Route",
        "distance": "9.2 km",
        "duration": "18 mins",
        "safety_score": safety_score3,
        "risk_level": get_risk_level(safety_score3),
        "safety_features": get_safety_features(route3_areas, time_of_day),
        "coordinates": {
            "start": base_coords["start"],
            "end": base_coords["end"],
            "path": [
                [28.6139, 77.2090],
                [28.6170, 77.2110],
                [28.6240, 77.2140],
                [28.6304, 77.2177]
            ]
        }
    })
    
    return routes

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    print("Starting SafeRoute AI Backend...")
    print(f"API will be available at: https://saferoute-ai-2-no7k.onrender.com")
    app.run(debug=False, host='0.0.0.0', port=port)