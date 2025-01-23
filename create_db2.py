import sqlite3

connection = sqlite3.connect('database2.db')

with open('schema2.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

# Ajout de données à la table "livres"
livres = [
    ('Le Petit Prince', 'Antoine de Saint-Exupéry', 'Conte', '1943-04-06'),
    ('1984', 'George Orwell', 'Dystopie', '1949-06-08'),
    ('L\'Étranger', 'Albert Camus', 'Philosophie', '1942-05-19'),
    ('Harry Potter à l\'école des sorciers', 'J.K. Rowling', 'Fantastique', '1997-06-26'),
    ('Les Misérables', 'Victor Hugo', 'Roman', '1862-01-01'),
    ('Don Quichotte', 'Miguel de Cervantes', 'Aventure', '1605-01-16'),
    ('Pride and Prejudice', 'Jane Austen', 'Romance', '1813-01-28'),
    ('Moby Dick', 'Herman Melville', 'Aventure', '1851-10-18'),
    ('Le Comte de Monte-Cristo', 'Alexandre Dumas', 'Roman', '1844-08-28'),
    ('La Peste', 'Albert Camus', 'Philosophie', '1947-06-10'),
    ('To Kill a Mockingbird', 'Harper Lee', 'Roman', '1960-07-11'),
    ('Le Seigneur des Anneaux : La Communauté de l\'Anneau', 'J.R.R. Tolkien', 'Fantastique', '1954-07-29'),
    ('Crime et Châtiment', 'Fiodor Dostoïevski', 'Roman', '1866-01-01'),
    ('L\'Odyssée', 'Homère', 'Poésie épique', '-800-01-01'),
    ('Le Rouge et le Noir', 'Stendhal', 'Roman', '1830-01-01'),
    ('Les Fleurs du mal', 'Charles Baudelaire', 'Poésie', '1857-01-01'),
    ('Candide ou l\'Optimisme', 'Voltaire', 'Philosophie', '1759-01-01'),
    ('Frankenstein', 'Mary Shelley', 'Science-fiction', '1818-01-01'),
    ('Dracula', 'Bram Stoker', 'Horreur', '1897-01-01'),
    ('Beloved', 'Toni Morrison', 'Roman', '1987-09-16')
]

# Ajout des livres à la base de données
for livre in livres:
    cur.execute("INSERT INTO livres (titre, auteur, genre, date_publication, est_disponible) VALUES (?, ?, ?, ?, 1)", livre)

connection.commit()
connection.close()
