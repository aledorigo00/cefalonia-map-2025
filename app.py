import streamlit as st
import geopandas as gpd
import pandas as pd

# Coordinate luoghi
df = pd.DataFrame({
    'nome': ["Spiaggia Lourdas", "Lourdata", "Melissani Cave", "Sami", "Myrtos Beach", "Skala Beach",
             "Monte Ainos", "Old Vlachata", "Cantina Robola", "Assos", "Xi Beach",
             "Monastero Agios Gerasimos", "Argostoli", "Poros", "Trapezaki Beach"],
    'categoria': ["Spiaggia", "Città", "Escursione", "Città", "Spiaggia", "Spiaggia",
                  "Escursione", "Escursione", "Escursione", "Città", "Spiaggia",
                  "Escursione", "Città", "Città", "Spiaggia"],
    'lat': [38.1118, 38.1147, 38.2573, 38.2520, 38.3423, 38.0744, 38.1489, 38.1796,
            38.1748, 38.3773, 38.1697, 38.1649, 38.1732, 38.1484, 38.1236],
    'lon': [20.6403, 20.6403, 20.6235, 20.6474, 20.5350, 20.7980, 20.6664, 20.6370,
            20.5969, 20.5380, 20.4177, 20.5929, 20.4890, 20.7693, 20.6109]
})

st.title("🌍 Mappa dei punti di interesse a Cefalonia")

# Mostra mappa interattiva
st.map(df, latitude='lat', longitude='lon', zoom=10)

# Tabella punti di interesse
st.write("### 📍 Elenco completo punti di interesse")
st.dataframe(df)
