import sqlite3
import random
from faker import Faker

# Initialisation de la base de données SQLite
conn = sqlite3.connect('phones.db')
cursor = conn.cursor()

# Création des tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS phones (
    phone_number TEXT PRIMARY KEY,
    owner TEXT,
    company TEXT,
    location TEXT,
    last_called TEXT,
    password TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS companies (
    company_name TEXT PRIMARY KEY,
    block_start TEXT,
    block_end TEXT
)
''')

# Ajout des informations spécifiques des compagnies
companies_data = [
    ('BurnerBZH', '0733890000', '0733899999'),
    ('TechCorp', '0642000000', '0699000000'),
    ('MobileCo', '0600000000', '0641000000'),
    ('FastPhone', '0710200000', '0712200000'),
    ('Bleu', '0713000000', '0720000000'),
    ('O3', '0700000000', '0710000000'),
    ('SeaDigital', '0799000000', '0799900000'),
]

for company in companies_data:
    cursor.execute('''
    INSERT INTO companies (company_name, block_start, block_end) 
    VALUES (?, ?, ?)
    ''', company)

# Fonction pour générer des données fictives
fake = Faker()

def generate_phone_data():
    owner = fake.name() if random.random() > 0.1 else "None"  # 10% chance of being a burner phone
    
    if owner == 'None':
        cursor.execute("SELECT * FROM companies where company_name = 'BurnerBZH'")
    else:
        cursor.execute("SELECT * FROM companies where company_name != 'BurnerBZH'")
    companies = cursor.fetchall()
    company = random.choice(companies)
    company_name, block_start, block_end = company

    # Générer un numéro dans le bloc de la compagnie
    block_start_int = int(block_start)
    block_end_int = int(block_end)
    phone_number = "0"+str(random.randint(block_start_int, block_end_int))
    
    location = random.choice([
        'Vannes, France', 'Paris, France', 'Nantes, France', 
        'Lyon, France', 'Rennes, France', 'Berlin, Allemagne', 
        'Rochefort-En-Terre, France', 'Sidi Bou Said, Tunisie', 
        'Tunis, Tunisie'
    ])
    last_called = "0"+str(random.randint(block_start_int, block_end_int))  # Dernier appel en string
    password = fake.password(length=random.randint(6, 14)) if owner == "None" else "None"
    
    return (phone_number, owner, company_name, location, last_called, password)

# Insertion des données dans les tables
for _ in range(10000):
    phone_data = generate_phone_data()
    try:
        cursor.execute('''
        INSERT INTO phones (phone_number, owner, company, location, last_called, password)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', phone_data)
    except sqlite3.IntegrityError:
        continue  # Éviter les doublons

# Ajout des numéros spécifiques
specific_numbers = [
    ('0733896810', 'None', 'BurnerBZH', 'Vannes, France', '0612211345', 'Ashley'),
    ('0733896724', 'None', 'BurnerBZH', 'Vannes, France', '0613370991', 'Ashley'),
    ('0733891214', 'None', 'BurnerBZH', 'Vannes, France', '0718820030', 'Ashley'),
    ('0733891373', 'None', 'BurnerBZH', 'Vannes, France', '0618189304', 'Ashley')
]

for number in specific_numbers:
    try:
        cursor.execute('''
        INSERT INTO phones (phone_number, owner, company, location, last_called, password)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', number)
    except sqlite3.IntegrityError:
        continue  # Éviter les doublons

# Sauvegarde et fermeture de la base de données
conn.commit()
conn.close()

print("Base de données générée avec succès !")
