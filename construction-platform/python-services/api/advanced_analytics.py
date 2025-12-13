"""
Advanced analytics and machine learning features for Construction AI Agent
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, IsolationForest
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib
from typing import Dict, List, Tuple, Optional
import logging
from datetime import datetime, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots

logger = logging.getLogger(__name__)

class ConstructionAnalytics:
    """Advanced analytics for construction projects"""
    
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.load_models()
    
    def load_models(self):
        """Load pre-trained models"""
        try:
            # Load cost prediction model
            self.models['cost_predictor'] = joblib.load('models/cost_predictor.pkl')
            self.scalers['cost_scaler'] = joblib.load('models/cost_scaler.pkl')
        except FileNotFoundError:
            logger.warning("Pre-trained models not found. Will train new models.")
    
    def predict_project_cost(self, project_features: Dict) -> Dict:
        """Predict project cost using ML model"""
        try:
            # Prepare features
            features = self._prepare_cost_features(project_features)
            
            if 'cost_predictor' in self.models:
                # Use pre-trained model
                prediction = self.models['cost_predictor'].predict([features])[0]
                confidence = self._calculate_confidence(features)
            else:
                # Fallback to rule-based prediction
                prediction = self._rule_based_cost_prediction(project_features)
                confidence = 0.7
            
            return {
                "predicted_cost": float(prediction),
                "confidence": confidence,
                "features_used": list(project_features.keys()),
                "model_type": "ML" if 'cost_predictor' in self.models else "Rule-based"
            }
        except Exception as e:
            logger.error(f"Cost prediction failed: {e}")
            return {"error": str(e)}
    
    def detect_anomalies(self, project_data: List[Dict]) -> Dict:
        """Detect anomalous projects using isolation forest"""
        try:
            df = pd.DataFrame(project_data)
            
            # Prepare features for anomaly detection
            features = self._prepare_anomaly_features(df)
            
            # Train isolation forest
            iso_forest = IsolationForest(contamination=0.1, random_state=42)
            anomaly_scores = iso_forest.fit_predict(features)
            
            # Identify anomalies
            anomalies = df[anomaly_scores == -1].to_dict('records')
            
            return {
                "total_projects": len(project_data),
                "anomalies_detected": len(anomalies),
                "anomaly_rate": len(anomalies) / len(project_data),
                "anomalous_projects": anomalies
            }
        except Exception as e:
            logger.error(f"Anomaly detection failed: {e}")
            return {"error": str(e)}
    
    def cluster_projects(self, project_data: List[Dict], n_clusters: int = 3) -> Dict:
        """Cluster similar projects using K-means"""
        try:
            df = pd.DataFrame(project_data)
            
            # Prepare features for clustering
            features = self._prepare_clustering_features(df)
            
            # Perform clustering
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            cluster_labels = kmeans.fit_predict(features)
            
            # Add cluster labels to data
            df['cluster'] = cluster_labels
            
            # Analyze clusters
            cluster_analysis = {}
            for i in range(n_clusters):
                cluster_data = df[df['cluster'] == i]
                cluster_analysis[f"cluster_{i}"] = {
                    "size": len(cluster_data),
                    "avg_cost": cluster_data['total_cost'].mean() if 'total_cost' in cluster_data.columns else 0,
                    "common_materials": cluster_data['primary_material'].mode().tolist() if 'primary_material' in cluster_data.columns else [],
                    "avg_duration": cluster_data['duration_days'].mean() if 'duration_days' in cluster_data.columns else 0
                }
            
            return {
                "n_clusters": n_clusters,
                "cluster_analysis": cluster_analysis,
                "projects_with_clusters": df.to_dict('records')
            }
        except Exception as e:
            logger.error(f"Project clustering failed: {e}")
            return {"error": str(e)}
    
    def predict_material_demand(self, historical_data: List[Dict], forecast_days: int = 30) -> Dict:
        """Predict material demand using time series analysis"""
        try:
            df = pd.DataFrame(historical_data)
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
            
            predictions = {}
            
            for material in df['material'].unique():
                material_data = df[df['material'] == material].copy()
                material_data = material_data.set_index('date')
                
                # Simple moving average prediction
                window = min(7, len(material_data))
                if window > 0:
                    last_avg = material_data['quantity'].rolling(window=window).mean().iloc[-1]
                    predictions[material] = {
                        "predicted_demand": float(last_avg),
                        "confidence": 0.8,
                        "forecast_period": f"{forecast_days} days"
                    }
            
            return {
                "forecast_date": (datetime.now() + timedelta(days=forecast_days)).isoformat(),
                "predictions": predictions
            }
        except Exception as e:
            logger.error(f"Material demand prediction failed: {e}")
            return {"error": str(e)}
    
    def optimize_supplier_selection(self, materials: List[Dict], suppliers: List[Dict]) -> Dict:
        """Optimize supplier selection using cost and quality metrics"""
        try:
            optimization_results = {}
            
            for material in materials:
                material_name = material['name']
                required_quantity = material['quantity']
                
                # Find suppliers for this material
                material_suppliers = [s for s in suppliers if material_name in s['materials']]
                
                if not material_suppliers:
                    continue
                
                # Calculate optimization score for each supplier
                supplier_scores = []
                for supplier in material_suppliers:
                    score = self._calculate_supplier_score(supplier, material)
                    supplier_scores.append({
                        "supplier": supplier['name'],
                        "score": score,
                        "total_cost": supplier['price'] * required_quantity,
                        "delivery_time": supplier.get('delivery_days', 7),
                        "quality_rating": supplier.get('quality_rating', 3.0)
                    })
                
                # Sort by score (higher is better)
                supplier_scores.sort(key=lambda x: x['score'], reverse=True)
                
                optimization_results[material_name] = {
                    "recommended_supplier": supplier_scores[0],
                    "alternatives": supplier_scores[1:3],  # Top 3 alternatives
                    "savings_potential": self._calculate_savings_potential(supplier_scores)
                }
            
            return {
                "optimization_results": optimization_results,
                "total_savings": sum(r["savings_potential"] for r in optimization_results.values())
            }
        except Exception as e:
            logger.error(f"Supplier optimization failed: {e}")
            return {"error": str(e)}
    
    def _prepare_cost_features(self, project_features: Dict) -> List[float]:
        """Prepare features for cost prediction"""
        # Convert project features to numerical array
        features = []
        
        # Project size (area in m²)
        features.append(project_features.get('area', 100))
        
        # Number of floors
        features.append(project_features.get('floors', 1))
        
        # Construction type (encoded)
        construction_types = {'residential': 1, 'commercial': 2, 'industrial': 3}
        features.append(construction_types.get(project_features.get('type', 'residential'), 1))
        
        # Location factor (Estonian regions)
        location_factors = {'Tartu': 1.0, 'Tallinn': 1.1, 'Pärnu': 1.05, 'Narva': 0.95}
        features.append(location_factors.get(project_features.get('location', 'Tartu'), 1.0))
        
        # Complexity factor
        features.append(project_features.get('complexity', 1.0))
        
        return features
    
    def _prepare_anomaly_features(self, df: pd.DataFrame) -> np.ndarray:
        """Prepare features for anomaly detection"""
        features = []
        
        # Cost per square meter
        if 'total_cost' in df.columns and 'area' in df.columns:
            features.append((df['total_cost'] / df['area']).fillna(0))
        
        # Duration per square meter
        if 'duration_days' in df.columns and 'area' in df.columns:
            features.append((df['duration_days'] / df['area']).fillna(0))
        
        # Material cost ratio
        if 'material_cost' in df.columns and 'total_cost' in df.columns:
            features.append((df['material_cost'] / df['total_cost']).fillna(0))
        
        return np.column_stack(features) if features else np.array([[0]])
    
    def _prepare_clustering_features(self, df: pd.DataFrame) -> np.ndarray:
        """Prepare features for project clustering"""
        features = []
        
        # Numerical features
        numerical_cols = ['total_cost', 'area', 'duration_days', 'floors']
        for col in numerical_cols:
            if col in df.columns:
                features.append(df[col].fillna(0))
        
        return np.column_stack(features) if features else np.array([[0]])
    
    def _calculate_confidence(self, features: List[float]) -> float:
        """Calculate prediction confidence"""
        # Simple confidence calculation based on feature completeness
        non_zero_features = sum(1 for f in features if f > 0)
        return min(0.95, non_zero_features / len(features) + 0.5)
    
    def _rule_based_cost_prediction(self, project_features: Dict) -> float:
        """Fallback rule-based cost prediction"""
        base_cost_per_m2 = 800  # EUR per m²
        area = project_features.get('area', 100)
        
        # Apply multipliers
        multipliers = {
            'floors': 1 + (project_features.get('floors', 1) - 1) * 0.1,
            'complexity': project_features.get('complexity', 1.0),
            'location': {'Tartu': 1.0, 'Tallinn': 1.1, 'Pärnu': 1.05}.get(project_features.get('location', 'Tartu'), 1.0)
        }
        
        total_multiplier = 1.0
        for mult in multipliers.values():
            total_multiplier *= mult
        
        return base_cost_per_m2 * area * total_multiplier
    
    def _calculate_supplier_score(self, supplier: Dict, material: Dict) -> float:
        """Calculate supplier optimization score"""
        # Weighted score based on price, quality, and delivery time
        price_score = 1.0 / (supplier['price'] + 0.01)  # Lower price = higher score
        quality_score = supplier.get('quality_rating', 3.0) / 5.0
        delivery_score = 1.0 / (supplier.get('delivery_days', 7) + 1)
        
        # Weighted combination
        weights = {'price': 0.5, 'quality': 0.3, 'delivery': 0.2}
        score = (weights['price'] * price_score + 
                weights['quality'] * quality_score + 
                weights['delivery'] * delivery_score)
        
        return score
    
    def _calculate_savings_potential(self, supplier_scores: List[Dict]) -> float:
        """Calculate potential savings from optimization"""
        if len(supplier_scores) < 2:
            return 0.0
        
        best_cost = supplier_scores[0]['total_cost']
        worst_cost = supplier_scores[-1]['total_cost']
        
        return max(0, worst_cost - best_cost)

class EstonianMarketAnalytics:
    """Estonian construction market analytics"""
    
    def __init__(self):
        self.market_data = self._load_market_data()
    
    def _load_market_data(self) -> Dict:
        """Load Estonian construction market data"""
        return {
            "regional_prices": {
                "Tartu": {"concrete": 45, "steel": 0.85, "labor": 25},
                "Tallinn": {"concrete": 50, "steel": 0.90, "labor": 30},
                "Pärnu": {"concrete": 47, "steel": 0.87, "labor": 27},
                "Narva": {"concrete": 43, "steel": 0.82, "labor": 23}
            },
            "seasonal_factors": {
                "spring": 1.05,
                "summer": 1.10,
                "autumn": 1.0,
                "winter": 0.95
            },
            "market_trends": {
                "material_inflation": 0.03,  # 3% annual
                "labor_inflation": 0.05,     # 5% annual
                "demand_growth": 0.02        # 2% annual
            }
        }
    
    def analyze_market_conditions(self, region: str = "Tartu") -> Dict:
        """Analyze current market conditions"""
        current_season = self._get_current_season()
        
        return {
            "region": region,
            "season": current_season,
            "seasonal_factor": self.market_data["seasonal_factors"][current_season],
            "material_prices": self.market_data["regional_prices"].get(region, {}),
            "market_trends": self.market_data["market_trends"],
            "recommendations": self._generate_market_recommendations(region, current_season)
        }
    
    def _get_current_season(self) -> str:
        """Get current season"""
        month = datetime.now().month
        if month in [3, 4, 5]:
            return "spring"
        elif month in [6, 7, 8]:
            return "summer"
        elif month in [9, 10, 11]:
            return "autumn"
        else:
            return "winter"
    
    def _generate_market_recommendations(self, region: str, season: str) -> List[str]:
        """Generate market-based recommendations"""
        recommendations = []
        
        if season == "winter":
            recommendations.append("Consider indoor construction activities during winter months")
            recommendations.append("Plan material deliveries for spring construction start")
        
        if region == "Tallinn":
            recommendations.append("Higher costs expected in Tallinn - consider bulk purchasing")
        
        recommendations.append("Monitor material price trends for optimal purchasing timing")
        
        return recommendations

