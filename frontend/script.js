// API Configuration
const API_BASE_URL = 'http://localhost:5000';

// DOM Elements
const routeForm = document.getElementById('routeForm');
const loadingDiv = document.getElementById('loading');
const resultsDiv = document.getElementById('results');
const routeListDiv = document.getElementById('routeList');
const mapDiv = document.getElementById('map');

let map = null;

// Form submission handler
routeForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const source = document.getElementById('source').value;
    const destination = document.getElementById('destination').value;
    const timeOfDay = document.getElementById('timeOfDay').value;
    
    await findRoutes(source, destination, timeOfDay);
});

// Main function to find routes
async function findRoutes(source, destination, timeOfDay) {
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE_URL}/find-routes`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                source: source,
                destination: destination,
                time_of_day: timeOfDay
            })
        });
        
        if (!response.ok) {
            throw new Error('Failed to fetch routes');
        }
        
        const data = await response.json();
        displayRoutes(data.routes);
        
    } catch (error) {
        console.error('Error:', error);
        showError('Failed to find routes. Please try again.');
    }
}

// Show loading state
function showLoading() {
    loadingDiv.classList.remove('hidden');
    resultsDiv.classList.add('hidden');
    mapDiv.classList.add('hidden');
}

// Display routes
function displayRoutes(routes) {
    loadingDiv.classList.add('hidden');
    resultsDiv.classList.remove('hidden');
    
    routeListDiv.innerHTML = '';
    
    routes.forEach((route, index) => {
        const routeCard = createRouteCard(route, index);
        routeListDiv.appendChild(routeCard);
    });
    
    // Show map with routes
    showMap(routes);
}

// Create route card HTML
function createRouteCard(route, index) {
    const card = document.createElement('div');
    card.className = 'route-card';
    
    const safetyClass = getSafetyClass(route.safety_score);
    const safetyText = getSafetyText(route.safety_score);
    
    card.innerHTML = `
        <div class="route-header">
            <div class="route-name">${route.name}</div>
            <div class="safety-score ${safetyClass}">${safetyText}</div>
        </div>
        <div class="route-details">
            <div class="detail-item">
                <div class="detail-label">Distance</div>
                <div class="detail-value">${route.distance}</div>
            </div>
            <div class="detail-item">
                <div class="detail-label">Duration</div>
                <div class="detail-value">${route.duration}</div>
            </div>
            <div class="detail-item">
                <div class="detail-label">Safety Score</div>
                <div class="detail-value">${route.safety_score}/10</div>
            </div>
            <div class="detail-item">
                <div class="detail-label">Risk Level</div>
                <div class="detail-value">${route.risk_level}</div>
            </div>
        </div>
        <div style="margin-top: 10px; font-size: 0.9rem; color: #666;">
            <strong>Safety Features:</strong> ${route.safety_features.join(', ')}
        </div>
    `;
    
    return card;
}

// Get safety class for styling
function getSafetyClass(score) {
    if (score >= 7) return 'safety-high';
    if (score >= 4) return 'safety-medium';
    return 'safety-low';
}

// Get safety text
function getSafetyText(score) {
    if (score >= 7) return 'Safe';
    if (score >= 4) return 'Moderate';
    return 'Risky';
}

// Show map with routes
function showMap(routes) {
    mapDiv.classList.remove('hidden');
    
    if (map) {
        map.remove();
    }
    
    // Initialize map (centered on a default location)
    map = L.map('map').setView([28.6139, 77.2090], 12); // Delhi coordinates
    
    // Add tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);
    
    // Add route markers
    const colors = ['red', 'blue', 'green', 'orange', 'purple'];
    
    routes.forEach((route, index) => {
        const color = colors[index % colors.length];
        
        // Add start marker
        L.marker([route.coordinates.start.lat, route.coordinates.start.lng])
            .addTo(map)
            .bindPopup(`Start: ${route.name}`);
        
        // Add end marker
        L.marker([route.coordinates.end.lat, route.coordinates.end.lng])
            .addTo(map)
            .bindPopup(`End: ${route.name}`);
        
        // Add route line
        const routeLine = L.polyline(route.coordinates.path, {
            color: color,
            weight: 4,
            opacity: 0.7
        }).addTo(map);
        
        routeLine.bindPopup(`${route.name} - Safety: ${route.safety_score}/10`);
    });
    
    // Fit map to show all routes
    const group = new L.featureGroup();
    routes.forEach(route => {
        route.coordinates.path.forEach(coord => {
            L.marker(coord).addTo(group);
        });
    });
    
    if (group.getLayers().length > 0) {
        map.fitBounds(group.getBounds().pad(0.1));
    }
}

// Show error message
function showError(message) {
    loadingDiv.classList.add('hidden');
    resultsDiv.classList.remove('hidden');
    routeListDiv.innerHTML = `
        <div style="text-align: center; padding: 20px; color: #dc3545;">
            <h3>Error</h3>
            <p>${message}</p>
        </div>
    `;
}