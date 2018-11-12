import mysql.connector
from urllib.request import urlopen
import json
from time import gmtime, strftime

class Algorithm:
    def init(self):
        books = open("books.txt", "r")
        return self.iterate_file(books)

    def iterate_file(self, books):
        for index, book in enumerate(books):
            print("{} {} {}".format("Przetwarzam", index, "książkę"))
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
        now = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        sql = "INSERT INTO books (title, author, category, epochs, photo, link_to_txt, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (data['title'], data['authors'][0]['name'], data['kinds'][0]['name'], data['epochs'][0]['name'], data['cover'], data['txt'], now)
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


algorithm = Algorithm()
algorithm.init()