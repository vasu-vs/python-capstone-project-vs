import sqlite3


class BookDatabaseManager:

    def __init__(self, db_name="books.db"):
        self.db_name = db_name
        self.create_table()

    def connect(self):
        return sqlite3.connect(self.db_name)

    def create_table(self):
        with self.connect() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    price REAL NOT NULL,
                    in_stock INTEGER NOT NULL,
                    rating INTEGER NOT NULL
                )
            """)

            conn.commit()

    
    def insert_book(self, title, price, in_stock, rating):

        with self.connect() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO books (title, price, in_stock, rating)
                VALUES (?, ?, ?, ?)
            """, (title, price, in_stock, rating))

            conn.commit()

            return cursor.lastrowid

   
    def get_all_books(self):

        with self.connect() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM books")

            return [dict(row) for row in cursor.fetchall()]

   
    def get_book(self, book_id):

        with self.connect() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM books WHERE id = ?",
                (book_id,)
            )

            row = cursor.fetchone()

            return dict(row) if row else None

    # UPDATE
    def update_book(self, book_id, title, price, in_stock, rating):

        with self.connect() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE books
                SET title = ?, price = ?, in_stock = ?, rating = ?
                WHERE id = ?
            """, (title, price, in_stock, rating, book_id))

            conn.commit()

            return cursor.rowcount > 0

    
    def delete_book(self, book_id):

        with self.connect() as conn:
            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM books WHERE id = ?",
                (book_id,)
            )

            conn.commit()

            return cursor.rowcount > 0

    def clear_books(self):

        with self.connect() as conn:

            cursor = conn.cursor()

            cursor.execute("DELETE FROM books")

            conn.commit()



