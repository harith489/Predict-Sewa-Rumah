import streamlit as st
import pickle 
import numpy as np


def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data = load_model()

dec_tree_reg = data["model"]
le_locations = data["le_locations"]
le_property = data["le_property"]
le_furnished = data["le_furnished"]

def clean_size(x):
    if x < 400:
        return 300
    else:
        for i in range(400,2500,50):
            if x >= i and x <= i+50:
                return i

def show_predict_page():
    st.title("Jangkaan Harga Sewa Rumah")

    st.write("""#### Jangkaan harga rumah ini memerlukan beberapa informasi berdasarkan ciri-ciri rumah yang anda impikan""")
    
    locations = (
        "Cheras",               
        "Kajang",                
        "Setapak",               
        "Shah Alam",            
        "Cyberjaya",             
        "Sentul",                
        "Puchong",               
        "Seri Kembangan",        
        "Kepong",                
        "Ampang",                
        "Bukit Jalil",           
        "Petaling Jaya",         
        "Klang",                 
        "Wangsa Maju",           
        "Taman Desa",            
        "Keramat",               
        "Setia Alam",            
        "Semenyih",              
        "Old Klang Road",        
        "KL City",               
        "Sepang",                
        "Subang Jaya",          
        "Mont Kiara",            
        "Damansara Perdana",     
        "KLCC",                  
        "Jalan Ipoh",            
        "Damansara Damai",       
        "Kuchai Lama",          
        "Bangi",                 
        "Batu Caves",            
        "Sungai Besi",           
        "Segambut",              
        "Desa Pandan",           
        "Jalan Kuching",        
        "Kota Damansara",        
    )

    properties = (
        "Condominium",
        "Apartment",
        "Service Residence",
    )

    furnishes = (
        "Fully Furnished",
        "Partially Furnished",
        "Not Furnished"
    )

    rooms = (1,2,3,4)

    location = st.selectbox("Lokasi",locations) #Choice of location
    property = st.selectbox("Jenis Bangunan", properties) #Choice of property
    room = st.selectbox("Bilangan Bilik", rooms) #Choice of room
    furnishes = st.selectbox("Furnishing", furnishes) #Choice of furnishing
    size = st.slider("Saiz Rumah", 0, 1500, 100) #Choice of size
    size = clean_size(size)
    ok = st.button("Kira Harga Sewa Rumah") #Button to predict 
    if ok:
        X = np.array([[location, property, room, size, furnishes]])
        X[:,0] = le_locations.transform(X[:,0])
        X[:,1] = le_property.transform(X[:,1])
        X[:, 4] = le_furnished.transform(X[:, 4])
        X = X.astype(float)

        Rent = dec_tree_reg.predict(X)
        st.subheader(f"Jangkaan harga rumah adalah RM{Rent[0]:.2f}")
