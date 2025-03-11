import streamlit as st
import random
import string
import re

st.set_page_config(page_title="Password Strength Meter", page_icon=":key:")

st.title("🔐 Password Strength Meter")
st.subheader("🛡️ Check the strength of your password")

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
    
    # Determine strength level with emojis
    if strength_percentage == 100:
        strength_text = "Very Strong 💪"
        color = "green"
    elif strength_percentage >= 80:
        strength_text = "Strong 👍"
        color = "blue"
    elif strength_percentage >= 60:
        strength_text = "Moderate 🤔"
        color = "orange"
    else:
        strength_text = "Weak ⚠️"
        color = "red"

    return strength_percentage, strength_text, color, suggestions

def generate_password(length,use_digits,use_special_chars):
    characters = string.ascii_letters
    if use_digits:
        characters += string.digits
    if use_special_chars:
        characters += string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

# Add custom CSS for styling
st.markdown("""
    <style>
    .stProgress > div > div > div > div {
        background-image: linear-gradient(to right, #ff0000, #ffa500, #2196f3, #4caf50);
    }
    </style>
""", unsafe_allow_html=True)

# Password input section with styling
st.markdown("### 🔑 Enter your password")
user_password = st.text_input("", type="password", placeholder="Type your password here")

if user_password:
    strength_percentage, strength_text, color, suggestions = check_password_strength(user_password)
    
    # Display strength meter with colored box
    st.markdown(f"""
        <div style='
            padding: 10px;
            border-radius: 5px;
            background-color: {"rgba(255, 0, 0, 0.1)" if color == "red" else "rgba(255, 165, 0, 0.1)" if color == "orange" else "rgba(33, 150, 243, 0.1)" if color == "blue" else "rgba(76, 175, 80, 0.1)"};
            border-left: 5px solid {color};
            margin: 10px 0;'>
            <h4 style='color: {color}; margin: 0;'>Password Strength: {strength_text}</h4>
        </div>
    """, unsafe_allow_html=True)
    
    st.progress(int(strength_percentage))
    
    # Display suggestions if any with improved styling
    if suggestions:
        st.warning("💡 Suggestions to improve password strength:")
        for suggestion in suggestions:
            st.markdown(f"• {suggestion}")
    elif strength_percentage == 100:
        st.success("🎉 Excellent! Your password meets all security requirements.")

# Password generator section
st.markdown("### ⚡ Generate a Strong Password")
col1, col2 = st.columns(2)
with col1:
    length = st.slider("🔢 Password Length", min_value=8, max_value=32, value=16)
with col2:
    use_digits = st.checkbox("🔢 Include Digits")
    use_special_chars = st.checkbox("#️⃣ Include Special Characters")

if st.button("🎲 Generate Password", type="primary"):
    password = generate_password(length, use_digits, use_special_chars)
    st.success(f"🎯 Generated Password: `{password}`")

# Add footer
st.markdown("---")
st.markdown("### 🔐 Keep your passwords safe and strong! 💪")
