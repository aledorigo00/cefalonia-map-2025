import streamlit as st
import folium
import folium.plugins
import pandas as pd
from streamlit_folium import st_folium


# Force Streamlit to use full width
st.markdown("""
    <style>
    .st-emotion-cache-1w723zb {
        max-width: 100% !important;
    }
    </style>
    """, unsafe_allow_html=True)


# Data preparation
df = pd.DataFrame({
    'nome': ["Spiaggia Lourdas ", "Lourdata", "Melissani Cave", "Sami", "Myrtos Beach", "Skala Beach",
             "Monte Ainos", "Old Vlachata", "Cantina Robola", "Assos", "Xi Beach",
             "Monastero Agios Gerasimos", "Argostoli", "Poros", "Trapezaki Beach"],
    'categoria': ["Spiaggia", "Città", "Escursione", "Città", "Spiaggia", "Spiaggia",
                  "Escursione", "Escursione", "Escursione", "Città", "Spiaggia",
                  "Escursione", "Città", "Città", "Spiaggia"],
    'lat': [38.1118, 38.1147, 38.2573, 38.2520, 38.3423, 38.0744, 38.1489, 38.1796,
            38.1748, 38.3773, 38.1697, 38.1649, 38.1732, 38.1484, 38.1236],
    'lon': [20.6403, 20.6403, 20.6235, 20.6474, 20.5350, 20.7980, 20.6664, 20.6370,
            20.5969, 20.5380, 20.4177, 20.5929, 20.4890, 20.7693, 20.6109],
    'descrizione': [
        "Spiaggia famosa per le sue acque cristalline e la sabbia dorata.",
        "Piccolo villaggio con ristoranti tipici e vista sul mare.",
        "Grotta naturale con un lago sotterraneo visitabile in barca.",
        "Cittadina portuale con un vivace centro storico.",
        "Considerata la spiaggia più bella e fotografata di Cefalonia.",
        "Ampia spiaggia con servizi turistici.",
        "Montagna con sentieri escursionistici e vista panoramica.",
        "Villaggio antico abbandonato, luogo di escursione culturale.",
        "Cantina vinicola, perfetta per degustazioni.",
        "Suggestivo borgo costiero con castello veneziano.",
        "Famosa per la sua sabbia rossa e le scogliere bianche.",
        "Monastero storico, importante centro spirituale.",
        "Capoluogo dell'isola con negozi, ristoranti e vita notturna.",
        "Cittadina tranquilla con spiagge e atmosfera rilassante.",
        "Tranquilla spiaggia sabbiosa vicino a Vlachata."
    ]
})

# Color mapping based on category
color_map = {
    "Spiaggia": "red",
    "Escursione": "blue",
    "Città": "green"
}

st.title("🌍 Mappa interattiva di Cefalonia")

# Initialize Folium map
# m = folium.Map(location=[38.2, 20.6], zoom_start=10)

# Fullscreen Folium map
m = folium.Map(location=[38.2, 20.6], zoom_start=10)
folium.plugins.Fullscreen(position='topright', force_separate_button=False).add_to(m)


# Add markers
for idx, row in df.iterrows():
    folium.Marker(
        location=[row['lat'], row['lon']],
        popup=folium.Popup(f"<strong>{row['nome']}</strong><br>{row['descrizione']}", max_width=300),
        icon=folium.Icon(color=color_map[row['categoria']], icon='info-sign'),
    ).add_to(m)

# Render Folium map in Streamlit
st_folium(m, width='100%', height=700)

# Display DataFrame as additional reference
st.subheader("📍 Elenco completo punti di interesse")
st.dataframe(df[['nome', 'categoria', 'descrizione']])
