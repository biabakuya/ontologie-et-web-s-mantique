import streamlit as st
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import XSD
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
import os, json, csv
from io import StringIO
from dotenv import load_dotenv

load_dotenv()

# Namespace
EX = Namespace("http://example.org/retail/")
QB = Namespace("http://purl.org/linked-data/cube#")

api_key = os.getenv('OPENAI_KEY')

# Initialiser le modèle de langage OpenAI avec clé API
llm = ChatOpenAI(
    api_key=api_key,
    model="gpt-4")

# Définir un template pour le prompt
template = """
Vous êtes un agent d'analyse des ventes au détail. Vous recevez les données suivantes sur les ventes, les préférences des clients, les tendances saisonnières, et les niveaux de stock :
{data}

Fournissez une analyse détaillée des ventes, identifiez les tendances (produits les plus vendus, périodes d'achat de pointe, profils démographiques des clients), déterminez les niveaux de stock critiques, définissez les indicateurs de performance clés, et suggérez des actions stratégiques pour améliorer la gestion des stocks, les campagnes marketing ou les ajustements de prix.
"""

# Créer un PromptTemplate
prompt = PromptTemplate(template=template, input_variables=["data"])

# Créer une LLMChain
sales_chain = LLMChain(llm=llm, prompt=prompt)

# Interface Streamlit avec personnalisation
st.markdown("""
    <style>
    .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        text-align: center;
        padding: 10px 20px;
        background-color: #007bffd1;
        color: white;
        border-radius: 10px;
    }
    .header img {
        height: 60px;
    }
    h1 {
        font-size: 2rem;
    }
    .main {
        background-color: #f0f0f5;
        color: #333;
        padding: 20px;
        border-radius: 0 0 10px 10px;
    }
    .stTextArea label {
        color: black !important;
    }
    .stCodeBlock label {
        color: white;
    }
    .stTextArea textarea {
        color: white !important;
        background-color: #333333 !important;
        border: 2px solid #007bff !important;
        border-radius: 8px !important;
    }
    .stButton>button {
        background-color: #007bffd1;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
    }
    .stButton>button:hover {
        background-color: #0056b3;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #007bffd1;
        color: white;
        text-align: center;
        padding: 10px;
    }
    .white-text {
        color: black !important;
        font-size: 2rem !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="header">
        <h1>Agent d'Analyse de données</h1>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="main">
        <p>Bienvenue dans l'outil d'analyse des ventes au détail. Cet agent est conçu pour vous aider à comprendre 
        et optimiser vos ventes en analysant des données de vente, des préférences clients, des tendances saisonnières, 
        et des niveaux de stock. Entrez vos données ci-dessous pour commencer l'analyse.</p>
    </div>
""", unsafe_allow_html=True)

# Zone de texte pour les données de ventes et de stock
sales_data = st.text_area("Entrez les données de vente (JSON, ou texte structuré) :")

def detect_format(data):
    """Détecter le format des données d'entrée."""
    try:
        # Essayer de charger comme JSON
        json.loads(data)
        return "json"
    except json.JSONDecodeError:
        pass

    try:
        # Essayer de charger comme CSV
        csv.reader(StringIO(data))
        return "csv"
    except csv.Error:
        pass

    # Si aucune des options ci-dessus ne fonctionne, traiter comme texte structuré
    return "text"

def process_data(data, format_type):
    """Traiter les données selon le format détecté."""
    observations = []

    if format_type == "json":
        observations = json.loads(data)
    elif format_type == "csv":
        csv_reader = csv.DictReader(StringIO(data))
        for row in csv_reader:
            observations.append(row)
    elif format_type == "text":
        lines = data.strip().split("\n")
        for line in lines:
            try:
                produit, ventes, preferences, tendances, stock = line.split(", ")
                observations.append({
                    "Produit": produit,
                    "Ventes": int(ventes),
                    "Préférences": preferences,
                    "Tendances": tendances,
                    "Stock": stock
                })
            except ValueError:
                st.error(f"Erreur de format pour la ligne : {line}")
    return observations

# Fonction pour créer un cube RDF à partir des données d'analyse
def create_rdf_cube(graph, observations):
    for i, obs in enumerate(observations):
        observation = URIRef(EX[f"Observation{i + 1}"])
        graph.add((observation, RDF.type, QB.Observation))
        graph.add((observation, QB.dataSet, EX["RetailCube"]))

        # Ajout des propriétés RDF
        graph.add((observation, EX.product, Literal(obs["Produit"], datatype=XSD.string)))
        graph.add((observation, EX.salesAmount, Literal(obs["Ventes"], datatype=XSD.integer)))
        graph.add((observation, EX.stockLevel, Literal(obs.get("Stock", "N/A"), datatype=XSD.string)))
        graph.add((observation, EX.customerDemographic, Literal(obs.get("Préférences", "N/A"), datatype=XSD.string)))
        graph.add((observation, EX.peakSalesPeriod, Literal(obs.get("Tendances", "N/A"), datatype=XSD.string)))
    return graph

# Fonction pour interroger le cube RDF
def query_most_sold_products(graph):
    query = """
    PREFIX qb: <http://purl.org/linked-data/cube#>
    PREFIX ex: <http://example.org/retail/>

    SELECT ?product (SUM(?salesAmount) as ?totalSales)
    WHERE {
      ?obs a qb:Observation ;
           ex:product ?product ;
           ex:salesAmount ?salesAmount .
    }
    GROUP BY ?product
    ORDER BY DESC(?totalSales)
    """
    result = graph.query(query)
    st.markdown("<span class='white-text'>Produits les plus vendus</span>", unsafe_allow_html=True)
    for row in result:
        st.write(f"Produit : {row.product}, Ventes Totales : {row.totalSales}")

if st.button("Analyser les Ventes"):
    if sales_data:
        format_type = detect_format(sales_data)
        with st.spinner(f"Analyse en cours... (format détecté : {format_type})"):
            observations = process_data(sales_data, format_type)
            analysis = sales_chain.run({"data": sales_data})
            st.markdown("<div style='color:blue'> Analyse</div>", unsafe_allow_html=True)
            st.write(analysis)

            # Générer le cube RDF
            rdf_graph = Graph()
            rdf_graph.bind("ex", EX)
            rdf_graph.bind("qb", QB)
            rdf_graph = create_rdf_cube(rdf_graph, observations)

            st.markdown("<span class='white-text'>Cube RDF</span>", unsafe_allow_html=True)
            st.code(rdf_graph.serialize(format="turtle"), language="turtle")

            # Interroger le cube RDF
            query_most_sold_products(rdf_graph)
    else:
        st.error("Veuillez entrer les données de vente pour procéder à l'analyse.")

# Ajouter un pied de page
st.markdown('<div class="footer">LangChain et OpenAI | &#169; Groupe 3</div>',
            unsafe_allow_html=True)