import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st

def initialize_firebase():
    #cred = credentials.Certificate("gastos-personales-ad4c0-firebase-adminsdk-e0u3m-db0a5202b2.json")  # Ruta a tus credenciales
    #cred = credentials.Certificate(creds)
    cred = credentials.Certificate({
    "type": st.secrets["firebase_creds"]["type"],
    "project_id": st.secrets["firebase_creds"]["project_id"],
    "private_key_id": st.secrets["firebase_creds"]["private_key_id"],
    "private_key": st.secrets["firebase_creds"]["private_key"].replace("\\n", "\n"),  # Corrige las nuevas líneas
    "client_email": st.secrets["firebase_creds"]["client_email"],
    "client_id": st.secrets["firebase_creds"]["client_id"],
    "auth_uri": st.secrets["firebase_creds"]["auth_uri"],
    "token_uri": st.secrets["firebase_creds"]["token_uri"],
    "auth_provider_x509_cert_url": st.secrets["firebase_creds"]["auth_provider_x509_cert_url"],
    "client_x509_cert_url": st.secrets["firebase_creds"]["client_x509_cert_url"],
    "universe_domain": st.secrets["firebase_creds"]["universe_domain"]
})
    
    if not firebase_admin._apps:  # Para evitar múltiples inicializaciones
        firebase_admin.initialize_app(cred)
    return firestore.client()

# Crea una instancia de Firestore
db = initialize_firebase()
