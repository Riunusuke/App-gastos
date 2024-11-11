import firebase_admin
from firebase_admin import credentials, firestore

def initialize_firebase():
    cred = credentials.Certificate("gastos-personales-ad4c0-firebase-adminsdk-e0u3m-db0a5202b2.json")  # Ruta a tus credenciales
    if not firebase_admin._apps:  # Para evitar múltiples inicializaciones
        firebase_admin.initialize_app(cred)
    return firestore.client()

# Crea una instancia de Firestore
db = initialize_firebase()
