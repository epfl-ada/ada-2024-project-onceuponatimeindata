import pandas as pd
import plotly.graph_objects as go
from ipywidgets import widgets, interactive
from IPython.display import display
import ast
from src.utils.evaluation_utils import inflate



def extract_genres(genres, first_only=False):
    try:
        # Convertir la chaîne en liste de dictionnaires
        genres_list = ast.literal_eval(genres)
        if not genres_list:
            return None
        if first_only:
            return genres_list[0]['name']
        clean_genres = [genre['name'] for genre in genres_list if 'name' in genre]
        return ", ".join(clean_genres)
    except (ValueError, SyntaxError, TypeError):
        return None


#on fait en sorte que le premier film d'un collection determine le egnre de la colection poru plus de coherence comme ca chaque collection a un seul genre 
def prepare_data(df):
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
    df["release_year"] = df["release_date"].apply(lambda x: str(x)[:4] if str(x)[:4].isdigit() else np.nan)
    df.sort_values(by=['collection', 'release_date'], inplace=True)
    df.drop_duplicates(subset=["title"], keep="first", inplace=True)
    df['Numéro'] = df.groupby('collection').cumcount() + 1
    df["revenue"] = df.apply(lambda x: inflate(x["revenue"], x["release_year"]), axis=1)
    df = df[(df['budget'].notna()) & (df['budget'] != 0) &
            (df['revenue'].notna()) & (df['revenue'] != 0) &
            (df['vote_average'].notna()) & (df['vote_average'] != 0)]

    df = df[df['Numéro'] <= 5]
    df = df.groupby('collection').filter(lambda group: len(group) >= 5)

    df["revenue_previous"] = df.groupby("collection")["revenue"].transform(lambda x: x.shift(1))
    df["vote_previous"] = df.groupby("collection")["vote_average"].shift(1)

    return df

def set_colors(df, comparison):
    required_columns = {
        "revenus": ["revenue", "revenue_previous"],
        "notes": ["vote_average", "vote_previous"]
    }
    if comparison not in required_columns:
        raise ValueError(f"Invalid Comparison : {comparison}. Chose 'revenus' or 'notes'.")

    for col in required_columns[comparison]:
        if col not in df.columns:
            raise KeyError(f"The column '{col}' is not in the DataFrame.")

    if comparison == "revenus":
        df["Color"] = df.apply(
            lambda row: "The previous Film had a lower score" if pd.notna(row["revenue_previous"]) and row["revenue"] < row["revenue_previous"]
            else ("The previous Film had a higher score" if pd.notna(row["revenue_previous"]) else "First Film"), axis=1
        )
    elif comparison == "notes":
        df["Color"] = df.apply(
            lambda row: "The previous Film had a lower score" if pd.notna(row["vote_previous"]) and row["vote_average"] < row["vote_previous"]
            else ("The previous Film had a higher score" if pd.notna(row["vote_previous"]) else "First Film"), axis=1
        )

def plot_interactive(df):
    # Préparation des données
    df = prepare_data(df)

    # Initialisation du graphique
    fig = go.FigureWidget()

    # Configuration des limites de l'axe des budgets
    tick_vals = [1e6, 1e7, 1e8, 1e9]  # 1M, 10M, 100M, 1B, 10B
    tick_text = ["1M", "10M", "100M", "1B"]

    # Fonction de mise à jour
    def update_plot(num_film, comparison):
        set_colors(df, comparison)
        filtered_data = df[df["Numéro"] == num_film]

        # Vider les traces existantes
        fig.data = []

        if filtered_data.empty:
            fig.add_trace(go.Scatter(
                x=[], y=[], mode="markers",
                marker=dict(size=10, color="gray"),
                name="Aucun film trouvé"
            ))
        else:
            fig.add_trace(go.Scatter(
                x=filtered_data["budget"],
                y=filtered_data["vote_average"],
                mode="markers",
                marker=dict(
                    size=filtered_data["revenue"] / 1e7,
                    sizeref=max(filtered_data["revenue"] / 1e7) / 40,
                    sizemode="diameter",
                    color=filtered_data["Color"].map({"The previous Film had a higher score": "red", "The previous Film had a lower score": "blue", "First Film": "gray"}),
                ),
                text=filtered_data["title"],
                name="Films"
            ))

        # Mettre à jour le layout
        fig.update_layout(
            title=f"Analysis of the film number: {num_film} depending on the {comparison}",
            xaxis=dict(
                title="Budget (log scale, $)",
                type="log",
                tickvals=tick_vals,
                ticktext=tick_text,
                showgrid=False,
                zeroline=True,
                range=[6, 9],
            ),
            yaxis=dict(
                title="Note moyenne",
                showgrid=True,
            ),
        )

    # Configuration des widgets
    slider_num_film = widgets.IntSlider(min=1, max=int(df["Numéro"].max()), step=1, value=1, description="Numéro du film:")
    dropdown_comparison = widgets.Dropdown(options=["revenus", "notes"], value="revenus", description="Comparer par:")

    # Interactivité
    ui = interactive(update_plot, num_film=slider_num_film, comparison=dropdown_comparison)

    # Afficher les widgets et le graphique
    display(ui, fig)

