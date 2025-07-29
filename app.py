import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
from math import radians, sin, cos, sqrt, atan2
import folium.plugins

# style
st.markdown("""
    <style>
    /* Remove Streamlit default max-width constraint */
    .st-emotion-cache-1w723zb {
        max-width: 100% !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
    }

    /* Remove default page padding and margins for fullscreen map */
    .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
        margin: 0;
    }

    /* Title styling */
    h1 {
        font-size: 2em !important;
        text-align: center;
        margin: 0.2em 0;
    }

    /* Button styling */
    .nav-button {
        display: inline-block;
        background-color: #4CAF50;
        color: white;
        padding: 10px 16px;
        text-decoration: none;
        border-radius: 8px;
        font-size: 16px;
        font-weight: bold;
        margin-top: 8px;
    }
    .nav-button:hover { background-color: #45a049; }
    </style>
""", unsafe_allow_html=True)

places = [
    ("Spiaggia Lourdas", "Spiaggia", 38.1118, 20.6403,
     "Spiaggia famosa per le sue acque cristalline e la sabbia dorata."),
    ("Lourdata", "Città", 38.1147, 20.6403,
     "Piccolo villaggio con ristoranti tipici e vista sul mare."),
    ("Melissani Cave", "Escursione", 38.2573, 20.6235,
     "Grotta naturale con un lago sotterraneo visitabile in barca."),
    ("Sami", "Città", 38.2520, 20.6474,
     "Cittadina portuale con un vivace centro storico."),
    ("Myrtos Beach", "Spiaggia", 38.3423, 20.5350,
     "Considerata la spiaggia più bella e fotografata di Cefalonia."),
    ("Skala Beach", "Spiaggia", 38.0744, 20.7980,
     "Ampia spiaggia con servizi turistici."),
    ("Monte Ainos", "Escursione", 38.1489, 20.6664,
     "Montagna con sentieri escursionistici e vista panoramica."),
    ("Assos", "Città", 38.3773, 20.5380,
     "Suggestivo borgo costiero con castello veneziano."),
    ("Xi Beach", "Spiaggia", 38.1697, 20.4177,
     "Famosa per la sua sabbia rossa e le scogliere bianche."),
    ("Monastero Agios Gerasimos", "Escursione", 38.1649, 20.5929,
     "Monastero storico, importante centro spirituale."),
    ("Argostoli", "Città", 38.1732, 20.4890,
     "Capoluogo dell'isola con negozi, ristoranti e vita notturna."),
    ("Poros", "Città", 38.1484, 20.7693,
     "Cittadina tranquilla con spiagge e atmosfera rilassante."),
    ("Trapezaki Beach", "Spiaggia", 38.1236, 20.6109,
     "Tranquilla spiaggia sabbiosa vicino a Vlachata."),
    ("Fiskardo", "Città", 38.4571, 20.5763,
     "Borgo pittoresco con porto e case colorate, famoso per la sua architettura veneziana.")
]

df = pd.DataFrame(places, columns=["nome", "categoria", "lat", "lon", "descrizione"])
df["maps_link"] = df.apply(
    lambda row: f"https://www.google.com/maps/search/?api=1&query={row['lat']},{row['lon']}",
    axis=1
)

# ----------------------------
# DISTANCE FROM VLACHATA
# ----------------------------
VLACHATA_COORD = (38.1118, 20.6403)

def haversine(coord1, coord2):
    R = 6371
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1))*cos(radians(lat2))*sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return round(R * c, 1)

df["distanza_km"] = df.apply(lambda row: haversine(VLACHATA_COORD, (row["lat"], row["lon"])), axis=1)

itinerary_days = {
    "Giorno 1": ["Spiaggia Lourdas", "Lourdata"],
    "Giorno 2": ["Melissani Cave", "Sami"],
    "Giorno 3": ["Myrtos Beach", "Fiskardo", "Assos"],
    "Giorno 4": ["Argostoli"],
    "Giorno 5": ["Monastero Agios Gerasimos"],
    "Giorno 6": ["Monte Ainos", "Trapezaki Beach"],
    "Giorno 7": ["Spiaggia Lourdas"],
    "Giorno 8": ["Skala Beach", "Poros"],
    "Giorno 9": ["Argostoli"],
    "Giorno 10": ["Spiaggia Lourdas"]
}

# ----------------------------
# STYLING
# ----------------------------
st.markdown("""
    <style>
    .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
        margin: 0;
    }
    h1 {
        font-size: 2em !important;
        text-align: center;
        margin: 0.2em 0;
    }
    .nav-button {
        display: inline-block;
        background-color: #4CAF50;
        color: white;
        padding: 10px 16px;
        text-decoration: none;
        border-radius: 8px;
        font-size: 16px;
        font-weight: bold;
        margin-top: 8px;
    }
    .nav-button:hover { background-color: #45a049; }
    </style>
""", unsafe_allow_html=True)

# ----------------------------
# TITLE
# ----------------------------
st.title("Cefalonia 2025")

# ----------------------------
# SIDEBAR: SELECT DAY OR ALL
# ----------------------------
st.sidebar.header("Filtri")
day_options = ["Tutti i giorni"] + list(itinerary_days.keys())
selected_day = st.sidebar.selectbox("Mostra luoghi per:", day_options)

# Filter places based on selected day
if selected_day == "Tutti i giorni":
    filtered_places = df
else:
    day_places = itinerary_days[selected_day]
    filtered_places = df[df["nome"].isin(day_places)]

# ----------------------------
# FOLIUM MAP (FULL WIDTH & HEIGHT)
# ----------------------------
m = folium.Map(location=[38.2, 20.6], zoom_start=10, tiles="OpenStreetMap")
folium.plugins.Fullscreen(position='topright', force_separate_button=False).add_to(m)

color_map = {"Spiaggia": "red", "Escursione": "blue", "Città": "green"}

for _, row in filtered_places.iterrows():
    popup_html = f"""
    <strong>{row['nome']}</strong><br>
    Distanza: {row['distanza_km']} km<br>
    {row['descrizione']}<br><br>
    <a class="nav-button" href="{row['maps_link']}" target="_blank">Apri Google Maps</a>
    """
    folium.Marker(
        location=[row['lat'], row['lon']],
        popup=folium.Popup(popup_html, max_width=250),
        icon=folium.Icon(color=color_map[row['categoria']], icon='info-sign')
    ).add_to(m)

# Render map full width & large height
st_folium(m, width='100%', height=750)

# ----------------------------
# ITINERARY TABLE WITH LINKS
# ----------------------------
st.write("### Itinerario Giorno per Giorno")
for day, luoghi in itinerary_days.items():
    st.markdown(f"#### {day}")
    for luogo in luoghi:
        info = df[df["nome"] == luogo].iloc[0]
        st.markdown(f"- **{info['nome']}** ({info['categoria']}) – [Apri Google Maps]({info['maps_link']})")
    st.markdown("---")
