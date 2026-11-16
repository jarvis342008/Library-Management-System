
import sqlite3
from datetime import date
from contextlib import contextmanager

DB_NAME = "library.db"


@contextmanager
def connect_db():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")

    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


# CREATE TABLES
def initialize_db():

    with connect_db() as conn:

        conn.execute("""
            CREATE TABLE IF NOT EXISTS books (
                book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                available INTEGER NOT NULL
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS issued_books (
                issue_id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                student_name TEXT NOT NULL,
                student_id TEXT NOT NULL,
                issue_date TEXT NOT NULL,
                return_date TEXT,
                status TEXT DEFAULT 'Issued',
                FOREIGN KEY(book_id) REFERENCES books(book_id)
            )
        """)


# ADD BOOK
def add_book(title, author, quantity):

    with connect_db() as conn:

        conn.execute("""
            INSERT INTO books
            (title, author, quantity, available)
            VALUES (?, ?, ?, ?)
        """, (title, author, quantity, quantity))


# GET ALL BOOKS
def get_books():

    with connect_db() as conn:

        cursor = conn.execute("""
            SELECT book_id, title, author, quantity, available
            FROM books
            ORDER BY book_id
        """)

        return cursor.fetchall()


# SEARCH BOOKS
def search_books(keyword):

    with connect_db() as conn:

        cursor = conn.execute("""
            SELECT book_id, title, author, quantity, available
            FROM books
            WHERE title LIKE ? OR author LIKE ?
            ORDER BY book_id
        """, (f"%{keyword}%", f"%{keyword}%"))

        return cursor.fetchall()


# DELETE BOOK
def delete_book(book_id):

    with connect_db() as conn:

        cursor = conn.execute("""
            SELECT COUNT(*) FROM issued_books
            WHERE book_id = ? AND status = 'Issued'
        """, (book_id,))

        if cursor.fetchone()[0] > 0:
            return False, "This book has active issue records."

        cursor = conn.execute("""
            SELECT COUNT(*) FROM books WHERE book_id = ?
        """, (book_id,))

        if cursor.fetchone()[0] == 0:
            return False, "Book not found."

        conn.execute("""
            DELETE FROM books WHERE book_id = ?
        """, (book_id,))

        return True, "Book deleted successfully."


# ISSUE BOOK
def issue_book(book_id, student_name, student_id):

    with connect_db() as conn:

        cursor = conn.execute("""
            SELECT available FROM books
            WHERE book_id = ?
        """, (book_id,))

        book = cursor.fetchone()

        if book is None:
            return False, "Book not found."

        if book[0] <= 0:
            return False, "No copies are currently available."

        conn.execute("""
            INSERT INTO issued_books
            (book_id, student_name, student_id, issue_date, status)
            VALUES (?, ?, ?, ?, 'Issued')
        """, (
            book_id,
            student_name,
            student_id,
            str(date.today())
        ))

        conn.execute("""
            UPDATE books
            SET available = available - 1
            WHERE book_id = ?
        """, (book_id,))

        return True, "Book issued successfully!"


# RETURN BOOK
def return_book(issue_id):

    with connect_db() as conn:

        cursor = conn.execute("""
            SELECT book_id FROM issued_books
            WHERE issue_id = ? AND status = 'Issued'
        """, (issue_id,))

        record = cursor.fetchone()

        if record is None:
            return False, "Invalid issue ID or book already returned."

        book_id = record[0]

        conn.execute("""
            UPDATE issued_books
            SET status = 'Returned', return_date = ?
            WHERE issue_id = ? AND status = 'Issued'
        """, (str(date.today()), issue_id))

        conn.execute("""
            UPDATE books
            SET available = available + 1
            WHERE book_id = ?
        """, (book_id,))

        return True, "Book returned successfully!"


# GET ISSUED BOOKS
def get_issued_books():

    with connect_db() as conn:

        cursor = conn.execute("""
            SELECT
                i.issue_id,
                b.title,
                i.student_name,
                i.student_id,
                i.issue_date,
                COALESCE(i.return_date, '-'),
                i.status
            FROM issued_books i
            JOIN books b ON i.book_id = b.book_id
            ORDER BY i.issue_id DESC
        """)

        return cursor.fetchall()


# DASHBOARD STATISTICS
def get_dashboard_stats():

    with connect_db() as conn:

        titles = conn.execute("""
            SELECT COUNT(*) FROM books
        """).fetchone()[0]

        copies = conn.execute("""
            SELECT COALESCE(SUM(quantity), 0) FROM books
        """).fetchone()[0]

        available = conn.execute("""
            SELECT COALESCE(SUM(available), 0) FROM books
        """).fetchone()[0]

        issued = conn.execute("""
            SELECT COUNT(*) FROM issued_books
            WHERE status = 'Issued'
        """).fetchone()[0]

        return titles, copies, available, issued
