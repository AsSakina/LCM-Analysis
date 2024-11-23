import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from io import BytesIO
import fpdf
from fpdf import FPDF
from fpdf import *
import plotly.figure_factory as ff

# Charger les données
data = pd.read_csv("LCM-Data.csv")  # Remplacez par votre fichier CSV

# Configuration de la page avec un fond sombre
st.set_page_config(
    page_title="Le Corpus Médical - Analyse",
    page_icon=":chart_with_upwards_trend:",
    layout="wide"
)

# Fonction pour générer un PDF
def generate_pdf():
    from fpdf import FPDF
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.set_text_color(55, 107, 107)  # Couleur primaire (en RGB)
    pdf.cell(200, 10, txt="Rapport d'Analyse - Le Corpus Médical", ln=True, align="C")
    pdf.ln(10)
    pdf.multi_cell(0, 10, "Ce document contient un résumé des analyses des données des campagnes.")
    pdf.ln(10)
    pdf.cell(200, 10, txt="Graphiques disponibles dans l'application.", ln=True, align="L")
    pdf_output = BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)
    return pdf_output

# Section du logo et du bouton PDF
st.markdown(
    """
    <style>
        .main {background-color: #274C67;} /* Couleur du fond principal */
        .reportview-container {color: #46B3B3;} /* Texte en couleur charte */
    </style>
    """, unsafe_allow_html=True
)



col1, col2 = st.columns([1, 4])
with col1:
    st.image("2.png", width=120)  # Chemin vers le logo local
with col2:
    st.markdown("<h1 style='color: #46B3B3;'>Le Corpus Médical - Analyse</h1>", unsafe_allow_html=True)
    pdf_file = generate_pdf()
    st.download_button(
        label="📄 Télécharger le Rapport PDF",
        data=pdf_file,
        file_name="Rapport_Analyse_LeCorpusMedical.pdf",
        mime="application/pdf"
    )


st.markdown('<hr style="border: 1px solid #46B3B3;">', unsafe_allow_html=True)


# Assurez-vous que les dates sont converties correctement
data['Date'] = pd.to_datetime(data['Date'], errors='coerce')  # Convertit les dates au format datetime


