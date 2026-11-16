
import tkinter as tk
from tkinter import ttk, messagebox
import library


class LibraryManagementSystem:

    def __init__(self, root):

        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("1150x750")
        self.root.minsize(950, 650)
        self.root.configure(bg="#F1F5F9")

        self.NAVY = "#172554"
        self.BLUE = "#2563EB"
        self.TEAL = "#0D9488"
        self.BG = "#F1F5F9"
        self.WHITE = "#FFFFFF"
        self.TEXT = "#1E293B"
        self.MUTED = "#64748B"

        self.setup_styles()
        self.create_sidebar()

        self.content = tk.Frame(root, bg=self.BG)
        self.content.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.show_dashboard()

    # TABLE STYLE
    def setup_styles(self):

        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background="#FFFFFF",
            foreground="#1E293B",
            fieldbackground="#FFFFFF",
            rowheight=35,
            font=("Arial", 10)
        )

        style.configure(
            "Treeview.Heading",
            background="#DBEAFE",
            foreground="#172554",
            font=("Arial", 10, "bold")
        )

        style.map(
            "Treeview",
            background=[("selected", "#BFDBFE")],
            foreground=[("selected", "#172554")]
        )

    # BUTTON
    def make_button(self, parent, text, command,
                    color=None, hover=None):

        color = color or self.BLUE
        hover = hover or "#1D4ED8"

        button = tk.Label(
            parent,
            text=text,
            bg=color,
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=12,
            cursor="hand2"
        )

        button.bind(
            "<Button-1>",
            lambda event: command()
        )

        button.bind(
            "<Enter>",
            lambda event: button.config(bg=hover)
        )

        button.bind(
            "<Leave>",
            lambda event: button.config(bg=color)
        )

        return button

    # INPUT
    def make_entry(self, parent):

        entry = tk.Entry(
            parent,
            font=("Arial", 13),
            bg="white",
            fg=self.TEXT,
            insertbackground=self.TEXT,
            relief="flat",
            highlightthickness=1,
            highlightbackground="#CBD5E1",
            highlightcolor=self.BLUE
        )

        entry.pack(
            fill="x",
            pady=(7, 20),
            ipady=10
        )

        return entry

    # SIDEBAR
    def create_sidebar(self):

        sidebar = tk.Frame(
            self.root,
            bg=self.NAVY,
            width=235
        )

        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(
            sidebar,
            text="📚 LIBRARY",
            font=("Arial", 21, "bold"),
            bg=self.NAVY,
            fg="white"
        ).pack(pady=(40, 8))

        tk.Label(
            sidebar,
            text="MANAGEMENT SYSTEM",
            font=("Arial", 9, "bold"),
            bg=self.NAVY,
            fg="#93C5FD"
        ).pack(pady=(0, 35))

        menu = [
            ("▦   Dashboard", self.show_dashboard),
            ("＋   Add Books", self.show_add_books),
            ("▤   View Books", self.show_view_books),
            ("⌕   Search Books", self.show_search_books),
            ("↗   Issue Books", self.show_issue_books),
            ("↩   Return Books", self.show_return_books)
        ]

        for name, command in menu:

            button = tk.Label(
                sidebar,
                text=name,
                font=("Arial", 12, "bold"),
                bg=self.NAVY,
                fg="#E2E8F0",
                anchor="w",
                padx=22,
                pady=15,
                cursor="hand2"
            )

            button.pack(fill="x", padx=10, pady=4)

            button.bind(
                "<Button-1>",
                lambda event, cmd=command: cmd()
            )

            button.bind(
                "<Enter>",
                lambda event, b=button: b.config(bg="#334477")
            )

            button.bind(
                "<Leave>",
                lambda event, b=button: b.config(bg=self.NAVY)
            )

    # CLEAR PAGE
    def clear_content(self):

        for widget in self.content.winfo_children():
            widget.destroy()

    # HEADER
    def create_header(self, title, subtitle=""):

        tk.Label(
            self.content,
            text=title,
            font=("Arial", 27, "bold"),
            fg=self.TEXT,
            bg=self.BG
        ).pack(anchor="w", padx=35, pady=(30, 5))

        if subtitle:
            tk.Label(
                self.content,
                text=subtitle,
                font=("Arial", 11),
                fg=self.MUTED,
                bg=self.BG
            ).pack(anchor="w", padx=35, pady=(5, 25))

    # DASHBOARD
    def show_dashboard(self):

        self.clear_content()

        self.create_header(
            "Dashboard",
            "Welcome to your Library Management System"
        )

        titles, copies, available, issued = (
            library.dashboard_information()
        )

        cards = tk.Frame(self.content, bg=self.BG)
        cards.pack(fill="x", padx=25)

        stats = [
            ("BOOK TITLES", titles, "#2563EB"),
            ("TOTAL COPIES", copies, "#7C3AED"),
            ("AVAILABLE", available, "#059669"),
            ("ISSUED BOOKS", issued, "#EA580C")
        ]

        for title, value, color in stats:

            card = tk.Frame(
                cards,
                bg="white",
                padx=18,
                pady=25,
                highlightbackground="#E2E8F0",
                highlightthickness=1
            )

            card.pack(
                side="left",
                fill="both",
                expand=True,
                padx=7
            )

            tk.Label(
                card,
                text=title,
                bg="white",
                fg=self.MUTED,
                font=("Arial", 9, "bold")
            ).pack(anchor="w")

            tk.Label(
                card,
                text=str(value),
                bg="white",
                fg=color,
                font=("Arial", 29, "bold")
            ).pack(anchor="w", pady=10)

        welcome = tk.Frame(
            self.content,
            bg="white",
            padx=30,
            pady=30
        )

        welcome.pack(
            fill="both",
            expand=True,
            padx=32,
            pady=30
        )

        tk.Label(
            welcome,
            text="Library Overview",
            bg="white",
            fg=self.TEXT,
            font=("Arial", 19, "bold")
        ).pack(anchor="w")

        tk.Label(
            welcome,
            text="Manage books, search your collection and track student transactions.",
            bg="white",
            fg=self.MUTED,
            font=("Arial", 11)
        ).pack(anchor="w", pady=15)

        self.make_button(
            welcome,
            "＋ Add New Book",
            self.show_add_books
        ).pack(anchor="w", pady=10)

    # ADD BOOKS
    def show_add_books(self):

        self.clear_content()

        self.create_header(
            "Add New Book",
            "Enter book details to add a new record"
        )

        form = tk.Frame(
            self.content,
            bg="white",
            padx=35,
            pady=30
        )

        form.pack(fill="x", padx=35)

        tk.Label(
            form,
            text="BOOK TITLE",
            bg="white",
            fg=self.TEXT,
            font=("Arial", 10, "bold")
        ).pack(anchor="w")

        self.title_entry = self.make_entry(form)

        tk.Label(
            form,
            text="AUTHOR NAME",
            bg="white",
            fg=self.TEXT,
            font=("Arial", 10, "bold")
        ).pack(anchor="w")

        self.author_entry = self.make_entry(form)

        tk.Label(
            form,
            text="QUANTITY",
            bg="white",
            fg=self.TEXT,
            font=("Arial", 10, "bold")
        ).pack(anchor="w")

        self.quantity_entry = self.make_entry(form)

        self.make_button(
            form,
            "＋ Add Book",
            self.save_book
        ).pack(anchor="w")

    def save_book(self):

        success, message = library.add_new_book(
            self.title_entry.get(),
            self.author_entry.get(),
            self.quantity_entry.get()
        )

        if success:

            messagebox.showinfo("Success", message)

            self.title_entry.delete(0, tk.END)
            self.author_entry.delete(0, tk.END)
            self.quantity_entry.delete(0, tk.END)

        else:
            messagebox.showerror("Error", message)

    # VIEW BOOKS
    def show_view_books(self):

        self.clear_content()

        self.create_header(
            "View All Books",
            "Complete list of books in the library"
        )

        frame = tk.Frame(
            self.content,
            bg="white",
            padx=15,
            pady=15
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=30
        )

        columns = (
            "ID", "Title", "Author", "Quantity", "Available"
        )

        self.book_table = ttk.Treeview(
            frame,
            columns=columns,
            show="headings"
        )

        for col in columns:
            self.book_table.heading(col, text=col)
            self.book_table.column(
                col,
                width=120,
                anchor="center"
            )

        scroll = ttk.Scrollbar(
            frame,
            orient="vertical",
            command=self.book_table.yview
        )

        self.book_table.configure(yscrollcommand=scroll.set)

        self.book_table.pack(
            side="left",
            fill="both",
            expand=True
        )

        scroll.pack(side="right", fill="y")

        self.make_button(
            self.content,
            "Refresh Books",
            self.refresh_books,
            self.TEAL,
            "#0F766E"
        ).pack(anchor="e", padx=35, pady=10)

        self.make_button(
            self.content,
            "Delete Selected Book",
            self.delete_selected_book,
            "#DC2626",
            "#B91C1C"
        ).pack(anchor="e", padx=35, pady=(0, 15))

        self.refresh_books()

    def refresh_books(self):

        for item in self.book_table.get_children():
            self.book_table.delete(item)

        for book in library.display_books():
            self.book_table.insert("", tk.END, values=book)

    def delete_selected_book(self):

        selected = self.book_table.selection()

        if not selected:
            messagebox.showwarning(
                "Select Book",
                "Please select a book first."
            )
            return

        book = self.book_table.item(selected[0])["values"]
        book_id = book[0]

        if not messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this book?"
        ):
            return

        success, message = library.remove_book(book_id)

        if success:
            messagebox.showinfo("Success", message)
            self.refresh_books()
        else:
            messagebox.showerror("Error", message)

    # SEARCH BOOKS
    def show_search_books(self):

        self.clear_content()

        self.create_header(
            "Search Books",
            "Search using a book title or author name"
        )

        form = tk.Frame(
            self.content,
            bg="white",
            padx=25,
            pady=25
        )

        form.pack(fill="x", padx=30)

        tk.Label(
            form,
            text="SEARCH BOOK",
            bg="white",
            fg=self.TEXT,
            font=("Arial", 10, "bold")
        ).pack(anchor="w")

        self.search_entry = self.make_entry(form)

        self.make_button(
            form,
            "Search",
            self.search_records
        ).pack(anchor="w")

        columns = (
            "ID", "Title", "Author", "Quantity", "Available"
        )

        self.search_table = ttk.Treeview(
            self.content,
            columns=columns,
            show="headings"
        )

        for col in columns:
            self.search_table.heading(col, text=col)
            self.search_table.column(
                col,
                width=120,
                anchor="center"
            )

        self.search_table.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=20
        )

    def search_records(self):

        keyword = self.search_entry.get().strip()

        for item in self.search_table.get_children():
            self.search_table.delete(item)

        results = library.search_book(keyword)

        for book in results:
            self.search_table.insert("", tk.END, values=book)

        if not results:
            messagebox.showinfo("Search", "No books found.")

    # ISSUE BOOKS
    def show_issue_books(self):

        self.clear_content()

        self.create_header(
            "Issue Books",
            "Register a book issued to a student"
        )

        form = tk.Frame(
            self.content,
            bg="white",
            padx=35,
            pady=30
        )
        form.pack(fill="x", padx=35)

        tk.Label(
            form,
            text="BOOK ID",
            bg="white",
            fg=self.TEXT,
            font=("Arial", 10, "bold")
        ).pack(anchor="w")

        self.issue_book_id = self.make_entry(form)

        tk.Label(
            form,
            text="STUDENT NAME",
            bg="white",
            fg=self.TEXT,
            font=("Arial", 10, "bold")
        ).pack(anchor="w")

        self.student_name = self.make_entry(form)

        tk.Label(
            form,
            text="STUDENT ID",
            bg="white",
            fg=self.TEXT,
            font=("Arial", 10, "bold")
        ).pack(anchor="w")

        self.student_id = self.make_entry(form)

        self.make_button(
            form,
            "Issue Book",
            self.process_issue
        ).pack(anchor="w")

    def process_issue(self):

        success, message = library.issue_library_book(
            self.issue_book_id.get(),
            self.student_name.get(),
            self.student_id.get()
        )

        if success:

            messagebox.showinfo("Success", message)

            self.issue_book_id.delete(0, tk.END)
            self.student_name.delete(0, tk.END)
            self.student_id.delete(0, tk.END)

        else:
            messagebox.showerror("Issue Failed", message)

    # RETURN BOOKS
    def show_return_books(self):

        self.clear_content()

        self.create_header(
            "Return Books",
            "View issued records and process returns"
        )

        form = tk.Frame(
            self.content,
            bg="white",
            padx=25,
            pady=20
        )
        form.pack(fill="x", padx=30)

        tk.Label(
            form,
            text="ENTER ISSUE ID",
            bg="white",
            fg=self.TEXT,
            font=("Arial", 10, "bold")
        ).pack(anchor="w")

        self.return_issue_id = self.make_entry(form)

        self.make_button(
            form,
            "Return Book",
            self.process_return,
            self.TEAL,
            "#0F766E"
        ).pack(anchor="w")

        columns = (
            "Issue ID", "Book", "Student",
            "Student ID", "Issue Date",
            "Return Date", "Status"
        )

        frame = tk.Frame(self.content, bg="white")
        frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=20
        )

        self.issue_table = ttk.Treeview(
            frame,
            columns=columns,
            show="headings"
        )

        for col in columns:
            self.issue_table.heading(col, text=col)
            self.issue_table.column(
                col,
                width=110,
                anchor="center"
            )

        self.issue_table.pack(
            fill="both",
            expand=True
        )

        self.refresh_issued_books()

    def process_return(self):

        success, message = library.return_library_book(
            self.return_issue_id.get()
        )

        if success:

            messagebox.showinfo("Success", message)

            self.return_issue_id.delete(0, tk.END)
            self.refresh_issued_books()

        else:
            messagebox.showerror("Return Failed", message)

    def refresh_issued_books(self):

        for item in self.issue_table.get_children():
            self.issue_table.delete(item)

        for record in library.display_issued_books():
            self.issue_table.insert("", tk.END, values=record)


# START APPLICATION
if __name__ == "__main__":

    library.initialize_library()

    root = tk.Tk()

    app = LibraryManagementSystem(root)

    root.mainloop()
