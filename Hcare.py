import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Conectar a la base de datos SQLite (esto crea el archivo hcare.db si no existe)
conn = sqlite3.connect('hcare.db')
cursor = conn.cursor()

# Crear las tablas en SQLite
cursor.execute('''
CREATE TABLE IF NOT EXISTS Patients (
    Id TEXT PRIMARY KEY,
    BIRTHDATE TEXT,
    DEATHDATE TEXT,
    SSN TEXT,
    DRIVERS TEXT,
    PASSPORT TEXT,
    PREFIX TEXT,
    FIRST TEXT,
    LAST TEXT,
    SUFFIX TEXT,
    MAIDEN TEXT,
    MARITAL TEXT,
    RACE TEXT,
    ETHNICITY TEXT,
    GENDER TEXT,
    BIRTHPLACE TEXT,
    ADDRESS TEXT,
    CITY TEXT,
    STATE TEXT,
    ZIP TEXT,
    LAT REAL,
    LON REAL,
    HEALTHCARE_EXPENSES REAL,
    HEALTHCARE_COVERAGE REAL,
    INCOME INTEGER
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Conditions (
    START TEXT,
    STOP TEXT,
    PATIENT TEXT,
    ENCOUNTER TEXT,
    CODE INTEGER,
    DESCRIPTION TEXT,
    FOREIGN KEY (PATIENT) REFERENCES Patients(Id)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Encounters (
    Id TEXT PRIMARY KEY,
    START TEXT,
    STOP TEXT,
    PATIENT TEXT,
    ORGANIZATION TEXT,
    PROVIDER TEXT,
    PAYER TEXT,
    ENCOUNTERCLASS TEXT,
    CODE INTEGER,
    DESCRIPTION TEXT,
    BASE_ENCOUNTER_COST REAL,
    TOTAL_CLAIM_COST REAL,
    PAYER_COVERAGE REAL,
    REASONCODE INTEGER,
    REASONDESCRIPTION TEXT,
    FOREIGN KEY (PATIENT) REFERENCES Patients(Id)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Immunizations (
    DATE TEXT,
    PATIENT TEXT,
    ENCOUNTER TEXT,
    CODE INTEGER,
    DESCRIPTION TEXT,
    BASE_COST REAL,
    FOREIGN KEY (PATIENT) REFERENCES Patients(Id),
    FOREIGN KEY (ENCOUNTER) REFERENCES Encounters(Id)
);
''')

# Cargar los datos CSV en las tablas de SQLite
patients_df = pd.read_csv(r'C:\Users\sebae\Desktop\Ideas Portafolio\sql basic healthcare\Datos\patients.csv')
conditions_df = pd.read_csv(r'C:\Users\sebae\Desktop\Ideas Portafolio\sql basic healthcare\Datos\conditions.csv')
encounters_df = pd.read_csv(r'C:\Users\sebae\Desktop\Ideas Portafolio\sql basic healthcare\Datos\encounters.csv')
immunizations_df = pd.read_csv(r'C:\Users\sebae\Desktop\Ideas Portafolio\sql basic healthcare\Datos\immunizations.csv')

patients_df.to_sql('Patients', conn, if_exists='replace', index=False)
conditions_df.to_sql('Conditions', conn, if_exists='replace', index=False)
encounters_df.to_sql('Encounters', conn, if_exists='replace', index=False)
immunizations_df.to_sql('Immunizations', conn, if_exists='replace', index=False)

# 1 - Listar todas las condiciones de un paciente
query1 = '''SELECT p.FIRST, p.LAST, c.DESCRIPTION, c.START 
FROM Patients p
JOIN Conditions c ON p.Id = c.PATIENT
WHERE p.Id = '22d38175-77e1-5a3b-45bb-503acf690feb';'''

p_query1 = pd.read_sql_query(query1, conn)
print('---------------------------------------------------------------------------------------')
print("1- Condiciones de un solo paciente:")
print('---------------------------------------------------------------------------------------')
print(p_query1)
print('---------------------------------------------------------------------------------------')

# 2 - Listar todas las condiciones diagnosticadas en un encuentro en especifico
query2 = '''SELECT p.FIRST, p.LAST, i.DESCRIPTION, i.DATE
FROM Patients p
JOIN Immunizations i ON p.Id = i.PATIENT
WHERE p.Id = '22d38175-77e1-5a3b-45bb-503acf690feb';
'''
p_query2 = pd.read_sql_query(query2, conn)
print('---------------------------------------------------------------------------------------')
print("2- Condiciones diagnosticadas en un encuentro especifico:")
print('---------------------------------------------------------------------------------------')
print(p_query2)
print('---------------------------------------------------------------------------------------')

# 3 - Calcular el costo total de encuentros para un paciente

query3 = '''SELECT SUM(e.TOTAL_CLAIM_COST) 
FROM Encounters e
JOIN Patients p ON e.PATIENT = p.Id
WHERE p.Id = '22d38175-77e1-5a3b-45bb-503acf690feb';
'''
p_query3 = pd.read_sql_query(query3,conn)
print('---------------------------------------------------------------------------------------')
print("3- Costo total de ecuentros de un solo paciente:")
print('---------------------------------------------------------------------------------------')
print (round(p_query3),2)
print('---------------------------------------------------------------------------------------')

