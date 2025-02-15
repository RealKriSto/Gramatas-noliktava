import tkinter as tk
from tkinter import messagebox

# Grāmatas informācijas
ebooks = [
    {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "description": "A novel about the American dream.", "price": "$10.99"},
    {"title": "1984", "author": "George Orwell", "description": "A dystopian novel about a totalitarian regime.", "price": "$8.99"},
    {"title": "To Kill a Mockingbird", "author": "Harper Lee", "description": "A novel about racial inequality.", "price": "$12.99"},
    {"title": "Moby Dick", "author": "Herman Melville", "description": "The tale of the hunt for the great white whale.", "price": "$15.99"},
    {"title": "Pride and Prejudice", "author": "Jane Austen", "description": "A novel about love and societal expectations.", "price": "$9.99"},
    {"title": "The Catcher in the Rye", "author": "J.D. Salinger", "description": "A story about teenage rebellion and identity.", "price": "$11.99"},
    {"title": "The Hobbit", "author": "J.R.R. Tolkien", "description": "A fantasy novel about a hobbit's adventure.", "price": "$14.99"},
    {"title": "War and Peace", "author": "Leo Tolstoy", "description": "A historical novel set during the Napoleonic Wars.", "price": "$19.99"},
    {"title": "The Odyssey", "author": "Homer", "description": "A Greek epic about the journey of Odysseus.", "price": "$13.99"},
    {"title": "Crime and Punishment", "author": "Fyodor Dostoevsky", "description": "A novel about guilt and redemption.", "price": "$16.99"},
    {"title": "The Divine Comedy", "author": "Dante Alighieri", "description": "A journey through Hell, Purgatory, and Paradise.", "price": "$18.99"},
    {"title": "Anna Karenina", "author": "Leo Tolstoy", "description": "A novel about love, marriage, and society.", "price": "$22.99"},
    {"title": "Frankenstein", "author": "Mary Shelley", "description": "A novel about scientific ambition and its consequences.", "price": "$12.49"},
    {"title": "Dracula", "author": "Bram Stoker", "description": "A gothic novel about the infamous vampire.", "price": "$14.29"},
    {"title": "The Picture of Dorian Gray", "author": "Oscar Wilde", "description": "A novel about beauty, corruption, and morality.", "price": "$11.99"},
    {"title": "Wuthering Heights", "author": "Emily Brontë", "description": "A tragic tale of love and revenge.", "price": "$13.49"},
]

class EbookStoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Grāmatu Noliktava")
        self.root.geometry("900x600")  

        self.title_label = tk.Label(self.root, text="Valmieras bibliotekas pārpalikušo e-grāmatu noliktava", font=("Arial", 18))
        self.title_label.pack(pady=10)

        # Grāmatu meklēšana
        search_frame = tk.Frame(self.root)
        search_frame.pack(side="top", anchor="ne", padx=20, pady=10)

        search_label = tk.Label(search_frame, text="Meklēt:", font=("Arial", 14, "bold"))
        search_label.pack(side="top", anchor="ne")

        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var, font=("Arial", 12))
        self.search_entry.pack(side="top", padx=10, pady=5)
        self.search_entry.bind("<KeyRelease>", self.update_search)

        add_book_button = tk.Button(self.root, text="Pievienot grāmatu", font=("Arial", 12), command=self.open_add_book_window)
        add_book_button.pack(side="top", anchor="nw", padx=20, pady=10)

        # Kods priekš "scrollbar" funkcionēšanas
        self.canvas = tk.Canvas(self.root)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar_y = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollbar_y.pack(side="right", fill="y")

        self.scrollbar_x = tk.Scrollbar(self.root, orient="horizontal", command=self.canvas.xview)
        self.scrollbar_x.pack(side="bottom", fill="x")

        self.canvas.config(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)

        self.books_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.books_frame, anchor="nw")

        self.books_frame.bind("<Configure>", self.on_frame_configure)

        self.canvas.bind("<Configure>", lambda event: self.create_book_cards())

        self.create_book_cards()

    def on_frame_configure(self, event=None):
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def create_book_cards(self):
        for widget in self.books_frame.winfo_children():
            widget.destroy()
        self.book_cards = []

        num_columns = 10

        # E-grāmatas dizains un informācija.
        for idx, ebook in enumerate(ebooks):
            row = idx // num_columns
            column = idx % num_columns

            book_card = tk.Frame(self.books_frame, width=200, height=200, relief="solid", borderwidth=2)
            book_card.grid_propagate(False) 

            book_card.grid(row=row, column=column, padx=10, pady=10)

            title_label = tk.Label(book_card, text=ebook["title"], font=("Arial", 12, "bold"), width=15, anchor="w")
            title_label.pack(pady=5)
            self.book_cards.append({"title_label": title_label, "ebook": ebook})

            author_label = tk.Label(book_card, text=f"Autors: {ebook['author']}", font=("Arial", 10))
            author_label.pack(pady=5)

            price_label = tk.Label(book_card, text=f"Cena: {ebook['price']}", font=("Arial", 10))
            price_label.pack(pady=5)

            view_button = tk.Button(book_card, text="Detaļas", command=lambda idx=idx: self.view_details(idx))
            view_button.pack(pady=5)

            remove_button = tk.Button(book_card, text="Dzēst grāmatu", fg="red",
                                        command=lambda idx=idx: self.remove_book(idx))
            remove_button.pack(pady=5)

    def remove_book(self, idx):
        response = messagebox.askyesno("Grāmatas dzēšana", "Vai tiešām vēlaties dzēst šo grāmatu?")
        if response:
            del ebooks[idx]
            self.create_book_cards()

    def update_search(self, event):
        query = self.search_var.get().lower()  
        for card in self.book_cards:
            title = card["ebook"]["title"].lower()
            if query in title:
                card["title_label"].config(bg="lightyellow")
            else:
                card["title_label"].config(bg="white")

    def view_details(self, idx):
        ebook = ebooks[idx]
        details = (f"Nosaukums: {ebook['title']}\n"
                   f"Autors: {ebook['author']}\n"
                   f"Apraksts: {ebook['description']}\n"
                   f"Cena: {ebook['price']}")
        messagebox.showinfo("E-Grāmatas detaļas", details)

    def open_add_book_window(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Pievienot grāmatu")
        add_window.geometry("400x300")

        tk.Label(add_window, text="Nosaukums:", font=("Arial", 12)).pack(pady=5)
        title_entry = tk.Entry(add_window, font=("Arial", 12))
        title_entry.pack(pady=5)

        tk.Label(add_window, text="Autors:", font=("Arial", 12)).pack(pady=5)
        author_entry = tk.Entry(add_window, font=("Arial", 12))
        author_entry.pack(pady=5)

        tk.Label(add_window, text="Cena:", font=("Arial", 12)).pack(pady=5)
        price_entry = tk.Entry(add_window, font=("Arial", 12))
        price_entry.pack(pady=5)

        tk.Label(add_window, text="Apraksts:", font=("Arial", 12)).pack(pady=5)
        description_entry = tk.Entry(add_window, font=("Arial", 12))
        description_entry.pack(pady=5)

        def save_book():
            new_book = {
                "title": title_entry.get(),
                "author": author_entry.get(),
                "price": price_entry.get(),
                "description": description_entry.get(),
            }
            ebooks.append(new_book)
            self.create_book_cards()
            add_window.destroy()

        tk.Button(add_window, text="Saglabāt", command=save_book, font=("Arial", 12)).pack(pady=10)

root = tk.Tk()
app = EbookStoreApp(root)
root.mainloop()
