class DatabaseError(Exception):
    def __init__(self):
        super().__init__("Greška s bazom podataka.")