# Exemple de votre dataset
data = pd.DataFrame({
    'Type de campagne': ['Picnic', 'Journee de Consultation Camp Penal', 'Campagne de Tchicky', 
                         'Photos Consultations camps penal', 'Photos Campagne de Tchicky', 
                         'Affiche Dons Pouponnieres', 'Don de sang', 'Octobre Rose', 
                         'Octobre Rose', 'Don de sang', 'Don de sang'],
    'Date': ['2024-07-20', '2024-08-10', '2024-08-13', '2024-08-19', '2024-08-21', 
             '2024-09-16', '2024-09-25', '2024-10-08', '2024-10-19', '2024-10-29', '2024-11-08'],
    'Finish': ['2024-07-16', '2024-08-14', '2024-08-17', '2024-08-14', '2024-08-17', 
             '2024-09-28', '2024-09-25', '2024-10-08', '2024-10-20', '2024-11-09', '2024-11-09'],
    'Canal': ['Instagram/Facebook'] * 11,
    'Objectif': [None, 'Informer/Donation', 'Informer', 'Informer', 'Informer', 
                 'Informer/Donation', 'Sensibiliser', 'Informer', 'Informer', 'Informer', 'Sensibiliser'],
    'Likes': [161, 54, 21, 136, 183, 25, 32, 42, 19, 63, 47],
    'Commentaires': [2, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    'Partages': [9, 22, 1, 2, 1, 9, 14, 14, 1, 67, 6],
    'Save': [5, 0, 0, 1, 2, 0, 0, 0, 0, 2, 1],
    'Account Reached': [1677, 2225, 403, 1333, 852, 829, 1811, 1266, 2, 6023, 1369],
    'Followers ': [91.7, 22.4, 60.2, 52, 86.3, 88.5, 14, 26, 94.7, None, None],
    'Non-Followers': [8.3, 77.6, 39.8, 48, 13.7, 11.5, 86, 74, 5.3, None, None],
    'Profile Activity': [78, 56, 4, 14, 35, 5, 14, 16, 1, None, None],
    'PA-Visits': [72, 5, 3, 14, 30, 4, 14, 14, 1, None, None],
    'PA-Follows': [5, 1, 1, 0, 1, 0, 0, 2, 0, None, None],
    'PA-External Link Tap': [1, 0, 0, 0, 4, 1, None, 2, 0, None, None],
    'Observations': ['Followers ', "Le fait qu'on aie touche 77.6% de Non Followers. 22 Shares", None, 
                     "Plus cest des photos, plus on reach people", '185 Account Engaged/852Account Reached', 
                     'Non Followers ', 'Non Followers Reached', None, None, None, '1H45M2S'],
    'Budget': [None, None, None, None, None, None, None, None, None, None, None]
})

# Convertir la colonne 'Date' en datetime
data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d')
data['Finish'] = pd.to_datetime(data['Finish'], format='%Y-%m-%d')

# Ajouter la colonne 'Finish' en ajoutant 5 jours à la date de début
data['Finish'] = data['Date'] + pd.to_timedelta(5, unit='D')

# Convertir les dates en format 'YYYY-MM-DD' pour le Gantt
data['Date'] = data['Date'].dt.strftime('%Y-%m-%d')

# Créer une liste de dictionnaires pour le graphique Gantt
df_gantt = []

# Couleurs associées à chaque "Objectif"
colors = {
    'Informer': '#46B3B3',
    'Informer/Donation': '#274C67',
    'Sensibiliser': '#FF6347',  # Exemple de couleur différente pour "Sensibiliser"
    'Sans Objectif': '#FFD700'  # Couleur pour les campagnes sans objectif spécifié
}

for _, row in data.iterrows():
    df_gantt.append(dict(
        Task=row['Type de campagne'], 
        Start=row['Date'], 
        Finish=row['Finish'],
        Resource=row['Objectif'] if row['Objectif'] else 'Sans Objectif',
        Color=colors.get(row['Objectif'], colors['Sans Objectif'])  # Assigner la couleur basée sur l'Objectif
    ))

# Créer le graphique Gantt
fig = ff.create_gantt(df_gantt, show_colorbar=True, index_col='Resource', group_tasks=True)
# Personnalisation du layout : supprimer les backgrounds
fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',  # Aucun fond pour la zone du graphique
    paper_bgcolor='rgba(0,0,0,0)', # Aucun fond pour la zone extérieure
    font=dict(color='black'), # Couleur de la police
    xaxis=dict(showgrid=False), # Supprimer la grille sur l'axe X
    yaxis=dict(showgrid=False), # Supprimer la grille sur l'axe Y
    title='Timeline des Posts', # Titre
    title_font_size=20,
    title_font_color="#46B3B3",
    legend=dict(
        font=dict(color='#46B3B3'),  # Couleur du texte de la légende
        bordercolor='#46B3B3',  # Couleur de la bordure de la légende
        borderwidth=2,  # Largeur de la bordure de la légende
        bgcolor='rgba(0,0,0,0)'  # Fond transparent pour la légende
    )
)
# Afficher le graphique
st.plotly_chart(fig, use_container_width=True)




import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Graphique 1 : Nombre de Likes
fig1 = px.bar(
    data, x="Date", y="Likes",
    hover_data=["Objectif"], color="Likes",
    text_auto=True, title="Nombre de Likes par Mois",
    color_continuous_scale=["rgba(55, 107, 107, 0.7)", "rgba(70, 179, 179, 0.7)"]
)
fig1.update_layout(
    barmode="group", 
    title_font_color="#46B3B3", 
    paper_bgcolor="rgba(0,0,0,0)",  # Transparent
    plot_bgcolor="rgba(0,0,0,0)",  # Transparent
    font_color="#46B3B3",
    xaxis_title="Mois", 
    yaxis_title="Nombre de Likes",
    title_font_size=20
)

# Graphique 2 : Radar Chart pour les Likes par Campagne
campaigns = data['Type de campagne'].unique()
likes_per_campaign = [data[data['Type de campagne'] == campaign]['Likes'].sum() for campaign in campaigns]

fig2 = go.Figure()
fig2.add_trace(go.Scatterpolar(
    r=likes_per_campaign,
    theta=campaigns,
    fill='toself',
    name='Likes',
    marker=dict(color="#46B3B3")
))
fig2.update_layout(
    polar=dict(
        radialaxis=dict(visible=True, range=[0, max(likes_per_campaign)]),
    ),
    title="Nombre de Likes par Campagne",
    paper_bgcolor="rgba(0,0,0,0)",  # Transparent
    plot_bgcolor="rgba(0,0,0,0)",  # Transparent
    font_color="#46B3B3",
    title_font_color="#46B3B3",
    title_font_size=20
)

