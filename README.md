# Weather Forecast Application 

## About the Project
Flask application for viewing current weather in any city worldwide using OpenWeatherMap API.  
The project includes:
- Information about temperature, humidity, wind speed and other parameters
- Query history with PostgreSQL storage
- City autocompletion when typing
- Docker containerization for easy deployment

## Advantages
- Easy to use (intuitive interface)
- Local storage of query history
- Cross-platform support (works through Docker)
- API key protection

## Quick Start

### Prerequisites
- Docker Desktop (version 20.10.0+)
- Docker Compose (version 1.29.0+)
- Active OpenWeatherMap API key

### Installation
1. Register at https://openweathermap.org/ and get your API_KEY 
2. Download the repository using your preferred method
3. Launch Docker Engine
4. Open terminal in the project folder
5. For Windows enter:  
   $env:API_KEY="YOUR_KEY"; docker-compose up
   For Linux enter:
   API_KEY=YOUR_KEY docker-compose up
   The application will be available at: http://localhost:5000

### How to Use

- Start typing a city name in the search field
- Select the desired option from the dropdown list
- Click "Get Forecast" to view weather
- Use "Forecast History" to view query history

*For test task evaluation use: API_KEY="d9db6586cfd1077e913484e6117d8b3d"
