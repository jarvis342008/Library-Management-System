
import database


def initialize_library():
    database.initialize_db()


# ADD BOOK
def add_new_book(title, author, quantity):

    title = title.strip()
    author = author.strip()

    if not title or not author:
        return False, "Please enter book title and author."

    try:
        quantity = int(quantity)

        if quantity <= 0:
            return False, "Quantity must be greater than zero."

        database.add_book(title, author, quantity)

        return True, "Book added successfully!"

    except ValueError:
        return False, "Quantity must be a valid number."

    except Exception as error:
        return False, str(error)


# VIEW BOOKS
def display_books():
    return database.get_books()


# SEARCH BOOKS
def search_book(keyword):
    return database.search_books(keyword.strip())


# DELETE BOOK
def remove_book(book_id):

    try:
        book_id = int(book_id)

        if book_id <= 0:
            return False, "Invalid book ID."

        return database.delete_book(book_id)

    except ValueError:
        return False, "Enter a valid book ID."

    except Exception as error:
        return False, str(error)


# ISSUE BOOK
def issue_library_book(book_id, student_name, student_id):

    student_name = student_name.strip()
    student_id = student_id.strip()

    if not student_name or not student_id:
        return False, "Enter student name and student ID."

    try:
        book_id = int(book_id)

        if book_id <= 0:
            return False, "Invalid book ID."

        return database.issue_book(
            book_id,
            student_name,
            student_id
        )

    except ValueError:
        return False, "Enter a valid book ID."

    except Exception as error:
        return False, str(error)


# RETURN BOOK
def return_library_book(issue_id):

    try:
        issue_id = int(issue_id)

        if issue_id <= 0:
            return False, "Invalid issue ID."

        return database.return_book(issue_id)

    except ValueError:
        return False, "Enter a valid issue ID."

    except Exception as error:
        return False, str(error)


# VIEW ISSUE RECORDS
def display_issued_books():
    return database.get_issued_books()


# DASHBOARD
def dashboard_information():
    return database.get_dashboard_stats()
