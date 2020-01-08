#! /usr/bin/env python3
import sqlite3 as sql
import logging

logger = logging.Logger


class CancelledClassesDB(sql.Connection):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cur = self.cursor()
        self.table_name = "cc_table"
        self.cur.execute("""SELECT COUNT(name),name FROM sqlite_master WHERE type='table' AND name='cc_table';""")
        res = self.cur.fetchone()
        if res[0] == 1 and res[1] == "cc_table":
            logger.info("Table exists")
        else:
            logger.info("Table doesn't exist")
            logger.info("Creating it...")
            self.cur.execute("""CREATE TABLE 'cc_table' (
                                    ID INTEGER PRIMARY KEY AUTOINCREMENT, 
                                    class_name VARCHAR(50) NOT NULL,
                                    event_type VARCHAR(50) NOT NULL,
                                    date DATE NOT NULL,
                                    time TIME NOT NULL
                                )""")
            logger.info("Done")
        # Clear the buffer
        self.cur.fetchall()

    def get_all(self):
        query = "SELECT "


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    logger.addHandler(ch)
    db = CancelledClassesDB("cancelled_classes.db")
    exit(0)
