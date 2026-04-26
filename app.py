import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# Base de données SQLite (Efficace et Gratuit)
def init_db():
    conn = sqlite3.connect('notes_universite.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS etudiants 
                 (nom TEXT, prenom TEXT, matricule TEXT, filiere TEXT, 
                  niveau TEXT, annee TEXT, sexe TEXT)''')
    conn.commit()
    conn.close()

init_db()

st.set_page_config(page_title="TP INF232 - Collecte", layout="centered")

st.title("📊 Collecte & Analyse Descriptive INF 232")

# --- FORMULAIRE DE COLLECTE ---
with st.expander("➕ Ajouter un nouvel étudiant", expanded=True):
    with st.form("form_collecte"):
        nom = st.text_input("Nom")
        prenom = st.text_input("Prénom")
        matricule = st.text_input("Matricule")
        filiere = st.selectbox("Filière", ["Informatique", "Génie Logiciel", "Réseaux", "Sécurité"])
        niveau = st.select_slider("Niveau Académique", options=["L1", "L2", "L3", "M1", "M2"])
        annee = st.date_input("Année Scolaire (Date)")
        sexe = st.radio("Sexe", ["Masculin", "Féminin"], horizontal=True)
        
        if st.form_submit_button("Enregistrer"):
            conn = sqlite3.connect('notes_universite.db')
            c = conn.cursor()
            c.execute("INSERT INTO etudiants VALUES (?,?,?,?,?,?,?)", 
                      (nom, prenom, matricule, filiere, niveau, str(annee), sexe))
            conn.commit()
            conn.close()
            st.success("Données enregistrées !")

# --- ANALYSE DESCRIPTIVE ---
st.divider()
st.header("📈 Visualisation Descriptive")

conn = sqlite3.connect('notes_universite.db')
df = pd.read_sql_query("SELECT * FROM etudiants", conn)
conn.close()

if not df.empty:
    st.subheader("Données brutes")
    st.dataframe(df, use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Répartition par Sexe**")
        st.bar_chart(df['sexe'].value_counts())
    with col2:
        st.write("**Répartition par Filière**")
        st.write(df['filiere'].value_counts())
else:
    st.info("Aucune donnée disponible. Remplissez le formulaire.")
