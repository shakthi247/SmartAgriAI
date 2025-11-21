"""
Performance monitoring and optimization utilities
"""
import time
import functools
import streamlit as st
from typing import Any, Callable

def timer(func: Callable) -> Callable:
    """Decorator to measure function execution time"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        
        # Only show in debug mode
        if st.session_state.get('debug_mode', False):
            st.sidebar.text(f"{func.__name__}: {(end-start)*1000:.1f}ms")
        
        return result
    return wrapper

@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_static_data(data_type: str) -> dict:
    """Cache static agricultural data"""
    static_data = {
        'crop_prices': {
            "wheat": 2200, "rice": 2800, "corn": 1800, "soybean": 3800,
            "cotton": 6000, "sugarcane": 3200, "potato": 1200, "tomato": 1500
        },
        'typical_yields': {
            "wheat": 45, "rice": 40, "corn": 50, "soybean": 25,
            "cotton": 20, "sugarcane": 800, "potato": 250, "tomato": 300
        },
        'cultivation_costs': {
            "wheat": 35000, "rice": 45000, "corn": 38000, "soybean": 32000,
            "cotton": 55000, "sugarcane": 75000, "potato": 60000, "tomato": 65000
        }
    }
    return static_data.get(data_type, {})

def optimize_dataframe(df):
    """Optimize pandas DataFrame memory usage"""
    for col in df.select_dtypes(include=['float64']).columns:
        df[col] = df[col].astype('float32')
    
    for col in df.select_dtypes(include=['int64']).columns:
        df[col] = df[col].astype('int32')
    
    return df

class PerformanceMonitor:
    """Simple performance monitoring context manager"""
    
    def __init__(self, operation_name: str):
        self.operation_name = operation_name
        self.start_time = None
    
    def __enter__(self):
        self.start_time = time.perf_counter()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = time.perf_counter() - self.start_time
        if duration > 1.0:  # Only log slow operations
            st.warning(f"Slow operation: {self.operation_name} took {duration:.2f}s")

# Memory-efficient constants
SEASONS = ("winter", "summer", "monsoon")
MODELS = ("llama3", "llama2", "mistral", "codellama", "phi3")
MAIN_CROPS = ("wheat", "rice", "corn", "soybean", "cotton", "sugarcane")