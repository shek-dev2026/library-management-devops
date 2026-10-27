from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


def init_db():
    with sqlite3.connect("library.db") as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL
            )
        """)


@app.route("/")
def home():
    with sqlite3.connect("library.db") as db:
        books = db.execute(
            "SELECT id, title, author FROM books"
        ).fetchall()

    return render_template("index.html", books=books)


@app.route("/add", methods=["POST"])
def add_book():
    title = request.form.get("title", "").strip()
    author = request.form.get("author", "").strip()

    if title and author:
        with sqlite3.connect("library.db") as db:
            db.execute(
                "INSERT INTO books (title, author) VALUES (?, ?)",
                (title, author)
            )

    return redirect("/")


@app.route("/delete/<int:book_id>", methods=["POST"])
def delete_book(book_id):
    with sqlite3.connect("library.db") as db:
        db.execute(
            "DELETE FROM books WHERE id = ?", (book_id,)
        )

    return redirect("/")


init_db()

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=False)