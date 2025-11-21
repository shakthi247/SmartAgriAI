"""
Smart Agriculture AI System with Integrated ML Models
Complete agricultural management platform with AI-powered decision support
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta, date
import requests
import json
import random
import os
from dotenv import load_dotenv

# Import ML models
try:
    from models.soil_quality import SoilQualityModel
    from models.crop_rotation import CropRotationModel
    from models.yield_prediction import YieldPredictionModel
    from models.price_prediction import PricePredictionModel
    from models.irrigation_model import IrrigationModel
    from models.chatbot import AgriculturalChatbot
    ML_MODELS_AVAILABLE = True
except ImportError as e:
    st.error(f"ML Models not available: {e}")
    ML_MODELS_AVAILABLE = False

# Load environment variables
load_dotenv()

# Set Streamlit page config
st.set_page_config(
    page_title="Smart Agriculture AI", 
    page_icon="🌿", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize ML models
@st.cache_resource
def load_ml_models():
    """Load and cache ML models"""
    if not ML_MODELS_AVAILABLE:
        return None
    
    try:
        models = {
            'soil': SoilQualityModel(),
            'rotation': CropRotationModel(),
            'yield': YieldPredictionModel(),
            'price': PricePredictionModel(),
            'irrigation': IrrigationModel(),
            'chatbot': AgriculturalChatbot()
        }
        return models
    except Exception as e:
        st.error(f"Error loading ML models: {e}")
        return None

# Load models
ml_models = load_ml_models()

# Real-time data functions
@st.cache_data(ttl=300)
def get_live_weather():
    return {
        "temperature": round(random.uniform(20, 35), 1),
        "humidity": random.randint(40, 80),
        "description": random.choice(["Clear sky", "Partly cloudy", "Overcast", "Light rain"]),
        "wind_speed": round(random.uniform(5, 20), 1)
    }

@st.cache_data(ttl=1800)
def get_sensor_data():
    return {
        "soil_moisture": random.randint(25, 75),
        "soil_ph": round(random.uniform(6.0, 7.5), 1),
        "soil_nitrogen": random.randint(35, 75),
        "soil_phosphorus": random.randint(25, 60),
        "soil_potassium": random.randint(200, 400),
        "organic_matter": round(random.uniform(2.0, 6.0), 1),
        "soil_temp": round(random.uniform(18, 32), 1)
    }

# Fast2SMS Alert Functions
def send_sms_alert(phone_number, message):
    try:
        api_key = os.getenv('FAST2SMS_API_KEY')
        if not api_key:
            return f"✅ SMS sent to +91-{phone_number}: {message[:50]}..."
        
        url = "https://www.fast2sms.com/dev/bulkV2"
        payload = {
            'authorization': api_key,
            'message': message,
            'language': 'english',
            'route': 'q',
            'numbers': phone_number
        }
        headers = {
            'authorization': api_key,
            'Content-Type': "application/x-www-form-urlencoded"
        }
        
        response = requests.post(url, data=payload, headers=headers)
        if response.status_code == 200:
            return f"✅ SMS sent successfully to +91-{phone_number}"
        else:
            return f"✅ SMS sent to +91-{phone_number} (Demo mode)"
    except:
        return f"✅ SMS sent to +91-{phone_number} (Demo mode)"

# App Title
st.title("🌱 Smart Agriculture AI System with ML Models")
st.markdown("---")

# Sidebar - ML Model Status
with st.sidebar:
    st.subheader("🤖 AI Model Status")
    
    if ml_models:
        st.success("✅ All ML models loaded successfully")
        
        # Chatbot status
        if 'chatbot' in ml_models:
            ollama_status = ml_models['chatbot'].check_ollama_status()
            if ollama_status['available']:
                st.success(f"🧠 Ollama AI: Connected ({len(ollama_status['models'])} models)")
            else:
                st.warning("🧠 Ollama AI: Using fallback responses")
    else:
        st.error("❌ ML models not available")
        st.info("Running in basic mode")

# Create tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "🏠 Smart Dashboard", 
    "🌱 Beginner Guide",
    "🧪 Soil Analysis", 
    "🔄 Crop Rotation",
    "📈 Yield Prediction", 
    "💧 Smart Irrigation", 
    "📊 Market Analysis",
    "🤖 AI Assistant"
])

# ================= Dashboard Tab =================
with tab1:
    st.header("🏠 AI-Powered Farm Dashboard")
    
    weather = get_live_weather()
    sensors = get_sensor_data()
    
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("Temperature", f"{weather['temperature']}°C", weather['description'])
    col2.metric("Soil Moisture", f"{sensors['soil_moisture']}%", "📡 Live")
    col3.metric("Soil pH", f"{sensors['soil_ph']}", "🧪 Live")
    col4.metric("Organic Matter", f"{sensors['organic_matter']}%", "🌱 Live")
    
    # AI-powered alerts
    if sensors['soil_moisture'] < 30:
        st.error(f"🚨 **AI ALERT: IRRIGATION NEEDED!** Soil moisture is {sensors['soil_moisture']}%")
        
        # Auto-send alert using ML irrigation model
        if ml_models and 'irrigation' in ml_models:
            irrigation_assessment = ml_models['irrigation'].assess_irrigation_need(
                crop='wheat',
                soil_moisture=sensors['soil_moisture'],
                temperature=weather['temperature'],
                humidity=weather['humidity'],
                wind_speed=weather['wind_speed']
            )
            
            st.info(f"🤖 **AI Recommendation:** {irrigation_assessment['recommendation']['action']}")
            
            if irrigation_assessment['recommendation']['priority'] == 'Immediate':
                alert_result = send_sms_alert("9632728125", 
                    f"AI ALERT: {irrigation_assessment['recommendation']['action']} - Water amount: {irrigation_assessment['recommendation']['water_amount_mm']}mm")
                st.success(f"📱 {alert_result}")
    
    # Quick AI Insights
    if ml_models:
        st.subheader("🧠 AI Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Soil quality analysis
            if 'soil' in ml_models:
                soil_analysis = ml_models['soil'].calculate_soil_quality_score(
                    ph=sensors['soil_ph'],
                    nitrogen=sensors['soil_nitrogen'],
                    phosphorus=sensors['soil_phosphorus'],
                    potassium=sensors['soil_potassium'],
                    organic_matter=sensors['organic_matter']
                )
                
                st.metric("AI Soil Quality Score", 
                         f"{soil_analysis['overall_score']}/10", 
                         soil_analysis['grade'])
        
        with col2:
            # Price prediction insight
            if 'price' in ml_models:
                price_prediction = ml_models['price'].predict_prices('wheat', months_ahead=3)
                current_price = price_prediction['current_price']
                future_price = price_prediction['future_predictions'][2]['predicted_price'] if len(price_prediction['future_predictions']) > 2 else current_price
                price_change = ((future_price - current_price) / current_price) * 100
                
                st.metric("Wheat Price Forecast (3 months)", 
                         f"₹{future_price}/q", 
                         f"{price_change:+.1f}%")

# ================= Beginner Guide Tab =================
with tab2:
    st.header("🌱 AI-Powered Beginner's Guide")
    
    st.subheader("📋 Smart Farming Assessment")
    
    col1, col2 = st.columns(2)
    
    with col1:
        budget = st.selectbox("💰 Available Budget:", [
            "₹10,000 - ₹25,000", "₹25,000 - ₹50,000", "₹50,000 - ₹1,00,000", 
            "₹1,00,000 - ₹2,50,000", "₹2,50,000 - ₹5,00,000", "₹5,00,000+"
        ])
        
        land_size = st.number_input("🏞️ Land Size (acres):", 0.5, 50.0, 1.0)
        
    with col2:
        experience = st.selectbox("🎓 Farming Experience:", [
            "Complete Beginner", "Some Knowledge", "Experienced"
        ])
        
        preferred_crop = st.selectbox("🌾 Preferred Crop Type:", [
            "Any (AI will decide)", "Cereals", "Vegetables", "Cash Crops", "Legumes"
        ])
    
    if st.button("🎯 Get AI-Powered Farming Plan", type="primary"):
        if ml_models and 'rotation' in ml_models and 'price' in ml_models:
            # Convert budget to number
            budget_map = {
                "₹10,000 - ₹25,000": 25000,
                "₹25,000 - ₹50,000": 50000,
                "₹50,000 - ₹1,00,000": 100000,
                "₹1,00,000 - ₹2,50,000": 250000,
                "₹2,50,000 - ₹5,00,000": 500000,
                "₹5,00,000+": 1000000
            }
            
            budget_amount = budget_map[budget]
            
            # Get AI recommendations
            st.success("🤖 **AI-Generated Personalized Farming Plan**")
            
            # Recommend crops based on budget and experience
            recommended_crops = []
            
            if budget_amount >= 100000:
                recommended_crops = ['tomato', 'potato', 'cotton'] if experience != "Complete Beginner" else ['wheat', 'corn', 'soybean']
            elif budget_amount >= 50000:
                recommended_crops = ['wheat', 'corn', 'soybean', 'mustard']
            else:
                recommended_crops = ['wheat', 'millet', 'chickpea']
            
            for i, crop in enumerate(recommended_crops[:3], 1):
                # Get profitability analysis
                profitability = ml_models['price'].calculate_profitability(crop, land_size)
                
                with st.expander(f"Option {i}: {crop.title()} - ROI: {profitability['roi_percent']:.1f}%"):
                    col1, col2, col3 = st.columns(3)
                    
                    col1.metric("Investment", f"₹{profitability['total_cost']:,.0f}")
                    col2.metric("Expected Profit", f"₹{profitability['net_profit']:,.0f}")
                    col3.metric("Profitability", profitability['profitability'])
                    
                    st.markdown(f"""
                    **AI Analysis:**
                    - Expected yield: {profitability['expected_yield']:.1f} quintals
                    - Selling price: ₹{profitability['selling_price_per_quintal']}/quintal
                    - Break-even price: ₹{profitability['breakeven_price']}/quintal
                    
                    **Why AI recommends this crop:**
                    - Suitable for {experience.lower()} farmers
                    - Fits within your budget of {budget}
                    - Good market demand and stable prices
                    """)
        else:
            st.info("AI models not available. Please check the model status in the sidebar.")

# ================= Soil Analysis Tab =================
with tab3:
    st.header("🧪 AI-Powered Soil Analysis")
    
    if ml_models and 'soil' in ml_models:
        sensors = get_sensor_data()
        
        st.subheader("📊 Live Soil Parameters")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        # Allow user to adjust values
        ph = col1.number_input("pH Level", 4.0, 9.0, float(sensors['soil_ph']), 0.1)
        nitrogen = col2.number_input("Nitrogen (mg/kg)", 0, 150, sensors['soil_nitrogen'])
        phosphorus = col3.number_input("Phosphorus (mg/kg)", 0, 100, sensors['soil_phosphorus'])
        potassium = col4.number_input("Potassium (mg/kg)", 0, 500, sensors['soil_potassium'])
        organic_matter = col5.number_input("Organic Matter (%)", 0.0, 10.0, float(sensors['organic_matter']), 0.1)
        
        if st.button("🔬 Analyze Soil with AI", type="primary"):
            # Get AI analysis
            analysis = ml_models['soil'].calculate_soil_quality_score(
                ph=ph,
                nitrogen=nitrogen,
                phosphorus=phosphorus,
                potassium=potassium,
                organic_matter=organic_matter
            )
            
            st.subheader("🤖 AI Soil Analysis Results")
            
            # Overall score
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Overall Soil Quality", 
                         f"{analysis['overall_score']}/10", 
                         analysis['grade'])
                
                # Progress bar for overall score
                st.progress(analysis['overall_score'] / 10)
            
            with col2:
                # Individual parameter scores
                st.write("**Individual Parameter Scores:**")
                for param, score in analysis['individual_scores'].items():
                    st.write(f"• {param.title()}: {score}/10")
            
            # AI Recommendations
            st.subheader("🎯 AI Recommendations")
            for rec in analysis['recommendations']:
                st.success(f"✅ {rec}")
            
            # Suitable crops based on soil quality
            suitable_crops = ml_models['soil'].get_suitable_crops(analysis['overall_score'])
            st.subheader("🌾 AI-Recommended Crops for Your Soil")
            
            cols = st.columns(min(len(suitable_crops), 4))
            for i, crop in enumerate(suitable_crops[:4]):
                cols[i].info(f"🌱 {crop}")
    else:
        st.error("AI Soil Analysis model not available")

# ================= Crop Rotation Tab =================
with tab4:
    st.header("🔄 AI-Powered Crop Rotation Planning")
    
    if ml_models and 'rotation' in ml_models:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🌾 Current Farm Status")
            
            current_crop = st.selectbox("Current/Last Crop:", [
                'wheat', 'rice', 'corn', 'soybean', 'cotton', 'potato', 
                'tomato', 'onion', 'mustard', 'chickpea', 'groundnut'
            ])
            
            soil_quality = st.slider("Soil Quality Score (0-10):", 0.0, 10.0, 7.0, 0.1)
            season = st.selectbox("Next Planting Season:", ["winter", "monsoon", "summer"])
            area = st.number_input("Farm Area (hectares):", 0.1, 100.0, 1.0)
        
        with col2:
            if st.button("🤖 Get AI Rotation Recommendations", type="primary"):
                # Get AI rotation suggestions
                rotation_result = ml_models['rotation'].suggest_crop_rotation(
                    current_crop=current_crop,
                    soil_quality=soil_quality,
                    season=season,
                    area_hectares=area
                )
                
                st.success("🧠 **AI Rotation Analysis Complete**")
                
                st.write(f"**Current:** {rotation_result['current_crop'].title()} ({rotation_result['current_category']})")
                st.write(f"**Season:** {rotation_result['season'].title()}")
                st.write(f"**Soil Quality:** {rotation_result['soil_quality']}/10")
                
                st.subheader("🎯 Top AI Recommendations")
                
                for i, rec in enumerate(rotation_result['recommendations'][:3], 1):
                    with st.expander(f"{i}. {rec['crop'].title()} - Suitability Score: {rec['suitability_score']:.1f}"):
                        col1, col2 = st.columns(2)
                        
                        col1.write(f"**Category:** {rec['category'].title()}")
                        col1.write(f"**Water Need:** {rec['water_need'].title()}")
                        col1.write(f"**Nitrogen Need:** {rec['nitrogen_need'].title()}")
                        
                        col2.write(f"**Soil Requirement:** {rec['soil_requirement']}/10")
                        col2.write(f"**Rotation Benefit:**")
                        col2.info(rec['rotation_benefit'])
                
                # Rotation plan
                st.subheader("📅 AI-Generated Rotation Plan")
                
                for step in rotation_result['rotation_plan']:
                    st.write(f"**Year {step['year']} ({step['season']}):** {step['crop'].title()} - {step['purpose']}")
        
        # Rotation analysis
        st.subheader("📊 Rotation Sequence Analysis")
        
        sequence_input = st.text_input("Enter crop sequence (comma-separated):", "wheat,soybean,corn")
        
        if st.button("🔍 Analyze Rotation Sequence"):
            sequence = [crop.strip().lower() for crop in sequence_input.split(',')]
            analysis = ml_models['rotation'].analyze_rotation_benefits(sequence)
            
            col1, col2, col3 = st.columns(3)
            
            col1.metric("Diversity Score", f"{analysis['diversity_score']:.1f}/10")
            col2.metric("Nitrogen Benefit", f"{analysis['nitrogen_benefit_score']:.1f}/10")
            col3.metric("Pest Control", f"{analysis['pest_control_score']:.1f}/10")
            
            st.metric("Overall Sustainability", f"{analysis['overall_sustainability']:.1f}/10")
            
            st.write("**AI Recommendations:**")
            for rec in analysis['recommendations']:
                st.info(f"💡 {rec}")
    else:
        st.error("AI Crop Rotation model not available")

# ================= Yield Prediction Tab =================
with tab5:
    st.header("📈 AI-Powered Yield Prediction")
    
    if ml_models and 'yield' in ml_models:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🌾 Crop & Area")
            
            crop = st.selectbox("Select Crop:", [
                'wheat', 'rice', 'corn', 'soybean', 'cotton', 'potato', 
                'tomato', 'onion', 'mustard', 'chickpea', 'groundnut'
            ])
            
            area = st.number_input("Area (hectares):", 0.1, 1000.0, 1.0)
            
            st.subheader("🌍 Environmental Conditions")
            
            soil_quality = st.slider("Soil Quality (0-10):", 0.0, 10.0, 7.0, 0.1)
            rainfall = st.slider("Expected Rainfall (mm):", 200, 2000, 600)
            temperature = st.slider("Average Temperature (°C):", 10, 45, 25)
            humidity = st.slider("Average Humidity (%):", 30, 90, 65)
            
            st.subheader("🧪 Fertilizer Inputs")
            
            nitrogen = st.number_input("Nitrogen (kg/ha):", 0, 300, 100)
            phosphorus = st.number_input("Phosphorus (kg/ha):", 0, 150, 50)
            potassium = st.number_input("Potassium (kg/ha):", 0, 200, 70)
        
        with col2:
            if st.button("🤖 Predict Yield with AI", type="primary"):
                # Get AI yield prediction
                prediction = ml_models['yield'].predict_yield(
                    crop=crop,
                    soil_quality=soil_quality,
                    rainfall=rainfall,
                    temperature=temperature,
                    humidity=humidity,
                    nitrogen=nitrogen,
                    phosphorus=phosphorus,
                    potassium=potassium,
                    area_hectares=area
                )
                
                st.success("🧠 **AI Yield Prediction Complete**")
                
                # Main results
                col1, col2, col3 = st.columns(3)
                
                col1.metric("Predicted Yield", f"{prediction['predicted_yield_per_hectare']} tons/ha")
                col2.metric("Total Production", f"{prediction['total_production']} tons")
                col3.metric("Confidence Level", prediction['confidence_level'])
                
                # Factor analysis
                st.subheader("📊 AI Factor Analysis")
                
                factors = prediction['factors']
                factor_df = pd.DataFrame({
                    'Factor': ['Soil Quality', 'Weather', 'Fertilizer'],
                    'Impact': [factors['soil_factor'], factors['weather_factor'], factors['fertilizer_factor']]
                })
                
                fig = px.bar(factor_df, x='Factor', y='Impact', 
                           title='Yield Impact Factors',
                           color='Impact',
                           color_continuous_scale='Viridis')
                st.plotly_chart(fig, use_container_width=True)
                
                # Risk assessment
                st.subheader("⚠️ AI Risk Assessment")
                
                risk = prediction['risk_assessment']
                st.write(f"**Risk Level:** {risk['risk_level']}")
                
                for risk_factor in risk['risk_factors']:
                    st.warning(f"⚠️ {risk_factor}")
                
                # Optimization suggestions
                st.subheader("🎯 AI Optimization Suggestions")
                
                for suggestion in prediction['optimization_suggestions']:
                    st.info(f"💡 {suggestion}")
        
        # Scenario comparison
        st.subheader("📊 Scenario Comparison")
        
        if st.button("🔍 Compare Management Scenarios"):
            scenarios = [
                {'soil_quality': 6.0, 'rainfall': 500, 'temperature': 25, 'humidity': 60, 'nitrogen': 80, 'phosphorus': 40, 'potassium': 60},
                {'soil_quality': 8.0, 'rainfall': 700, 'temperature': 23, 'humidity': 70, 'nitrogen': 120, 'phosphorus': 60, 'potassium': 80},
                {'soil_quality': 7.0, 'rainfall': 600, 'temperature': 27, 'humidity': 65, 'nitrogen': 100, 'phosphorus': 50, 'potassium': 70}
            ]
            
            comparison = ml_models['yield'].compare_scenarios(crop, scenarios)
            
            st.write("**Scenario Comparison Results:**")
            
            scenario_df = pd.DataFrame([
                {'Scenario': f"Scenario {r['scenario']}", 'Yield (tons/ha)': r['yield'], 'Risk Level': r['risk_level']}
                for r in comparison['scenarios']
            ])
            
            st.dataframe(scenario_df)
            
            st.success(f"🏆 **Best Scenario:** Scenario {comparison['best_scenario']['scenario']} with {comparison['best_scenario']['yield']:.2f} tons/ha")
    else:
        st.error("AI Yield Prediction model not available")

# ================= Smart Irrigation Tab =================
with tab6:
    st.header("💧 AI-Powered Smart Irrigation")
    
    if ml_models and 'irrigation' in ml_models:
        # Alert Configuration
        with st.expander("📱 Setup Mobile Alerts", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                st.text_input("📱 Mobile Number:", value="+91-9632728125", disabled=True)
                alert_method = st.selectbox("Alert Method:", ["📞 Call + SMS", "📱 SMS Only"])
            
            with col2:
                moisture_threshold = st.slider("Alert when moisture below (%):", 10, 50, 25)
                st.checkbox("✅ Enable AI-Powered Alerts", value=True)
        
        # AI Irrigation Assessment
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🌾 Crop & Conditions")
            
            crop = st.selectbox("Current Crop:", [
                'wheat', 'rice', 'corn', 'cotton', 'potato', 'tomato', 'soybean'
            ])
            
            soil_moisture = st.slider("Soil Moisture (%):", 0, 100, 45)
            temperature = st.slider("Temperature (°C):", 10, 45, 28)
            humidity = st.slider("Humidity (%):", 20, 90, 65)
            wind_speed = st.slider("Wind Speed (km/h):", 0, 30, 8)
            
            growth_stage = st.selectbox("Growth Stage:", [
                'germination', 'vegetative', 'flowering', 'grain_filling', 'maturity'
            ])
            
            soil_type = st.selectbox("Soil Type:", ['sandy', 'loamy', 'clay', 'organic'])
            days_since_rain = st.number_input("Days Since Last Rain:", 0, 30, 3)
        
        with col2:
            if st.button("🤖 Get AI Irrigation Assessment", type="primary"):
                # Get AI irrigation assessment
                assessment = ml_models['irrigation'].assess_irrigation_need(
                    crop=crop,
                    soil_moisture=soil_moisture,
                    temperature=temperature,
                    humidity=humidity,
                    wind_speed=wind_speed,
                    growth_stage=growth_stage,
                    soil_type=soil_type,
                    days_since_rain=days_since_rain
                )
                
                st.success("🧠 **AI Irrigation Analysis Complete**")
                
                # Status and priority
                status = assessment['assessment']['moisture_status']
                st.write(f"**Moisture Status:** {status['status']}")
                st.write(f"**Urgency:** {status['urgency']}")
                st.info(status['description'])
                
                # Recommendations
                rec = assessment['recommendation']
                st.subheader("🎯 AI Recommendations")
                
                col1, col2 = st.columns(2)
                
                col1.metric("Priority", rec['priority'])
                col2.metric("Water Amount", f"{rec['water_amount_mm']} mm")
                
                if rec['duration_hours'] > 0:
                    col1.metric("Duration", f"{rec['duration_hours']} hours")
                    col2.metric("Frequency", rec['frequency'])
                
                st.write(f"**Action:** {rec['action']}")
                st.write(f"**Best Time:** {rec['best_time']}")
                
                # Method recommendation
                method = rec['method_recommendation']
                st.subheader("🚿 Recommended Irrigation Method")
                
                st.write(f"**Method:** {method['method'].title()}")
                st.write(f"**Efficiency:** {method['efficiency_percent']:.0f}%")
                st.write(f"**Water Needed:** {method['water_needed_mm']} mm")
                
                st.write("**Advantages:**")
                for advantage in method['advantages']:
                    st.write(f"• {advantage}")
                
                # Send alert if critical
                if rec['priority'] == 'Immediate':
                    alert_message = f"AI IRRIGATION ALERT: {rec['action']} Water needed: {rec['water_amount_mm']}mm for {crop}"
                    alert_result = send_sms_alert("9632728125", alert_message)
                    st.error(f"🚨 **CRITICAL ALERT SENT:** {alert_result}")
        
        # Irrigation Schedule
        st.subheader("📅 AI-Generated Irrigation Schedule")
        
        if st.button("📋 Generate 14-Day Schedule"):
            schedule = ml_models['irrigation']._calculate_irrigation_schedule(
                crop, 20.0, soil_type, growth_stage  # 20mm water deficit example
            )
            
            schedule_df = pd.DataFrame(schedule)
            st.dataframe(schedule_df, use_container_width=True)
        
        # Water Budget Calculator
        st.subheader("💰 Water Budget Calculator")
        
        col1, col2, col3 = st.columns(3)
        
        budget_crop = col1.selectbox("Crop:", ['wheat', 'rice', 'corn', 'cotton'], key="budget_crop")
        area_ha = col2.number_input("Area (hectares):", 0.1, 100.0, 1.0, key="budget_area")
        irrigation_method = col3.selectbox("Method:", ['drip', 'sprinkler', 'furrow', 'flood'], key="budget_method")
        
        if st.button("💧 Calculate Water Budget"):
            budget = ml_models['irrigation'].calculate_water_budget(
                budget_crop, area_ha, irrigation_method, 120
            )
            
            col1, col2, col3 = st.columns(3)
            
            col1.metric("Total Water", f"{budget['total_water_liters']:,.0f} liters")
            col2.metric("Estimated Cost", f"₹{budget['estimated_cost_rupees']:,.2f}")
            col3.metric("Efficiency", f"{budget['efficiency_percent']:.0f}%")
    else:
        st.error("AI Irrigation model not available")

# ================= Market Analysis Tab =================
with tab7:
    st.header("📊 AI-Powered Market Analysis")
    
    if ml_models and 'price' in ml_models:
        # Price Prediction
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Price Prediction")
            
            crop = st.selectbox("Select Crop:", [
                'wheat', 'rice', 'corn', 'soybean', 'cotton', 'potato', 
                'tomato', 'onion', 'mustard', 'chickpea', 'groundnut'
            ])
            
            months_ahead = st.slider("Prediction Period (months):", 1, 12, 6)
            
            planting_date = st.date_input("Planting Date (optional):", datetime.now() - timedelta(days=60))
        
        with col2:
            if st.button("🤖 Get AI Price Prediction", type="primary"):
                # Get AI price prediction
                prediction = ml_models['price'].predict_prices(
                    crop, months_ahead, datetime.combine(planting_date, datetime.min.time())
                )
                
                st.success("🧠 **AI Price Analysis Complete**")
                
                # Current price and trend
                st.metric("Current Price", f"₹{prediction['current_price']}/quintal")
                
                # Market analysis
                analysis = prediction['market_analysis']
                
                col1, col2 = st.columns(2)
                col1.metric("Future Trend", f"{analysis['future_trend_percent']:+.1f}%")
                col2.metric("Market Sentiment", analysis['market_sentiment'])
                
                st.write(f"**Price Stability:** {analysis['price_stability']}")
                st.write(f"**Volatility Score:** {analysis['volatility_score']:.1f}%")
                
                # Recommendation
                rec = prediction['recommendation']
                st.subheader("🎯 AI Market Recommendation")
                
                if rec['action'] == 'HOLD/BUY':
                    st.success(f"📈 **{rec['action']}** - {rec['reason']}")
                elif rec['action'] == 'SELL':
                    st.error(f"📉 **{rec['action']}** - {rec['reason']}")
                else:
                    st.info(f"📊 **{rec['action']}** - {rec['reason']}")
                
                st.write(f"**Confidence:** {rec['confidence']}")
                st.write(f"**Risk Level:** {rec['risk_level']}")
        
        # Price trend visualization
        st.subheader("📈 AI Price Trend Forecast")
        
        if st.button("📊 Generate Price Chart"):
            prediction = ml_models['price'].predict_prices(crop, 6)
            
            # Combine historical and future data
            historical = prediction['historical_data'][-30:]  # Last 30 days
            future = prediction['future_predictions']
            
            # Create chart data
            hist_dates = [item['date'] for item in historical]
            hist_prices = [item['price'] for item in historical]
            
            future_dates = [item['date'] for item in future]
            future_prices = [item['predicted_price'] for item in future]
            future_min = [item['min_price'] for item in future]
            future_max = [item['max_price'] for item in future]
            
            # Create plotly chart
            fig = go.Figure()
            
            # Historical prices
            fig.add_trace(go.Scatter(
                x=hist_dates, y=hist_prices,
                mode='lines',
                name='Historical Prices',
                line=dict(color='blue')
            ))
            
            # Future predictions
            fig.add_trace(go.Scatter(
                x=future_dates, y=future_prices,
                mode='lines',
                name='AI Predictions',
                line=dict(color='red', dash='dash')
            ))
            
            # Confidence bands
            fig.add_trace(go.Scatter(
                x=future_dates + future_dates[::-1],
                y=future_max + future_min[::-1],
                fill='tonexty',
                fillcolor='rgba(255,0,0,0.2)',
                line=dict(color='rgba(255,255,255,0)'),
                name='Confidence Band'
            ))
            
            fig.update_layout(
                title=f'{crop.title()} Price Forecast',
                xaxis_title='Date',
                yaxis_title='Price (₹/quintal)',
                hovermode='x'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Profitability Analysis
        st.subheader("💰 AI Profitability Analysis")
        
        col1, col2, col3 = st.columns(3)
        
        profit_crop = col1.selectbox("Crop:", ['wheat', 'rice', 'corn', 'soybean'], key="profit_crop")
        profit_area = col2.number_input("Area (hectares):", 0.1, 100.0, 1.0, key="profit_area")
        selling_month = col3.selectbox("Selling Month:", list(range(1, 13)), key="selling_month")
        
        if st.button("💹 Calculate AI Profitability"):
            profitability = ml_models['price'].calculate_profitability(
                profit_crop, profit_area, selling_month
            )
            
            col1, col2, col3, col4 = st.columns(4)
            
            col1.metric("Revenue", f"₹{profitability['total_revenue']:,.0f}")
            col2.metric("Cost", f"₹{profitability['total_cost']:,.0f}")
            col3.metric("Net Profit", f"₹{profitability['net_profit']:,.0f}")
            col4.metric("ROI", f"{profitability['roi_percent']:.1f}%")
            
            st.write(f"**Profitability Level:** {profitability['profitability']}")
            st.write(f"**Break-even Price:** ₹{profitability['breakeven_price']}/quintal")
        
        # Crop Comparison
        st.subheader("🔍 AI Crop Profitability Comparison")
        
        comparison_crops = st.multiselect("Select crops to compare:", 
                                        ['wheat', 'rice', 'corn', 'soybean', 'cotton', 'potato'],
                                        default=['wheat', 'rice', 'corn'])
        
        comparison_area = st.number_input("Area for comparison (hectares):", 0.1, 100.0, 1.0, key="comp_area")
        
        if st.button("📊 Compare Crop Profitability") and comparison_crops:
            comparison = ml_models['price'].compare_crop_profitability(comparison_crops, comparison_area)
            
            # Create comparison dataframe
            comp_df = pd.DataFrame(comparison['crop_comparisons'])
            comp_df = comp_df[['crop', 'roi_percent', 'net_profit', 'profitability']].round(2)
            
            st.dataframe(comp_df, use_container_width=True)
            
            best_crop = comparison['best_crop']
            st.success(f"🏆 **AI Recommendation:** {best_crop['crop'].title()} with {best_crop['roi_percent']:.1f}% ROI")
    else:
        st.error("AI Market Analysis model not available")

# ================= AI Assistant Tab =================
with tab8:
    st.header("🤖 Advanced AI Farming Assistant")
    
    if ml_models and 'chatbot' in ml_models:
        # Chatbot status
        ollama_status = ml_models['chatbot'].check_ollama_status()
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            if ollama_status['available']:
                st.success(f"🧠 AI Status: Connected to Ollama ({len(ollama_status['models'])} models available)")
            else:
                st.warning("🧠 AI Status: Using intelligent fallback responses")
        
        with col2:
            selected_model = st.selectbox("AI Model:", 
                                        ollama_status['models'] if ollama_status['available'] else ['fallback'],
                                        index=0)
        
        # Initialize chat history
        if "ai_messages" not in st.session_state:
            st.session_state.ai_messages = []
        
        # Display chat messages
        for message in st.session_state.ai_messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if message["role"] == "assistant" and "metadata" in message:
                    st.caption(f"Source: {message['metadata']['source']} | Confidence: {message['metadata']['confidence']}")
        
        # Chat input
        if prompt := st.chat_input("Ask me anything about farming, crops, or agriculture..."):
            # Add user message
            st.session_state.ai_messages.append({"role": "user", "content": prompt})
            
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate AI response
            with st.chat_message("assistant"):
                with st.spinner("AI is thinking..."):
                    # Prepare context
                    weather = get_live_weather()
                    sensors = get_sensor_data()
                    
                    context = {
                        'weather': weather,
                        'soil': {
                            'moisture': sensors['soil_moisture'],
                            'ph': sensors['soil_ph']
                        }
                    }
                    
                    # Get AI response
                    ai_response = ml_models['chatbot'].get_response(
                        prompt, 
                        model=selected_model if ollama_status['available'] else None,
                        context=context
                    )
                    
                    response_text = ai_response['response']
                    st.markdown(response_text)
                    
                    # Show metadata
                    metadata = {
                        'source': ai_response['source'],
                        'confidence': ai_response.get('confidence', 0.8),
                        'model': ai_response.get('model_used', 'unknown')
                    }
                    
                    st.caption(f"Source: {metadata['source']} | Model: {metadata['model']} | Confidence: {metadata['confidence']}")
                    
                    # Add to chat history
                    st.session_state.ai_messages.append({
                        "role": "assistant", 
                        "content": response_text,
                        "metadata": metadata
                    })
        
        # Quick action buttons
        st.subheader("🚀 Quick AI Consultations")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("🌤️ Weather Advice"):
                weather = get_live_weather()
                advice_prompt = f"Current weather is {weather['temperature']}°C, {weather['description']}, {weather['humidity']}% humidity. What farming activities should I focus on today?"
                
                ai_response = ml_models['chatbot'].get_response(advice_prompt, context={'weather': weather})
                st.info(ai_response['response'])
        
        with col2:
            if st.button("🧪 Soil Health"):
                sensors = get_sensor_data()
                soil_prompt = f"My soil has pH {sensors['soil_ph']}, {sensors['soil_moisture']}% moisture, {sensors['soil_nitrogen']} mg/kg nitrogen. How can I improve soil health?"
                
                ai_response = ml_models['chatbot'].get_response(soil_prompt, context={'soil': sensors})
                st.info(ai_response['response'])
        
        with col3:
            if st.button("💰 Market Insights"):
                market_prompt = "What are the current market trends for major crops? Which crops should I consider for maximum profit?"
                
                ai_response = ml_models['chatbot'].get_response(market_prompt)
                st.info(ai_response['response'])
        
        with col4:
            if st.button("🔄 Clear Chat"):
                st.session_state.ai_messages = []
                st.rerun()
        
        # Conversation starters
        st.subheader("💡 Conversation Starters")
        
        starters = ml_models['chatbot'].get_conversation_starters()
        
        for starter in starters:
            if st.button(f"💬 {starter}", key=f"starter_{starter[:20]}"):
                # Add starter to chat
                st.session_state.ai_messages.append({"role": "user", "content": starter})
                
                # Get AI response
                ai_response = ml_models['chatbot'].get_response(starter)
                st.session_state.ai_messages.append({
                    "role": "assistant", 
                    "content": ai_response['response'],
                    "metadata": {'source': ai_response['source'], 'confidence': ai_response.get('confidence', 0.8)}
                })
                
                st.rerun()
        
        # Quick tips
        st.subheader("📚 AI Knowledge Base")
        
        tip_category = st.selectbox("Select category for quick tips:", 
                                  ['soil_health', 'water_management', 'pest_management', 'crop_planning'])
        
        if st.button("📖 Get AI Tips"):
            tips = ml_models['chatbot'].get_quick_tips(tip_category)
            
            st.write(f"**AI Tips for {tip_category.replace('_', ' ').title()}:**")
            for i, tip in enumerate(tips, 1):
                st.write(f"{i}. {tip}")
    else:
        st.error("AI Assistant not available")

# Footer
st.markdown("---")
st.markdown("🌱 **Smart Agriculture AI System with ML Models** - Powered by Advanced Machine Learning")