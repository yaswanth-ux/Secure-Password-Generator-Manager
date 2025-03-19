#Deloveped by YASWANTH
# 📌 Description:
# A web-based secure password generator and manager built using Python and Streamlit, enabling users to generate strong passwords and store them securely in Google Sheets. The system ensures compliance with customizable security rules and allows easy retrieval of saved passwords.

# 📌 Technologies & Modules Used:
# ✔ Python – Core logic & development
# ✔ Streamlit – Web-based UI for user interaction
# ✔ Google Sheets API (gspread) – Secure storage & retrieval of passwords
# ✔ Pyperclip – Clipboard functionality for easy password copying
# ✔ Random & String Modules – Strong password generation logic

# 📌 Key Features:
# ✅ Customizable Password Rules: Users can select uppercase, lowercase, numbers, and symbols to generate secure passwords.
# ✅ Real-Time Password Storage: Securely stores passwords in Google Sheets for future reference.
# ✅ Auto-Copy to Clipboard: Simplifies password usage by automatically copying generated passwords.
# ✅ Interactive UI: Developed with Streamlit for a user-friendly experience.



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

# Function to validate custom password
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

# Function to generate an easy-to-read and remember password
def generate_easy_password():
    # Ensure a pattern like: Xx@12345 (Easy to Read & Remember)
    uppercase = random.choice(string.ascii_uppercase)  # 1 Uppercase
    lowercase1 = random.choice(string.ascii_lowercase)  # 1 Lowercase
    lowercase2 = random.choice(string.ascii_lowercase)  # 1 Lowercase
    symbol = random.choice("!@#$%^&*")  # 1 Symbol
    numbers = "".join(random.choices(string.digits, k=5))  # 5 Digits

    password = uppercase + lowercase1 + symbol + lowercase2 + numbers
    return password

# Function to check if category already exists
def check_existing_category(category):
    records = sheet.get_all_records()
    for i, row in enumerate(records, start=2):  # Start from row 2 (row 1 has headers)
        if row['category'].lower() == category.lower():
            return i, row['password generated']  # Return row index and existing password
    return None, None

# User Input
password_type = st.radio("Choose Password Type:", ["Auto-Generated", "Custom Password"])
category = st.text_input("Enter the category (e.g., Instagram, Facebook, LinkedIn):")

if category:
    row_index, existing_password = check_existing_category(category)
    if existing_password:
        st.warning(f"⚠️ A password for '{category}' already exists! You can update it.")
        st.text_input("Existing Password:", value=existing_password, key="existing_password", disabled=True)
    
    if password_type == "Auto-Generated":
        if st.button("🔄 Generate Password"):
            password = generate_easy_password()
            st.text_input("Generated Password:", value=password, key="generated_password", disabled=True)
            pyperclip.copy(password)
            if row_index:
                sheet.update_cell(row_index, 2, password)
            else:
                sheet.append_row([category, password])
            st.success(f"✅ Password for '{category}' saved & copied to clipboard!")

    elif password_type == "Custom Password":
        st.markdown("### Select Rules for Your Custom Password:")
        uppercase = st.checkbox("Must contain Uppercase Letters")
        lowercase = st.checkbox("Must contain Lowercase Letters")
        numbers = st.checkbox("Must contain Numbers")
        symbols = st.checkbox("Must contain Symbols")
        
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
                if validation_error:
                    st.error(validation_error)
                else:
                    if st.button("💾 Save or Update Password"):
                        if row_index:
                            sheet.update_cell(row_index, 2, password)
                        else:
                            sheet.append_row([category, password])
                        st.success(f"✅ Password for '{category}' updated & saved!")
                        pyperclip.copy(password)

# Copy Button
if 'password' in locals() and password:
    if st.button("📋 Copy Password"):
        pyperclip.copy(password)
        st.success("✅ Password copied to clipboard!")

# Footer
st.markdown("---")
st.text("Developed by Yaswanth 🚀")
