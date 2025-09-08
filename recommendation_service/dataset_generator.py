"""
Dataset Generator for Project Recommendations
Creates a comprehensive dataset of project ideas for the recommendation system
"""

import json
import random
from typing import List, Dict

def generate_project_dataset() -> List[Dict]:
    """Generate a comprehensive dataset of project ideas"""
    
    projects = []
    
    # Web Development Projects
    web_projects = [
        {
            "project_id": "web_001",
            "title": "Personal Portfolio Website",
            "description": "Build a responsive portfolio website showcasing your projects and skills with modern design",
            "difficulty": "beginner",
            "estimated_time": "1-2 weeks",
            "technologies": ["HTML", "CSS", "JavaScript", "React"],
            "categories": ["web-development", "frontend", "portfolio"],
            "learning_objectives": ["Responsive design", "Modern CSS", "JavaScript DOM manipulation", "React basics"],
            "prerequisites": ["Basic HTML/CSS knowledge"],
            "project_type": "portfolio",
            "domain": "web-development",
            "complexity_score": 3,
            "popularity_score": 8.5,
            "tags": ["portfolio", "responsive", "modern", "showcase"]
        },
        {
            "project_id": "web_002",
            "title": "E-commerce Store",
            "description": "Create a full-stack e-commerce platform with shopping cart, user authentication, and payment integration",
            "difficulty": "intermediate",
            "estimated_time": "4-6 weeks",
            "technologies": ["React", "Node.js", "Express", "MongoDB", "Stripe"],
            "categories": ["web-development", "fullstack", "ecommerce"],
            "learning_objectives": ["Full-stack development", "Payment processing", "User authentication", "Database design"],
            "prerequisites": ["JavaScript", "React basics", "Node.js basics"],
            "project_type": "application",
            "domain": "web-development",
            "complexity_score": 7,
            "popularity_score": 9.2,
            "tags": ["ecommerce", "fullstack", "payment", "authentication"]
        },
        {
            "project_id": "web_003",
            "title": "Real-time Chat Application",
            "description": "Build a real-time chat app with WebSocket support, multiple rooms, and user presence",
            "difficulty": "intermediate",
            "estimated_time": "3-4 weeks",
            "technologies": ["Socket.io", "Node.js", "React", "MongoDB"],
            "categories": ["web-development", "realtime", "websockets"],
            "learning_objectives": ["WebSocket programming", "Real-time communication", "State management", "User presence"],
            "prerequisites": ["JavaScript", "Node.js", "React"],
            "project_type": "application",
            "domain": "web-development",
            "complexity_score": 6,
            "popularity_score": 8.8,
            "tags": ["chat", "realtime", "websockets", "communication"]
        },
        {
            "project_id": "web_004",
            "title": "Task Management Dashboard",
            "description": "Create a comprehensive task management system with drag-and-drop, team collaboration, and analytics",
            "difficulty": "advanced",
            "estimated_time": "6-8 weeks",
            "technologies": ["React", "TypeScript", "Node.js", "PostgreSQL", "Redis"],
            "categories": ["web-development", "productivity", "dashboard"],
            "learning_objectives": ["Complex state management", "Drag-and-drop interfaces", "Team collaboration", "Data visualization"],
            "prerequisites": ["Advanced React", "TypeScript", "Database design"],
            "project_type": "application",
            "domain": "web-development",
            "complexity_score": 9,
            "popularity_score": 8.0,
            "tags": ["productivity", "dashboard", "collaboration", "analytics"]
        },
        {
            "project_id": "web_005",
            "title": "Weather App with Maps",
            "description": "Build a weather application with interactive maps, forecasts, and location-based services",
            "difficulty": "beginner",
            "estimated_time": "2-3 weeks",
            "technologies": ["JavaScript", "OpenWeather API", "Leaflet.js", "CSS"],
            "categories": ["web-development", "api-integration", "maps"],
            "learning_objectives": ["API integration", "Map libraries", "Geolocation", "Responsive design"],
            "prerequisites": ["JavaScript basics", "HTML/CSS"],
            "project_type": "application",
            "domain": "web-development",
            "complexity_score": 4,
            "popularity_score": 7.5,
            "tags": ["weather", "maps", "api", "geolocation"]
        }
    ]
    
    # Mobile Development Projects
    mobile_projects = [
        {
            "project_id": "mobile_001",
            "title": "Fitness Tracking App",
            "description": "Create a mobile app for tracking workouts, nutrition, and fitness goals with data visualization",
            "difficulty": "intermediate",
            "estimated_time": "4-5 weeks",
            "technologies": ["React Native", "Firebase", "Chart.js", "AsyncStorage"],
            "categories": ["mobile-development", "health", "tracking"],
            "learning_objectives": ["Mobile development", "Data persistence", "Charts and graphs", "User experience"],
            "prerequisites": ["JavaScript", "React basics"],
            "project_type": "application",
            "domain": "mobile-development",
            "complexity_score": 6,
            "popularity_score": 8.3,
            "tags": ["fitness", "tracking", "mobile", "health"]
        },
        {
            "project_id": "mobile_002",
            "title": "Food Delivery App",
            "description": "Build a food delivery mobile app with restaurant listings, ordering, and real-time tracking",
            "difficulty": "advanced",
            "estimated_time": "8-10 weeks",
            "technologies": ["Flutter", "Firebase", "Google Maps", "Stripe"],
            "categories": ["mobile-development", "ecommerce", "delivery"],
            "learning_objectives": ["Cross-platform development", "Real-time updates", "Payment integration", "Location services"],
            "prerequisites": ["Dart/Flutter", "Firebase", "Mobile development"],
            "project_type": "application",
            "domain": "mobile-development",
            "complexity_score": 9,
            "popularity_score": 9.0,
            "tags": ["delivery", "ecommerce", "mobile", "realtime"]
        },
        {
            "project_id": "mobile_003",
            "title": "Note-Taking App",
            "description": "Develop a cross-platform note-taking app with rich text editing, organization, and sync",
            "difficulty": "intermediate",
            "estimated_time": "3-4 weeks",
            "technologies": ["React Native", "SQLite", "CloudKit", "Rich Text Editor"],
            "categories": ["mobile-development", "productivity", "notes"],
            "learning_objectives": ["Mobile development", "Local storage", "Cloud sync", "Rich text editing"],
            "prerequisites": ["JavaScript", "React Native basics"],
            "project_type": "application",
            "domain": "mobile-development",
            "complexity_score": 5,
            "popularity_score": 7.8,
            "tags": ["notes", "productivity", "mobile", "sync"]
        }
    ]
    
    # Data Science & ML Projects
    data_projects = [
        {
            "project_id": "data_001",
            "title": "Stock Price Predictor",
            "description": "Build a machine learning model to predict stock prices using historical data and technical indicators",
            "difficulty": "intermediate",
            "estimated_time": "4-5 weeks",
            "technologies": ["Python", "Pandas", "Scikit-learn", "Matplotlib", "Yahoo Finance API"],
            "categories": ["data-science", "machine-learning", "finance"],
            "learning_objectives": ["Time series analysis", "Feature engineering", "Model evaluation", "Financial data"],
            "prerequisites": ["Python", "Pandas", "Basic ML concepts"],
            "project_type": "analysis",
            "domain": "data-science",
            "complexity_score": 7,
            "popularity_score": 8.7,
            "tags": ["stocks", "prediction", "ml", "finance"]
        },
        {
            "project_id": "data_002",
            "title": "Customer Segmentation Analysis",
            "description": "Analyze customer data to create segments and develop targeted marketing strategies",
            "difficulty": "intermediate",
            "estimated_time": "3-4 weeks",
            "technologies": ["Python", "Pandas", "Scikit-learn", "Seaborn", "Jupyter"],
            "categories": ["data-science", "clustering", "business"],
            "learning_objectives": ["Clustering algorithms", "Data visualization", "Business insights", "Statistical analysis"],
            "prerequisites": ["Python", "Pandas", "Basic statistics"],
            "project_type": "analysis",
            "domain": "data-science",
            "complexity_score": 6,
            "popularity_score": 8.1,
            "tags": ["clustering", "business", "analysis", "customers"]
        },
        {
            "project_id": "data_003",
            "title": "Image Classification App",
            "description": "Create a web app that classifies images using deep learning with a user-friendly interface",
            "difficulty": "advanced",
            "estimated_time": "5-6 weeks",
            "technologies": ["Python", "TensorFlow", "Flask", "OpenCV", "HTML/CSS"],
            "categories": ["data-science", "deep-learning", "computer-vision"],
            "learning_objectives": ["Deep learning", "Computer vision", "Model deployment", "Web integration"],
            "prerequisites": ["Python", "TensorFlow basics", "Web development"],
            "project_type": "application",
            "domain": "data-science",
            "complexity_score": 8,
            "popularity_score": 8.9,
            "tags": ["image", "classification", "deep-learning", "computer-vision"]
        },
        {
            "project_id": "data_004",
            "title": "Sales Dashboard",
            "description": "Build an interactive dashboard for sales data analysis with charts, filters, and insights",
            "difficulty": "intermediate",
            "estimated_time": "3-4 weeks",
            "technologies": ["Python", "Streamlit", "Pandas", "Plotly", "SQL"],
            "categories": ["data-science", "visualization", "dashboard"],
            "learning_objectives": ["Data visualization", "Interactive dashboards", "Business intelligence", "SQL queries"],
            "prerequisites": ["Python", "Pandas", "Basic SQL"],
            "project_type": "dashboard",
            "domain": "data-science",
            "complexity_score": 5,
            "popularity_score": 7.9,
            "tags": ["dashboard", "sales", "visualization", "business"]
        }
    ]
    
    # DevOps & Cloud Projects
    devops_projects = [
        {
            "project_id": "devops_001",
            "title": "Dockerized Microservices",
            "description": "Containerize a multi-service application and set up orchestration with Docker Compose",
            "difficulty": "intermediate",
            "estimated_time": "2-3 weeks",
            "technologies": ["Docker", "Docker Compose", "Nginx", "PostgreSQL"],
            "categories": ["devops", "containers", "microservices"],
            "learning_objectives": ["Containerization", "Service orchestration", "Load balancing", "Database setup"],
            "prerequisites": ["Docker basics", "Microservices concepts"],
            "project_type": "infrastructure",
            "domain": "devops",
            "complexity_score": 6,
            "popularity_score": 8.4,
            "tags": ["docker", "microservices", "containers", "orchestration"]
        },
        {
            "project_id": "devops_002",
            "title": "CI/CD Pipeline",
            "description": "Set up automated testing, building, and deployment pipeline using GitHub Actions",
            "difficulty": "intermediate",
            "estimated_time": "2-3 weeks",
            "technologies": ["GitHub Actions", "Docker", "AWS/Heroku", "Testing frameworks"],
            "categories": ["devops", "cicd", "automation"],
            "learning_objectives": ["CI/CD concepts", "Automated testing", "Cloud deployment", "Pipeline optimization"],
            "prerequisites": ["Git", "Docker", "Cloud platforms"],
            "project_type": "infrastructure",
            "domain": "devops",
            "complexity_score": 7,
            "popularity_score": 8.6,
            "tags": ["cicd", "automation", "testing", "deployment"]
        },
        {
            "project_id": "devops_003",
            "title": "Infrastructure as Code",
            "description": "Use Terraform to provision cloud infrastructure and manage resources programmatically",
            "difficulty": "advanced",
            "estimated_time": "3-4 weeks",
            "technologies": ["Terraform", "AWS/Azure", "Ansible", "Git"],
            "categories": ["devops", "iac", "cloud"],
            "learning_objectives": ["Infrastructure as Code", "Cloud provisioning", "Resource management", "Automation"],
            "prerequisites": ["Cloud platforms", "YAML", "Command line"],
            "project_type": "infrastructure",
            "domain": "devops",
            "complexity_score": 8,
            "popularity_score": 8.2,
            "tags": ["terraform", "iac", "cloud", "automation"]
        }
    ]
    
    # Game Development Projects
    game_projects = [
        {
            "project_id": "game_001",
            "title": "2D Platformer Game",
            "description": "Create a 2D platformer game with physics, animations, and multiple levels",
            "difficulty": "intermediate",
            "estimated_time": "4-5 weeks",
            "technologies": ["Unity", "C#", "Photoshop", "Audacity"],
            "categories": ["game-development", "2d", "platformer"],
            "learning_objectives": ["Game physics", "Animation systems", "Level design", "Game programming"],
            "prerequisites": ["C# basics", "Unity basics"],
            "project_type": "game",
            "domain": "game-development",
            "complexity_score": 6,
            "popularity_score": 8.5,
            "tags": ["platformer", "2d", "unity", "game"]
        },
        {
            "project_id": "game_002",
            "title": "Web-based Puzzle Game",
            "description": "Build a browser-based puzzle game with HTML5 Canvas and JavaScript",
            "difficulty": "beginner",
            "estimated_time": "2-3 weeks",
            "technologies": ["HTML5 Canvas", "JavaScript", "CSS", "Web Audio API"],
            "categories": ["game-development", "web", "puzzle"],
            "learning_objectives": ["Canvas programming", "Game loops", "User input", "Audio integration"],
            "prerequisites": ["JavaScript", "HTML/CSS"],
            "project_type": "game",
            "domain": "game-development",
            "complexity_score": 4,
            "popularity_score": 7.2,
            "tags": ["puzzle", "web", "canvas", "game"]
        },
        {
            "project_id": "game_003",
            "title": "Multiplayer Card Game",
            "description": "Develop a real-time multiplayer card game with WebSocket communication",
            "difficulty": "advanced",
            "estimated_time": "6-8 weeks",
            "technologies": ["Node.js", "Socket.io", "React", "MongoDB"],
            "categories": ["game-development", "multiplayer", "realtime"],
            "learning_objectives": ["Real-time communication", "Game state management", "Multiplayer architecture", "WebSocket programming"],
            "prerequisites": ["Node.js", "WebSocket concepts", "Game development"],
            "project_type": "game",
            "domain": "game-development",
            "complexity_score": 9,
            "popularity_score": 8.8,
            "tags": ["multiplayer", "cards", "realtime", "websockets"]
        }
    ]
    
    # Desktop Application Projects
    desktop_projects = [
        {
            "project_id": "desktop_001",
            "title": "File Manager Application",
            "description": "Create a desktop file manager with advanced features like search, preview, and organization",
            "difficulty": "intermediate",
            "estimated_time": "3-4 weeks",
            "technologies": ["Electron", "React", "Node.js", "File System API"],
            "categories": ["desktop-development", "file-management", "productivity"],
            "learning_objectives": ["Desktop app development", "File system operations", "Cross-platform development", "Native integration"],
            "prerequisites": ["JavaScript", "React", "Electron basics"],
            "project_type": "application",
            "domain": "desktop-development",
            "complexity_score": 6,
            "popularity_score": 7.6,
            "tags": ["file-manager", "desktop", "productivity", "electron"]
        },
        {
            "project_id": "desktop_002",
            "title": "System Monitor Dashboard",
            "description": "Build a system monitoring tool that displays CPU, memory, and network usage in real-time",
            "difficulty": "intermediate",
            "estimated_time": "3-4 weeks",
            "technologies": ["Python", "Tkinter", "Psutil", "Matplotlib"],
            "categories": ["desktop-development", "monitoring", "system"],
            "learning_objectives": ["System programming", "Real-time data", "GUI development", "Performance monitoring"],
            "prerequisites": ["Python", "GUI frameworks"],
            "project_type": "application",
            "domain": "desktop-development",
            "complexity_score": 5,
            "popularity_score": 7.3,
            "tags": ["monitoring", "system", "desktop", "performance"]
        }
    ]
    
    # Combine all projects
    all_projects = (web_projects + mobile_projects + data_projects + 
                   devops_projects + game_projects + desktop_projects)
    
    # Add some additional generated projects for variety
    additional_projects = generate_additional_projects()
    
    return all_projects + additional_projects

