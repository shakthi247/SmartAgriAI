"""
Crop Rotation & Recommendation Model
Expert system for intelligent crop sequencing and selection
"""

import random
from typing import Dict, List, Tuple
from datetime import datetime, timedelta

class CropRotationModel:
    def __init__(self):
        # Comprehensive crop database with agronomic requirements
        self.crop_database = {
            # Cereals
            "wheat": {"soil_min": 6, "season": "winter", "category": "cereals", "nitrogen_need": "medium", "water_need": "medium"},
            "rice": {"soil_min": 7, "season": "monsoon", "category": "cereals", "nitrogen_need": "high", "water_need": "high"},
            "corn": {"soil_min": 6, "season": "monsoon", "category": "cereals", "nitrogen_need": "high", "water_need": "medium"},
            "barley": {"soil_min": 5, "season": "winter", "category": "cereals", "nitrogen_need": "medium", "water_need": "low"},
            "millet": {"soil_min": 4, "season": "monsoon", "category": "cereals", "nitrogen_need": "low", "water_need": "low"},
            
            # Legumes (Nitrogen fixers)
            "soybean": {"soil_min": 6, "season": "monsoon", "category": "legumes", "nitrogen_need": "low", "water_need": "medium"},
            "chickpea": {"soil_min": 6, "season": "winter", "category": "legumes", "nitrogen_need": "low", "water_need": "low"},
            "lentil": {"soil_min": 6, "season": "winter", "category": "legumes", "nitrogen_need": "low", "water_need": "low"},
            "groundnut": {"soil_min": 5, "season": "monsoon", "category": "legumes", "nitrogen_need": "low", "water_need": "medium"},
            
            # Vegetables
            "potato": {"soil_min": 6, "season": "winter", "category": "vegetables", "nitrogen_need": "medium", "water_need": "medium"},
            "tomato": {"soil_min": 7, "season": "all", "category": "vegetables", "nitrogen_need": "high", "water_need": "high"},
            "onion": {"soil_min": 6, "season": "winter", "category": "vegetables", "nitrogen_need": "medium", "water_need": "medium"},
            "cabbage": {"soil_min": 6, "season": "winter", "category": "vegetables", "nitrogen_need": "medium", "water_need": "medium"},
            
            # Cash crops
            "cotton": {"soil_min": 6, "season": "monsoon", "category": "cash_crops", "nitrogen_need": "high", "water_need": "medium"},
            "sugarcane": {"soil_min": 7, "season": "all", "category": "cash_crops", "nitrogen_need": "high", "water_need": "high"},
            
            # Oilseeds
            "mustard": {"soil_min": 5, "season": "winter", "category": "oilseeds", "nitrogen_need": "medium", "water_need": "low"},
            "sunflower": {"soil_min": 5, "season": "winter", "category": "oilseeds", "nitrogen_need": "medium", "water_need": "medium"},
        }
        
        # Rotation benefits matrix
        self.rotation_benefits = {
            'cereals': ['legumes', 'oilseeds', 'vegetables'],
            'legumes': ['cereals', 'cash_crops', 'vegetables'], 
            'oilseeds': ['cereals', 'legumes', 'vegetables'],
            'vegetables': ['cereals', 'legumes', 'oilseeds'],
            'cash_crops': ['legumes', 'cereals', 'oilseeds']
        }
        
        # Season mapping
        self.seasons = {
            'winter': ['winter', 'all'],
            'monsoon': ['monsoon', 'all'],
            'summer': ['summer', 'all']
        }
    
    def suggest_crop_rotation(self, current_crop: str, soil_quality: float, 
                            season: str, area_hectares: float = 1.0) -> Dict:
        """
        Suggest optimal crop rotation based on current crop and conditions
        
        Args:
            current_crop: Currently grown crop
            soil_quality: Soil quality score (0-10)
            season: Next planting season (winter/monsoon/summer)
            area_hectares: Farm area in hectares
            
        Returns:
            Dict with rotation suggestions and analysis
        """
        
        # Get current crop category
        current_category = self.crop_database.get(current_crop, {}).get('category', 'unknown')
        
        # Get beneficial rotation categories
        beneficial_categories = self.rotation_benefits.get(current_category, ['cereals', 'legumes'])
        
        # Filter crops by season and soil requirements
        suitable_crops = []
        for crop, data in self.crop_database.items():
            if (data['season'] in self.seasons.get(season, [season]) and 
                data['soil_min'] <= soil_quality + 2):  # Allow 2-point tolerance
                
                # Calculate rotation benefit score
                benefit_score = 0
                if data['category'] in beneficial_categories:
                    benefit_score = 3
                elif data['category'] == current_category:
                    benefit_score = 1  # Same category penalty
                else:
                    benefit_score = 2
                
                # Calculate overall suitability score
                soil_match = min(10, soil_quality - data['soil_min'] + 5)
                total_score = benefit_score * 2 + soil_match
                
                suitable_crops.append({
                    'crop': crop,
                    'category': data['category'],
                    'suitability_score': total_score,
                    'rotation_benefit': self._get_rotation_benefit(current_category, data['category']),
                    'soil_requirement': data['soil_min'],
                    'water_need': data['water_need'],
                    'nitrogen_need': data['nitrogen_need']
                })
        
        # Sort by suitability score
        suitable_crops.sort(key=lambda x: x['suitability_score'], reverse=True)
        
        # Get top 5 recommendations
        top_recommendations = suitable_crops[:5]
        
        # Generate rotation plan
        rotation_plan = self._generate_rotation_plan(current_crop, top_recommendations[0]['crop'] if top_recommendations else 'wheat')
        
        return {
            'current_crop': current_crop,
            'current_category': current_category,
            'recommendations': top_recommendations,
            'rotation_plan': rotation_plan,
            'season': season,
            'soil_quality': soil_quality
        }
    
    def _get_rotation_benefit(self, current_category: str, next_category: str) -> str:
        """Explain the benefit of crop rotation"""
        benefits = {
            ('cereals', 'legumes'): "Legumes fix nitrogen, reducing fertilizer needs for next cereal crop",
            ('legumes', 'cereals'): "Cereals utilize nitrogen fixed by previous legume crop",
            ('cereals', 'oilseeds'): "Different root systems improve soil structure",
            ('vegetables', 'cereals'): "Rotation breaks pest cycles common in vegetable crops",
            ('cash_crops', 'legumes'): "Legumes restore soil fertility after nutrient-intensive cash crops",
            ('oilseeds', 'cereals'): "Oilseeds improve soil organic matter for cereal production"
        }
        
        return benefits.get((current_category, next_category), 
                          "Crop rotation improves soil health and breaks pest cycles")
    
    def _generate_rotation_plan(self, current_crop: str, next_crop: str) -> List[Dict]:
        """Generate a 3-year rotation plan"""
        plan = [
            {
                'year': 1,
                'season': 'Current',
                'crop': current_crop,
                'purpose': 'Current cultivation'
            },
            {
                'year': 1,
                'season': 'Next',
                'crop': next_crop,
                'purpose': 'Recommended rotation crop'
            }
        ]
        
        # Add third crop for complete rotation
        next_category = self.crop_database.get(next_crop, {}).get('category', 'cereals')
        third_options = []
        
        for crop, data in self.crop_database.items():
            if (data['category'] in self.rotation_benefits.get(next_category, ['cereals']) and 
                crop not in [current_crop, next_crop]):
                third_options.append(crop)
        
        third_crop = random.choice(third_options) if third_options else 'wheat'
        
        plan.append({
            'year': 2,
            'season': 'Following',
            'crop': third_crop,
            'purpose': 'Complete rotation cycle'
        })
        
        return plan
    
    def analyze_rotation_benefits(self, rotation_sequence: List[str]) -> Dict:
        """Analyze the benefits of a crop rotation sequence"""
        
        categories = [self.crop_database.get(crop, {}).get('category', 'unknown') 
                     for crop in rotation_sequence]
        
        # Calculate diversity score
        unique_categories = len(set(categories))
        diversity_score = min(10, unique_categories * 2.5)
        
        # Check for nitrogen fixation
        has_legumes = 'legumes' in categories
        nitrogen_benefit = 8 if has_legumes else 3
        
        # Check for pest break
        consecutive_same = any(categories[i] == categories[i+1] 
                             for i in range(len(categories)-1))
        pest_control_score = 3 if consecutive_same else 8
        
        # Overall sustainability score
        sustainability_score = (diversity_score + nitrogen_benefit + pest_control_score) / 3
        
        return {
            'diversity_score': diversity_score,
            'nitrogen_benefit_score': nitrogen_benefit,
            'pest_control_score': pest_control_score,
            'overall_sustainability': sustainability_score,
            'has_nitrogen_fixers': has_legumes,
            'recommendations': self._get_sustainability_recommendations(
                diversity_score, nitrogen_benefit, pest_control_score
            )
        }
    
    def _get_sustainability_recommendations(self, diversity: float, 
                                         nitrogen: float, pest: float) -> List[str]:
        """Generate recommendations for improving rotation sustainability"""
        recommendations = []
        
        if diversity < 6:
            recommendations.append("Include more diverse crop categories in rotation")
        
        if nitrogen < 6:
            recommendations.append("Add nitrogen-fixing legumes (soybean, chickpea, lentil)")
        
        if pest < 6:
            recommendations.append("Avoid growing same crop category consecutively")
        
        if not recommendations:
            recommendations.append("Excellent rotation plan - maintain this sequence")
        
        return recommendations

