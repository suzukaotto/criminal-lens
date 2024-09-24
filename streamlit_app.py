import streamlit as st
import requests

st.set_page_config(
    page_title="CriminalLens",
    page_icon=":eyeglasses:",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title(":eyeglasses: CriminalLens")

st.sidebar.header(":eyeglasses: Welcome to CriminalLens")
sel_menu = st.sidebar.radio("Select menu", ["How to use", "Search", "Regi Criminal", "About"])

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
    submit_url = "http://localhost/search"

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
                response = requests.post(submit_url, timeout=10, files={'image': criminal_image})
                
                if response.status_code == 200:
                    st.success("You have Searching. Thank you!")
                else:
                    st.error("Failed to find.")
            except Exception as e:
                st.error(f"Search failed. Are you connected to the Internet?")
            

elif sel_menu == "Regi Criminal":
    submit_url = "http://localhost/regi"

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
                response = requests.post(submit_url, timeout=10, data={'name': criminal_name, 'desc': criminal_desc}, files={'image': criminal_image})
                
                if response.status_code == 200:
                    st.success("You have registered. Thank you!")
                else:
                    st.error("Registration failed.")
            except Exception as e:
                st.error(f"Registration failed. Are you connected to the Internet?")
            

elif sel_menu == "About":
    st.header("About")
    st.write("CriminalLens is a project that helps you to search for criminals.")
    st.write("Are you curious? [Visit the site below](https://sites.google.com/view/teamtteokbokki)")
    st.write("")
    st.write("")
    st.write("")
    st.write("Rate flan: [View](https://sites.google.com/view/teamtteokbokki/finance-%EC%9E%AC%EB%AC%B4?authuser=0)")
    st.write("")
    st.write("")
    st.write("")
    st.write("This project is developed by Team tteokbokki.")
    st.write("Are you curious about the source code? This is our [GitHub](https://github.com/brainai-tteokbokki)")