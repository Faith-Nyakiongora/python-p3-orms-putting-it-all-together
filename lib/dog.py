import sqlite3

CONN = sqlite3.connect("lib/dogs.db")
CURSOR = CONN.cursor()


class Dog:
    def __init__(self, name, breed, id=None):
        self.id = id
        self.name = name
        self.breed = breed

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                breed TEXT
            )
        """
        CURSOR.execute(sql)

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS dogs
        """
        CURSOR.execute(sql)

    def save(self):
        if self.id is None:
            sql = """
                INSERT INTO dogs (name, breed)
                VALUES (?, ?)
            """
            CURSOR.execute(sql, (self.name, self.breed))
            self.id = CURSOR.lastrowid
        else:
            sql = """
                UPDATE dogs
                SET name=?, breed=?
                WHERE id=?
            """
            CURSOR.execute(sql, (self.name, self.breed, self.id))

    @classmethod
    def create(cls, name, breed):
        dog = Dog(name, breed)
        dog.save()
        return dog

    @classmethod
    def new_from_db(cls, row):
        id, name, breed = row
        return cls(name, breed, id)

    @classmethod
    def get_all(cls):
        sql = """
            SELECT * FROM dogs
        """
        rows = CURSOR.execute(sql).fetchall()
        return [cls.new_from_db(row) for row in rows]

    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT * FROM dogs
            WHERE name=?
        """
        row = CURSOR.execute(sql, (name,)).fetchone()
        if row:
            return cls.new_from_db(row)
        else:
            return None

    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT * FROM dogs
            WHERE id=?
        """
        row = CURSOR.execute(sql, (id,)).fetchone()
        if row:
            return cls.new_from_db(row)
        else:
            return None

    @classmethod
    def find_or_create_by(cls, name, breed):
        dog = cls.find_by_name(name)
        if dog is None:
            return cls.create(name, breed)
        return dog

    def update(self):
        if self.id is not None:
            self.save()
