from flask import Flask, render_template_string, render_template, jsonify, request, redirect, url_for, session, g
from flask import render_template
from flask import json
from urllib.request import urlopen
from werkzeug.utils import secure_filename
import sqlite3
import time  # Pour gérer le timestamp

app = Flask(__name__)                                                                                                                  
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Clé secrète pour les sessions

#------------------------SEQUENCE 5---------------------------

DB_FILE = "database.db"
DB_LIVRE = "database2.db"

# Durée maximale d'inactivité en secondes (10 minutes)
SESSION_TIMEOUT = 10 * 60

# Rendre la session disponible dans tous les templates
@app.context_processor
def inject_session():
    return dict(session=session)

# Fonction pour créer une clé "authentifie" dans la session utilisateur
# Vérification des rôles dans la session 
def est_admin():
    return session.get('role') == 'admin'

def est_user():
    return session.get('role') == 'user'

# Vérification du timeout avant chaque requête
@app.before_request
def verifier_inactivite():
    # Vérifier si l'utilisateur est connecté
    if 'role' in session:
        dernier_acces = session.get('dernier_acces', None)
        maintenant = time.time()
        
        # Si le dernier accès est défini et dépasse le timeout
        if dernier_acces and (maintenant - dernier_acces > SESSION_TIMEOUT):
            # Supprimer la session et rediriger vers la déconnexion
            session.clear()
            return redirect(url_for('logout'))
        
        # Mettre à jour le timestamp du dernier accès
        session['dernier_acces'] = maintenant

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/lecture')
def lecture():
    if not est_admin() and not est_user():
        # Rediriger vers la page d'authentification si l'utilisateur n'est pas authentifié
        return redirect(url_for('authentification', next=request.path))
    elif est_admin():
        return "<h2>Bravo, vous êtes admin</h2>"
    elif est_user():
        return "<h2>Bravo, vous êtes user</h2>"

@app.route('/authentification', methods=['GET', 'POST'])
def authentification():
    next_url = request.args.get('next') or request.form.get('next') or url_for('lecture')
    print(f"Next URL: {next_url}")
    if request.method == 'POST':
        # Vérifier les identifiants admin
        if request.form['username'] == 'admin' and request.form['password'] == 'password': # password à cacher par la suite
            session['role'] = "admin"
            session['username'] = request.form['username']
            session['dernier_acces'] = time.time()  # Enregistrer le timestamp
            return redirect(next_url)
        # Vérifier les identifiants admin
        elif request.form['username'] == 'user' and request.form['password'] == '12345': # password à cacher par la suite
            session['role'] = "user"
            session['username'] = request.form['username']
            session['dernier_acces'] = time.time()  # Enregistrer le timestamp
            return redirect(next_url)
        else:
            # Afficher un message d'erreur si les identifiants sont incorrects 
            return render_template('formulaire_authentification.html', error=True, next=next_url)
    return render_template('formulaire_authentification.html', error=False, next=next_url)

# Déconnexion (pour tous les utilisateurs)
@app.route('/logout')
def logout():
    if not est_admin() and not est_user():
        return "<h2>Déjà déconnecté !</h2>"
    session.pop('role', None)
    session.pop('username', None)
    return render_template('logout.html')

