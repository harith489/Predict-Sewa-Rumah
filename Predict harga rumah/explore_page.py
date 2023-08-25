import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map

def clean_size(x):
    if x < 400:
        return 300
    else:
        for i in range(400,2500,50):
            if x >= i and x <= i+50:
                return i
        
def load_data():
    df = pd.read_csv('mudah-apartment-kl-selangor.csv')
    df = df[["monthly_rent", "location","property_type","rooms","size","furnished"]]
    df['monthly_rent'] = df['monthly_rent'].str.replace('\D', '', regex=True)
    df['location'] = df['location'].str.replace('Kuala Lumpur - ', '')
    df['location'] = df['location'].str.replace('Selangor - ', '')
    df['size'] = df['size'].str.replace('sq.ft.', '')
    df = df.astype({'monthly_rent':'float'})
    df= df.dropna()
    df = df.astype({'size':'float'})
    rooms_map = shorten_categories(df.rooms.value_counts(), 100)
    df['rooms'] = df['rooms'].map(rooms_map)
    df = df[df['rooms'] != 'Other']
    df = df.astype({'rooms':'float'})
    locations_map = shorten_categories(df.location.value_counts(), 150)
    df['location'] = df['location'].map(locations_map)
    df = df[df['location'] != 'Other']
    df = df[df["monthly_rent"] >= 100]
    df = df[df["monthly_rent"] <= 10000]
    property_map = shorten_categories(df.property_type.value_counts(), 500)
    df['property_type'] = df['property_type'].map(property_map)
    df = df[df['property_type'] != 'Other']
    df = df[df["size"] <= 2500]
    df = df[df['size'] >= 200]
    df['size'] = df['size'].apply(clean_size)
    df['rooms'] = df['rooms'].astype(int)
    df = df[df['size'] <= 1500]
    return df

df = load_data()

def show_explore_page():
    st.title("Explore House Rent")

    st.write(
        """
### Mudah Property Rent 2023
"""
    )

    #Create a barchart on mean house rent price based on location
    st.write("""### Mean House Rent Price Based on Location""")

    data = df.groupby(["location"])["monthly_rent"].mean().sort_values(ascending=True)
    st.bar_chart(data)

    #Create a barchart on mean house rent price based on property type
    st.write("""### Mean House Rent Price Based on property type""")

    data = df.groupby(["property_type"])["monthly_rent"].mean().sort_values(ascending=True)
    st.bar_chart(data)

    #Create a linechart based on number of room
    st.write("""### Mean House Rent based on no. room""")
    data = df.groupby(["rooms"])["monthly_rent"].mean().sort_values(ascending=True)
    st.line_chart(data)

    #Create a linechart based on size
    st.write("""### Mean House Rent based on house size per sq. ft""")
    data = df.groupby(["size"])["monthly_rent"].mean().sort_values(ascending=True)
    st.line_chart(data)