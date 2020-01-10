#! /usr/bin/env python3
import sqlite3 as sql
import logging
import json

logger = logging.getLogger(__name__)


class CancelledClassesDB(sql.Connection):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cur = self.cursor()
        self.cur.row_factory = sql.Row
        self.table_name = "cc_table"
        self.cur.execute("""SELECT COUNT(name),name 
                            FROM sqlite_master 
                            WHERE type='table' AND name='cc_table'
                            ;""")
        res = self.cur.fetchone()
        if res[0] == 1 and res[1] == "cc_table":
            logger.info("Table exists")
        else:
            logger.info("Table doesn't exist")
            logger.info("Creating it...")
            query = """CREATE TABLE 'cc_table' (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    class_name VARCHAR(50) NOT NULL,
                    event_type VARCHAR(50) NOT NULL,
                    day INTEGER NOT NULL,
                    month INTEGER NOT NULL,
                    year INTEGER NOT NULL,
                    hour INTEGER NOT NULL,
                    minute INTEGER NOT NULL
                    );"""
            logger.debug(f"Running query: {query}")
            try:
                self.cur.execute(query)
            except sql.OperationalError:
                logger.error("Error executing query")
            logger.info("Done")
        # Clear the buffer
        self.cur.fetchall()

    def get_all(self):
        query = "SELECT class_name, " \
                "event_type, day, " \
                "month, year, " \
                "hour, minute " \
                "FROM cc_table"
        res = self.cur.execute(query).fetchall()
        logger.info(f"Query result:\n {res}")
        return {"all_events": [dict(item) for item in res]}

    def close(self):
        self.cur.close()
        super().close()


if __name__ == "__main__":
    # logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    logger.addHandler(ch)
    db = CancelledClassesDB("cancelled_classes.db")
    db.get_all()
    exit(0)