# Exemple d'utilisation
if __name__ == "__main__":
    df1_part1 = pd.read_csv("data/collections/sequels_and_original_1880_2010_extended.csv")
    df1_part2 = pd.read_csv("data/collections/sequels_and_original_2010_2024_extended.csv")

    # Concaténer les deux parties
    df1 = pd.concat([df1_part1, df1_part2], ignore_index=True)

    # Appeler la fonction interactive
    plot_interactive(df1)



#Since we could not convert our widgets in html, we just plot several times our figure. 
def build_figure(df, num_film, comparison="revenus"):
    df=prepare_data(df)
    set_colors(df, comparison)  # Appliquer les couleurs dynamiquement
    filtered_data = df[df["Numéro"] == num_film]

    if filtered_data.empty:
        print(f"Aucun film trouvé pour le numéro {num_film}")
        return None

    fig = px.scatter(
        filtered_data,
        x="budget",
        y="vote_average",
        size="revenue",
        color="Color",
        hover_name="title",
        title=f"Analysis of the film number: {num_film} depending on the {comparison}",
        labels={"budget": "Budget (M$)", "id": "Film ID"},
        range_y=[4, 9],
        range_x=[1e6, 1e9],  # Fixer l'axe des x de 1M à 1B
        color_discrete_map={"The previous Film had a higher score": "red", "The previous Film had a lower score": "blue", "First Film": "grey"},
        log_x=True,
    )
    return fig







import pandas as pd
import plotly.express as px
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def load_and_clean_data(df):
    """
    Charger et nettoyer les données directement à partir d'un DataFrame.
    """
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')

    # Nettoyage des données
    df = df[(df['budget'].notna()) & (df['budget'] > 0) &
            (df['revenue'].notna()) & (df['revenue'] > 0) &
            (df['vote_average'].notna()) & (df['vote_average'] > 0)]

    # Ajouter des calculs supplémentaires
    df = df.sort_values(by=['collection', 'release_date'])
    df['Numéro'] = df.groupby('collection').cumcount() + 1
    df['ROI'] = (df['revenue'] - df['budget']) / df['budget']
    df['note_growth'] = df.groupby('collection')['vote_average'].diff()
    df['roi_growth'] = df.groupby('collection')['ROI'].diff()
    df['is_last_film'] = df['collection'] != df['collection'].shift(-1)

    return df

def get_last_films(df):
    """
    Extraire les derniers films de chaque collection.
    """
    df_last_films = df[df['is_last_film']].copy()
    features = ['ROI', 'note_growth', 'roi_growth', 'budget', 'revenue']
    df_last_films = df_last_films.dropna(subset=features)
    return df_last_films

def train_model(df_last_films):
    """
    Entraîner un modèle XGBoost pour prédire le succès.
    """
    features = ['ROI', 'note_growth', 'roi_growth', 'budget', 'revenue']
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_last_films[features])

    # Ajouter la colonne cible
    success_threshold = 0.5
    df_last_films['success'] = (df_last_films['ROI'] > success_threshold) & (df_last_films['vote_average'] > 6)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, df_last_films['success'], test_size=0.3, random_state=42
    )

    model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        objective='binary:logistic',
        random_state=42
    )
    model.fit(X_train, y_train)

    df_last_films['success_probability'] = model.predict_proba(X_scaled)[:, 1]
    df_last_films['success_probability'] = df_last_films['success_probability'].clip(lower=0, upper=1)

    return model, df_last_films

def probability_of_success(df):
    """
    Fonction principale qui gère tout le pipeline et retourne le graphique.
    """
    df = load_and_clean_data(df)
    df_last_films = get_last_films(df)
    _, df_last_films = train_model(df_last_films)

    success_threshold = 0.5
    fig = px.scatter(
        df_last_films,
        x="ROI",
        y="vote_average",
        size="budget",
        color="success_probability",
        hover_name="collection",
        title="Probabilités de succès pour les derniers films des collections",
        labels={"ROI": "Retour sur Investissement", "vote_average": "Note Moyenne", "success_probability": "Probabilité de Succès"},
        color_continuous_scale="Viridis",
        log_x=True

    )

    # Ajouter une ligne pour le seuil de succès
    fig.add_vline(x=success_threshold, line_dash="dot", line_color="red", annotation_text="Seuil de succès")

    # Fixer la plage des valeurs de ROI
    fig.update_layout(
        height=600,
        width=800,
        xaxis=dict(range=[-1, 2])
    )

    return fig



