import mysql.connector
from urllib.request import urlopen
import json

class Algorithm:
    def init(self):
        books = open("books.txt", "r")
        return self.iterate_file(books)

    def iterate_file(self, books):
        for book in books:
            self.check_name_in_api(book)

    def check_name_in_api(self, book):
        book = book.replace(" ", "-").lower()

        try:
            data = urlopen("https://wolnelektury.pl/api/books/" + book)
            data = json.loads(data.read().decode())
            self.check_name_in_database(data)
        except:
            pass

    def check_name_in_database(self, data):
        db = self.get_db_connect()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM books WHERE title=%s", [(data['title'])])
        result = cursor.fetchone()

        if result == None:
            self.create_book_record_in_db(data)

    def create_book_record_in_db(self, data):
        db = self.get_db_connect()
        cursor = db.cursor()
        sql = "INSERT INTO books (title, author, category, epochs, photo, link_to_txt) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (data['title'], data['authors'][0]['name'], data['kinds'][0]['name'], data['epochs'][0]['name'], data['cover'], data['txt'])
        cursor.execute(sql, val)
        db.commit()


    def get_db_connect(self):
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database=""
        )
        return db





alg = Algorithm()
print(alg.init())