# Graphique 3 : Followers vs Non-Followers
fig3 = go.Figure()
fig3.add_trace(go.Bar(
    x=data["Date"], y=data["Followers "], name="Followers", marker_color="rgba(55, 107, 107, 0.7)"
))
fig3.add_trace(go.Bar(
    x=data["Date"], y=data["Non-Followers"], name="Non-Followers", marker_color="rgba(70, 179, 179, 0.7)"
))
fig3.update_layout(
    barmode="group", 
    title="Analyse du Reach et de l'Engagement: Followers vs Non-Followers",
    paper_bgcolor="rgba(0,0,0,0)",  # Transparent
    title_font_color="#46B3B3",
    plot_bgcolor="rgba(0,0,0,0)",  # Transparent
    font_color="#46B3B3", 
    xaxis_title="Mois", 
    yaxis_title="Reach",
    title_font_size=20
)

# Affichage des graphiques
st.markdown('<hr style="border: 1px solid #46B3B3;">', unsafe_allow_html=True)
st.plotly_chart(fig1, use_container_width=True)
st.markdown('<hr style="border: 1px solid #46B3B3;">', unsafe_allow_html=True)
st.plotly_chart(fig2, use_container_width=True)
st.markdown('<hr style="border: 1px solid #46B3B3;">', unsafe_allow_html=True)
st.plotly_chart(fig3, use_container_width=True)
st.markdown('<hr style="border: 1px solid #46B3B3;">', unsafe_allow_html=True)




# Texte explicatif avec couleur de fond secondaire
st.markdown(
    """
    <div style='background-color: #38A4A4; padding: 15px; border-radius: 5px;'>
    <h2 style='color: #46B3B3;'>Analyse des Données</h2>
    <p style='color: white;'>Voici une analyse détaillée des performances des campagnes menées par Le Corpus Médical. 
    Les graphiques ci-dessus illustrent les performances en termes de likes, reach, et engagement pour les followers et non-followers.</p>
    </div>
    """, unsafe_allow_html=True
)


# Texte explicatif avec couleur de fond secondaire et sections
st.markdown(
    """
    <style>
        .section {
            background-color: #38A4A4; /* Secondary background color */
            color: white; /* Text color */
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            font-family: 'Arial', sans-serif;
        }
        h2 {
            color: #46B3B3; /* Text color for headings */
        }
        p {
            color: white; /* Text color for paragraphs */
            line-height: 1.6;
        }
    </style>
    """, unsafe_allow_html=True
)

# Section 1: Analyse des Objectifs de Campagne
st.markdown(
    """
    <div class="section">
        <h2>1. Analyse des Objectifs de Campagne</h2>
        <p>
        Les campagnes ont différents objectifs : informer, sensibiliser, ou encourager des dons.
        Certaines campagnes comme celui du <strong>"Don de sang"</strong> visent à sensibiliser, tandis que 
        les posts des campagnes tels que <strong> ceux de la "Journée de Consultation du Camp Pénal"</strong> ont un objectif 
        d'informer et de collecter des dons. 
        En fonction de l'objectif, le niveau d'engagement 
        (likes, commentaires) varie, tout comme l'impact en termes de <strong>reach</strong> (comptes touchés).
        </p>
    </div>
    """, unsafe_allow_html=True
)

# Section 2: Analyse de l'Audience Touchée
st.markdown(
    """
    <div class="section">
        <h2>2. Analyse de l'Audience Touchée (Followers vs Non-Followers)</h2>
        <p>
        Les campagnes ciblent souvent des <strong>Followers</strong> ou des <strong>Non-Followers</strong>.
        Par exemple, la campagne de <strong>"Tchicky"</strong> du 21 août a touché principalement 
        des <strong>Followers</strong> (86.3%), alors que la <strong>"Journée de Consultation du Camp Penal"</strong> 
        a ciblé 77.6% de <strong>Non-Followers</strong>. Les types de campagnes ayant un fort taux de reach de 
        <strong>Non-Followers</strong> peuvent être efficaces pour attirer un nouveau public.
        </p>
    </div>
    """, unsafe_allow_html=True
)


