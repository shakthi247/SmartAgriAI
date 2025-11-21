"""
Soil Quality Analysis Model
Multi-parameter weighted scoring system for soil health assessment
"""

import numpy as np
from typing import Dict, Tuple

class SoilQualityModel:
    def __init__(self):
        # Optimal values for soil parameters
        self.optimal_values = {
            'ph': 6.5,
            'nitrogen': 50,      # mg/kg
            'phosphorus': 40,    # mg/kg
            'potassium': 300,    # mg/kg
            'organic_matter': 5  # percentage
        }
        
        # Weights based on agricultural importance
        self.weights = {
            'ph': 0.20,
            'nitrogen': 0.25,
            'phosphorus': 0.25,
            'potassium': 0.20,
            'organic_matter': 0.10
        }
    
    def calculate_soil_quality_score(self, ph: float, nitrogen: float, 
                                   phosphorus: float, potassium: float, 
                                   organic_matter: float) -> Dict:
        """
        Calculate comprehensive soil quality score (0-10)
        
        Args:
            ph: Soil pH level (4.0-9.0)
            nitrogen: Nitrogen content in mg/kg
            phosphorus: Phosphorus content in mg/kg
            potassium: Potassium content in mg/kg
            organic_matter: Organic matter percentage
            
        Returns:
            Dict with overall score, individual scores, and recommendations
        """
        
        # Calculate individual parameter scores
        ph_score = max(0, 10 * (1 - abs(self.optimal_values['ph'] - ph) / 3.5))
        nitrogen_score = min(nitrogen / self.optimal_values['nitrogen'] * 10, 10)
        phosphorus_score = min(phosphorus / self.optimal_values['phosphorus'] * 10, 10)
        potassium_score = min(potassium / self.optimal_values['potassium'] * 10, 10)
        organic_matter_score = min(organic_matter / self.optimal_values['organic_matter'] * 10, 10)
        
        # Calculate weighted overall score
        overall_score = (
            ph_score * self.weights['ph'] +
            nitrogen_score * self.weights['nitrogen'] +
            phosphorus_score * self.weights['phosphorus'] +
            potassium_score * self.weights['potassium'] +
            organic_matter_score * self.weights['organic_matter']
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            ph, nitrogen, phosphorus, potassium, organic_matter
        )
        
        return {
            'overall_score': round(overall_score, 2),
            'individual_scores': {
                'ph': round(ph_score, 2),
                'nitrogen': round(nitrogen_score, 2),
                'phosphorus': round(phosphorus_score, 2),
                'potassium': round(potassium_score, 2),
                'organic_matter': round(organic_matter_score, 2)
            },
            'grade': self._get_grade(overall_score),
            'recommendations': recommendations
        }
    
    def _get_grade(self, score: float) -> str:
        """Convert numerical score to letter grade"""
        if score >= 8.5:
            return "Excellent"
        elif score >= 7.0:
            return "Good"
        elif score >= 5.5:
            return "Fair"
        elif score >= 4.0:
            return "Poor"
        else:
            return "Very Poor"
    
    def _generate_recommendations(self, ph: float, nitrogen: float, 
                                phosphorus: float, potassium: float, 
                                organic_matter: float) -> list:
        """Generate specific recommendations based on soil parameters"""
        recommendations = []
        
        # pH recommendations
        if ph < 6.0:
            recommendations.append("Add lime to increase soil pH (acidic soil)")
        elif ph > 7.5:
            recommendations.append("Add sulfur or organic matter to decrease pH (alkaline soil)")
        
        # Nutrient recommendations
        if nitrogen < 30:
            recommendations.append("Apply nitrogen-rich fertilizer (urea, ammonium sulfate)")
        elif nitrogen > 80:
            recommendations.append("Reduce nitrogen fertilizer to prevent nutrient burn")
            
        if phosphorus < 25:
            recommendations.append("Add phosphorus fertilizer (DAP, SSP)")
        
        if potassium < 200:
            recommendations.append("Apply potassium fertilizer (muriate of potash)")
        
        if organic_matter < 3:
            recommendations.append("Increase organic matter with compost, manure, or cover crops")
        
        if not recommendations:
            recommendations.append("Soil quality is optimal - maintain current practices")
            
        return recommendations

    def get_suitable_crops(self, soil_score: float) -> list:
        """Recommend crops based on soil quality score"""
        if soil_score >= 8.0:
            return ["Rice", "Wheat", "Corn", "Tomato", "Cotton", "Sugarcane"]
        elif soil_score >= 6.5:
            return ["Wheat", "Corn", "Soybean", "Potato", "Onion", "Cabbage"]
        elif soil_score >= 5.0:
            return ["Millet", "Sorghum", "Groundnut", "Sunflower", "Mustard"]
        elif soil_score >= 3.5:
            return ["Barley", "Oats", "Castor", "Safflower"]
        else:
            return ["Hardy crops only - improve soil first"]

# Example usage and testing
if __name__ == "__main__":
    model = SoilQualityModel()
    
    # Test with sample data
    result = model.calculate_soil_quality_score(
        ph=6.8,
        nitrogen=45,
        phosphorus=35,
        potassium=280,
        organic_matter=4.2
    )
    
    print("Soil Quality Analysis Results:")
    print(f"Overall Score: {result['overall_score']}/10 ({result['grade']})")
    print("\nIndividual Scores:")
    for param, score in result['individual_scores'].items():
        print(f"  {param.title()}: {score}/10")
    
    print("\nRecommendations:")
    for rec in result['recommendations']:
        print(f"  • {rec}")
    
    print(f"\nSuitable Crops: {', '.join(model.get_suitable_crops(result['overall_score']))}")