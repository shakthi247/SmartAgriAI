"""
Price Prediction & Market Analysis Model
Time series analysis and market forecasting for agricultural commodities
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
from datetime import datetime, timedelta
import random

class PricePredictionModel:
    def __init__(self):
        # Current market prices (₹/quintal)
        self.current_prices = {
            'wheat': 2200, 'rice': 2800, 'corn': 1800, 'barley': 1900, 'millet': 2500,
            'soybean': 4500, 'chickpea': 5500, 'lentil': 6000, 'groundnut': 5800,
            'potato': 1200, 'tomato': 1500, 'onion': 1800, 'cabbage': 800,
            'cotton': 5500, 'sugarcane': 350, 'mustard': 5200, 'sunflower': 6000
        }
        
        # Typical yields (quintals/hectare)
        self.typical_yields = {
            'wheat': 45, 'rice': 40, 'corn': 50, 'barley': 35, 'millet': 25,
            'soybean': 20, 'chickpea': 18, 'lentil': 15, 'groundnut': 22,
            'potato': 250, 'tomato': 300, 'onion': 200, 'cabbage': 400,
            'cotton': 15, 'sugarcane': 800, 'mustard': 18, 'sunflower': 20
        }
        
        # Cultivation costs (₹/hectare)
        self.cultivation_costs = {
            'wheat': 35000, 'rice': 45000, 'corn': 30000, 'barley': 28000, 'millet': 20000,
            'soybean': 32000, 'chickpea': 28000, 'lentil': 25000, 'groundnut': 35000,
            'potato': 60000, 'tomato': 80000, 'onion': 50000, 'cabbage': 45000,
            'cotton': 50000, 'sugarcane': 120000, 'mustard': 25000, 'sunflower': 30000
        }
        
        # Seasonal patterns (price multipliers by month)
        self.seasonal_patterns = {
            'wheat': [1.1, 1.1, 1.0, 0.9, 0.8, 0.8, 0.9, 1.0, 1.1, 1.2, 1.2, 1.1],
            'rice': [0.9, 0.9, 1.0, 1.1, 1.2, 1.2, 1.1, 1.0, 0.9, 0.8, 0.8, 0.9],
            'potato': [0.8, 0.8, 0.9, 1.0, 1.2, 1.3, 1.2, 1.1, 1.0, 0.9, 0.8, 0.8],
            'tomato': [1.2, 1.1, 1.0, 0.9, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.2, 1.2]
        }
        
        # Market volatility factors
        self.volatility = {
            'vegetables': 0.15,  # High volatility
            'cereals': 0.08,     # Medium volatility
            'pulses': 0.12,      # Medium-high volatility
            'cash_crops': 0.10   # Medium volatility
        }
    
    def predict_prices(self, crop: str, months_ahead: int = 6, 
                      planting_date: datetime = None) -> Dict:
        """
        Predict future prices for a crop
        
        Args:
            crop: Crop name
            months_ahead: Number of months to predict
            planting_date: When crop was/will be planted
            
        Returns:
            Dict with price predictions and analysis
        """
        
        if crop not in self.current_prices:
            return {'error': f'Price data not available for {crop}'}
        
        current_price = self.current_prices[crop]
        
        # Generate historical data (6 months back)
        historical_data = self._generate_historical_data(crop, current_price)
        
        # Generate future predictions
        future_predictions = self._generate_future_predictions(
            crop, current_price, months_ahead
        )
        
        # Calculate harvest timing impact
        harvest_impact = self._calculate_harvest_impact(crop, planting_date) if planting_date else {}
        
        # Market analysis
        market_analysis = self._analyze_market_trends(crop, historical_data, future_predictions)
        
        return {
            'crop': crop,
            'current_price': current_price,
            'historical_data': historical_data,
            'future_predictions': future_predictions,
            'harvest_impact': harvest_impact,
            'market_analysis': market_analysis,
            'recommendation': self._get_market_recommendation(crop, market_analysis)
        }
    
    def _generate_historical_data(self, crop: str, current_price: float) -> List[Dict]:
        """Generate realistic historical price data"""
        
        historical_data = []
        base_date = datetime.now() - timedelta(days=180)  # 6 months back
        
        # Get crop category for volatility
        category = self._get_crop_category(crop)
        volatility = self.volatility.get(category, 0.10)
        
        price = current_price * 0.9  # Start slightly lower
        
        for i in range(180):  # Daily data for 6 months
            date = base_date + timedelta(days=i)
            
            # Add seasonal effect
            month = date.month
            seasonal_multiplier = self.seasonal_patterns.get(crop, [1.0] * 12)[month - 1]
            
            # Add random volatility
            daily_change = random.uniform(-volatility/30, volatility/30)
            price *= (1 + daily_change)
            
            # Apply seasonal effect gradually
            price = price * (0.99 + 0.01 * seasonal_multiplier)
            
            if i % 7 == 0:  # Weekly data points
                historical_data.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'price': round(price, 2),
                    'volume': random.randint(1000, 5000)  # Mock volume data
                })
        
        return historical_data
    
    def _generate_future_predictions(self, crop: str, current_price: float, 
                                   months_ahead: int) -> List[Dict]:
        """Generate future price predictions"""
        
        predictions = []
        base_date = datetime.now()
        
        # Calculate trend based on crop type and season
        trend = self._calculate_price_trend(crop)
        
        category = self._get_crop_category(crop)
        volatility = self.volatility.get(category, 0.10)
        
        price = current_price
        
        for month in range(1, months_ahead + 1):
            future_date = base_date + timedelta(days=30 * month)
            
            # Apply trend
            price *= (1 + trend/12)  # Monthly trend application
            
            # Add seasonal effect
            seasonal_multiplier = self.seasonal_patterns.get(crop, [1.0] * 12)[future_date.month - 1]
            seasonal_price = price * seasonal_multiplier
            
            # Add uncertainty range
            uncertainty = volatility * month * 0.1  # Uncertainty increases with time
            min_price = seasonal_price * (1 - uncertainty)
            max_price = seasonal_price * (1 + uncertainty)
            
            predictions.append({
                'month': month,
                'date': future_date.strftime('%Y-%m'),
                'predicted_price': round(seasonal_price, 2),
                'min_price': round(min_price, 2),
                'max_price': round(max_price, 2),
                'confidence': max(0.5, 1.0 - month * 0.1)  # Decreasing confidence
            })
        
        return predictions
    
    def _calculate_price_trend(self, crop: str) -> float:
        """Calculate expected price trend based on market factors"""
        
        # Base trend factors
        trends = {
            'wheat': 0.05,    # Moderate increase
            'rice': 0.03,     # Stable
            'potato': 0.08,   # Higher volatility
            'tomato': 0.10,   # High volatility
            'cotton': 0.06,   # Export dependent
            'soybean': 0.07   # Global demand
        }
        
        base_trend = trends.get(crop, 0.05)
        
        # Add random market factors
        market_factor = random.uniform(-0.03, 0.03)
        
        return base_trend + market_factor
    
    def _calculate_harvest_impact(self, crop: str, planting_date: datetime) -> Dict:
        """Calculate impact of harvest timing on prices"""
        
        # Typical crop durations (days)
        crop_durations = {
            'wheat': 120, 'rice': 120, 'corn': 100, 'potato': 90,
            'tomato': 80, 'cotton': 180, 'soybean': 100
        }
        
        duration = crop_durations.get(crop, 100)
        harvest_date = planting_date + timedelta(days=duration)
        
        # Price impact around harvest
        days_to_harvest = (harvest_date - datetime.now()).days
        
        if days_to_harvest < 0:
            impact = "Harvest completed - prices may be stabilizing"
        elif days_to_harvest < 30:
            impact = "Harvest approaching - prices may decline due to increased supply"
        elif days_to_harvest < 60:
            impact = "Pre-harvest period - prices may remain stable"
        else:
            impact = "Growing season - prices following seasonal trends"
        
        return {
            'planting_date': planting_date.strftime('%Y-%m-%d'),
            'expected_harvest_date': harvest_date.strftime('%Y-%m-%d'),
            'days_to_harvest': days_to_harvest,
            'harvest_impact': impact
        }
    
    def _analyze_market_trends(self, crop: str, historical: List[Dict], 
                             future: List[Dict]) -> Dict:
        """Analyze market trends and patterns"""
        
        # Calculate historical trend
        if len(historical) >= 2:
            start_price = historical[0]['price']
            end_price = historical[-1]['price']
            historical_trend = (end_price - start_price) / start_price * 100
        else:
            historical_trend = 0
        
        # Calculate future trend
        if len(future) >= 2:
            current_price = self.current_prices[crop]
            future_price = future[-1]['predicted_price']
            future_trend = (future_price - current_price) / current_price * 100
        else:
            future_trend = 0
        
        # Market sentiment
        if future_trend > 10:
            sentiment = "Bullish"
        elif future_trend < -10:
            sentiment = "Bearish"
        else:
            sentiment = "Neutral"
        
        # Volatility analysis
        if len(historical) > 1:
            prices = [item['price'] for item in historical]
            volatility_score = np.std(prices) / np.mean(prices) * 100
        else:
            volatility_score = 0
        
        return {
            'historical_trend_percent': round(historical_trend, 2),
            'future_trend_percent': round(future_trend, 2),
            'market_sentiment': sentiment,
            'volatility_score': round(volatility_score, 2),
            'price_stability': 'High' if volatility_score < 5 else 'Medium' if volatility_score < 15 else 'Low'
        }
    
    def _get_market_recommendation(self, crop: str, analysis: Dict) -> Dict:
        """Generate market recommendations"""
        
        future_trend = analysis['future_trend_percent']
        sentiment = analysis['market_sentiment']
        
        if future_trend > 5:
            action = "HOLD/BUY"
            reason = "Prices expected to rise - good time to hold or buy"
        elif future_trend < -5:
            action = "SELL"
            reason = "Prices expected to decline - consider selling soon"
        else:
            action = "MONITOR"
            reason = "Stable prices expected - monitor market conditions"
        
        # Risk assessment
        volatility = analysis['volatility_score']
        if volatility > 15:
            risk = "High"
        elif volatility > 8:
            risk = "Medium"
        else:
            risk = "Low"
        
        return {
            'action': action,
            'reason': reason,
            'risk_level': risk,
            'confidence': 'High' if abs(future_trend) > 8 else 'Medium' if abs(future_trend) > 3 else 'Low'
        }
    
    def _get_crop_category(self, crop: str) -> str:
        """Get crop category for volatility analysis"""
        
        categories = {
            'vegetables': ['potato', 'tomato', 'onion', 'cabbage'],
            'cereals': ['wheat', 'rice', 'corn', 'barley', 'millet'],
            'pulses': ['soybean', 'chickpea', 'lentil', 'groundnut'],
            'cash_crops': ['cotton', 'sugarcane', 'mustard', 'sunflower']
        }
        
        for category, crops in categories.items():
            if crop in crops:
                return category
        
        return 'cereals'  # Default
    
    def calculate_profitability(self, crop: str, area_hectares: float, 
                              selling_month: int = None) -> Dict:
        """Calculate expected profitability"""
        
        current_price = self.current_prices[crop]
        typical_yield = self.typical_yields[crop]
        cultivation_cost = self.cultivation_costs[crop]
        
        # Adjust price for selling month if specified
        if selling_month and 1 <= selling_month <= 12:
            seasonal_multiplier = self.seasonal_patterns.get(crop, [1.0] * 12)[selling_month - 1]
            selling_price = current_price * seasonal_multiplier
        else:
            selling_price = current_price
        
        # Calculate economics
        total_production = typical_yield * area_hectares
        total_revenue = total_production * selling_price
        total_cost = cultivation_cost * area_hectares
        net_profit = total_revenue - total_cost
        profit_margin = (net_profit / total_revenue) * 100 if total_revenue > 0 else 0
        roi = (net_profit / total_cost) * 100 if total_cost > 0 else 0
        
        return {
            'crop': crop,
            'area_hectares': area_hectares,
            'expected_yield': total_production,
            'selling_price_per_quintal': selling_price,
            'total_revenue': round(total_revenue, 2),
            'total_cost': round(total_cost, 2),
            'net_profit': round(net_profit, 2),
            'profit_margin_percent': round(profit_margin, 2),
            'roi_percent': round(roi, 2),
            'breakeven_price': round(cultivation_cost / typical_yield, 2),
            'profitability': 'High' if roi > 50 else 'Medium' if roi > 20 else 'Low' if roi > 0 else 'Loss'
        }
    
    def compare_crop_profitability(self, crops: List[str], area_hectares: float = 1.0) -> Dict:
        """Compare profitability of multiple crops"""
        
        comparisons = []
        
        for crop in crops:
            if crop in self.current_prices:
                profitability = self.calculate_profitability(crop, area_hectares)
                comparisons.append(profitability)
        
        # Sort by ROI
        comparisons.sort(key=lambda x: x['roi_percent'], reverse=True)
        
        return {
            'area_hectares': area_hectares,
            'crop_comparisons': comparisons,
            'best_crop': comparisons[0] if comparisons else None,
            'summary': {
                'highest_roi': comparisons[0]['roi_percent'] if comparisons else 0,
                'lowest_roi': comparisons[-1]['roi_percent'] if comparisons else 0,
                'average_roi': sum(c['roi_percent'] for c in comparisons) / len(comparisons) if comparisons else 0
            }
        }

# Example usage and testing
if __name__ == "__main__":
    model = PricePredictionModel()
    
    # Test price prediction
    result = model.predict_prices('wheat', months_ahead=6)
    
    print("Price Prediction Results:")
    print(f"Crop: {result['crop'].title()}")
    print(f"Current Price: ₹{result['current_price']}/quintal")
    
    print(f"\nFuture Predictions:")
    for pred in result['future_predictions'][:3]:
        print(f"Month {pred['month']}: ₹{pred['predicted_price']} (Range: ₹{pred['min_price']}-₹{pred['max_price']})")
    
    print(f"\nMarket Analysis:")
    analysis = result['market_analysis']
    print(f"Trend: {analysis['future_trend_percent']}% ({analysis['market_sentiment']})")
    print(f"Volatility: {analysis['volatility_score']:.1f}% ({analysis['price_stability']} stability)")
    
    print(f"\nRecommendation: {result['recommendation']['action']}")
    print(f"Reason: {result['recommendation']['reason']}")
    
    # Test profitability
    profit = model.calculate_profitability('wheat', 2.0)
    print(f"\nProfitability Analysis (2 hectares):")
    print(f"Expected Profit: ₹{profit['net_profit']:,.0f}")
    print(f"ROI: {profit['roi_percent']:.1f}%")
    print(f"Profitability: {profit['profitability']}")