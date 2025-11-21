"""
AI Chatbot Model
Conversational AI for agricultural guidance and support
"""

import requests
import json
import random
from typing import Dict, List, Optional
import time

class AgriculturalChatbot:
    def __init__(self):
        self.ollama_url = "http://localhost:11434/api/generate"
        self.available_models = ["llama3", "llama2", "mistral", "codellama", "phi3"]
        self.default_model = "llama2"
        
        # Fallback responses for when Ollama is unavailable
        self.fallback_responses = {
            'weather': [
                "Weather is crucial for farming. Monitor temperature, rainfall, and humidity regularly.",
                "Check local weather forecasts daily to plan irrigation and field activities.",
                "Extreme weather can damage crops - prepare protective measures in advance."
            ],
            'soil': [
                "Good soil health is the foundation of successful farming. Test pH and nutrients regularly.",
                "Maintain soil pH between 6.0-7.5 for most crops. Add lime if too acidic, sulfur if too alkaline.",
                "Organic matter improves soil structure. Add compost or well-rotted manure annually."
            ],
            'irrigation': [
                "Water crops early morning or late evening to reduce evaporation losses.",
                "Check soil moisture before irrigating. Overwatering can be as harmful as underwatering.",
                "Drip irrigation is most efficient, saving 30-50% water compared to flood irrigation."
            ],
            'fertilizer': [
                "Apply fertilizers based on soil test results. Avoid over-fertilization.",
                "Nitrogen promotes leaf growth, phosphorus helps roots, potassium improves disease resistance.",
                "Organic fertilizers release nutrients slowly and improve soil health long-term."
            ],
            'pest': [
                "Regular field inspection helps detect pest problems early when they're easier to control.",
                "Use integrated pest management (IPM) - combine biological, cultural, and chemical methods.",
                "Encourage beneficial insects by planting diverse crops and avoiding broad-spectrum pesticides."
            ],
            'crop': [
                "Choose crops suitable for your climate, soil type, and market demand.",
                "Rotate crops to break pest cycles and maintain soil fertility.",
                "Plant disease-resistant varieties when available to reduce pesticide use."
            ],
            'market': [
                "Study market prices and demand before deciding what crops to grow.",
                "Diversify crops to spread risk and ensure steady income throughout the year.",
                "Consider value-addition like processing or direct marketing for better profits."
            ],
            'general': [
                "Farming success depends on good planning, regular monitoring, and timely actions.",
                "Keep detailed records of activities, inputs, and yields to improve decision-making.",
                "Stay updated with latest agricultural techniques and government schemes.",
                "Join farmer groups or cooperatives for better access to inputs and markets."
            ]
        }
        
        # Agricultural knowledge base
        self.knowledge_base = {
            'crop_seasons': {
                'kharif': ['rice', 'corn', 'cotton', 'sugarcane', 'soybean'],
                'rabi': ['wheat', 'barley', 'mustard', 'chickpea', 'potato'],
                'zaid': ['watermelon', 'cucumber', 'fodder crops']
            },
            'soil_ph_requirements': {
                'acidic_tolerant': ['tea', 'coffee', 'potato'],
                'neutral': ['wheat', 'rice', 'corn', 'soybean'],
                'alkaline_tolerant': ['barley', 'sugar beet']
            },
            'water_requirements': {
                'high': ['rice', 'sugarcane', 'banana'],
                'medium': ['wheat', 'corn', 'cotton'],
                'low': ['millet', 'sorghum', 'groundnut']
            }
        }
    
    def get_response(self, user_input: str, model: str = None, 
                    context: Dict = None) -> Dict:
        """
        Get AI response to user query
        
        Args:
            user_input: User's question or message
            model: Ollama model to use (optional)
            context: Additional context like weather, soil data (optional)
            
        Returns:
            Dict with response and metadata
        """
        
        # Try Ollama first
        ollama_response = self._try_ollama_response(user_input, model, context)
        
        if ollama_response['success']:
            return ollama_response
        
        # Fallback to rule-based response
        fallback_response = self._get_fallback_response(user_input, context)
        
        return {
            'response': fallback_response,
            'source': 'fallback',
            'success': True,
            'model_used': 'rule_based',
            'confidence': 0.7
        }
    
    def _try_ollama_response(self, user_input: str, model: str = None, 
                           context: Dict = None) -> Dict:
        """Try to get response from Ollama"""
        
        try:
            model_name = model or self.default_model
            
            # Create agricultural context prompt
            system_prompt = self._create_system_prompt(context)
            full_prompt = f"{system_prompt}\n\nUser Question: {user_input}\n\nResponse:"
            
            payload = {
                "model": model_name,
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "max_tokens": 500
                }
            }
            
            response = requests.post(
                self.ollama_url, 
                json=payload, 
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    'response': result.get('response', '').strip(),
                    'source': 'ollama',
                    'success': True,
                    'model_used': model_name,
                    'confidence': 0.9
                }
            else:
                return {'success': False, 'error': f'HTTP {response.status_code}'}
                
        except requests.exceptions.RequestException as e:
            return {'success': False, 'error': f'Connection error: {str(e)}'}
        except Exception as e:
            return {'success': False, 'error': f'Unexpected error: {str(e)}'}
    
    def _create_system_prompt(self, context: Dict = None) -> str:
        """Create system prompt with agricultural expertise"""
        
        base_prompt = """You are an expert agricultural advisor with deep knowledge of:
- Crop cultivation and management
- Soil health and fertilization
- Irrigation and water management
- Pest and disease control
- Market analysis and farming economics
- Sustainable farming practices

Provide practical, actionable advice suitable for farmers. Be specific and include:
- Clear recommendations
- Reasoning behind suggestions
- Potential risks or considerations
- Cost-effective solutions when possible

Keep responses concise but comprehensive."""
        
        if context:
            context_info = "\n\nCurrent Conditions:\n"
            
            if 'weather' in context:
                weather = context['weather']
                context_info += f"- Temperature: {weather.get('temperature', 'N/A')}°C\n"
                context_info += f"- Humidity: {weather.get('humidity', 'N/A')}%\n"
                context_info += f"- Weather: {weather.get('description', 'N/A')}\n"
            
            if 'soil' in context:
                soil = context['soil']
                context_info += f"- Soil Moisture: {soil.get('moisture', 'N/A')}%\n"
                context_info += f"- Soil pH: {soil.get('ph', 'N/A')}\n"
            
            if 'crop' in context:
                context_info += f"- Current Crop: {context['crop']}\n"
            
            base_prompt += context_info
        
        return base_prompt
    
    def _get_fallback_response(self, user_input: str, context: Dict = None) -> str:
        """Generate rule-based fallback response"""
        
        user_input_lower = user_input.lower()
        
        # Identify topic based on keywords
        topic = self._identify_topic(user_input_lower)
        
        # Get base response
        base_responses = self.fallback_responses.get(topic, self.fallback_responses['general'])
        base_response = random.choice(base_responses)
        
        # Add context-specific information
        contextual_info = self._add_contextual_info(topic, context)
        
        # Combine response
        full_response = base_response
        if contextual_info:
            full_response += f"\n\n{contextual_info}"
        
        # Add specific recommendations based on input
        specific_advice = self._get_specific_advice(user_input_lower, topic)
        if specific_advice:
            full_response += f"\n\nSpecific advice: {specific_advice}"
        
        return full_response
    
    def _identify_topic(self, user_input: str) -> str:
        """Identify the main topic of user's question"""
        
        topic_keywords = {
            'weather': ['weather', 'rain', 'temperature', 'climate', 'season'],
            'soil': ['soil', 'ph', 'nutrient', 'fertilizer', 'compost', 'organic'],
            'irrigation': ['water', 'irrigation', 'moisture', 'drought', 'watering'],
            'pest': ['pest', 'insect', 'disease', 'fungus', 'spray', 'control'],
            'crop': ['crop', 'plant', 'seed', 'variety', 'cultivation', 'harvest'],
            'market': ['price', 'market', 'sell', 'profit', 'cost', 'economics']
        }
        
        topic_scores = {}
        
        for topic, keywords in topic_keywords.items():
            score = sum(1 for keyword in keywords if keyword in user_input)
            if score > 0:
                topic_scores[topic] = score
        
        if topic_scores:
            return max(topic_scores, key=topic_scores.get)
        
        return 'general'
    
    def _add_contextual_info(self, topic: str, context: Dict = None) -> str:
        """Add context-specific information to response"""
        
        if not context:
            return ""
        
        contextual_info = []
        
        if topic == 'irrigation' and 'soil' in context:
            moisture = context['soil'].get('moisture', 0)
            if moisture < 30:
                contextual_info.append(f"Your current soil moisture is {moisture}% - irrigation is needed soon.")
            elif moisture > 70:
                contextual_info.append(f"Your soil moisture is {moisture}% - no irrigation needed currently.")
        
        if topic == 'weather' and 'weather' in context:
            temp = context['weather'].get('temperature', 0)
            if temp > 35:
                contextual_info.append("High temperature detected - ensure adequate irrigation and shade.")
            elif temp < 10:
                contextual_info.append("Low temperature - protect crops from frost damage.")
        
        if topic == 'soil' and 'soil' in context:
            ph = context['soil'].get('ph', 7)
            if ph < 6:
                contextual_info.append(f"Your soil pH is {ph} (acidic) - consider adding lime.")
            elif ph > 8:
                contextual_info.append(f"Your soil pH is {ph} (alkaline) - consider adding sulfur.")
        
        return " ".join(contextual_info)
    
    def _get_specific_advice(self, user_input: str, topic: str) -> str:
        """Get specific advice based on user input"""
        
        specific_responses = {
            'when to plant': "Plant timing depends on your location and crop. Kharif crops (June-July), Rabi crops (October-December), Zaid crops (March-April).",
            'how much water': "Water requirements vary by crop and growth stage. Generally, 2-3 inches per week during growing season.",
            'fertilizer amount': "Apply fertilizers based on soil test. Typical NPK ratio: 4:2:1 for most crops.",
            'pest control': "Use IPM approach: monitor regularly, use biological controls first, chemicals as last resort.",
            'soil preparation': "Plow 2-3 times, add organic matter, level the field, and ensure proper drainage.",
            'harvest time': "Harvest when crops reach physiological maturity. Look for color change, moisture content, and field drying."
        }
        
        for key, advice in specific_responses.items():
            if key in user_input:
                return advice
        
        return ""
    
    def get_quick_tips(self, category: str) -> List[str]:
        """Get quick tips for specific farming categories"""
        
        quick_tips = {
            'soil_health': [
                "Test soil pH annually and maintain between 6.0-7.5",
                "Add 2-3 tons of organic matter per hectare yearly",
                "Rotate crops to maintain soil fertility",
                "Avoid over-tillage to preserve soil structure"
            ],
            'water_management': [
                "Install drip irrigation for 40-50% water savings",
                "Mulch around plants to reduce evaporation",
                "Collect rainwater for dry season use",
                "Monitor soil moisture before irrigating"
            ],
            'pest_management': [
                "Scout fields weekly for early pest detection",
                "Use pheromone traps for monitoring",
                "Encourage beneficial insects with diverse plantings",
                "Apply pesticides only when economic threshold is reached"
            ],
            'crop_planning': [
                "Choose varieties suited to local climate",
                "Plan crop rotation to break pest cycles",
                "Diversify crops to spread market risk",
                "Consider market demand before planting"
            ]
        }
        
        return quick_tips.get(category, [])
    
    def check_ollama_status(self) -> Dict:
        """Check if Ollama service is available"""
        
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                available_models = [model['name'] for model in models]
                return {
                    'available': True,
                    'models': available_models,
                    'status': 'Connected'
                }
            else:
                return {
                    'available': False,
                    'models': [],
                    'status': f'HTTP Error {response.status_code}'
                }
        except Exception as e:
            return {
                'available': False,
                'models': [],
                'status': f'Connection failed: {str(e)}'
            }
    
    def get_conversation_starters(self) -> List[str]:
        """Get conversation starter questions"""
        
        starters = [
            "What crops should I plant this season?",
            "How can I improve my soil quality?",
            "When should I irrigate my crops?",
            "What are the signs of nutrient deficiency?",
            "How do I control pests naturally?",
            "What's the best time to harvest wheat?",
            "How can I increase my crop yield?",
            "What fertilizers should I use for tomatoes?",
            "How do I prepare soil for planting?",
            "What are current market prices for crops?"
        ]
        
        return random.sample(starters, 5)

