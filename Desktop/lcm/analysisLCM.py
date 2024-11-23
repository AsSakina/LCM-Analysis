import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots
import streamlit as st

# Configuration de la page
st.set_page_config(page_title="Le Corpus Médical - Analyse", page_icon=":chart_with_upwards_trend:", layout="wide")

# Inclure le logo local
st.markdown("<h1 style='text-align: center; color: #46B3B3;'>Le Corpus Médical - Analyse</h1>", unsafe_allow_html=True)
st.image("/Users/user/Desktop/LCM-Analysis/LCM/logo/2.png", width=200)  # Chemin vers votre logo local



#Load Data 
data = pd.read_csv('LCM-Data.csv')

# Supposons que vos données sont déjà chargées dans `data`

# 1er graphique - Likes par Objectifs
fig1 = px.bar(data, x='Date', y='Likes', hover_data='Objectif', color='Likes', height=400, text_auto=True, title='Likes By Posts Objectives', barmode="overlay")
fig1.update_layout(
    barmode="group",  # Les barres seront affichées côte à côte
    title="Nombre de Likes Obtenus par Mois",
    font_family="Courier New",
    xaxis_title="Mois",
    yaxis_title="Reach",
    legend_title="Groupes",
)

# 2ème graphique - Account Reached par Mois
fig2 = px.bar(data, x='Date', y='Account Reached', hover_data='Objectif', color='Likes', labels={'Likes': 'Like'}, height=400, text_auto=True, title='Account Reached over Month', barmode="overlay")
fig2.update_layout(
    barmode="group",  # Les barres seront affichées côte à côte
    title="Nombre de Comptes Touchés par Mois",
    font_family="Courier New",
    xaxis_title="Mois",
    yaxis_title="Reach",
    legend_title="Groupes",
)

# 3ème graphique - Pourcentage de Followers et Non-Followers Touchés
fig3 = go.Figure()
fig3.add_trace(go.Bar(x=data["Date"], y=data["Followers "], name="Followers", marker_color='rgba(186, 85, 211, 0.7)'))
fig3.add_trace(go.Bar(x=data["Date"], y=data["Non-Followers"], name="Non-followers", marker_color='rgba(255, 99, 71, 0.7)'))
fig3.update_layout(
    barmode="group",  # Les barres seront affichées côte à côte
    title="Pourcentage de Followers et de Non-Followers Touchés",
    xaxis_title="Mois",
    yaxis_title="Reach",
    legend_title="Groupes",
    font_family="Courier New"
)

# Disposition des graphiques sur la même page
fig = make_subplots(
    rows=1, cols=3,
    subplot_titles=("Likes par Objectifs", "Account Reached par Mois", "Followers vs Non-Followers"),
)

# Ajouter les traces des graphiques à la disposition
fig.add_trace(fig1['data'][0], row=1, col=1)
#fig.add_trace(fig1['data'][1], row=1, col=1)
fig.add_trace(fig2['data'][0], row=1, col=2)
#fig.add_trace(fig2['data'][1], row=1, col=2)
fig.add_trace(fig3['data'][0], row=1, col=3)
#fig.add_trace(fig3['data'][1], row=1, col=3)

# Ajouter un logo à la mise en page
fig.update_layout(
    title_text="Analyse des Données sur les Mois",
    showlegend=True,
    plot_bgcolor="black",  # Le fond de la figure est maintenant noir
    font_family="Courier New",
    images=[
        dict(
            source="/Users/user/Desktop/LCM-Analysis/LCM/logo/2.png",  # Remplacez par le chemin de votre logo
            xref="paper", yref="paper",
            x=0.98, y=0.98,
            sizex=0.1, sizey=0.1,
            xanchor="right", yanchor="top"
        )
    ]
)

# Sauvegarder le fichier HTML avec analyse
html_content = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Analyse des Campagnes</title>
    <style>
        body { font-family: 'Arial', sans-serif; margin: 0; padding: 0; }
        h1 { text-align: center; color: #4A90E2; }
        .container { width: 80%; margin: auto; padding: 20px; }
        .section { margin: 40px 0; }
        .section h2 { color: #4A90E2; }
        .section p { font-size: 1.1em; color: #333; }
        .section ul { font-size: 1em; color: #555; }
        footer { text-align: center; padding: 20px; background-color: #f4f4f4; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Analyse des Campagnes : Graphiques et Insights</h1>

        <div class="section">
            <h2>1. Analyse des Objectifs de Campagne</h2>
            <p>
                Les campagnes ont différents objectifs : informer, sensibiliser, ou encourager des dons. 
                Certaines campagnes comme **"Don de sang"** visent à sensibiliser, tandis que des campagnes telles que **"Journée de Consultation Camp Penal"** ont un objectif d'informer et de collecter des dons. 
                En fonction de l'objectif, le niveau d'engagement (likes, commentaires) varie, tout comme l'impact en termes de **reach** (compte touché).
            </p>
        </div>

        <div class="section">
            <h2>2. Analyse de l'Audience Touchée (Followers vs Non-Followers)</h2>
            <p>
                Les campagnes ciblent souvent des **Followers** ou des **Non-Followers**. Par exemple, la campagne de **"Campagne de Tchicky"** du 21 août a touché principalement des **Followers** (86.3%), alors que la **"Journée de Consultation Camp Penal"** a ciblé 77.6% de **Non-Followers**. Les campagnes ayant un fort taux de reach parmi les **Non-Followers** peuvent être efficaces pour attirer un nouveau public.
            </p>
        </div>

        <div class="section">
            <h2>3. Analyse du Reach et de l'Engagement</h2>
            <p>
                Certaines campagnes, malgré un grand **reach** (ex : **"Don de sang"** du 29 octobre), n'ont pas généré autant d'engagement (likes, partages). Cela pourrait indiquer que le contenu est moins engageant ou que l'appel à l'action n'était pas assez fort. À l'inverse, des campagnes ciblant des audiences plus petites, comme **"Photos Consultations camps penal"**, ont eu un meilleur engagement par utilisateur.
            </p>
        </div>

        <div class="section">
            <h2>4. Impact de la Campagne sur l'Activité du Profil</h2>
            <p>
                L'impact des campagnes sur l'**activité du profil** (visites, abonnements) est également un indicateur clé. Certaines campagnes ont généré beaucoup de **PA-Visits** mais peu de **PA-Follows**, ce qui suggère une bonne visibilité sans conversion directe. D'autres campagnes ont montré une forte interaction avec des **clics externes** et **abonnements**.
            </p>
        </div>

        <div class="section">
            <h2>5. Corrélation entre Budget et Performance</h2>
            <p>
                Bien que certains budgets ne soient pas renseignés, il peut être intéressant de noter que des campagnes à faible budget (comme **"Don de sang"**) ont montré de bons résultats en termes de reach, tandis que d'autres campagnes nécessitant un budget plus important pourraient bénéficier d'une meilleure cible ou d'un contenu plus engageant.
            </p>
        </div>

        <footer>
            <p>&copy; 2024 Analyse des Campagnes | Tous droits réservés.</p>
        </footer>
    </div>
</body>
</html>
"""

# Sauvegarder la page HTML avec l'analyse
with open("analyse_campagnes_avec_graphiques.html", "w") as file:
    file.write(html_content)

# Afficher la figure dans le même fichier HTML
fig.write_html("analyse_campagnes_avec_graphiques.html", include_plotlyjs='cdn', full_html=False)

# Afficher la page HTML
fig.show()
