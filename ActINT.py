#MARTHA DELIA LÓPEZ FIGUEROA
#A01369970


import pandas as pd
import plotly.express as px
import streamlit as st
import folium
from streamlit_folium import st_folium, folium_static

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/

st.set_page_config(
    page_title='Departamento de Policía',
    page_icon='bar_chart',
    layout='wide'
)

df = pd.read_csv("c:/Users/MARTHA LOPEZ/Documents/Analitica/Integral/ActividadIntegral.csv")
#df.dropna(inplace=True)
st.dataframe(df)

# ---SIDEBAR---

st.sidebar.header("Please Filter Here:")

police_district = st.sidebar.multiselect(
    "Select the Police District:",
    options=df["Police District"].unique(),
    default=df["Police District"].unique()
)

incident_category = st.sidebar.multiselect(
    "Select the Incident Category:",
    options=df["Incident Category"].unique(),
    default=df["Incident Category"].unique()
)

incident_subcategory = st.sidebar.multiselect(
    "Select the Incident Subcategory:",
    options=df["Incident Subcategory"].unique(),
    default=df["Incident Subcategory"].unique()
)

resolution = st.sidebar.multiselect(
    "Select the Resolution:",
    options=df["Resolution"].unique(),
    default=df["Resolution"].unique()
)

incident_year = st.sidebar.multiselect(
    "Select the Incident Year:",
    options=df["Incident Year"].unique(),
    default=df["Incident Year"].unique()
)


df_selection = df.loc[
    df["Police District"].isin(police_district) &
    df["Incident Category"].isin(incident_category) &
    df["Incident Subcategory"].isin(incident_subcategory) &
    df["Resolution"].isin(resolution) &
    df["Incident Year"].isin(incident_year)
]

st.dataframe(df_selection)

# ---- MAINPAGE ----
st.title(":bar_chart: Departamento de Policía")
st.markdown("##")

# TOP KPI's

if not df_selection.empty:
    IC = df_selection['Incident Category'].mode().iloc[0]
    ISub = df_selection['Incident Subcategory'].mode().iloc[0]
    AN = df_selection['Analysis Neighborhood'].mode().iloc[0]
    SD = df_selection['Supervisor District'].mode().iloc[0]

    st.subheader('Incident Category:')
    st.subheader(f'Mode: {IC}')

    st.subheader('Incident Subcategory:')
    st.subheader(f'Mode: {ISub}')

    st.subheader('Analysis Neighborhood:')
    st.subheader(f'Mode: {AN}')

    st.subheader('Supervisor District:')
    st.subheader(f'Mode: {SD}')
else:
    st.subheader('No data available for the selected filters')

st.markdown('---')


#INCIDENTES POR DISTRITO
incident_pd= df_selection['Police District'].value_counts().sort_index()

fig_district_incident = px.bar(
    incident_pd,
    x=incident_pd.values,
    y=incident_pd.index,
    orientation='h',
    title='<b>Incident Cases by Police District</b>',
    color_discrete_sequence=['#0083B8'] * len(incident_pd),
    template='plotly_white',
)

fig_district_incident.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(showgrid=False),
)


#INCIDENTES POR DÍA
fig_day_incident = px.bar(
    df_selection['Incident Day of Week'].value_counts(),
    orientation='h',
    title='<b>Incident Cases by Day of Week</b>',
    color_discrete_sequence=['#0083B8'],
    template='plotly_white'
)

fig_day_incident.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(showgrid=False)
)


#INCIDENTES POR AÑO
fig_year_indicent = px.bar(
    df_selection['Incident Year'].value_counts(),
    orientation='h',
    title='<b>Incident Cases by Year</b>',
    color_discrete_sequence=['#0083B8'],
    template='plotly_white'
)

fig_year_indicent.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(showgrid=False)
)

#GRAFICARRRRRR
col1, col2 = st.columns(2)
col1.plotly_chart(fig_day_incident, use_container_width=True)
col1.plotly_chart(fig_year_indicent, use_container_width=True)
col2.plotly_chart(fig_district_incident, use_container_width=True)

#MAPA INTERACTIVO
df_selection.dropna(subset=['Latitude', 'Longitude'], inplace=True)


#TARDA DEMASIADOOOOO, PROBABLEMENTE TIENE ALGÚN ERROR QUE NO SUPE SOLUCIONAR:(
# Crear mapa
m = folium.Map(location=[df_selection['Latitude'].iloc[0], df_selection['Longitude'].iloc[0]], zoom_start=10)

# Marcadores en el mapa
for _, row in df_selection.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        #popup=row['name'],
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

# Mostrar el mapa en Streamlit
st_folium(m)
