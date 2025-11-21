"""
Smart Irrigation Model
Intelligent irrigation scheduling and water management system
"""

import numpy as np
from typing import Dict, List, Tuple
from datetime import datetime, timedelta
import random

class IrrigationModel:
    def __init__(self):
        # Crop water requirements (mm/day during peak growth)
        self.crop_water_requirements = {
            'wheat': 4.5, 'rice': 8.0, 'corn': 6.0, 'barley': 4.0, 'millet': 3.5,
            'soybean': 5.5, 'chickpea': 3.0, 'lentil': 2.5, 'groundnut': 4.5,
            'potato': 5.0, 'tomato': 6.5, 'onion': 4.0, 'cabbage': 5.5,
            'cotton': 7.0, 'sugarcane': 8.5, 'mustard': 3.5, 'sunflower': 5.0
        }
        
        # Growth stage water multipliers
        self.growth_stage_multipliers = {
            'germination': 0.3,
            'vegetative': 0.7,
            'flowering': 1.2,
            'grain_filling': 1.0,
            'maturity': 0.4
        }
        
        # Soil water holding capacity (mm/cm depth)
        self.soil_water_capacity = {
            'sandy': 1.0,
            'loamy': 1.5,
            'clay': 2.0,
            'organic': 2.5
        }
        
        # Critical moisture thresholds (% of field capacity)
        self.moisture_thresholds = {
            'critical': 30,    # Immediate irrigation needed
            'stress': 50,      # Irrigation recommended
            'optimal': 70,     # No irrigation needed
            'excess': 90       # Risk of waterlogging
        }
        
        # Irrigation efficiency by method
        self.irrigation_efficiency = {
            'flood': 0.45,
            'furrow': 0.60,
            'sprinkler': 0.75,
            'drip': 0.90,
            'micro_sprinkler': 0.85
        }
    
    def assess_irrigation_need(self, crop: str, soil_moisture: float, 
                             temperature: float, humidity: float, 
                             wind_speed: float = 5.0, growth_stage: str = 'vegetative',
                             soil_type: str = 'loamy', days_since_rain: int = 3) -> Dict:
        """
        Assess irrigation requirements based on multiple factors
        
        Args:
            crop: Crop type
            soil_moisture: Current soil moisture (%)
            temperature: Air temperature (°C)
            humidity: Relative humidity (%)
            wind_speed: Wind speed (km/h)
            growth_stage: Current growth stage
            soil_type: Soil type
            days_since_rain: Days since last rainfall
            
        Returns:
            Dict with irrigation assessment and recommendations
        """
        
        # Calculate evapotranspiration (ET)
        et_rate = self._calculate_evapotranspiration(
            crop, temperature, humidity, wind_speed, growth_stage
        )
        
        # Assess soil moisture status
        moisture_status = self._assess_moisture_status(soil_moisture, soil_type)
        
        # Calculate water deficit
        water_deficit = self._calculate_water_deficit(
            crop, soil_moisture, et_rate, days_since_rain, soil_type
        )
        
        # Generate irrigation recommendation
        recommendation = self._generate_irrigation_recommendation(
            moisture_status, water_deficit, et_rate, crop
        )
        
        # Calculate irrigation schedule
        schedule = self._calculate_irrigation_schedule(
            crop, water_deficit, soil_type, growth_stage
        )
        
        return {
            'crop': crop,
            'current_conditions': {
                'soil_moisture': soil_moisture,
                'temperature': temperature,
                'humidity': humidity,
                'wind_speed': wind_speed,
                'growth_stage': growth_stage
            },
            'assessment': {
                'moisture_status': moisture_status,
                'et_rate': round(et_rate, 2),
                'water_deficit': round(water_deficit, 2),
                'irrigation_priority': recommendation['priority']
            },
            'recommendation': recommendation,
            'irrigation_schedule': schedule,
            'efficiency_tips': self._get_efficiency_tips(crop, soil_type, temperature)
        }
    
    def _calculate_evapotranspiration(self, crop: str, temperature: float, 
                                    humidity: float, wind_speed: float, 
                                    growth_stage: str) -> float:
        """Calculate crop evapotranspiration rate (mm/day)"""
        
        # Base crop water requirement
        base_et = self.crop_water_requirements.get(crop, 5.0)
        
        # Growth stage adjustment
        stage_multiplier = self.growth_stage_multipliers.get(growth_stage, 1.0)
        
        # Temperature effect (optimal around 25°C)
        temp_factor = 1.0 + (temperature - 25) * 0.02
        temp_factor = max(0.5, min(1.5, temp_factor))
        
        # Humidity effect (higher humidity reduces ET)
        humidity_factor = 1.0 - (humidity - 50) * 0.005
        humidity_factor = max(0.7, min(1.3, humidity_factor))
        
        # Wind effect (higher wind increases ET)
        wind_factor = 1.0 + (wind_speed - 5) * 0.01
        wind_factor = max(0.8, min(1.4, wind_factor))
        
        et_rate = base_et * stage_multiplier * temp_factor * humidity_factor * wind_factor
        
        return max(1.0, et_rate)  # Minimum 1mm/day
    
    def _assess_moisture_status(self, soil_moisture: float, soil_type: str) -> Dict:
        """Assess current soil moisture status"""
        
        if soil_moisture <= self.moisture_thresholds['critical']:
            status = "Critical"
            description = "Immediate irrigation required - crops under severe stress"
            urgency = "High"
        elif soil_moisture <= self.moisture_thresholds['stress']:
            status = "Stress"
            description = "Irrigation recommended - crops beginning to show stress"
            urgency = "Medium"
        elif soil_moisture <= self.moisture_thresholds['optimal']:
            status = "Adequate"
            description = "Soil moisture adequate - monitor conditions"
            urgency = "Low"
        elif soil_moisture <= self.moisture_thresholds['excess']:
            status = "Optimal"
            description = "Excellent soil moisture - no irrigation needed"
            urgency = "None"
        else:
            status = "Excess"
            description = "Risk of waterlogging - ensure proper drainage"
            urgency = "Drainage"
        
        return {
            'status': status,
            'description': description,
            'urgency': urgency,
            'moisture_level': soil_moisture
        }
    
    def _calculate_water_deficit(self, crop: str, soil_moisture: float, 
                               et_rate: float, days_since_rain: int, 
                               soil_type: str) -> float:
        """Calculate water deficit in mm"""
        
        # Target moisture level for crop
        target_moisture = self.moisture_thresholds['optimal']
        
        # Current deficit based on moisture
        moisture_deficit = max(0, target_moisture - soil_moisture)
        
        # Water lost due to ET since last rain
        et_loss = et_rate * days_since_rain
        
        # Soil water holding capacity factor
        soil_capacity = self.soil_water_capacity.get(soil_type, 1.5)
        
        # Total water deficit
        total_deficit = (moisture_deficit / 100) * soil_capacity * 300 + et_loss  # 300mm root zone
        
        return max(0, total_deficit)
    
    def _generate_irrigation_recommendation(self, moisture_status: Dict, 
                                          water_deficit: float, et_rate: float, 
                                          crop: str) -> Dict:
        """Generate specific irrigation recommendations"""
        
        urgency = moisture_status['urgency']
        
        if urgency == "High":
            priority = "Immediate"
            action = "Start irrigation within 2-4 hours"
            duration = max(2, water_deficit / 10)  # Hours
            frequency = "Daily until moisture improves"
        elif urgency == "Medium":
            priority = "Soon"
            action = "Irrigate within 12-24 hours"
            duration = max(1, water_deficit / 15)
            frequency = "Every 2-3 days"
        elif urgency == "Low":
            priority = "Monitor"
            action = "Continue monitoring, irrigate if conditions worsen"
            duration = 0
            frequency = "As needed"
        elif urgency == "Drainage":
            priority = "Drainage"
            action = "Improve drainage, avoid irrigation"
            duration = 0
            frequency = "None - focus on drainage"
        else:
            priority = "None"
            action = "No irrigation needed"
            duration = 0
            frequency = "Monitor daily"
        
        # Calculate water amount needed
        water_amount = water_deficit if water_deficit > 0 else 0
        
        return {
            'priority': priority,
            'action': action,
            'duration_hours': round(duration, 1),
            'frequency': frequency,
            'water_amount_mm': round(water_amount, 1),
            'best_time': self._get_best_irrigation_time(),
            'method_recommendation': self._recommend_irrigation_method(crop, water_deficit)
        }
    
    def _calculate_irrigation_schedule(self, crop: str, water_deficit: float, 
                                     soil_type: str, growth_stage: str) -> List[Dict]:
        """Calculate detailed irrigation schedule"""
        
        schedule = []
        
        if water_deficit <= 0:
            return [{'day': 1, 'action': 'Monitor soil moisture', 'amount_mm': 0}]
        
        # Base irrigation frequency by crop and growth stage
        base_frequency = {
            'rice': 1, 'sugarcane': 2, 'cotton': 3, 'wheat': 4, 'corn': 3,
            'tomato': 2, 'potato': 3, 'onion': 3
        }
        
        frequency_days = base_frequency.get(crop, 3)
        
        # Adjust for growth stage
        if growth_stage in ['flowering', 'grain_filling']:
            frequency_days = max(1, frequency_days - 1)
        elif growth_stage == 'maturity':
            frequency_days += 2
        
        # Calculate irrigation amounts
        total_days = 14  # 2-week schedule
        irrigation_days = list(range(1, total_days + 1, frequency_days))
        
        daily_requirement = self.crop_water_requirements.get(crop, 5.0)
        irrigation_amount = daily_requirement * frequency_days
        
        for day in range(1, total_days + 1):
            if day in irrigation_days:
                schedule.append({
                    'day': day,
                    'action': f'Irrigate - {irrigation_amount:.1f}mm',
                    'amount_mm': irrigation_amount,
                    'duration_hours': irrigation_amount / 5,  # Assuming 5mm/hour application rate
                    'best_time': '6:00 AM - 8:00 AM'
                })
            else:
                schedule.append({
                    'day': day,
                    'action': 'Monitor',
                    'amount_mm': 0,
                    'duration_hours': 0,
                    'best_time': 'Check soil moisture'
                })
        
        return schedule
    
    def _get_best_irrigation_time(self) -> str:
        """Recommend best time for irrigation"""
        
        times = [
            "Early morning (5:00-7:00 AM) - minimal evaporation",
            "Late evening (6:00-8:00 PM) - reduced wind and temperature",
            "Avoid midday (11:00 AM-3:00 PM) - high evaporation losses"
        ]
        
        return times[0]  # Default to early morning
    
    def _recommend_irrigation_method(self, crop: str, water_deficit: float) -> Dict:
        """Recommend best irrigation method"""
        
        # Method recommendations by crop type
        crop_methods = {
            'rice': 'flood',
            'sugarcane': 'furrow',
            'tomato': 'drip',
            'potato': 'sprinkler',
            'cotton': 'drip',
            'wheat': 'sprinkler',
            'corn': 'furrow'
        }
        
        recommended_method = crop_methods.get(crop, 'sprinkler')
        efficiency = self.irrigation_efficiency[recommended_method]
        
        # Calculate actual water needed considering efficiency
        actual_water_needed = water_deficit / efficiency if efficiency > 0 else water_deficit
        
        return {
            'method': recommended_method,
            'efficiency_percent': efficiency * 100,
            'water_needed_mm': round(actual_water_needed, 1),
            'advantages': self._get_method_advantages(recommended_method)
        }
    
    def _get_method_advantages(self, method: str) -> List[str]:
        """Get advantages of irrigation method"""
        
        advantages = {
            'drip': [
                "90% water efficiency",
                "Precise water application",
                "Reduced weed growth",
                "Lower labor requirements"
            ],
            'sprinkler': [
                "75% water efficiency",
                "Good for field crops",
                "Uniform water distribution",
                "Can apply fertilizers"
            ],
            'furrow': [
                "60% water efficiency",
                "Low initial cost",
                "Suitable for row crops",
                "Easy maintenance"
            ],
            'flood': [
                "45% water efficiency",
                "Suitable for rice",
                "Low labor requirement",
                "Traditional method"
            ]
        }
        
        return advantages.get(method, ["Standard irrigation method"])
    
    def _get_efficiency_tips(self, crop: str, soil_type: str, temperature: float) -> List[str]:
        """Get water efficiency tips"""
        
        tips = [
            "Irrigate during early morning or late evening",
            "Use mulching to reduce evaporation",
            "Monitor soil moisture regularly"
        ]
        
        if temperature > 30:
            tips.append("Increase irrigation frequency during hot weather")
        
        if soil_type == 'sandy':
            tips.append("Apply smaller, more frequent irrigations for sandy soil")
        elif soil_type == 'clay':
            tips.append("Allow longer intervals between irrigations for clay soil")
        
        if crop in ['tomato', 'potato', 'cotton']:
            tips.append("Consider drip irrigation for higher efficiency")
        
        return tips
    
    def calculate_water_budget(self, crop: str, area_hectares: float, 
                             irrigation_method: str, season_days: int = 120) -> Dict:
        """Calculate seasonal water budget"""
        
        daily_requirement = self.crop_water_requirements.get(crop, 5.0)
        efficiency = self.irrigation_efficiency.get(irrigation_method, 0.75)
        
        # Total water requirement for season
        total_requirement_mm = daily_requirement * season_days
        
        # Actual water needed considering efficiency
        actual_water_needed_mm = total_requirement_mm / efficiency
        
        # Convert to liters for the area
        total_liters = actual_water_needed_mm * area_hectares * 10000  # 1 hectare = 10000 m²
        
        # Cost estimation (₹0.50 per 1000 liters)
        water_cost = total_liters * 0.0005
        
        return {
            'crop': crop,
            'area_hectares': area_hectares,
            'irrigation_method': irrigation_method,
            'season_days': season_days,
            'daily_requirement_mm': daily_requirement,
            'total_requirement_mm': round(total_requirement_mm, 1),
            'actual_water_needed_mm': round(actual_water_needed_mm, 1),
            'total_water_liters': round(total_liters, 0),
            'efficiency_percent': efficiency * 100,
            'estimated_cost_rupees': round(water_cost, 2),
            'water_savings_potential': round((actual_water_needed_mm - total_requirement_mm), 1)
        }

