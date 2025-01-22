import sqlite3

connection = sqlite3.connect('database2.db')

with open('schema2.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

# Ajout de données à la table "livres"
cur.execute("INSERT INTO livres (titre, auteur, genre, date_publication, est_disponible) VALUES (?, ?, ?, ?, 1)",
            ('Le Petit Prince', 'Antoine de Saint-Exupéry', 'Conte', '1943-04-06'))
cur.execute("INSERT INTO livres (titre, auteur, genre, date_publication, est_disponible) VALUES (?, ?, ?, ?, 1)",
            ('1984', 'George Orwell', 'Dystopie', '1949-06-08'))
cur.execute("INSERT INTO livres (titre, auteur, genre, date_publication, est_disponible) VALUES (?, ?, ?, ?, 1)",
            ('L\'Étranger', 'Albert Camus', 'Philosophie', '1942-05-19'))
cur.execute("INSERT INTO livres (titre, auteur, genre, date_publication, est_disponible) VALUES (?, ?, ?, ?, 1)",
            ('Harry Potter à l\'école des sorciers', 'J.K. Rowling', 'Fantastique', '1997-06-26'))
cur.execute("INSERT INTO livres (titre, auteur, genre, date_publication, est_disponible) VALUES (?, ?, ?, ?, 1)",
            ('Les Misérables', 'Victor Hugo', 'Roman', '1862-01-01'))

# Ajout d'autres entrées à la table "livres"
cur.execute("INSERT INTO livres (titre, auteur, genre, date_publication, est_disponible) VALUES (?, ?, ?, ?, 1)",
            ('DUPONT', 'Emilie', '123, Rue des Lilas, 75001 Paris', None))
cur.execute("INSERT INTO livres (titre, auteur, genre, date_publication, est_disponible) VALUES (?, ?, ?, ?, 1)",
            ('LEROUX', 'Lucas', '456, Avenue du Soleil, 31000 Toulouse', None))
cur.execute("INSERT INTO livres (titre, auteur, genre, date_publication, est_disponible) VALUES (?, ?, ?, ?, 1)",
            ('MARTIN', 'Amandine', '789, Rue des Érables, 69002 Lyon', None))
cur.execute("INSERT INTO livres (titre, auteur, genre, date_publication, est_disponible) VALUES (?, ?, ?, ?, 1)",
            ('TREMBLAY', 'Antoine', '1010, Boulevard de la Mer, 13008 Marseille', None))
cur.execute("INSERT INTO livres (titre, auteur, genre, date_publication, est_disponible) VALUES (?, ?, ?, ?, 1)",
            ('LAMBERT', 'Sarah', '222, Avenue de la Liberté, 59000 Lille', None))
cur.execute("INSERT INTO livres (titre, auteur, genre, date_publication, est_disponible) VALUES (?, ?, ?, ?, 1)",
            ('GAGNON', 'Nicolas', '456, Boulevard des Cerisiers, 69003 Lyon', None))
cur.execute("INSERT INTO livres (titre, auteur, genre, date_publication, est_disponible) VALUES (?, ?, ?, ?, 1)",
            ('DUBOIS', 'Charlotte', '789, Rue des Roses, 13005 Marseille', None))
cur.execute("INSERT INTO livres (titre, auteur, genre, date_publication, est_disponible) VALUES (?, ?, ?, ?, 1)",
            ('LEFEVRE', 'Thomas', '333, Rue de la Paix, 75002 Paris', None))

connection.commit()
connection.close()