# Section 3: Analyse du Reach et de l'Engagement
st.markdown(
    """
    <div class="section">
        <h2>3. Analyse du Reach et de l'Engagement</h2>
        <p>
        Certaines campagnes, malgré un grand <strong>reach</strong> (ex : <strong> Post "Don de sang"</strong> du 29 octobre), 
        n'ont pas généré autant d'engagement (likes, partages). Cela pourrait indiquer que le contenu est moins engageant 
        ou que l'appel à l'action n'était pas assez fort. À l'inverse, des campagnes ciblant des audiences plus petites, 
        comme <strong> les "Photos Consultations camps penal"</strong>, ont eu un meilleur engagement par utilisateur.
        </p>
    </div>
    """, unsafe_allow_html=True
)


# Styles pour appliquer les couleurs de la charte
st.markdown(
    """
    <style>
        .section {
            background-color: #274C67;
            color: #46B3B3;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        h2 {
            color: #38A4A4;
        }
        p {
            color: white;
        }
        strong {
            color: #38A4A4;
        }
    </style>
    """, unsafe_allow_html=True
)

st.markdown('<hr style="border: 1px solid #46B3B3;">', unsafe_allow_html=True)

# Section 1: Résumé comparatif
st.markdown(
    """
    <div class="section">
        <h2>1. Résumé Comparatif : Post Boosté vs. Non Boosté</h2>
        <p>
        <strong>Post Boosté (Janvier)</strong> :
        <ul>
            <li><strong>Reach</strong> : 8,051 comptes atteints, dont 7,774 grâce à la publicité.</li>
            <li><strong>Impressions</strong> : 17,675, dont 16,830 issues de l'annonce publicitaire.</li>
            <li><strong>Interactions</strong> : 115 interactions (91 likes, 10 partages, 14 sauvegardes).</li>
            <li><strong>Activité sur le profil</strong> : 189 visites de profil, avec 172 générées par l'annonce.</li>
            <li><strong>Coût par visite de profil</strong> : 0,08 € pour un budget total de 14 € sur 7 jours.</li>
            <li><strong>Audience géographique</strong> : Dakar (93.1%), Thiès (3.9%), Saint-Louis (1%)</li>
            <li><strong>Genre</strong> : Femmes (53.9%), Hommes (45.6%), Non Specifié (0.6%)</li>
            <li><strong>Tranche d'Âge</strong> : 18-24 ans (32.9%), 25-34 ans (50.9%), 35-44 ans (8.8%), 45-54 ans (1.4%), 55-64 ans (1.4%), 65+ ans (4.6%)</li>
        </ul>
        <strong>Posts Non Boostés (Moyennes générales)</strong> :
        <ul>
            <li><strong>Reach</strong> : Environ 1,500 à 2,000 comptes touchés.</li>
            <li><strong>Impressions</strong> : Généralement limitées à 1,500-3,000.</li>
            <li><strong>Interactions</strong> : Faibles, avec une moyenne de 30 à 50 likes.</li>
            <li><strong>Activité sur le profil</strong> : Moins de 50 visites en moyenne.</li>      
        </ul>
        </p>
        <p>
        Les posts boostés montrent une efficacité significative pour augmenter la visibilité et l'engagement,
        avec un coût raisonnable par interaction.
        </p>
    </div>
    """, unsafe_allow_html=True
)


# Section 2: Recommandations pour l'année à venir
st.markdown(
    """
    <div class="section">
        <h2>2. Recommandations pour l'Année à Venir</h2>
        <p>
        <strong>1. Allouer un budget stratégique pour les publicités</strong> : Booster les campagnes clés avec un budget moyen de 15-20 € (9791 - 13 100 Franc cfa ) par post pour maximiser le reach et l'engagement.
        </p>
        <p>
        <strong>2. Segmenter l'audience pour un impact optimal</strong> : Adapter les annonces selon les régions et centres d'intérêt afin d'améliorer la pertinence.
        </p>
        <p>
        <strong>3. Renforcer le storytelling</strong> : Partager des témoignages et des histoires visuelles pour capter l'attention des donateurs et membres potentiels.
        </p>
        <p>
        <strong>4. Collaboration avec des influenceurs locaux</strong> : Travailler avec des micro-influenceurs pour étendre le reach et renforcer la crédibilité.
        </p>
        
    </div>
    """, unsafe_allow_html=True
)

st.write("Le public ciblé pour la Location de Matériels Médicaux se compose majoritairement de femmes (53.9%), avec une forte concentration dans la tranche d'âge 25-34 ans (50.9%). Il faudra prévoir de relancer le post pour atteindre davantage de personnes de cette catégorie.")
st.markdown('<hr style="border: 1px solid #46B3B3;">', unsafe_allow_html=True)