@app.route('/fiche_client/<int:post_id>')
def Readfiche(post_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients WHERE id = ?', (post_id,))
    data = cursor.fetchall()
    conn.close()
    # Rendre le template HTML et transmettre les données
    return render_template('read_data.html', data=data)

@app.route('/consultation/')
def ReadBDD():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients;')
    data = cursor.fetchall()
    conn.close()
    return render_template('read_data.html', data=data)

@app.route('/enregistrer_client', methods=['GET'])
def formulaire_client():
    return render_template('formulaire_new_client.html')  # afficher le formulaire

@app.route('/enregistrer_client', methods=['POST'])
def enregistrer_client():
    nom = request.form['nom']
    prenom = request.form['prenom']

    # Connexion à la base de données
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Exécution de la requête SQL pour insérer un nouveau client
    cursor.execute('INSERT INTO clients (created, nom, prenom, adresse) VALUES (?, ?, ?, ?)', (1002938, nom, prenom, "ICI"))
    conn.commit()
    conn.close()
    return redirect('/consultation/')  # Rediriger vers la page d'accueil après l'enregistrement 

# Route pour afficher le formulaire de recherche
@app.route("/fiche_nom", methods=["GET"])
def formulaire_search():
    if est_admin() or est_user():
        return render_template("formulaire_search.html")
    print(request.path)
    return redirect(url_for('authentification', next=request.path))

# Route pour traiter la recherche
@app.route("/fiche_nom", methods=["POST"])
def search_client():
    nom = request.form["name"]

    # Connexion à la base de données
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Requête pour rechercher le nom
    cursor.execute("SELECT * FROM clients WHERE nom LIKE ? or prenom LIKE ?", ('%' + nom + '%','%' + nom + '%'))
    data = cursor.fetchall()
    conn.close()

    # Envoyer les résultats au template HTML
    return render_template("read_data.html", data=data)


#-----------------------------------------------------------------

#---------------------------SEQUENCE 6----------------------------

@app.route('/consultation_livre/', methods=['GET', 'POST'])
def ReadBDD_livre():
    conn = sqlite3.connect(DB_LIVRE)
    cursor = conn.cursor()
    

    if request.method == 'POST':
        # Emprunter un livre
        livre_id = request.form.get('emprunter_id')
        if livre_id:
            cursor.execute('UPDATE livres SET est_disponible = 0 WHERE id = ?', (livre_id,))
            conn.commit()

        # Rendre un livre
        rendre_id = request.form.get('rendre_id')
        if rendre_id:
            cursor.execute('UPDATE livres SET est_disponible = 1 WHERE id = ?', (rendre_id,))
            conn.commit()

    # Recherche des livres
    recherche = request.args.get('recherche', '')
    if recherche:
        cursor.execute("SELECT * FROM livres WHERE titre LIKE ? OR auteur LIKE ?", (f"%{recherche}%", f"%{recherche}%"))
    else:
        cursor.execute('SELECT * FROM livres;')
    
    data = cursor.fetchall()

    # Liste des livres empruntés par l'utilisateur
    # Ajoutez un champ utilisateur_id pour stocker qui emprunte quoi
    cursor.execute('SELECT * FROM livres WHERE est_disponible = 0 AND ? IS NOT NULL;', ('0',))
    livres_empruntes = cursor.fetchall()

    conn.close()

    return render_template('read_livre.html', data=data, livres_empruntes=livres_empruntes)

@app.route('/livres/', methods=['GET', 'POST'])
def gestion_livres_user():
    if est_user():
        conn = sqlite3.connect(DB_LIVRE)
        cursor = conn.cursor()
    
        # Si une action POST est effectuée (ajout, emprunt, ou retour d'un livre)
        if request.method == 'POST':
            if 'emprunter' in request.form:
                # Emprunt d'un livre
                id_livre = request.form['id_livre']
                id_utilisateur = request.form['id_utilisateur']
                cursor.execute("""
                    INSERT INTO emprunts (id_livre, id_utilisateur, est_retourne)
                    VALUES (?, ?, 0)
                """, (id_livre, id_utilisateur))
                cursor.execute("""
                    UPDATE stock
                    SET exemplaires_disponibles = exemplaires_disponibles - 1
                    WHERE id_livre = ? AND exemplaires_disponibles > 0
                """, (id_livre,))
    
            elif 'rendre' in request.form:
                # Retour d'un livre
                id_emprunt = request.form['id_emprunt']
                id_livre = request.form['id_livre']
                cursor.execute("""
                    UPDATE emprunts
                    SET est_retourne = 1, date_retour = CURRENT_DATE
                    WHERE id_emprunt = ?
                """, (id_emprunt,))
                cursor.execute("""
                    UPDATE stock
                    SET exemplaires_disponibles = exemplaires_disponibles + 1
                    WHERE id_livre = ?
                """, (id_livre,))
    
            conn.commit()
            return redirect(url_for('gestion_livres_user'))
    
        # Récupération des données
        cursor.execute("""
            SELECT l.id_livre, l.titre, l.auteur, l.genre, l.date_publication, s.total_exemplaires, s.exemplaires_disponibles
            FROM livres l
            LEFT JOIN stock s ON l.id_livre = s.id_livre
        """)
        livres = cursor.fetchall()
    
        cursor.execute("""
            SELECT e.id_emprunt, l.id_livre, l.titre, e.date_emprunt, e.date_retour, e.est_retourne
            FROM emprunts e
            INNER JOIN livres l ON e.id_livre = l.id_livre
            WHERE e.id_utilisateur = ?
        """, (1,))  # Remplacez par l'ID de l'utilisateur connecté
        emprunts = cursor.fetchall()
    
        conn.close()
        return render_template('gestion_user_livres.html', livres=livres, emprunts=emprunts)
    elif est_admin():
        return redirect(url_for('gestion_livres'))
    else :
        return redirect(url_for('authentification', next=request.path))

@app.route('/gestion_livres/', methods=['GET', 'POST'])
def gestion_livres():
    if est_admin() :
        if request.method == 'POST':
            # Connexion à la base de données
            conn = sqlite3.connect(DB_LIVRE)
            cursor = conn.cursor()
            
            # Si le formulaire d'ajout est soumis
            if 'ajouter' in request.form:
                titre = request.form['titre']
                auteur = request.form['auteur']
                genre = request.form['genre']
                date_publication = request.form['date_publication']
                total_exemplaires = int(request.form['total_exemplaires'])
                exemplaires_disponibles = total_exemplaires  # Initialement, tous les exemplaires sont disponibles
                
                # Insérer le livre dans la table "livres"
                cursor.execute("""
                    INSERT INTO livres (titre, auteur, genre, date_publication, est_disponible)
                    VALUES (?, ?, ?, ?, 1)
                """, (titre, auteur, genre, date_publication))
                
                # Récupérer l'ID du livre ajouté
                id_livre = cursor.lastrowid
                
                # Ajouter les informations de stock pour ce livre
                cursor.execute("""
                    INSERT INTO stock (id_livre, total_exemplaires, exemplaires_disponibles)
                    VALUES (?, ?, ?)
                """, (id_livre, total_exemplaires, exemplaires_disponibles))
            
            # Si une suppression est demandée
            if 'supprimer' in request.form:
                id_livre = request.form['id_livre']
                # Supprimer le livre de la table "livres" et ses informations de stock
                cursor.execute("DELETE FROM stock WHERE id_livre = ?", (id_livre,))
                cursor.execute("DELETE FROM livres WHERE id_livre = ?", (id_livre,))
            
            # Validation des modifications
            conn.commit()
            conn.close()
            
            return redirect(url_for('gestion_livres'))
        
        # Récupération des livres avec les informations de stock
        conn = sqlite3.connect(DB_LIVRE)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT l.id_livre, l.titre, l.auteur, l.genre, l.date_publication, 
                   s.total_exemplaires, s.exemplaires_disponibles
            FROM livres l
            LEFT JOIN stock s ON l.id_livre = s.id_livre
        """)
        livres = cursor.fetchall()
        conn.close()
        
        return render_template('livres.html', livres=livres)
    else :
        return redirect(url_for('home'))

if __name__ == "__main__":
  app.run(debug=True)