import pandas as pd
import plotly.graph_objects as go
import numpy as np
import plotly.io as pio

pio.templates.default = "simple_white"

def prepare_data_for_race_chart(df):
    """
    Prépare les données pour créer un race chart de l'évolution du ROI Progressif.
    """
    df=prepare_data(df)
    # Étape 1 : Fixer le budget du premier film pour chaque collection
    df['first_movie_budget'] = df.groupby('collection')['budget'].transform('first')

    # Étape 2 : Recalculer les revenus cumulés par collection
    df['cumulative_revenue'] = df.groupby('collection')['revenue'].cumsum()

    # Étape 3 : Calculer le ROI progressif et l'arrondir
    df['ROI_progressif'] = ((df['cumulative_revenue'] - df['first_movie_budget']) / df['first_movie_budget']).round(1)
    df['main_genre'] = df['genres'].apply(lambda x: extract_genres(x, first_only=True))

    # Étape 4 : Préparer les données pour la race chart
    df_race = df.groupby(['Numéro', 'collection', 'main_genre'], as_index=False).agg({
        'ROI_progressif': 'last',
        'main_genre': 'first'
    })
    df_race['collection_clean'] = df_race['collection'].str.replace(r'\s*Collection$', '', regex=True)

    # Tri dynamique par Numéro et ROI_progressif
    df_race = df_race.sort_values(['Numéro', 'ROI_progressif'], ascending=[True, False])

    return df_race

def assign_fixed_colors(df_race):
    """
    Attribue des couleurs fixes pour chaque genre dans le race chart.
    """
    fixed_colors = {
        'Horror': 'darkblue',
        'Comedy': 'yellow',
        'Action': 'green',
        'Romance': 'pink',
        'Drama': 'blue',
        'Fantasy': 'purple',
        'Science Fiction': 'lightblue',
        'Adventure': 'blue',
        'Thriller': 'brown',
        'Animation': 'cyan',
        'Other': 'gray'
    }

    # Si un genre n'est pas dans les couleurs fixes, attribuer "Other"
    df_race['main_genre'] = df_race['main_genre'].apply(lambda x: x if x in fixed_colors else 'Other')

    return df_race, fixed_colors

def get_top_15(data, num):
    """
    Récupère les 10 premières collections par ROI progressif pour un numéro donné.
    """
    filtered = data[data['Numéro'] == num]
    return filtered.nlargest(15, 'ROI_progressif')

def create_race_chart(df_race, fixed_colors):
    """
    Crée un graphique interactif pour afficher le race chart.
    """
    # Frames de l'animation
    frames = []
    for num in sorted(df_race['Numéro'].unique()):
        top10 = get_top_15(df_race, num)
        frames.append(go.Frame(
            data=[go.Bar(x=top10['collection_clean'], y=top10['ROI_progressif'],
                         marker_color=[fixed_colors[genre] for genre in top10['main_genre']],
                         text=top10['ROI_progressif'].astype(str) + "%",
                         textposition='outside', cliponaxis=False)],
            layout=go.Layout(title_text=f"Évolution du ROI Progressif - Film {num}")
        ))

    # Données initiales
    initial_data = get_top_15(df_race, df_race['Numéro'].min())

    # Création du graphique
    fig = go.Figure(
        data=[go.Bar(x=initial_data['collection_clean'], y=initial_data['ROI_progressif'],
                     marker_color=[fixed_colors[genre] for genre in initial_data['main_genre']],
                     text=initial_data['ROI_progressif'].astype(str) + "%",
                     textposition='outside', cliponaxis=False)],
        layout=go.Layout(
            title="Évolution du ROI Progressif par Collection et Genre",
            font=dict(size=20),
            height=800,
            xaxis=dict(title="Collection", showline=False, tickangle=-90),
            yaxis=dict(title="Retour sur Investissement (ROI)", type="log", range=[0,4], showline=False),
            updatemenus=[dict(
                type="buttons",
                x=0.85, y=1,
                showactive=False,
                buttons=[
                    dict(label="Play",
                         method="animate",
                         args=[None, {"frame": {"duration": 1000, "redraw": True},
                                      "fromcurrent": True}]),
                    dict(label="Pause",
                         method="animate",
                         args=[[None], {"frame": {"duration": 0, "redraw": False},
                                        "mode": "immediate"}])
                ]
            )],
            showlegend=False
        ),
        frames=frames
    )

    return fig

def generate_race_chart(df):
    """
    Pipeline complet pour préparer les données, assigner les Colors et créer le graphique.
    """
    df_race = prepare_data_for_race_chart(df)
    df_race, fixed_colors = assign_fixed_colors(df_race)
    fig = create_race_chart(df_race, fixed_colors)
    return fig
