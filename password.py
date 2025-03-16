import streamlit as st
import random
import string
import gspread
from google.oauth2.service_account import Credentials
import pyperclip  # For copying to clipboard

# Google Sheets Setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = Credentials.from_service_account_file("C:/Users/saike/Downloads/soy-totem-452815-t2-085bc3f557c0.json", scopes=scope)
client = gspread.authorize(credentials)
spreadsheet = client.open("PasswordStorage")  # Change to your Google Sheet name
sheet = spreadsheet.sheet1  # Selecting the first sheet

# Password rules display
st.title("Secure Password Generator")
st.markdown("### Password Rules:")
st.markdown("""
- Must contain **uppercase** and **lowercase** letters  
- Must include **numbers** and **multiple symbols**  
- Should be **easy to read & remember**  
- No confusing characters (e.g., `O` vs `0`, `l` vs `1`)  
""")

# Function to validate custom password based on selected rules
def validate_password(password, rules):
    if len(password) < 10:
        return "❌ Password must be at least 10 characters long!"
    if rules["Uppercase"] and not any(c.isupper() for c in password):
        return "❌ Password must contain at least one uppercase letter!"
    if rules["Lowercase"] and not any(c.islower() for c in password):
        return "❌ Password must contain at least one lowercase letter!"
    if rules["Numbers"] and not any(c.isdigit() for c in password):
        return "❌ Password must contain at least one number!"
    if rules["Symbols"] and not any(c in "!@#$%^&*" for c in password):
        return "❌ Password must contain at least one special character (!@#$%^&*)!"
    return None

# Function to generate an easy-to-read password
def generate_easy_password(length=12):
    letters = string.ascii_letters.replace('l', '').replace('O', '').replace('I', '')
    numbers = "23456789"
    symbols = "!@#$%^&*"
    
    part1 = ''.join(random.choices(letters, k=4))
    part2 = ''.join(random.choices(symbols, k=2))
    part3 = ''.join(random.choices(numbers, k=4))
    part4 = ''.join(random.choices(letters, k=2))
    
    return f"{part1}{part2}{part3}{part4}"

# Initialize password variable
password = ""

# Get user input
password_type = st.radio("Choose Password Type:", ["Auto-Generated", "Custom Password"])
category = st.text_input("Enter the category (e.g., Instagram, Facebook, LinkedIn):")

if password_type == "Auto-Generated":
    password_length = st.slider("Select Password Length:", 10, 16, 12)
    if category:
        if st.button("🔄 Generate Password"):
            password = generate_easy_password(password_length)
            st.text_input("Generated Password:", value=password, key="password", disabled=True)
            pyperclip.copy(password)
            sheet.append_row([category, password])
            st.success(f"✅ Password for '{category}' saved & copied to clipboard!")
    else:
        st.warning("⚠️ Please enter a category before generating a password.")

elif password_type == "Custom Password":
    st.markdown("### Select Rules for Your Custom Password:")
    uppercase = st.checkbox("Must contain Uppercase Letters")
    lowercase = st.checkbox("Must contain Lowercase Letters")
    numbers = st.checkbox("Must contain Numbers")
    symbols = st.checkbox("Must contain Symbols")
    
    # Apply default rule (all rules enabled) if no checkboxes are selected
    if not any([uppercase, lowercase, numbers, symbols]):
        uppercase, lowercase, numbers, symbols = True, True, True, True
    
    selected_rules = {"Uppercase": uppercase, "Lowercase": lowercase, "Numbers": numbers, "Symbols": symbols}
    
    password = st.text_input("Enter Your Custom Password:", type="password")
    confirm_password = st.text_input("Confirm Your Password:", type="password")
    
    if password and confirm_password:
        if password != confirm_password:
            st.error("❌ Passwords do not match!")
        else:
            validation_error = validate_password(password, selected_rules)
            
            # ✅ Enforce user-selected rules strictly
            if validation_error:
                st.error(validation_error)
            else:
                # Enforce only allowed characters based on user selection
                if uppercase and not lowercase and not numbers and not symbols:
                    if not all(c.isupper() for c in password):
                        st.error("❌ Password must contain only uppercase letters!")
                        st.stop()
                if lowercase and not uppercase and not numbers and not symbols:
                    if not all(c.islower() for c in password):
                        st.error("❌ Password must contain only lowercase letters!")
                        st.stop()
                if numbers and not uppercase and not lowercase and not symbols:
                    if not all(c.isdigit() for c in password):
                        st.error("❌ Password must contain only numbers!")
                        st.stop()
                if symbols and not uppercase and not lowercase and not numbers:
                    if not all(c in "!@#$%^&*" for c in password):
                        st.error("❌ Password must contain only symbols!")
                        st.stop()

                if category and st.button("💾 Save Password"):
                    sheet.append_row([category, password])
                    st.success(f"✅ Custom Password for '{category}' saved!")

if password:
    if st.button("📋 Copy to Clipboard"):
        pyperclip.copy(password)
        st.success("📋 Password copied to clipboard!")

st.markdown("---")
st.text("Developed by Sai 🚀")