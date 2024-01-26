import os
from tinydb import TinyDB, Query
from serializer import serializer
from validate_email_address import validate_email

class User:
    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json'), storage=serializer).table('users')

    def __init__(self, id, name) -> None:
        self.name = name
        self.id = id

    def __str__(self):
        return f'User {self.id} ({self.name})'

    def store_data(self):
        print("Storing user data...")

        # Überprüfen, ob der Benutzer bereits existiert
        user_query = Query()
        existing_user = self.db_connector.search(user_query.name == self.name)

        if existing_user:
            print("User already exists.")
        else:
            # Wenn der Benutzer nicht existiert, in die Datenbank schreiben
            self.db_connector.insert({'name': self.name, 'id': self.id})
            print("User data inserted.")

    @classmethod
    def user_exists(cls, user_name):
        print("Checking if user exists...")
        user_query = Query()
        result = cls.db_connector.search(user_query.name == user_name)

        if result:
            print("User already exists.")
            return True
        else:
            print("User does not exist.")
            return False
        
    @classmethod
    def validate_and_create_user(cls, user_name, email):
        # Überprüfen, ob beide Felder ausgefüllt sind
        if not user_name.strip() or not email.strip():
            return "Bitte fülle beide Felder aus."

        # Überprüfen, ob die E-Mail-Adresse gültig ist und die gewünschte Endung hat
        if not validate_email(email) or not email.endswith((".at", ".de", ".com")):

            return "Ungültige E-Mail-Adresse oder falsche Endung."

        # Überprüfen, ob der Benutzer bereits existiert
        if cls.user_exists(email):
            return "Nutzer mit dieser E-Mail existiert bereits!"

        # Wenn alles in Ordnung ist, neuen Benutzer erstellen und speichern
        new_user = cls(user_name, email)
        new_user.store_data()
        return "Nutzer erfolgreich angelegt."