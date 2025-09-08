"""
ML Models for Project Recommendation System
Implements content-based filtering and collaborative filtering algorithms
"""

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
from typing import List, Dict, Tuple
import json
import pickle
import os

class ProjectRecommendationEngine:
    """Main recommendation engine combining multiple ML approaches"""
    
    def __init__(self, dataset_path: str = "project_dataset.json"):
        self.dataset_path = dataset_path
        self.projects_df = None
        self.tfidf_vectorizer = None
        self.tfidf_matrix = None
        self.scaler = StandardScaler()
        self.user_interactions = {}  # Store user feedback for collaborative filtering
        
        self.load_dataset()
        self.initialize_models()
    
    def load_dataset(self):
        """Load and preprocess the project dataset"""
        try:
            with open(self.dataset_path, 'r', encoding='utf-8') as f:
                projects = json.load(f)
            
            self.projects_df = pd.DataFrame(projects)
            
            # Create combined text features for TF-IDF
            self.projects_df['combined_text'] = (
                self.projects_df['title'] + ' ' +
                self.projects_df['description'] + ' ' +
                self.projects_df['categories'].apply(lambda x: ' '.join(x)) + ' ' +
                self.projects_df['technologies'].apply(lambda x: ' '.join(x)) + ' ' +
                self.projects_df['learning_objectives'].apply(lambda x: ' '.join(x))
            )
            
            print(f"Loaded {len(self.projects_df)} projects")
            
        except FileNotFoundError:
            print(f"Dataset file {self.dataset_path} not found. Please run dataset_generator.py first.")
            raise
    
    def initialize_models(self):
        """Initialize TF-IDF vectorizer and other models"""
        # Initialize TF-IDF vectorizer
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=2
        )
        
        # Fit TF-IDF on combined text
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(
            self.projects_df['combined_text']
        )
        
        print("TF-IDF model initialized")
    
    def content_based_recommendations(self, 
                                    user_goal: str, 
                                    user_domain: str = None,
                                    difficulty_preference: str = None,
                                    limit: int = 10) -> List[Dict]:
        """Generate content-based recommendations using TF-IDF and cosine similarity"""
        
        # Create user profile text
        user_text = user_goal.lower()
        if user_domain:
            user_text += f" {user_domain.lower()}"
        
        # Vectorize user input
        user_vector = self.tfidf_vectorizer.transform([user_text])
        
        # Calculate cosine similarity
        similarities = cosine_similarity(user_vector, self.tfidf_matrix).flatten()
        
        # Get top similar projects
        similar_indices = np.argsort(similarities)[::-1]
        
        # Filter by domain if specified
        if user_domain:
            domain_mask = self.projects_df['domain'].str.contains(
                user_domain, case=False, na=False
            )
            similar_indices = similar_indices[domain_mask[similar_indices]]
        
        # Filter by difficulty if specified
        if difficulty_preference:
            difficulty_mask = self.projects_df['difficulty'] == difficulty_preference
            similar_indices = similar_indices[difficulty_mask[similar_indices]]
        
        # Filter out low-quality matches (similarity < 0.1)
        quality_mask = similarities[similar_indices] >= 0.1
        similar_indices = similar_indices[quality_mask]
        
        # Get top recommendations
        top_indices = similar_indices[:limit]
        recommendations = []
        
        for idx in top_indices:
            project = self.projects_df.iloc[idx].to_dict()
            project['similarity_score'] = float(similarities[idx])
            recommendations.append(project)
        
        return recommendations
    
    def collaborative_filtering_recommendations(self, 
                                             user_id: str, 
                                             limit: int = 10) -> List[Dict]:
        """Generate collaborative filtering recommendations based on user interactions"""
        
        if user_id not in self.user_interactions:
            return []
        
        user_interactions = self.user_interactions[user_id]
        
        # Simple collaborative filtering: find users with similar preferences
        similar_users = self.find_similar_users(user_id)
        
        # Get projects liked by similar users
        recommended_projects = []
        for similar_user, similarity in similar_users:
            user_projects = self.user_interactions[similar_user]
            for project_id, rating in user_projects.items():
                if project_id not in user_interactions and rating >= 4:  # Only high-rated projects
                    recommended_projects.append((project_id, rating * similarity))
        
        # Sort by weighted rating
        recommended_projects.sort(key=lambda x: x[1], reverse=True)
        
        # Get project details
        recommendations = []
        for project_id, score in recommended_projects[:limit]:
            project = self.projects_df[self.projects_df['project_id'] == project_id]
            if not project.empty:
                project_dict = project.iloc[0].to_dict()
                project_dict['collaborative_score'] = score
                recommendations.append(project_dict)
        
        return recommendations
    
    def find_similar_users(self, user_id: str, top_k: int = 5) -> List[Tuple[str, float]]:
        """Find users with similar preferences using cosine similarity"""
        
        if user_id not in self.user_interactions:
            return []
        
        user_vector = self.user_interactions[user_id]
        similarities = []
        
        for other_user, other_interactions in self.user_interactions.items():
            if other_user == user_id:
                continue
            
            # Calculate Jaccard similarity for user interactions
            user_projects = set(user_vector.keys())
            other_projects = set(other_interactions.keys())
            
            if not user_projects or not other_projects:
                continue
            
            intersection = len(user_projects.intersection(other_projects))
            union = len(user_projects.union(other_projects))
            
            if union > 0:
                similarity = intersection / union
                similarities.append((other_user, similarity))
        
        # Sort by similarity and return top k
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]
    
    def hybrid_recommendations(self, 
                             user_goal: str,
                             user_id: str = None,
                             user_domain: str = None,
                             difficulty_preference: str = None,
                             content_weight: float = 0.7,
                             collaborative_weight: float = 0.3,
                             limit: int = 10) -> List[Dict]:
        """Generate hybrid recommendations combining content-based and collaborative filtering"""
        
        # Get content-based recommendations
        content_recs = self.content_based_recommendations(
            user_goal, user_domain, difficulty_preference, limit * 2
        )
        
        # Get collaborative recommendations if user exists
        collab_recs = []
        if user_id:
            collab_recs = self.collaborative_filtering_recommendations(user_id, limit)
        
        # Combine recommendations
        combined_scores = {}
        
        # Add content-based scores
        for rec in content_recs:
            project_id = rec['project_id']
            combined_scores[project_id] = {
                'project': rec,
                'content_score': rec['similarity_score'] * content_weight,
                'collaborative_score': 0
            }
        
        # Add collaborative scores
        for rec in collab_recs:
            project_id = rec['project_id']
            if project_id in combined_scores:
                combined_scores[project_id]['collaborative_score'] = rec['collaborative_score'] * collaborative_weight
            else:
                combined_scores[project_id] = {
                    'project': rec,
                    'content_score': 0,
                    'collaborative_score': rec['collaborative_score'] * collaborative_weight
                }
        
        # Calculate final scores
        final_recommendations = []
        for project_id, scores in combined_scores.items():
            final_score = scores['content_score'] + scores['collaborative_score']
            project = scores['project'].copy()
            project['final_score'] = final_score
            project['content_score'] = scores['content_score']
            project['collaborative_score'] = scores['collaborative_score']
            final_recommendations.append(project)
        
        # Sort by final score and return top recommendations
        final_recommendations.sort(key=lambda x: x['final_score'], reverse=True)
        return final_recommendations[:limit]
    
    def add_user_feedback(self, user_id: str, project_id: str, rating: int, feedback: str = None):
        """Add user feedback for collaborative filtering"""
        
        if user_id not in self.user_interactions:
            self.user_interactions[user_id] = {}
        
        self.user_interactions[user_id][project_id] = rating
        
        # Save feedback to file for persistence
        self.save_user_interactions()
    
    def save_user_interactions(self):
        """Save user interactions to file"""
        with open('user_interactions.json', 'w') as f:
            json.dump(self.user_interactions, f)
    
    def load_user_interactions(self):
        """Load user interactions from file"""
        try:
            with open('user_interactions.json', 'r') as f:
                self.user_interactions = json.load(f)
        except FileNotFoundError:
            self.user_interactions = {}
    
    def get_trending_projects(self, domain: str = None, limit: int = 10) -> List[Dict]:
        """Get trending projects based on popularity scores"""
        
        df = self.projects_df.copy()
        
        if domain:
            df = df[df['domain'].str.contains(domain, case=False, na=False)]
        
        # Sort by popularity score
        trending = df.nlargest(limit, 'popularity_score')
        
        return trending.to_dict('records')
    
    def get_projects_by_difficulty(self, difficulty: str, limit: int = 10) -> List[Dict]:
        """Get projects filtered by difficulty level"""
        
        filtered = self.projects_df[self.projects_df['difficulty'] == difficulty]
        return filtered.head(limit).to_dict('records')
    
    def get_projects_by_technology(self, technology: str, limit: int = 10) -> List[Dict]:
        """Get projects that use a specific technology"""
        
        tech_mask = self.projects_df['technologies'].apply(
            lambda x: any(tech.lower() == technology.lower() for tech in x)
        )
        
        filtered = self.projects_df[tech_mask]
        return filtered.head(limit).to_dict('records')
    
    def get_domain_statistics(self) -> Dict:
        """Get statistics about project distribution across domains"""
        
        stats = {}
        
        # Domain distribution
        stats['domains'] = self.projects_df['domain'].value_counts().to_dict()
        
        # Difficulty distribution
        stats['difficulties'] = self.projects_df['difficulty'].value_counts().to_dict()
        
        # Technology distribution
        all_technologies = []
        for techs in self.projects_df['technologies']:
            all_technologies.extend(techs)
        
        tech_counts = pd.Series(all_technologies).value_counts()
        stats['technologies'] = tech_counts.head(20).to_dict()
        
        # Average complexity by domain
        complexity_by_domain = self.projects_df.groupby('domain')['complexity_score'].mean()
        stats['avg_complexity_by_domain'] = complexity_by_domain.to_dict()
        
        return stats

# Initialize the recommendation engine
recommendation_engine = ProjectRecommendationEngine()
