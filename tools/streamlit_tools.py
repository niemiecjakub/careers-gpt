import streamlit as st
from functools import wraps

DEFAULT_MESSAGE = "Loading..."

def spinner_async(message=DEFAULT_MESSAGE):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            placeholder = st.empty()
            placeholder.info(f"⏳ {message}")
            try:
                result = await func(*args, **kwargs)
            finally:
                placeholder.empty()
            return result
        return wrapper
    return decorator

def spinner(message=DEFAULT_MESSAGE):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            placeholder = st.empty()
            placeholder.info(f"⏳ {message}")
            try:
                result = func(*args, **kwargs)
            finally:
                placeholder.empty()
            return result
        return wrapper
    return decorator
