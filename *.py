import sqlite3
import random

# Nom du fichier de la base de données SQLite
DB_FILE = "database2.db"

def ajouter_exemplaires_aleatoires():
    try:
        # Connexion à la base de données
        connexion = sqlite3.connect(DB_FILE)
        curseur = connexion.cursor()

        # Récupérer tous les IDs des livres existants
        curseur.execute("SELECT id_livre FROM livres")
        livres = curseur.fetchall()

        # Ajouter un nombre aléatoire d'exemplaires pour chaque livre
        for livre in livres:
            id_livre = livre[0]
            total_exemplaires = random.randint(1, 20)  # Nombre total entre 1 et 20
            exemplaires_disponibles = random.randint(0, total_exemplaires)  # Nombre disponible entre 0 et total

            # Vérifier si une entrée pour ce livre existe déjà dans "stock"
            curseur.execute("SELECT COUNT(*) FROM stock WHERE id_livre = ?", (id_livre,))
            existe = curseur.fetchone()[0]

            if existe:
                # Mise à jour des exemplaires si déjà présent
                curseur.execute("""
                    UPDATE stock
                    SET total_exemplaires = ?, exemplaires_disponibles = ?
                    WHERE id_livre = ?
                """, (total_exemplaires, exemplaires_disponibles, id_livre))
            else:
                # Insertion d'une nouvelle entrée
                curseur.execute("""
                    INSERT INTO stock (id_livre, total_exemplaires, exemplaires_disponibles)
                    VALUES (?, ?, ?)
                """, (id_livre, total_exemplaires, exemplaires_disponibles))

        # Valider les modifications
        connexion.commit()
        print("Exemplaires ajoutés ou mis à jour avec succès.")

    except Exception as e:
        print(f"Une erreur est survenue : {e}")

    finally:
        if curseur:
            curseur.close()
        if connexion:
            connexion.close()

if __name__ == "__main__":
    ajouter_exemplaires_aleatoires()
