import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup as bs
from requests import get
import matplotlib.pyplot as plt
import numpy as np
import os




st.markdown("<h1 style='text-align: center; color: black;'>MY BEST DATA APP</h1>", unsafe_allow_html=True)

st.markdown("""
This app performs webscraping of data from dakar-auto over multiples pages. And we can also
download scraped data from the app directly without scraping them.
* **Python libraries:**  pandas, streamlit, requests, bs4,os,matplotlib.pyplot,numpy
* **Data source:[Dakar-Auto](https://dakar-auto.com/senegal/voitures-4)** 


""")




@st.cache_data

def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


def load(dataframe, titre, key, key1) :
    # Créer 3 colonnes avec celle du milieu plus large
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button(titre, key1):
            st.subheader('Display data dimension')
            st.write('Data dimension: ' + str(dataframe.shape[0]) + ' rows and ' + str(dataframe.shape[1]) + ' columns.')
            st.dataframe(dataframe)

            csv = convert_df(dataframe)

            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name='Data.csv',
                mime='text/csv',
                key=key)


def charger_donnees(nom_fichier):
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path,'voitures_scooters_locations', nom_fichier)
    return pd.read_excel(file_path)

def charger_donnees_csv(nom_fichier):
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path,'voitures_scooters_locations', nom_fichier)
    return pd.read_csv(file_path)




def load_vehicles_data(multi_page):
    df=pd.DataFrame()
    for index in range(1,int(multi_page)+1):
        url1=f'https://dakar-auto.com/senegal/voitures-4?&page={index}'
        res=get(url1)
        soup=bs(res.content,'html.parser')
        containers=soup.find_all('div','listing-card__content__inner')
        data=[]
        for container in containers:
                url_container='https://dakar-auto.com'+container.find('a')['href']
                res_container=get(url_container)
                soup_container=bs(res_container.content,'html.parser')
                try:
                    info=soup_container.find('h1','listing-item__title').text.split()
                    marque=" ".join(info[0:-2])
                    annee=info[-2]
                    prix=soup_container.find('h4','listing-item__price font-weight-bold text-uppercase mb-2').text.split()
                    prix_FCFA="".join(prix[0:-2])
                    info_g=soup_container.find('span','listing-item__address-location').text.split()
                    adresse=" ".join(info_g)
                    info_g2=soup_container.find('ul','listing-item__attribute-list list-inline').text.split()
                    kilometrage_km=info_g2[0]
                    boite_vit=info_g2[-2]
                    carburant=info_g2[-1]
                    proprietaire=soup_container.find('h4','listing-item-sidebar__author-name').text.strip()
                    dict={"marque":marque,"annee":annee,
                            "prix_FCFA":prix_FCFA,"adresse":adresse,
                            "kilometrage_km":kilometrage_km,"boite_vit":boite_vit,
                            "boite_vit":boite_vit,"carburant":carburant,
                            "proprietaire":proprietaire}
                    data.append(dict)

                except:
                    pass
        DF=pd.DataFrame(data)
        df=pd.concat([df,DF],axis=0).reset_index(drop=True)
    return df   

def load_scooters_data(multi_page):
    df=pd.DataFrame()
    for index in range(1,int(multi_page)+1):
        url2=f'https://dakar-auto.com/senegal/motos-and-scooters-3?&page={index}'
        res=get(url2)
        soup=bs(res.content,'html.parser')
        containers=soup.find_all('div','listings-cards__list-item mb-md-3 mb-3')
        data=[]
        for container in containers:
            url_container='https://dakar-auto.com'+container.find('a')['href']
            res_container=get(url_container)
            soup_container=bs(res_container.content,'html.parser')
            try:
                info=soup_container.find('h1','listing-item__title').text.split()
                marque=" ".join(info[0:-2])
                annee=info[-2]
                prix=soup_container.find('h4','listing-item__price font-weight-bold text-uppercase mb-2').text.split()
                prix_FCFA=int("".join(prix[0:-2]))
                adres=soup_container.find('span','listing-item__address-location').text.split()
                adresse=" ".join(adres)
                info_g=soup_container.find('ul','listing-item__attribute-list list-inline').text.split()
                kilometrage_km=info_g[0]
                proprietaire=soup_container.find('h4','listing-item-sidebar__author-name').text.strip()
                dict={"marque":marque,"annee":annee,
                    "prix_FCFA":prix_FCFA,"adresse":adresse,
                    "kilometrage_km":kilometrage_km,"proprietaire":proprietaire}
                data.append(dict)
            except:
                pass
        DF=pd.DataFrame(data)
        df=pd.concat([df,DF],axis=0).reset_index(drop=True)
    return df   

