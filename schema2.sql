-- Schéma relationnel adapté pour SQLite
CREATE TABLE livres (
    id_livre INTEGER PRIMARY KEY AUTOINCREMENT,
    titre TEXT NOT NULL,
    auteur TEXT NOT NULL,
    genre TEXT,
    date_publication DATE,
    est_disponible BOOLEAN DEFAULT 1
);

CREATE TABLE utilisateurs (
    id_utilisateur INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_utilisateur TEXT UNIQUE NOT NULL,
    mot_de_passe_hache TEXT NOT NULL,
    nom_complet TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    est_admin BOOLEAN DEFAULT 0
);

CREATE TABLE emprunts (
    id_emprunt INTEGER PRIMARY KEY AUTOINCREMENT,
    id_livre INTEGER NOT NULL,
    id_utilisateur INTEGER NOT NULL,
    date_emprunt DATE NOT NULL DEFAULT CURRENT_DATE,
    date_retour DATE,
    est_retourne BOOLEAN DEFAULT 0,
    FOREIGN KEY (id_livre) REFERENCES livres (id_livre),
    FOREIGN KEY (id_utilisateur) REFERENCES utilisateurs (id_utilisateur)
);

CREATE TABLE stock (
    id_livre INTEGER PRIMARY KEY,
    total_exemplaires INTEGER NOT NULL,
    exemplaires_disponibles INTEGER NOT NULL,
    FOREIGN KEY (id_livre) REFERENCES livres (id_livre)
);

CREATE TABLE recommandations (
    id_recommandation INTEGER PRIMARY KEY AUTOINCREMENT,
    id_utilisateur INTEGER NOT NULL,
    id_livre INTEGER NOT NULL,
    date_recommandation DATE NOT NULL DEFAULT CURRENT_DATE,
    FOREIGN KEY (id_utilisateur) REFERENCES utilisateurs (id_utilisateur),
    FOREIGN KEY (id_livre) REFERENCES livres (id_livre)
);

-- Insérer un utilisateur administrateur par défaut
INSERT INTO utilisateurs (nom_utilisateur, mot_de_passe_hache, nom_complet, email, est_admin)
VALUES ('admin', 'mot_de_passe_haché_ici', 'Administrateur', 'admin@bibliotheque.com', 1);