# Example usage and testing
if __name__ == "__main__":
    model = IrrigationModel()
    
    # Test irrigation assessment
    result = model.assess_irrigation_need(
        crop='wheat',
        soil_moisture=35,
        temperature=28,
        humidity=60,
        wind_speed=8,
        growth_stage='flowering',
        soil_type='loamy',
        days_since_rain=4
    )
    
    print("Irrigation Assessment Results:")
    print(f"Crop: {result['crop'].title()}")
    print(f"Moisture Status: {result['assessment']['moisture_status']['status']}")
    print(f"Priority: {result['recommendation']['priority']}")
    print(f"Action: {result['recommendation']['action']}")
    
    if result['recommendation']['water_amount_mm'] > 0:
        print(f"Water Needed: {result['recommendation']['water_amount_mm']} mm")
        print(f"Duration: {result['recommendation']['duration_hours']} hours")
    
    print(f"\nRecommended Method: {result['recommendation']['method_recommendation']['method'].title()}")
    print(f"Efficiency: {result['recommendation']['method_recommendation']['efficiency_percent']:.0f}%")
    
    print(f"\nEfficiency Tips:")
    for tip in result['efficiency_tips']:
        print(f"  • {tip}")
    
    # Test water budget
    budget = model.calculate_water_budget('wheat', 2.0, 'drip', 120)
    print(f"\nWater Budget (2 hectares, 120 days):")
    print(f"Total Water Needed: {budget['total_water_liters']:,.0f} liters")
    print(f"Estimated Cost: ₹{budget['estimated_cost_rupees']:,.2f}")
    print(f"Efficiency: {budget['efficiency_percent']:.0f}%")