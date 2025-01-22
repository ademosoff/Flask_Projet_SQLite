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

connection.commit()
connection.close()