# Example usage and testing
if __name__ == "__main__":
    chatbot = AgriculturalChatbot()
    
    # Check Ollama status
    status = chatbot.check_ollama_status()
    print(f"Ollama Status: {status['status']}")
    print(f"Available Models: {status['models']}")
    
    # Test conversation
    test_questions = [
        "How do I improve soil fertility?",
        "When should I water my wheat crop?",
        "What are the signs of nitrogen deficiency?"
    ]
    
    print("\nTesting Chatbot Responses:")
    print("=" * 50)
    
    for question in test_questions:
        print(f"\nQ: {question}")
        
        # Add sample context
        context = {
            'weather': {'temperature': 28, 'humidity': 65, 'description': 'Partly cloudy'},
            'soil': {'moisture': 45, 'ph': 6.8},
            'crop': 'wheat'
        }
        
        response = chatbot.get_response(question, context=context)
        print(f"A: {response['response']}")
        print(f"Source: {response['source']} | Model: {response.get('model_used', 'N/A')}")
    
    # Test quick tips
    print(f"\nQuick Tips for Soil Health:")
    tips = chatbot.get_quick_tips('soil_health')
    for i, tip in enumerate(tips, 1):
        print(f"{i}. {tip}")
    
    # Test conversation starters
    print(f"\nConversation Starters:")
    starters = chatbot.get_conversation_starters()
    for i, starter in enumerate(starters, 1):
        print(f"{i}. {starter}")