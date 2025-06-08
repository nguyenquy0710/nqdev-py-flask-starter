import sqlite3
from app.config import Config, logger

_current_db_path = Config.DB_PATH  # dùng mặc định


def set_db_path(path):
    global _current_db_path
    _current_db_path = path


def init_sqlite_db():
    conn = sqlite3.connect(_current_db_path)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS symbols (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT UNIQUE,
            buy_price REAL,
            sell_price REAL,
            profit_loss REAL
        )
    """)
    conn.commit()

    # Check if "MBB" exists and add it if it doesn't
    if not c.execute("SELECT 1 FROM symbols WHERE symbol = ?", ("MBB",)).fetchone():
        add_symbol("MBB", buy_price=21.125,
                   sell_price=24.500, profit_loss=15.98)

    if not c.execute("SELECT 1 FROM symbols WHERE symbol = ?", ("ACB",)).fetchone():
        add_symbol("ACB", buy_price=19.621,
                   sell_price=26.650, profit_loss=14.69)

    if not c.execute("SELECT 1 FROM symbols WHERE symbol = ?", ("PNJ",)).fetchone():
        add_symbol("PNJ", buy_price=92.708,
                   sell_price=100.000, profit_loss=10.0)

    if not c.execute("SELECT 1 FROM symbols WHERE symbol = ?", ("OCB",)).fetchone():
        add_symbol("OCB", buy_price=11.159,
                   sell_price=12.500, profit_loss=10.0)

    conn.close()
    logger.info("Symbols database initialized successfully")


def add_symbol(symbol, buy_price, sell_price, profit_loss):
    conn = sqlite3.connect(_current_db_path)
    try:
        conn.execute("INSERT INTO symbols (symbol, buy_price, sell_price, profit_loss) VALUES (?, ?, ?, ?)",
                     (symbol, buy_price, sell_price, profit_loss))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    conn.close()


def get_all_symbols():
    conn = sqlite3.connect(_current_db_path)
    symbols = [row[0] for row in conn.execute("SELECT symbol FROM symbols")]
    conn.close()
    return symbols


def delete_symbol(symbol):
    conn = sqlite3.connect(_current_db_path)
    conn.execute("DELETE FROM symbols WHERE symbol = ?", (symbol,))
    conn.commit()
    conn.close()


def get_symbol_info_all():
    conn = sqlite3.connect(_current_db_path)
    c = conn.cursor()
    c.execute("SELECT symbol, buy_price, sell_price, profit_loss FROM symbols")
    rows = c.fetchall()
    conn.close()
    return {r[0]: {"buy_price": r[1], "sell_price": r[2], "profit_loss": r[3]} for r in rows}