def generate_additional_projects() -> List[Dict]:
    """Generate additional projects for more variety"""
    
    additional = []
    
    # More web development projects
    web_templates = [
        ("Blog Platform", "Create a full-featured blog with admin panel, comments, and SEO optimization", "intermediate", 5, ["React", "Node.js", "MongoDB", "SEO"]),
        ("Social Media Dashboard", "Build a dashboard for managing multiple social media accounts", "advanced", 8, ["React", "Express", "OAuth", "APIs"]),
        ("Learning Management System", "Develop an LMS with courses, quizzes, and progress tracking", "advanced", 9, ["Vue.js", "Django", "PostgreSQL", "Stripe"]),
        ("API Documentation Tool", "Create an interactive API documentation generator", "intermediate", 6, ["React", "OpenAPI", "Markdown", "Swagger"]),
        ("Code Snippet Manager", "Build a tool for organizing and sharing code snippets", "beginner", 4, ["JavaScript", "Local Storage", "Syntax Highlighting"]),
    ]
    
    for i, (title, desc, difficulty, complexity, techs) in enumerate(web_templates):
        additional.append({
            "project_id": f"web_add_{i+1:03d}",
            "title": title,
            "description": desc,
            "difficulty": difficulty,
            "estimated_time": f"{complexity-1}-{complexity+1} weeks",
            "technologies": techs,
            "categories": ["web-development", "application"],
            "learning_objectives": ["Full-stack development", "Database design", "User experience"],
            "prerequisites": ["JavaScript", "Web development basics"],
            "project_type": "application",
            "domain": "web-development",
            "complexity_score": complexity,
            "popularity_score": round(random.uniform(7.0, 9.0), 1),
            "tags": ["web", "application", "fullstack"]
        })
    
    # More data science projects
    data_templates = [
        ("Sentiment Analysis Tool", "Analyze social media sentiment using NLP and machine learning", "intermediate", 7, ["Python", "NLTK", "Scikit-learn", "Twitter API"]),
        ("Recommendation Engine", "Build a content recommendation system using collaborative filtering", "advanced", 8, ["Python", "Pandas", "Scikit-learn", "Flask"]),
        ("Data Visualization Dashboard", "Create interactive visualizations for business intelligence", "intermediate", 6, ["Python", "Plotly", "Streamlit", "SQL"]),
        ("Fraud Detection System", "Develop ML models to detect fraudulent transactions", "advanced", 9, ["Python", "Scikit-learn", "Pandas", "Imbalanced Learning"]),
    ]
    
    for i, (title, desc, difficulty, complexity, techs) in enumerate(data_templates):
        additional.append({
            "project_id": f"data_add_{i+1:03d}",
            "title": title,
            "description": desc,
            "difficulty": difficulty,
            "estimated_time": f"{complexity-1}-{complexity+1} weeks",
            "technologies": techs,
            "categories": ["data-science", "machine-learning"],
            "learning_objectives": ["Machine learning", "Data analysis", "Model evaluation"],
            "prerequisites": ["Python", "Pandas", "ML basics"],
            "project_type": "analysis",
            "domain": "data-science",
            "complexity_score": complexity,
            "popularity_score": round(random.uniform(7.5, 9.0), 1),
            "tags": ["ml", "analysis", "data", "python"]
        })
    
    return additional

def save_dataset():
    """Generate and save the complete dataset"""
    projects = generate_project_dataset()
    
    # Save as JSON
    with open('project_dataset.json', 'w', encoding='utf-8') as f:
        json.dump(projects, f, indent=2, ensure_ascii=False)
    
    print(f"Generated {len(projects)} project ideas")
    print("Dataset saved as 'project_dataset.json'")
    
    # Print some statistics
    domains = {}
    difficulties = {}
    for project in projects:
        domain = project['domain']
        difficulty = project['difficulty']
        
        domains[domain] = domains.get(domain, 0) + 1
        difficulties[difficulty] = difficulties.get(difficulty, 0) + 1
    
    print("\nDomain distribution:")
    for domain, count in domains.items():
        print(f"  {domain}: {count} projects")
    
    print("\nDifficulty distribution:")
    for difficulty, count in difficulties.items():
        print(f"  {difficulty}: {count} projects")

if __name__ == "__main__":
    save_dataset()

