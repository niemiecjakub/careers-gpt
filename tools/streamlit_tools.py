import streamlit as st
from functools import wraps

def spinner_async(message="Loading..."):
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

import streamlit as st
from functools import wraps

def spinner(message="Loading..."):
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
