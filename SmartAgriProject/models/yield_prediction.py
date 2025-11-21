"""
Yield Prediction Model
Multi-factor regression model for crop yield forecasting
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
from datetime import datetime, timedelta
import random

class YieldPredictionModel:
    def __init__(self):
        # Base yields for different crops (tons/hectare)
        self.base_yields = {
            'wheat': 4.5, 'rice': 3.8, 'corn': 5.2, 'barley': 3.5, 'millet': 2.8,
            'soybean': 2.5, 'chickpea': 1.8, 'lentil': 1.5, 'groundnut': 2.2,
            'potato': 25.0, 'tomato': 30.0, 'onion': 20.0, 'cabbage': 40.0,
            'cotton': 1.5, 'sugarcane': 80.0, 'mustard': 1.8, 'sunflower': 2.0
        }
        
        # Optimal conditions for maximum yield
        self.optimal_conditions = {
            'soil_quality': 8.0,
            'rainfall': 600,  # mm
            'temperature': 25,  # °C
            'humidity': 65,  # %
            'nitrogen': 120,  # kg/ha
            'phosphorus': 60,  # kg/ha
            'potassium': 80   # kg/ha
        }
        
        # Crop-specific requirements
        self.crop_requirements = {
            'wheat': {'temp_min': 15, 'temp_max': 25, 'rainfall_min': 300, 'rainfall_max': 800},
            'rice': {'temp_min': 20, 'temp_max': 35, 'rainfall_min': 1000, 'rainfall_max': 2000},
            'corn': {'temp_min': 18, 'temp_max': 30, 'rainfall_min': 500, 'rainfall_max': 1200},
            'cotton': {'temp_min': 20, 'temp_max': 35, 'rainfall_min': 500, 'rainfall_max': 1000},
            'potato': {'temp_min': 15, 'temp_max': 25, 'rainfall_min': 400, 'rainfall_max': 700}
        }
    
    def predict_yield(self, crop: str, soil_quality: float, rainfall: float, 
                     temperature: float, humidity: float, nitrogen: float = 100,
                     phosphorus: float = 50, potassium: float = 70,
                     area_hectares: float = 1.0) -> Dict:
        """
        Predict crop yield based on environmental and management factors
        
        Args:
            crop: Crop type
            soil_quality: Soil quality score (0-10)
            rainfall: Annual rainfall (mm)
            temperature: Average temperature (°C)
            humidity: Average humidity (%)
            nitrogen: Nitrogen fertilizer (kg/ha)
            phosphorus: Phosphorus fertilizer (kg/ha)
            potassium: Potassium fertilizer (kg/ha)
            area_hectares: Farm area in hectares
            
        Returns:
            Dict with yield prediction and analysis
        """
        
        if crop not in self.base_yields:
            return {'error': f'Crop {crop} not supported'}
        
        base_yield = self.base_yields[crop]
        
        # Calculate individual factor impacts
        soil_factor = self._calculate_soil_factor(soil_quality)
        weather_factor = self._calculate_weather_factor(crop, rainfall, temperature, humidity)
        fertilizer_factor = self._calculate_fertilizer_factor(nitrogen, phosphorus, potassium)
        
        # Calculate predicted yield per hectare
        yield_per_hectare = base_yield * soil_factor * weather_factor * fertilizer_factor
        
        # Add some realistic variability
        variability = random.uniform(0.9, 1.1)
        yield_per_hectare *= variability
        
        # Calculate total production
        total_production = yield_per_hectare * area_hectares
        
        # Risk assessment
        risk_factors = self._assess_risks(crop, rainfall, temperature, soil_quality)
        
        # Optimization suggestions
        optimization = self._get_optimization_suggestions(
            crop, soil_quality, rainfall, temperature, nitrogen, phosphorus, potassium
        )
        
        return {
            'crop': crop,
            'predicted_yield_per_hectare': round(yield_per_hectare, 2),
            'total_production': round(total_production, 2),
            'area_hectares': area_hectares,
            'factors': {
                'soil_factor': round(soil_factor, 3),
                'weather_factor': round(weather_factor, 3),
                'fertilizer_factor': round(fertilizer_factor, 3)
            },
            'conditions': {
                'soil_quality': soil_quality,
                'rainfall': rainfall,
                'temperature': temperature,
                'humidity': humidity,
                'nitrogen': nitrogen,
                'phosphorus': phosphorus,
                'potassium': potassium
            },
            'risk_assessment': risk_factors,
            'optimization_suggestions': optimization,
            'confidence_level': self._calculate_confidence(soil_factor, weather_factor, fertilizer_factor)
        }
    
    def _calculate_soil_factor(self, soil_quality: float) -> float:
        """Calculate soil quality impact on yield"""
        optimal_soil = self.optimal_conditions['soil_quality']
        
        if soil_quality >= optimal_soil:
            return 1.0
        elif soil_quality >= 6.0:
            return 0.8 + (soil_quality - 6.0) * 0.1
        elif soil_quality >= 4.0:
            return 0.6 + (soil_quality - 4.0) * 0.1
        else:
            return 0.4 + soil_quality * 0.05
    
    def _calculate_weather_factor(self, crop: str, rainfall: float, 
                                temperature: float, humidity: float) -> float:
        """Calculate weather impact on yield"""
        
        # Get crop-specific requirements
        requirements = self.crop_requirements.get(crop, {
            'temp_min': 15, 'temp_max': 30, 'rainfall_min': 400, 'rainfall_max': 1000
        })
        
        # Temperature factor
        if requirements['temp_min'] <= temperature <= requirements['temp_max']:
            temp_factor = 1.0
        else:
            temp_deviation = min(abs(temperature - requirements['temp_min']), 
                               abs(temperature - requirements['temp_max']))
            temp_factor = max(0.3, 1.0 - temp_deviation * 0.05)
        
        # Rainfall factor
        if requirements['rainfall_min'] <= rainfall <= requirements['rainfall_max']:
            rain_factor = 1.0
        elif rainfall < requirements['rainfall_min']:
            rain_factor = max(0.4, rainfall / requirements['rainfall_min'])
        else:
            excess = rainfall - requirements['rainfall_max']
            rain_factor = max(0.5, 1.0 - excess / requirements['rainfall_max'] * 0.3)
        
        # Humidity factor (optimal around 60-70%)
        if 60 <= humidity <= 70:
            humidity_factor = 1.0
        else:
            humidity_factor = max(0.7, 1.0 - abs(humidity - 65) * 0.01)
        
        return temp_factor * rain_factor * humidity_factor
    
    def _calculate_fertilizer_factor(self, nitrogen: float, phosphorus: float, 
                                   potassium: float) -> float:
        """Calculate fertilizer impact on yield"""
        
        # Nitrogen factor (most important)
        n_optimal = self.optimal_conditions['nitrogen']
        if nitrogen <= n_optimal:
            n_factor = 0.7 + (nitrogen / n_optimal) * 0.3
        else:
            # Diminishing returns and potential toxicity
            excess = nitrogen - n_optimal
            n_factor = max(0.8, 1.0 - excess / n_optimal * 0.2)
        
        # Phosphorus factor
        p_optimal = self.optimal_conditions['phosphorus']
        p_factor = min(1.0, 0.8 + (phosphorus / p_optimal) * 0.2)
        
        # Potassium factor
        k_optimal = self.optimal_conditions['potassium']
        k_factor = min(1.0, 0.9 + (potassium / k_optimal) * 0.1)
        
        return n_factor * 0.6 + p_factor * 0.25 + k_factor * 0.15
    
    def _assess_risks(self, crop: str, rainfall: float, temperature: float, 
                     soil_quality: float) -> Dict:
        """Assess production risks"""
        
        risks = []
        risk_level = "Low"
        
        requirements = self.crop_requirements.get(crop, {})
        
        # Weather risks
        if temperature < requirements.get('temp_min', 15) - 5:
            risks.append("Cold stress risk - consider frost protection")
            risk_level = "High"
        elif temperature > requirements.get('temp_max', 30) + 5:
            risks.append("Heat stress risk - ensure adequate irrigation")
            risk_level = "High"
        
        if rainfall < requirements.get('rainfall_min', 400) * 0.7:
            risks.append("Drought risk - plan supplemental irrigation")
            risk_level = "High" if risk_level != "High" else "High"
        elif rainfall > requirements.get('rainfall_max', 1000) * 1.3:
            risks.append("Waterlogging risk - ensure proper drainage")
            risk_level = "Medium" if risk_level == "Low" else risk_level
        
        # Soil risks
        if soil_quality < 5.0:
            risks.append("Poor soil quality - consider soil improvement")
            risk_level = "Medium" if risk_level == "Low" else risk_level
        
        if not risks:
            risks.append("Favorable conditions - low production risk")
        
        return {
            'risk_level': risk_level,
            'risk_factors': risks,
            'mitigation_strategies': self._get_mitigation_strategies(risks)
        }
    
    def _get_mitigation_strategies(self, risks: List[str]) -> List[str]:
        """Get risk mitigation strategies"""
        strategies = []
        
        for risk in risks:
            if "cold stress" in risk.lower():
                strategies.append("Use row covers, plant after last frost date")
            elif "heat stress" in risk.lower():
                strategies.append("Provide shade, increase irrigation frequency")
            elif "drought" in risk.lower():
                strategies.append("Install drip irrigation, use mulching")
            elif "waterlogging" in risk.lower():
                strategies.append("Improve drainage, use raised beds")
            elif "soil quality" in risk.lower():
                strategies.append("Add organic matter, balance nutrients")
        
        return strategies
    
    def _get_optimization_suggestions(self, crop: str, soil_quality: float, 
                                    rainfall: float, temperature: float,
                                    nitrogen: float, phosphorus: float, 
                                    potassium: float) -> List[str]:
        """Get yield optimization suggestions"""
        suggestions = []
        
        if soil_quality < 7.0:
            suggestions.append(f"Improve soil quality from {soil_quality:.1f} to 7+ for better yields")
        
        requirements = self.crop_requirements.get(crop, {})
        
        if nitrogen < 100:
            suggestions.append("Increase nitrogen fertilizer for better vegetative growth")
        elif nitrogen > 150:
            suggestions.append("Reduce nitrogen to prevent lodging and disease")
        
        if phosphorus < 40:
            suggestions.append("Add phosphorus fertilizer for root development")
        
        if potassium < 60:
            suggestions.append("Apply potassium for disease resistance and quality")
        
        if not suggestions:
            suggestions.append("Current management practices are optimal")
        
        return suggestions
    
    def _calculate_confidence(self, soil_factor: float, weather_factor: float, 
                            fertilizer_factor: float) -> str:
        """Calculate prediction confidence level"""
        
        avg_factor = (soil_factor + weather_factor + fertilizer_factor) / 3
        
        if avg_factor >= 0.9:
            return "High (90%+)"
        elif avg_factor >= 0.7:
            return "Medium (70-90%)"
        else:
            return "Low (<70%)"
    
    def compare_scenarios(self, crop: str, scenarios: List[Dict]) -> Dict:
        """Compare multiple management scenarios"""
        
        results = []
        
        for i, scenario in enumerate(scenarios):
            prediction = self.predict_yield(crop, **scenario)
            results.append({
                'scenario': i + 1,
                'yield': prediction['predicted_yield_per_hectare'],
                'conditions': scenario,
                'risk_level': prediction['risk_assessment']['risk_level']
            })
        
        # Find best scenario
        best_scenario = max(results, key=lambda x: x['yield'])
        
        return {
            'crop': crop,
            'scenarios': results,
            'best_scenario': best_scenario,
            'yield_range': {
                'min': min(r['yield'] for r in results),
                'max': max(r['yield'] for r in results),
                'average': sum(r['yield'] for r in results) / len(results)
            }
        }

# Example usage and testing
if __name__ == "__main__":
    model = YieldPredictionModel()
    
    # Test yield prediction
    result = model.predict_yield(
        crop='wheat',
        soil_quality=7.2,
        rainfall=550,
        temperature=22,
        humidity=65,
        nitrogen=110,
        phosphorus=55,
        potassium=75,
        area_hectares=2.5
    )
    
    print("Yield Prediction Results:")
    print(f"Crop: {result['crop'].title()}")
    print(f"Predicted Yield: {result['predicted_yield_per_hectare']} tons/hectare")
    print(f"Total Production: {result['total_production']} tons")
    print(f"Confidence: {result['confidence_level']}")
    
    print(f"\nFactor Analysis:")
    for factor, value in result['factors'].items():
        print(f"  {factor}: {value}")
    
    print(f"\nRisk Assessment: {result['risk_assessment']['risk_level']}")
    for risk in result['risk_assessment']['risk_factors']:
        print(f"  • {risk}")
    
    print(f"\nOptimization Suggestions:")
    for suggestion in result['optimization_suggestions']:
        print(f"  • {suggestion}")