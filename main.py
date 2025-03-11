import streamlit as st
import random
import string
import re

st.set_page_config(page_title="Password Strength Meter", page_icon=":key:")

st.title("Password Strength Meter")
st.subheader("Check the strength of your password")

def check_password_strength(password):
    suggestions = []
    strength = 0
    
    # Check length
    if len(password) < 8:
        suggestions.append("Password should be at least 8 characters long")
    elif len(password) > 32:
        suggestions.append("Password should not exceed 32 characters")
    else:
        strength += 1

    # Check uppercase
    if not re.search(r'[A-Z]', password):
        suggestions.append("Add at least one uppercase letter")
    else:
        strength += 1

    # Check lowercase
    if not re.search(r'[a-z]', password):
        suggestions.append("Add at least one lowercase letter")
    else:
        strength += 1

    # Check digits
    if not re.search(r'\d', password):
        suggestions.append("Add at least one number")
    else:
        strength += 1

    # Check special characters
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        suggestions.append("Add at least one special character")
    else:
        strength += 1

    # Calculate strength percentage
    strength_percentage = (strength / 5) * 100
    
    # Determine strength level
    if strength_percentage == 100:
        strength_text = "Very Strong"
        color = "green"
    elif strength_percentage >= 80:
        strength_text = "Strong"
        color = "blue"
    elif strength_percentage >= 60:
        strength_text = "Moderate"
        color = "orange"
    else:
        strength_text = "Weak"
        color = "red"

    return strength_percentage, strength_text, color, suggestions

def generate_password(length,use_digits,use_special_chars):
    characters = string.ascii_letters
    if use_digits:
        characters += string.digits
    if use_special_chars:
        characters += string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

# Add password input field
user_password = st.text_input("### Enter your password to check strength", type="password")

if user_password:
    strength_percentage, strength_text, color, suggestions = check_password_strength(user_password)
    
    # Display strength meter
    st.write(f"Password Strength: {strength_text}")
    st.progress(int(strength_percentage))
    
    # Display suggestions if any
    if suggestions:
        st.warning("Suggestions to improve password strength:")
        for suggestion in suggestions:
            st.write(f"• {suggestion}")
    elif strength_percentage == 100:
        st.success("Excellent! Your password meets all security requirements.")

st.markdown("### OR generate a password")
length = st.slider("Password Length", min_value=8, max_value=32, value=16)
use_digits = st.checkbox("Include Digits")
use_special_chars = st.checkbox("Include Special Characters")

if st.button("Generate Password"):
    password = generate_password(length, use_digits, use_special_chars)
    st.success(f"Generated Password: {password}")
