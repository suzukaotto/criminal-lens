import base64
import json
import os
import requests
import streamlit as st
from dotenv import load_dotenv
import src.utils as utils
load_dotenv()

SERVER_URL = os.getenv("SERVER_URL")
AUTH_KEY = os.getenv("AUTH_KEY")
TEMP_DIR = os.path.join(os.getcwd(), "src", "temp_dir")
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

st.set_page_config(
    page_title="CriminalLens",
    page_icon=":eyeglasses:",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title(":eyeglasses: CriminalLens")

st.sidebar.header(":eyeglasses: Welcome to CriminalLens")
sel_menu = st.sidebar.radio("Select menu", ["How to use", "View criminals", "Search Criminal", "Regi Criminal", "Del Criminal", "Rate Plan", "About"])

# How to use
if sel_menu == "How to use":
    st.header("How to use?")
    st.write("1. Click on [ View criminals ] in the sidebar to view the list of criminals registered.")
    st.write("2. Click on [ Search Criminal ] in the sidebar to search for a criminal.")
    st.write("3. Click on [ Regi Criminal ] in the sidebar to register a criminal.")
    st.write("4. Click on [ Del Criminal ] in the sidebar to delete a criminal.")
    st.write("5. Click on [ Rate Plan ] in the sidebar to view the rate plan.")
    st.write("6. Click on [ About ] in the sidebar to know more about the project.")
    st.write("")
    st.write(":eyeglasses: Find the criminal!")

# View criminals
elif sel_menu == "View criminals":
    submit_url = f"{SERVER_URL}/api/list"
    
    st.header("View criminals")
    try:
        st.warning("Loading list of criminals...")
        
        res = requests.get(submit_url, data={"authKey": AUTH_KEY}, timeout=10)
        res_json = res.json()
        
        if res_json.get('error', True):
            st.error(f"Loading failed: {res_json.get('detail', 'Unknown error')}")
        else:
            st.success(f"Loading successful: {res_json.get('detail', 'Unknown result')}")
            
            res_json = res_json['data']
            if res_json == []:
                st.write("No criminals registered.")
            
            else:
                crimi_layout_cell = []
                for i in range((len(res_json) + 2) // 3):
                    crimi_layout_cell.append(st.columns(3))

                crimi_layout_cell = [col for row in crimi_layout_cell for col in row]

                for index, criminal in enumerate(res_json):
                    crimi_layout_cell[index].write(f"Name: {criminal['crimi_name']}")
                    crimi_layout_cell[index].write(f"Desc: {criminal['crimi_desc']}")
                    if criminal.get('crimi_face', None) != None:
                        try:
                            with open(os.path.join(TEMP_DIR, 'view_temp.jpg'), 'wb') as f:
                                f.write(base64.b64decode(criminal['crimi_face'][0]))
                            crimi_layout_cell[index].image(os.path.join(TEMP_DIR, 'view_temp.jpg'), use_column_width=True)
                            os.remove(os.path.join(TEMP_DIR, 'view_temp.jpg'))
                        except:
                            if os.path.exists(os.path.join(TEMP_DIR, 'view_temp.jpg')):
                                os.remove(os.path.join(TEMP_DIR, 'view_temp.jpg'))
                            crimi_layout_cell[index].write("Error loading image")
                    else:
                        crimi_layout_cell[index].write("No image")
                    
                    crimi_layout_cell[index].write(f"RegiTime: {criminal['regi_time']}")
                    crimi_layout_cell[index].write(f"RegiUser: {criminal['regi_user']}")
                    
                    crimi_layout_cell[index].write("")
                    crimi_layout_cell[index].write("")
                    crimi_layout_cell[index].write("")
        
    except Exception as e:
        st.error("Failed to load criminals. Are you connected to the Internet?")

# Search Criminal
elif sel_menu == "Search Criminal":
    submit_url = f"{SERVER_URL}/api/search"
    
    st.header("Search Criminal")
    
    upload_type = st.radio("Select upload type", ["Upload image", "Take a picture"])

    criminal_image = None
    if upload_type == "Upload image":
        criminal_image = st.file_uploader("Criminal image")
    else:
        picture = st.camera_input("Take a picture")
        if picture:
            st.image(picture)
            criminal_image = picture

    st.write("Uploaded photos will be deleted immediately after processing.")
    submit_button = st.button(label='Search')
    
    if submit_button:
        if criminal_image == None:
            st.error("Please upload or take a picture of the criminal.")
        else:
            st.warning("Searching...")
            
            try:
                res = requests.post(submit_url, data={'authKey': AUTH_KEY}, files={"crimi_face": criminal_image}, timeout=10)
                res_json = res.json()
                
                if res_json.get("error", True):
                    st.error(f"Search failed: {res_json.get("detail", "Unknown error")}")
                else:
                    st.success(f"Search successful: {res_json.get("detail", "Unknown result")}")
                    
                    similar_layout_cell = []
                    for i in range((len(res_json["similar_info"]) + 2 + 3) // 3):
                        similar_layout_cell.append(st.columns(3))
                    similar_layout_cell = [col for row in similar_layout_cell for col in row]
                    
                    suspect_layout_cell = []
                    for i in range((len(res_json["suspect_info"]) + 2 + 3) // 3):
                        suspect_layout_cell.append(st.columns(3))
                    suspect_layout_cell = [col for row in suspect_layout_cell for col in row]
                    
                    similar_layout_cell[0].header("Similar")
                    for index, simil_crimi in enumerate(res_json["similar_info"]):
                        similar_layout_cell[index+3].write(f"Name: {simil_crimi['crimi_name']}")
                        similar_layout_cell[index+3].write(f"Desc: {simil_crimi['crimi_desc']}")
                        if simil_crimi.get('crimi_face', None) != None:
                            with open(os.path.join(TEMP_DIR, 'search_temp.jpg'), 'wb') as f:
                                f.write(base64.b64decode(simil_crimi['crimi_face']))
                            similar_layout_cell[index+3].image(os.path.join(TEMP_DIR, 'search_temp.jpg'), use_column_width=True)
                            os.remove(os.path.join(TEMP_DIR, 'search_temp.jpg'))
                        else:
                            similar_layout_cell[index+3].write("No image")
                        similar_layout_cell[index+3].write("")
                    
                    suspect_layout_cell[0].header("Suspect")
                    for index, sus_crimi in enumerate(res_json["suspect_info"]):
                        suspect_layout_cell[index+3].write(f"Name: {sus_crimi['crimi_name']}")
                        suspect_layout_cell[index+3].write(f"Desc: {sus_crimi['crimi_desc']}")
                        if sus_crimi.get('crimi_face', None) != None:
                            with open(os.path.join(TEMP_DIR, 'search_temp.jpg'), 'wb') as f:
                                f.write(base64.b64decode(sus_crimi['crimi_face']))
                            suspect_layout_cell[index+3].image(os.path.join(TEMP_DIR, 'search_temp.jpg'), use_column_width=True)
                            os.remove(os.path.join(TEMP_DIR, 'search_temp.jpg'))
                        else:
                            suspect_layout_cell[index+3].write("No image")
                        suspect_layout_cell[index+3].write("")
                
            except Exception as e:
                st.error(f"Search failed. Are you connected to the Internet?: {e}")
            
# Regi Criminal
elif sel_menu == "Regi Criminal":
    submit_url = f"{SERVER_URL}/api/regi"
    
    st.header("Registration Criminal")
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
    
    agree_ckbox = st.checkbox("The information you upload will be stored on the server for processing purposes only. The information you upload may be shared. Do not upload sensitive information. Your IP will be recorded when you register. We will not assume any legal responsibility. If you understand all of the above, please check the box next to it.")

    submit_button = st.button(label='Register')
    
    if submit_button:
        if not criminal_name:
            st.error("Please enter the criminal name.")
        elif not criminal_desc:
            st.error("Please enter the criminal desc.")
        elif criminal_image == None:
            st.error("Please upload or take a picture of the criminal.")
        elif not agree_ckbox:
            st.error("Please agree to the terms.")
        else:
            st.warning("Registering...")
            
            try:
                req_data = {
                    'authKey'    : AUTH_KEY,
                    'crimi_name' : criminal_name,
                    'crimi_desc' : criminal_desc,
                    'is_agree'   : agree_ckbox,
                    'regi_time'  : utils.get_now_ftime()
                }
                req_file = {
                    'crimi_face': criminal_image
                }
                
                res = requests.post(submit_url, data=req_data, files=req_file, timeout=10)
                res_json = res.json()
                
                if res_json.get('error', True):
                    st.error(f"Registration failed: {res_json.get('detail', 'Unknown error')}")
                else:
                    st.success(f"Registration successful: {res_json.get('detail', 'Unknown result')}")
                    
            except Exception as e:
                st.error(f"Registration failed. Are you connected to the Internet?")

# Del Criminal
elif sel_menu == "Del Criminal":
    submit_url = f"{SERVER_URL}/api/del"
    
    st.header("Delete Criminal")
    criminal_name = st.text_input("Criminal name")
    st.write("When you click the Delete button, all data of the criminal registered under the entered name will be deleted from the server. The deleted criminal will no longer be processed on the server.")

    submit_button = st.button(label='Delete')
    
    if submit_button:
        if not criminal_name:
            st.error("Please enter the criminal name.")
        else:
            st.warning("Deleting...")
            
            try:
                req_data = {
                    'authKey'    : AUTH_KEY,
                    'crimi_name' : criminal_name
                }
                
                res = requests.post(submit_url, data=req_data, timeout=10)
                res_json = res.json()
                
                if res_json.get('error', True):
                    st.error(f"Deletion failed: {res_json.get('detail', 'Unknown error')}")
                else:
                    st.success(f"Deletion successful: {res_json.get('detail', 'Unknown result')}")
                    
            except Exception as e:
                st.error(f"Deletion failed. Are you connected to the Internet?")

# Rate Plan
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

# About
elif sel_menu == "About":
    st.header("About")
    st.write("CriminalLens is a project that helps you to search for criminals.")
    st.write("Are you curious? [Visit the site below](https://sites.google.com/view/teamtteokbokki)")
    st.write("")
    st.write("Rate flan detail view: [View](https://sites.google.com/view/teamtteokbokki/finance-%EC%9E%AC%EB%AC%B4?authuser=0)")
    st.write("")
    st.write("This project is developed by Team tteokbokki.")
    st.write("Are you curious about the source code? This is our [GitHub](https://github.com/brainai-tteokbokki)")
    