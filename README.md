# Ontology Data Project

Ce projet est un **outil d'analyse des ventes au détail** qui utilise des technologies telles que **LangChain**, **OpenAI GPT-4**, **RDFLib**, et **Streamlit**. Il permet d'analyser les données de ventes, de détecter des tendances importantes, de générer des cubes RDF et de fournir des recommandations stratégiques basées sur ces données.

## Fonctionnalités

- **Analyse des ventes** : En utilisant un modèle de langage GPT-4, l'outil analyse les données de vente pour identifier les produits les plus vendus, les pics de vente, les profils démographiques des clients, les niveaux de stock critiques, etc.
- **Support multi-format** : Les données peuvent être fournies sous forme de JSON ou texte structuré.
- **Génération de cubes RDF** : Les données d'observations sont transformées en un cube RDF pour permettre des requêtes SPARQL et une meilleure manipulation sémantique des informations.
- **Interface utilisateur via Streamlit** : L'application dispose d'une interface simple pour saisir les données et afficher les résultats sous forme de tableau, d'analyse et de cube RDF en format Turtle.

## Prérequis

Pour exécuter ce projet, vous devez avoir installé les dépendances suivantes :

- **Python 3.8+**
- **Streamlit**
- **LangChain**
- **OpenAI** (clé API requise)
- **rdflib**
- **dotenv**

Vous pouvez installer les dépendances via `pip` en exécutant la commande suivante dans votre terminal :

```bash
pip install streamlit langchain openai rdflib python-dotenv
```


Utilisation

Clonez ce dépôt sur votre machine locale.
Créez un fichier .env à la racine du projet et ajoutez votre clé API OpenAI au format suivant :

```bash
OPENAI_KEY=sk-xxxxxx
```

Lancez l'application Streamlit en exécutant :

```bash
python -m streamlit run app.py
```

Saisissez vos données de ventes dans l'interface, puis cliquez sur "Analyser les Ventes" pour générer l'analyse et le cube RDF.

Vidéo de démonstration
[Vidéo de démonstration](https://drive.google.com/file/d/1zeyiBs1TcxS6iLD2X9cq3T_HTLzdkbe1/view?usp=sharing)


## Auteurs: 
1. **BIABA KUYA Jirince**
2. **LOUGBEGNON G. Amedée**
3. **DIALLO Ibrahima**
4. **TAKOUCHOUANG Fraisse Sacré**
5. **TOUMBA NGONGO Christine**
