-- Schéma relationnel
-- Table : livres
CREATE TABLE livres (
    id_livre SERIAL PRIMARY KEY,
    titre VARCHAR(255) NOT NULL,
    auteur VARCHAR(255) NOT NULL,
    genre VARCHAR(100),
    date_publication DATE,
    est_disponible BOOLEAN DEFAULT TRUE
);

-- Table : utilisateurs
CREATE TABLE utilisateurs (
    id_utilisateur SERIAL PRIMARY KEY,
    nom_utilisateur VARCHAR(100) UNIQUE NOT NULL,
    mot_de_passe_hache VARCHAR(255) NOT NULL,
    nom_complet VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    est_admin BOOLEAN DEFAULT FALSE
);

-- Table : emprunts
CREATE TABLE emprunts (
    id_emprunt SERIAL PRIMARY KEY,
    id_livre INT NOT NULL,
    id_utilisateur INT NOT NULL,
    date_emprunt DATE NOT NULL DEFAULT CURRENT_DATE,
    date_retour DATE,
    est_retourne BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (id_livre) REFERENCES livres (id_livre),
    FOREIGN KEY (id_utilisateur) REFERENCES utilisateurs (id_utilisateur)
);

-- Table : stock
CREATE TABLE stock (
    id_livre INT PRIMARY KEY,
    total_exemplaires INT NOT NULL,
    exemplaires_disponibles INT NOT NULL,
    FOREIGN KEY (id_livre) REFERENCES livres (id_livre)
);

-- Table : recommandations
CREATE TABLE recommandations (
    id_recommandation SERIAL PRIMARY KEY,
    id_utilisateur INT NOT NULL,
    id_livre INT NOT NULL,
    date_recommandation DATE NOT NULL DEFAULT CURRENT_DATE,
    FOREIGN KEY (id_utilisateur) REFERENCES utilisateurs (id_utilisateur),
    FOREIGN KEY (id_livre) REFERENCES livres (id_livre)
);

-- Insérer un utilisateur administrateur par défaut
INSERT INTO utilisateurs (nom_utilisateur, mot_de_passe_hache, nom_complet, email, est_admin)
VALUES ('admin', 'mot_de_passe_haché_ici', 'Administrateur', 'admin@bibliotheque.com', TRUE);
