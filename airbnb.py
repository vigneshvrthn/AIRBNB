import pandas as pd
import numpy as np
import pymongo
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from streamlit_option_menu import option_menu
st.set_page_config(page_title="AirBnb-Analysis", page_icon=":bar_chart:", layout="wide")

st.title(":bar_chart:   AirBnb-Analysis")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
select_fun=option_menu("Menu",["Home","Explore","Contact"],icons=["house", "bar-chart", "at"],
    default_index=2,
    orientation="horizontal",
    styles={"container": {"padding": "0!important", "background-color": "white", "size": "cover", "width": "100"},
            "icon": {"color": "black", "font-size": "20px"},

            "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px", "--hover-color": "#6F36AD"},
            "nav-link-selected": {"background-color": "#6F36AD"}})




if select_fun=="Home":
    st.header('Airbnb Analysis')
    st.subheader("Airbnb is an American San Francisco-based company operating an online marketplace for short- and long-term homestays and experiences. The company acts as a broker and charges a commission from each booking. The company was founded in 2008 by Brian Chesky, Nathan Blecharczyk, and Joe Gebbia. Airbnb is a shortened version of its original name, AirBedandBreakfast.com. The company is credited with revolutionizing the tourism industry, while also having been the subject of intense criticism by residents of tourism hotspot cities like Barcelona and Venice for enabling an unaffordable increase in home rents, and for a lack of regulation.")
    st.subheader('Skills take away From This Project:')
    st.subheader('Python Scripting, Data Preprocessing, Visualization, EDA, Streamlit, MongoDb, PowerBI')
    st.subheader('Domain:')
    st.subheader('Travel Industry, Property management and Tourism')
if select_fun=="Explore":
    df=pd.read_csv(r"C:\Users\krish\OneDrive\Desktop\project\phonepe\sample_airbnb.listingsAndReviews.csv")
    from statistics import mode
    df["review_scores.review_scores_value"]=df["review_scores.review_scores_value"].fillna(mode(df["review_scores.review_scores_value"]))

    for i in df.columns[1:]:
        if df[i].isna().sum()>=500:
            del(df[i])   

    for i in df.columns[1:]:
        if df[i].dtype=="object":
            df[i]=df[i].fillna("None")
        elif df[i].dtype=="int64" or df[i].dtype=="float64":
            df[i] = df[i].fillna(mode(df[i]))

    
        
    
    with st.sidebar:  
            country=st.multiselect("Select Country",df['address.country'].unique()) 
            accommodates=st.multiselect("Select accommodates",sorted(df["accommodates"].unique()))
            room_type=st.multiselect("Select room_type",df["room_type"].unique())
            review=st.selectbox("Select Review score",(df["review_scores.review_scores_value"].unique()))                
            property_type=st.multiselect("Select Property_Type",df["property_type"].unique())        
            price=st.number_input("enter the price below to search",step=100,value=200)
            sort_option = st.select_slider("Select one option for price", ["Low to High", "High to Low"])

    def coun (df,country):
        if country:
            out = df[df['address.country'].isin(country)]
            return(out)
        else:
            out=df
            return(out)
    
    out=coun(df,country)
    def room(out,room_type):
        if room_type:        
            out = out[out["room_type"].isin(room_type)]
            return(out)
        else:
            return(out) 
    out=room(out,room_type)
    def proper(out,property_type):
        if property_type:
            out=out[out["property_type"].isin(property_type)]
            return(out)
        else:
            return(out)
    out=proper(out,property_type)
    def acco(out,accommodates):
        if accommodates:
            out=out[out["accommodates"].isin(accommodates)]
            return(out)
        else:
            return(out)
    out=acco(out,accommodates)    
    def revi(out,review):
        if review:
            out = out[(out["review_scores.review_scores_value"]) == (review)]
            return(out)
        else:
            return(out)
    out=revi(out,review)
    def pr(out,price):
        if price:
            out=out[out["price"]<price] 
            return(out)    
        else:
            return(out)
    out=pr(out,price)
    def srt(out,sort_option):
        if sort_option=="Low to High":
            out=out.sort_values(by="price",ascending=True)
            return (out)
        elif sort_option=="High to Low":
            out=out.sort_values(by="price",ascending=False)
            return(out)
    out=srt(out,sort_option)
        
    out.index=range(1,len(out)+1)
    st.markdown("Drop down and see the detail report for the filter")
    with st.expander("Detail report for the selected filter option"):
        st.write(out.style.background_gradient(cmap="Oranges"))
        csv = out.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data", data=csv, file_name="detail_report_for_the_selected_filter.csv", mime="text/csv",
                           help='Click here to download the data as a CSV file')
    
    df=out[["room_type","price"]]
    df2 = out.groupby("room_type").size().reset_index(name='count')
    df2=(df2[["room_type", "count"]])
    fig1 = px.pie(df2, labels="room_type", values="count", hole=0.3, hover_data=["room_type"])
    fig2=px.scatter(out,x="room_type",y="price",color="room_type",hover_data=["room_type","price","name","address.government_area","address.market","address.country"])
    
    

    cols1 = st.columns([1, 1])
    with cols1[0]:
         st.write("HOTELS COUNT BY ROOM_TYTPE")
         st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False}, layout={'margin': {'l': 0, 'r': 0, 't': 0, 'b': 0}})
         st.markdown("Drop down and see the detail report for the filter")
         with st.expander("Detail report for the selected filter option"):
            st.write(df2.style.background_gradient(cmap="Oranges"))
    with cols1[1]:
        st.write("PRICE AND THE ADDRESS FOR THE HOTEL")
        st.plotly_chart(fig2)
        st.markdown("Drop down and see the detail report for the filter")
        with st.expander("Detail report for the selected filter option"):
            st.write(out[["name","room_type","price","address.government_area","address.market","address.country"]].style.background_gradient(cmap="Oranges"))
            csv = out[["name","room_type","price","address.government_area","address.market","address.country"]].to_csv(index=False).encode('utf-8')
            st.download_button("Download Data", data=csv, file_name="PRICE AND THE ADDRESS FOR THE HOTEL.csv", mime="text/csv",
                           help='Click here to download the data as a CSV file')
    mapdf =out
# Create a scatter plot with Plotly Express
    st.write("MAP FOR THE SELECTED FILTER")
    fig = px.scatter_mapbox(mapdf, lat='address.location.coordinates[1]', lon='address.location.coordinates[0]',hover_data=["name","property_type","room_type","price","images.picture_url","address.government_area","address.market","address.country","review_scores.review_scores_value"], zoom=0,width=900)

    # Update layout for better visualization
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig)
page_bg_img = '''
    <style>
    [data-testid=stAppViewContainer] {
        background-image: url("https://clipground.com/images/airbnb-logo-vector-6.png");
        background-size: 50% 50%; /* Cover the entire container */
        background-repeat: no-repeat; /* Ensure background image doesn't repeat */ background-position: center;/* Align the background image to the center */
    }
    </style>
    '''
st.markdown(page_bg_img, unsafe_allow_html=True)
col1, col2 = st.columns(2)

 # Load and display the image
with col1:
        image_url = "https://tse1.mm.bing.net/th?id=OIP.kWWXIRrdzHyfCHSjuD98MwHaEK&pid=Api&P=0&h=220"
        st.image(image_url, width=350)
        
with col2:
    col2.subheader("NAME : VIGNESH")
    col2.subheader("EMAIL: vigneshvrthn@gmail.com")
    col2.subheader("CONTACT : +919360776848")

        
        
    

