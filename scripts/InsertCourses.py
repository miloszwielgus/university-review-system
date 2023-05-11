import mysql.connector

cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="ProjectIO"
)

cursor = cnx.cursor()

sql = "INSERT INTO Course (course_name, syllabus, university_id,degree, cycle) VALUES (%s,%s,%s,%s,%s)"
values = [
    ("Aministracja", "https://rekrutacja.ukw.edu.pl/oferta/studia-pierwszego-stopnia/administracja#.ZFfbr3ZBw2w",1, "licencjat", "I stopnia"),
    ("Biologia", "https://rekrutacja.ukw.edu.pl/oferta/studia-pierwszego-stopnia/biologia-licencjackie#.ZFfcEHZBw2w",1, "licencjat", "I stopnia"),
    ("Informatyka", "https://sylabus.uj.edu.pl/pl/5/1/3/19/88?masterElement=19",2, "licencjat", "I stopnia"),
    ("Edytorstwo", "https://sylabus.uj.edu.pl/pl/5/1/3/21/92?masterElement=21",2, "licencjat", "I stopnia"),
    ("Architektura", "https://rekrutacja.p.lodz.pl/pl/architektura-i-stopnia-wydzial-budownictwa-architektury-i-inzynierii-srodowiska",3, "inżynier", "I stopnia"),
    ("Budownictwo", "https://rekrutacja.p.lodz.pl/pl/budownictwo-i-stopnia-wydzial-budownictwa-architektury-i-inzynierii-srodowiska",3, "inżynier", "I stopnia")
]

cursor.executemany(sql, values)
cnx.commit()

cursor.close()
cnx.close()