# 4 - Encuentra el paciente con el mayor número de condiciones diagnosticadas

query4 = '''SELECT p.FIRST, p.LAST, COUNT(c.CODE) as condition_count
FROM Patients p
JOIN Conditions c ON p.Id = c.PATIENT
GROUP BY p.Id
ORDER BY condition_count DESC
LIMIT 1;
'''

p_query4 = pd.read_sql_query(query4,conn)
print('---------------------------------------------------------------------------------------')
print("4- Paciente con mayor numero de condiciones:")
print('---------------------------------------------------------------------------------------')
print (p_query4)
print('---------------------------------------------------------------------------------------')

# 5 - Obtener los encuentros más costosos por paciente
query5 = '''SELECT p.FIRST, p.LAST, e.DESCRIPTION, e.TOTAL_CLAIM_COST
FROM Patients p
JOIN Encounters e ON p.Id = e.PATIENT
ORDER BY e.TOTAL_CLAIM_COST DESC
LIMIT 10;
'''
p_query5 = pd.read_sql_query(query5,conn)

print('---------------------------------------------------------------------------------------')
print("5- Encuentro mas costoso por paciente:")
print('---------------------------------------------------------------------------------------')
print (p_query5)
print('---------------------------------------------------------------------------------------')



# 6- Listar las condiciones mas comenes entre pacientes 

query6 = '''SELECT c.DESCRIPTION, COUNT(c.CODE) as condition_count
FROM Conditions c
GROUP BY c.CODE
ORDER BY condition_count DESC
LIMIT 5;
'''
p_query6 = pd.read_sql_query(query6,conn)
print('---------------------------------------------------------------------------------------')
print("6- Condiciones mas comunes entres pacientes:")
print('---------------------------------------------------------------------------------------')
print (p_query6)
print('---------------------------------------------------------------------------------------')

# 7- Obtener la edad promedio de los pacientes en el dataset

query7 = '''SELECT AVG(strftime('%Y', 'now') - SUBSTR(BIRTHDATE, 1, 4)) AS avg_age
FROM Patients;
'''
p_query7 = pd.read_sql_query(query7,conn)
print('---------------------------------------------------------------------------------------')
print("7- Edad promedio de los pacientes:")
print('---------------------------------------------------------------------------------------')
print (round(p_query7))
print('---------------------------------------------------------------------------------------')

# 8- Numero de pacientes por estado

query8 = '''SELECT p.STATE, COUNT(p.Id)
FROM Patients p
GROUP BY p.STATE;
'''
p_query8 = pd.read_sql_query(query8,conn)
print('---------------------------------------------------------------------------------------')
print("8- Número de pacientes por estado:")
print('---------------------------------------------------------------------------------------')
print (p_query8)
print('---------------------------------------------------------------------------------------')

# 9- Identificar el proveedor que ha atendido mas encuentros

query9 = '''SELECT e.PROVIDER, COUNT(e.Id)
FROM Encounters e
GROUP BY e.PROVIDER
ORDER BY COUNT(e.Id) DESC
LIMIT 1;
'''
p_query9 = pd.read_sql_query(query9,conn)
print('---------------------------------------------------------------------------------------')
print("9- Proveedor que ha atendido a mas pacientes:")
print('---------------------------------------------------------------------------------------')
print (p_query9)
print('---------------------------------------------------------------------------------------')

# 10- Listar los pacientes que han fallecido 

query10 = '''SELECT p.FIRST, p.LAST, p.BIRTHDATE, p.DEATHDATE
FROM Patients p
WHERE p.DEATHDATE IS NOT NULL;
'''
p_query10 = pd.read_sql_query(query10,conn)
print('---------------------------------------------------------------------------------------')
print("10- Pacientes fallecidos:")
print('---------------------------------------------------------------------------------------')
print (p_query10)
print('---------------------------------------------------------------------------------------')


#Graficos

#Query 5
# Preparar los datos para el gráfico
p_query5['PATIENT_NAME'] = p_query5['FIRST'] + ' ' + p_query5['LAST']
patients = p_query5['PATIENT_NAME'] + "\n" + p_query5['DESCRIPTION']
costs = p_query5['TOTAL_CLAIM_COST']

# Crear el gráfico de barras
plt.figure(figsize=(10, 5))
plt.barh(patients, costs, color='skyblue')
plt.xlabel('Costo Total del Reclamo ($)')
plt.ylabel('Paciente y Descripción del Encuentro')
plt.title('Top 10 Encuentros Más Costosos por Paciente')
plt.gca().invert_yaxis()  # Invertir el eje Y para que el más caro esté arriba
plt.tight_layout()
plt.show()


#Query 6

# Preparar los datos para el gráfico
conditions = p_query6['DESCRIPTION']
counts = p_query6['condition_count']

# Crear el gráfico de barras
plt.figure(figsize=(10, 6))
plt.bar(conditions, counts, color='coral')
plt.xlabel('Condición')
plt.ylabel('Cantidad de Pacientes')
plt.title('Top 5 Condiciones Más Comunes Entre Pacientes')
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()


# Cerrar la conexión
conn.close()
