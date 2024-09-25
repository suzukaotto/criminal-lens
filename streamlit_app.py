import streamlit as st
import requests
from dotenv import load_dotenv
import os
load_dotenv()

SERVER_URL = os.getenv("SERVER_URL")
submit_url = f"{SERVER_URL}/api/search"
submit_url = f"{SERVER_URL}/api/regi"

st.set_page_config(
    page_title="CriminalLens",
    page_icon=":eyeglasses:",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title(":eyeglasses: CriminalLens")

st.sidebar.header(":eyeglasses: Welcome to CriminalLens")
sel_menu = st.sidebar.radio("Select menu", ["How to use", "Search", "Regi Criminal", "Rate Plan", "About"])

if sel_menu == "How to use":
    st.header("How to use?")
    st.write("1. Click on 'Search' in the sidebar to search for a criminal.")
    st.write("2. Click on 'Regi Criminal' in the sidebar to register a criminal.")
    st.write("3. Click on 'About' in the sidebar to know more about the project.")
    st.write(":eyeglasses: Find it!")
    st.write("")
    st.write("")
    st.write("")
    st.write("The feature is not implemented yet ...")

elif sel_menu == "Search":
    st.header("Search Criminal")
    
    upload_type = st.radio("Select upload type", ["Upload image", "Take a picture"])

    upload_type = None
    if upload_type == "Upload image":
        criminal_image = st.file_uploader("Criminal image")
    else:
        picture = st.camera_input("Take a picture")
        if picture:
            st.image(picture)
            criminal_image = picture

    submit_button = st.button(label='Search')
    
    if submit_button:
        if criminal_image == None:
            st.error("Please upload or take a picture of the criminal.")
        else:
            st.warning("Searching...")
            
            try:
                res = requests.post(submit_url, timeout=10, files={'image': criminal_image})
                res_content = res.json()
                
                if res_content.get('error', True):
                    st.error(f"Search failed: {res_content.get('detail', 'Unknown error')}")
                else:
                    print(res_content)
                    st.success(f"Search successful: {res_content.get('detail', 'Unknown result')}")
            except Exception as e:
                st.error(f"Search failed. Are you connected to the Internet?")
            

elif sel_menu == "Regi Criminal":
    st.header("Regi Criminal")
    
    criminal_name = st.text_input("Criminal name")
    criminal_desc = st.text_input("Criminal Desc")
    upload_type = st.radio("Select upload type", ["Upload image", "Take a picture"])

    criminal_image = None
    if upload_type == "Upload image":
        criminal_image = st.file_uploader("Criminal image")
    else:
        picture = st.camera_input("Take a picture")
        if picture:
            st.image(picture)
            criminal_image = picture

    submit_button = st.button(label='Register')
    
    if submit_button:
        if not criminal_name:
            st.error("Please enter the criminal name.")
        elif not criminal_desc:
            st.error("Please enter the criminal desc.")
        elif criminal_image == None:
            st.error("Please upload or take a picture of the criminal.")
        else:
            st.warning("Registering...")
            
            try:
                res = requests.post(submit_url, timeout=10, data={'name': criminal_name, 'desc': criminal_desc}, files={'image': criminal_image})
                
                if res.status_code == 200:
                    st.success("You have registered. Thank you!")
                else:
                    st.error("Registration failed.")
            except Exception as e:
                st.error(f"Registration failed. Are you connected to the Internet?")

elif sel_menu == "Rate Plan":
    st.header("Rate Plan")
    
    col1, col2, col3 = st.columns(3)
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    
    col1.header("Free Plan (Basic)")
    col1.write("Cost: $0")
    col1.write("Features: Limited to 30 facial scans per day, basic recognition with lower accuracy, ads included, and slower processing times.")
    if btn_col1.button("Free"):
        st.header("You are using the free tier. Thank you!")
    
    col2.header("Premium Plan (Individual)")
    col2.write("Monthly Subscription: $5.99/month")
    col2.write("Annual Subscription: $59.90/year (2 months free)")
    col2.write("Features: Unlimited facial scans, no ads, priority processing, high-accuracy recognition, historical data tracking (e.g., previously identified individuals), and alerts for matches.")
    if btn_col2.button("Subscribe now"):
        st.header("Thank you for signing up!")
    
    col3.header("Premium Plan (Business)")
    col3.write("Monthly Subscription: $2.99/user/month. (10 users or more)")
    col3.write("Features: Provides Premium Tier (Individual) features to all users")
    if btn_col3.button("Contact Us"):
        st.header("Please feel free to contact us for consultation.\nContact email: contact@tteokbokki.com")
    

elif sel_menu == "About":
    st.header("About")
    st.write("CriminalLens is a project that helps you to search for criminals.")
    st.write("Are you curious? [Visit the site below](https://sites.google.com/view/teamtteokbokki)")
    st.write("")
    st.write("Rate flan detail view: [View](https://sites.google.com/view/teamtteokbokki/finance-%EC%9E%AC%EB%AC%B4?authuser=0)")
    st.write("")
    st.write("This project is developed by Team tteokbokki.")
    st.write("Are you curious about the source code? This is our [GitHub](https://github.com/brainai-tteokbokki)")