# Example usage and testing
if __name__ == "__main__":
    model = CropRotationModel()
    
    # Test rotation suggestion
    result = model.suggest_crop_rotation(
        current_crop="wheat",
        soil_quality=7.5,
        season="monsoon",
        area_hectares=2.0
    )
    
    print("Crop Rotation Analysis:")
    print(f"Current: {result['current_crop']} ({result['current_category']})")
    print(f"Season: {result['season']}")
    print(f"Soil Quality: {result['soil_quality']}/10")
    
    print("\nTop Recommendations:")
    for i, rec in enumerate(result['recommendations'][:3], 1):
        print(f"{i}. {rec['crop'].title()} (Score: {rec['suitability_score']:.1f})")
        print(f"   Benefit: {rec['rotation_benefit']}")
    
    print("\nRotation Plan:")
    for step in result['rotation_plan']:
        print(f"Year {step['year']} ({step['season']}): {step['crop'].title()} - {step['purpose']}")
    
    # Test rotation analysis
    sequence = ["wheat", "soybean", "corn"]
    analysis = model.analyze_rotation_benefits(sequence)
    print(f"\nRotation Analysis for {' → '.join(sequence)}:")
    print(f"Sustainability Score: {analysis['overall_sustainability']:.1f}/10")
    print(f"Diversity: {analysis['diversity_score']:.1f}/10")
    print(f"Nitrogen Benefit: {analysis['nitrogen_benefit_score']:.1f}/10")