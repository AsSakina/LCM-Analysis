import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd 
import numpy as np

# Configuration de la page
st.set_page_config(page_title="Le Corpus Médical - Analyse", page_icon=":chart_with_upwards_trend:", layout="wide")

# Inclure le logo local
st.markdown("<h1 style='text-align: center; color: #46B3B3;'>Le Corpus Médical - Analyse</h1>", unsafe_allow_html=True)
st.image("/Users/user/Desktop/LCM-Analysis/LCM/logo/2.png", width=200)  # Chemin vers votre logo local


data = pd.read_csv('LCM-Data.csv')

# Conversion des dates au format datetime et gestion des valeurs incorrectes
data["Date"] = pd.to_datetime(data["Date"], errors='coerce')  # 'coerce' convertira les erreurs en NaT (Not a Time)

# Vérification des valeurs NaT ou nulles
#df = data.dropna(subset=["Date"])  # Supprimer les lignes avec des dates incorrectes ou manquantes


# Définir les couleurs de la charte graphique
primary_color = '#376B6B'
background_color = '#274C67'
text_color = '#46B3B3'
secondary_background_color = '#38A4A4'
# Supposons que vous avez déjà chargé les données dans `data`

# Définir les couleurs de la charte graphique (exemples)
color_follower = 'rgb(90, 130, 235)'  # Bleu clair (à adapter à votre charte)
color_non_follower = 'rgb(235, 65, 54)'  # Rouge clair (à adapter à votre charte)

# 1er graphique - Likes par Objectifs
fig1 = px.bar(data, x='Date', y='Likes', hover_data='Objectif', color='Likes', height=400, text_auto=True, title='Likes By Posts Objectives', barmode="overlay")
fig1.update_traces(marker_color=color_follower)  # Appliquer la couleur pour ce graphique

fig1.update_layout(
    barmode="group",  # Les barres seront affichées côte à côte
    title="Nombre de Likes Obtenus par Mois",
    font_family="Courier New",
    xaxis_title="Mois",
    yaxis_title="Reach",
    legend_title="Groupes",
    plot_bgcolor='black',  # Changer le fond en noir
    paper_bgcolor='black',  # Changer le fond global en noir
    font_color='white'  # Changer la couleur de la police pour qu'elle soit lisible
)

# 2ème graphique - Account Reached par Mois
fig2 = px.bar(data, x='Date', y='Account Reached', hover_data='Objectif', color='Likes', labels={'Likes': 'Like'}, height=400, text_auto=True, title='Account Reached over Month', barmode="overlay")
fig2.update_traces(marker_color=color_non_follower)  # Appliquer une autre couleur pour ce graphique

fig2.update_layout(
    barmode="group",  # Les barres seront affichées côte à côte
    title="Nombre de Comptes Touchés par Mois",
    font_family="Courier New",
    xaxis_title="Mois",
    yaxis_title="Reach",
    legend_title="Groupes",
    plot_bgcolor='black',  # Changer le fond en noir
    paper_bgcolor='black',  # Changer le fond global en noir
    font_color='white'  # Changer la couleur de la police pour qu'elle soit lisible
)

# 3ème graphique - Pourcentage de Followers et Non-Followers Touchés
fig3 = go.Figure()
fig3.add_trace(go.Bar(x=data["Date"], y=data["Followers "], name="Followers", marker_color=color_follower))  # Utiliser la couleur des followers
fig3.add_trace(go.Bar(x=data["Date"], y=data["Non-Followers"], name="Non-followers", marker_color=color_non_follower))  # Utiliser la couleur des non-followers

fig3.update_layout(
    barmode="group",  # Les barres seront affichées côte à côte
    title="Pourcentage de Followers et de Non-Followers Touchés",
    xaxis_title="Mois",
    yaxis_title="Reach",
    legend_title="Groupes",
    font_family="Courier New",
    plot_bgcolor='black',  # Changer le fond en noir
    paper_bgcolor='black',  # Changer le fond global en noir
    font_color='white'  # Changer la couleur de la police pour qu'elle soit lisible
)

# Disposition des graphiques sur la même page
fig = make_subplots(
    rows=1, cols=3,
    subplot_titles=("Likes par Objectifs", "Account Reached par Mois", "Followers vs Non-Followers"),
)

# Ajouter les traces des graphiques à la disposition
for trace in fig1['data']:
    fig.add_trace(trace, row=1, col=1)

for trace in fig2['data']:
    fig.add_trace(trace, row=1, col=2)

for trace in fig3['data']:
    fig.add_trace(trace, row=1, col=3)

# Ajouter le texte et le logo
st.markdown("""
    <style>
        .title {
            text-align: center;
            color: #4A90E2;
            font-size: 30px;
        }
        .section {
            margin: 20px;
            color: white;
            font-size: 16px;
        }
        .section h2 {
            font-size: 24px;
            color: #4A90E2;
        }
        .section p {
            font-size: 18px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">Analyse des Campagnes</div>', unsafe_allow_html=True)

# Texte pour chaque section
st.markdown('<div class="section"><h2>1. Analyse des Objectifs de Campagne</h2><p>Les campagnes ont différents objectifs : informer, sensibiliser, ou encourager des dons. Certaines campagnes comme "Don de sang" visent à sensibiliser, tandis que des campagnes telles que **"Journée de Consultation Camp Penal"** ont un objectif d\'informer et de collecter des dons. En fonction de l\'objectif, le niveau d\'engagement (likes, commentaires) varie, tout comme l\'impact en termes de **reach** (compte touché).</p></div>', unsafe_allow_html=True)

st.markdown('<div class="section"><h2>2. Analyse de l\'Audience Touchée (Followers vs Non-Followers)</h2><p>Les campagnes ciblent souvent des **Followers** ou des **Non-Followers**. Par exemple, la campagne de **"Campagne de Tchicky"** du 21 août a touché principalement des **Followers** (86.3%), alors que la **"Journée de Consultation Camp Penal"** a ciblé 77.6% de **Non-Followers**. Les campagnes ayant un fort taux de reach parmi les **Non-Followers** peuvent être efficaces pour attirer un nouveau public.</p></div>', unsafe_allow_html=True)

st.markdown('<div class="section"><h2>3. Analyse du Reach et de l\'Engagement</h2><p>Certaines campagnes, malgré un grand **reach** (ex : **"Don de sang"** du 29 octobre), n\'ont pas généré autant d\'engagement (likes, partages). Cela pourrait indiquer que le contenu est moins engageant ou que l\'appel à l\'action n\'était pas assez fort. À l\'inverse, des campagnes ciblant des audiences plus petites, comme **"Photos Consultations camps penal"**, ont eu un meilleur engagement par utilisateur.</p></div>', unsafe_allow_html=True)

# Afficher la figure finale
st.plotly_chart(fig, use_container_width=True)