# Titre de la page
st.markdown("<h1 style='color: #46B3B3;'>Téléchargement des Documents de la Commission Communication</h1>", unsafe_allow_html=True)

# Texte explicatif
#st.markdown(
    #"""
    #La Commission Communication de **Le Corpus Médical**:
    
    #- **Manuel de procédures** : Structurant les normes et lignes directrices de communication.
    #- **Organigramme** : Définissant les rôles et les responsabilités de chaque membre.
    #- **Document Descriptif des Rôles** : Clarifiant les missions de chaque poste (Président, Vice-président, Community Manager, Créateurs Visuels, etc.).
    #- **Document explicatif du processus de demande de publication**.
    #- **Modèle de demande de publication**.
    #- **Document de Marketing Humanitaire de la Stratégie Globale**.
    #- **Stratégie Marketing 2**.
    
    #Vous pouvez télécharger les documents ci-dessous.
    #"""
#)


# Créer des liens de téléchargement pour les PDF
pdf_documents = {
    "Organigramme": "COM_LCM_.pdf",
    "Stratégie Marketing": "LCMAnalysisStratégieMHumanLeCorpusMédical.pdf",
    "Manuel Procédures": "ManueldeProcédure.pdf",
    "Document Descriptif Rôles": "PostesàpourvoirCommissionCommunicationsLCMFeuille1.pdf",
    "Modèle Demande Publication": "DemandedePublication_LCM.pdf",
    "Marketing Humanitaire": "MarketingHumanitaire_LeCorpusMédical.pdf",
    "Demande Publication": "LCM-Analysis/GuidedeDemandedePublicationsurlesRéseaux.pdf",
}

# Ajouter du CSS personnalisé pour styliser le bouton
st.markdown(
    """
    <style>
    div.stButton > button {
        background-color: #46B3B3; /* Couleur d'arrière-plan */
        color: #FFFFFF; /* Couleur du texte */
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        font-family: 'Arial', sans-serif;
        font-weight: bold;
        cursor: pointer;
    }
    div.stButton > button:hover {
        background-color: #38A4A4; /* Couleur d'arrière-plan au survol */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sélection dans un menu déroulant
selected_doc = st.selectbox(
    "Sélectionnez un document à télécharger :",
    options=list(pdf_documents.keys()),
)

# Afficher le bouton de téléchargement
if selected_doc:
    file_path = pdf_documents[selected_doc]
    with open(file_path, "rb") as file:
        st.download_button(
            label="Télécharger",  # Bouton réduit à "Télécharger"
            data=file.read(),
            file_name=f"{selected_doc}.pdf",
            mime="application/pdf"
        )



# Appliquer le style global
st.markdown(
    """
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #274C67; /* Couleur de fond sombre */
            color: #FFFFFF; /* Texte en blanc */
        }
        .video-section {
            font-family: 'Courier New', monospace;
            text-align: center;
            padding: 20px;
            border: 1px solid #38A4A4;
            background-color: #376B6B;
            border-radius: 10px;
        }
        .download-btn {
            background-color: #46B3B3;
            color: #FFFFFF;
            font-weight: bold;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            text-align: center;
        }
        .download-btn:hover {
            background-color: #38A4A4;
            color: #376B6B;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# Texte explicatif avec style
st.markdown(
    """
    <div class="video-section">
        <h2> Contents Insights </h2>
        <p>
            Illustration des performances et des données clés 
            de nos campagnes sur Instagram.
        </p>
        <ul>
            </p>Followers: +2.8% </p>  
            <p>Le reach des campagnes récentes.</p>
            <p>Les interactions générées par chaque publication.</p>
            <p>Les performances auprès des followers et non-followers.</p>
            <p>Les zones géographiques et démographiques touchées.</p>
        </ul>
        <p>
            Visionnez la vidéo ci-dessous pour une vue d'ensemble !
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# URL ou chemin vers la vidéo
video_file = "LCM.mov"  # Remplacez par le chemin réel du fichier vidéo

# Intégration de la vidéo
st.video(video_file)

# Bouton de téléchargement avec style
with open(video_file, "rb") as file:
    st.markdown(
        """
        <a class="download-btn" href="LCM.mov" download="insights_instagram.mp4">
            Télécharger la vidéo des insights
        </a>
        """,
        unsafe_allow_html=True,
    )
