import mysql.connector


# Établir une connexion au serveur MySQL
conn = mysql.connector.connect(
    host='localhost',
    port='3306',
    user='root',
    password=''
)

cursor = conn.cursor()

# Créer une base de données
cursor.execute("CREATE DATABASE IF NOT EXISTS MADBPY")

# Utiliser cette base de données
cursor.execute("USE MADBPY")

# Créer une table

cursor.execute('''
CREATE TABLE if not exists partie (
    id INT PRIMARY KEY AUTO_INCREMENT, 
    Exercise VARCHAR(255) NOT NULL,
    Pseudo VARCHAR(255) NOT NULL,
    DateHour DATETIME NOT NULL,
    Duration TIME NOT NULL,
    NbTrials INT NOT NULL,
    NbOk INT NOT NULL
    
);
''')


def save_game_result(pseudo, exercise, duration, nb_trials, nb_success):
    # connection db
    conn = mysql.connector.connect(
        host='localhost',
        port='3306',
        user='root',
        password=''
    )
    cursor = conn.cursor()

    # pour choisir la bd
    cursor.execute("USE MADBPY")

    # pour insertion les donnees
    query = '''
    INSERT INTO partie (Exercise, Pseudo, DateHour, Duration, NbTrials,NbOk)
    VALUES (%s, %s, NOW(), %s, %s, %s)
    '''
    values = (exercise, pseudo, duration, nb_trials,nb_success)

    cursor.execute(query, values)
    conn.commit()

    cursor.close()
    conn.close()


def get_game_results(pseudo=None, exercise=None, start_date=None, end_date=None):
    conn = mysql.connector.connect(
        host='localhost',
        port='3306',
        user='root',
        password='',
        database='MADBPY'
    )
    cursor = conn.cursor()

    # pour obtenir les valeurs de table 'partie'
    query = "SELECT Pseudo AS 'Élevé', DateHour AS 'Date Heure', Duration AS 'Temps', Exercise AS 'Exercice', NbOk AS 'nb OK' , NbTrials AS 'nb Total' FROM partie WHERE 1=1"

    cursor.execute(query)
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results
