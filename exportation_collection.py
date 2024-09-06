import os
import firebase_admin
from firebase_admin import credentials, firestore
import json
from google.cloud.firestore_v1._helpers import DatetimeWithNanoseconds

# Initialisation de l'application Firebase avec la clé privée
cred = credentials.Certificate('chemin vers votre clé privé de votre projet firebase')
firebase_admin.initialize_app(cred)

# Initialisation de Firestore
db = firestore.client()

# Fonction pour convertir les objets non sérialisables en JSON, notamment les horodatages
def convert_to_serializable(obj):
    if isinstance(obj, DatetimeWithNanoseconds):
        return obj.isoformat()  # Convertir en chaîne de caractères ISO 8601
    raise TypeError(f"Type non sérialisable en JSON : {type(obj)}")

def export_all_documents(collection_name, output_file):
    # Référence à la collection
    collection_ref = db.collection(collection_name)
    docs = collection_ref.stream()

    all_docs = {}
    for doc in docs:
        all_docs[doc.id] = doc.to_dict()
    
    # Créer le dossier si nécessaire
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    # Écrire toutes les données dans un fichier JSON
    with open(output_file, 'w') as json_file:
        json.dump(all_docs, json_file, indent=2, default=convert_to_serializable)
    print(f'Tous les documents de la collection "{collection_name}" exportés avec succès dans {output_file}!')

def export_collections(collection_names, output_dir):
    for collection_name in collection_names:
        output_file = os.path.join(output_dir, f'{collection_name}.json')
        export_all_documents(collection_name, output_file)

# Liste des collections à exporter
collections = ['nom_collection_1', 'nom_collection_2']  # Ajoute ici toutes les collections nécessaires
output_directory = 'Table'

export_collections(collections, output_directory)
