import sqlite3
DATABASE_NAME = "colosseum.db"

def get_db():
    conn = sqlite3.connect(DATABASE_NAME)
    return conn

def create_tables():
    tables_users = [
        """     create table users (
                user_id integer primary key autoincrement,
                tg_id text unique NOT NULL,
                tg_num_phone text unique NOT NULL,
                tg_nick text,
                tg_chat_id TEXT UNIQUE NOT NULL,
                note TEXT
                );
        """]     
    tables_books = [
        """   
                create table books (
                book_id integer primary key autoincrement,
                name_book text NOT NULL unique,
                episode_num text NOT NULL,
                img_book blob NOT NULL,
                text_book text NOT NULL,
                date_add text NOT NULL,
                price_book text NOT NULL
                );
        """] 
    tables_purchases_books = [
        """
                create table purchases_books (
                purchase_id integer primary key autoincrement,
                id_tg int NOT NULL,
                id_book int NOT NULL,
                datatime_purchase text NOT NULL,
                foreign key (id_tg) references users (tg_id)
                foreign key (id_book) references books (book_id)
                );
        """]
    tables_bookmarks = [
        """
                create table bookmarks (
                bookmark_id integer primary key autoincrement,
                id_tg int NOT NULL,
                id_book int NOT NULL,
                position text NOT NULL,
                foreign key (id_tg) references users (tg_id)
                foreign key (id_book) references books (book_id)
                );
        """]
    tables_last_open= [
        """
                create table last_open (
                last_open_id integer primary key autoincrement,
                id_tg int NOT NULL,
                id_book int NOT NULL,
                last_open_book text NOT NULL,
                foreign key (id_tg) references users (tg_id)
                foreign key (id_book) references books (book_id)
                );
        """
    ]

    db = get_db()
    cursor = db.cursor()
    try:
        for table_users in tables_users:
            cursor.execute(table_users)
        
        for table_books in tables_books:
            cursor.execute(table_books)
        
        for table_purchases_books in tables_purchases_books:
            cursor.execute(table_purchases_books)
        
        for table_bookmarks in tables_bookmarks:
            cursor.execute(table_bookmarks)
        
        for table_last_open in tables_last_open:
            cursor.execute(table_last_open)
    except Exception:
        print("Таблицы существует")