def load_location_voiture_data(multi_page):
    df=pd.DataFrame()
    for index in range(1,int(multi_page)+1):
        url3= f'https://dakar-auto.com/senegal/location-de-voitures-19?&page={index}'
        res=get(url3)
        soup=bs(res.content,'html.parser')
        containers=soup.find_all('div','listing-card__content__inner')
        data=[]
        for container in containers:
            url_container='https://dakar-auto.com'+container.find('a')['href']
            res_container=get(url_container)
            soup_container=bs(res_container.content,'html.parser')
            try:
                info=soup_container.find('h1','listing-item__title').text.split()
                marque=" ".join(info[0:-2])
                annee=info[-2]
                prix=soup_container.find('h4','listing-item__price font-weight-bold text-uppercase mb-2').text.split()
                prix_FCFA="".join(prix[0:-2])
                adresse_info=soup_container.find('span','listing-item__address-location').text.split()
                adresse=" ".join(adresse_info[0:len(adresse_info)])
                proprietaire=soup_container.find('h4','listing-item-sidebar__author-name').text.strip()
                dict={"marque":marque,"annee":annee,"prix_FCFA":prix_FCFA,
                    "adresse":adresse,"proprietaire":proprietaire}
                data.append(dict)
            except:
                pass
        DF=pd.DataFrame(data)
        df=pd.concat([df,DF],axis=0).reset_index(drop=True)
    return df
st.sidebar.header('User Input Features')
Pages = st.sidebar.selectbox('Pages indexes', list([int(p) for p in np.arange(2, 600)]))
Choices = st.sidebar.selectbox('Options', ['Scrape data using beautifulSoup', 'Download scraped data', 'Dashbord of the data', 'Evaluate the App'])





if Choices=='Scrape data using beautifulSoup':

    Vehicles_data_mul_pag = load_vehicles_data(Pages)
    scooters_data_mul_pag = load_scooters_data(Pages)
    location_voiture_mul_pag=load_location_voiture_data(Pages)
    
    load(Vehicles_data_mul_pag, 'Vehicles data', '1', '101')
    load(scooters_data_mul_pag, 'scooters data', '2', '102')
    load(location_voiture_mul_pag,'location data','3','103')
elif Choices == 'Download scraped data': 
    Vehicles = charger_donnees('URL1_DAKAR_AUTO.xlsx')
    scooters_data = charger_donnees('url2_motos_scooters.xlsx')
    locations_voitures = charger_donnees('locations_voitures.xlsx')
    load(Vehicles, 'Vehicles data', '1', '101')
    load(scooters_data, 'scooters data', '2', '102')
    load(locations_voitures,'location data','3','103')

elif  Choices == 'Dashbord of the data': 
    df1 = charger_donnees_csv('URL1_CLEAN1_DAKAR_AUTO.csv.csv')
    df2 = charger_donnees_csv('url2_clean2_motos_scooters.csv')
    df3=charger_donnees_csv('locations_clean1_voitures.csv')
    col1,col2,col3= st.columns(3)

    with col1: 
        top_5_prix = df1.groupby('marque')['prix_FCFA'].max().sort_values(ascending=False)[:5]
        plot1 = plt.figure(figsize=(11,7))
        color_price = (0.8, 0.2, 0.2, 0.6) 
        plt.barh(top_5_prix.index, top_5_prix.values, color=color_price)
        plt.title('Top 5 marques les plus cheres voitures de l\'url1')
        plt.xlabel('Prix Max')
        plt.ylabel('Marques')
        st.pyplot(plot1)
    with col2:
        top_5_prix = df2.groupby('marque')['prix'].max().sort_values(ascending=False)[:5]
        plot2 = plt.figure(figsize=(11,7))
        color_price = (0.8, 0.2, 0.2, 0.6) 
        plt.barh(top_5_prix.index, top_5_prix.values, color=color_price)
        plt.title('Top 5  marques les plus chères motos-scooters de l\'url2')
        plt.xlabel('prix max')
        plt.ylabel('Marques')
        st.pyplot(plot2)
    with col3:
        top_5_prix = df3.groupby('marque')['prix'].max().sort_values(ascending=False)[:5]
        plot3 = plt.figure(figsize=(11,7))
        color_price = (0.8, 0.2, 0.2, 0.6) 
        plt.barh(top_5_prix.index, top_5_prix.values, color=color_price)
        plt.title('Top 5 marques les plus cheres locations-voitures de l\'url3')
        plt.xlabel('Prix max')
        plt.ylabel('Marques')
        st.pyplot(plot3)

   







 











