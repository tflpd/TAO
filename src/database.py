import sqlite3
import os
import json
from enum import Enum

from src.structs import Object, Association, invert_assoc

DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'db.sqlite3')


def connect_db(db_path=DEFAULT_PATH):
    con = sqlite3.connect(db_path)
    return con


class Database:
    def __init__(self):
        self.con = sqlite3.connect(DEFAULT_PATH)
        self.cur = self.con.cursor()
        self.cur.execute('DROP TABLE IF EXISTS objects')
        self.cur.execute('DROP TABLE IF EXISTS associations')
        self.cur.execute('''
                  CREATE TABLE IF NOT EXISTS objects
                  (object_id INTEGER PRIMARY KEY ASC,
                   otype VARCHAR(250) NOT NULL,
                   keys_values VARCHAR(250) NOT NULL)
                  ''')
        self.cur.execute('''
                  CREATE TABLE IF NOT EXISTS associations
                  (object_id1 INTEGER NOT NULL,
                   atype VARCHAR(250) NOT NULL,
                   object_id2 INTEGER NOT NULL,
                   creation_time INTEGER NOT NULL,
                   keys_values VARCHAR(250) NOT NULL,
                   PRIMARY KEY (object_id1, atype, object_id2));
                  ''')
        self.con.commit()

    # Helper methods

    def close(self):
        self.con.close()

    def get_all_associations(self):
        q = 'SELECT * FROM associations'
        self.cur.execute(q)
        keys_values_json = self.cur.fetchall()
        assocs = []
        if keys_values_json is not None:
            for i in keys_values_json:
                assocs.append(Association(i[0], i[1], i[2], i[3], json.loads(i[4])))
        return assocs

    # TAO official API endpoints

    def create_object(self, obj):
        keys_values_json = json.dumps(obj.keys_values)
        # self.cur.execute("INSERT OR REPLACE INTO objects (object_id, keys_values) VALUES (?, ?)", [object_id, keys_values_json])
        self.cur.execute("INSERT INTO objects (object_id, otype, keys_values) VALUES (?, ?, ?)",
                         [obj.object_id, obj.otype, keys_values_json])
        self.con.commit()

    def retrieve_object(self, object_id):
        self.cur.execute("SELECT otype, keys_values FROM objects WHERE object_id = ?", [object_id])
        self.con.commit()
        keys_values_json = self.cur.fetchone()
        if keys_values_json is not None:
            # return keys_values_json
            # return json.loads(keys_values_json[0]), keys_values_json[1]
            return Object(object_id, keys_values_json[0], json.loads(keys_values_json[1]))
        return None

    def update_object(self, obj):
        keys_values_json = json.dumps(obj.keys_values)
        # self.cur.execute("INSERT OR REPLACE INTO objects (object_id, keys_values) VALUES (?, ?)", [object_id, keys_values_json])
        self.cur.execute("INSERT OR REPLACE INTO objects (object_id, otype, keys_values) VALUES (?, ?, ?)",
                         [obj.object_id, obj.otype, keys_values_json])
        self.con.commit()

    def delete_object(self, obj):
        self.cur.execute("DELETE FROM objects WHERE object_id = ?", [obj.object_id])
        self.con.commit()

    def add_association(self, asoc):
        object_id1 = asoc.object_id1
        object_id2 = asoc.object_id2
        keys_values_json = json.dumps(asoc.keys_values)
        # self.cur.execute("INSERT OR REPLACE INTO associations (object_id1, atype, object_id2, creation_time, "
        #                  "keys_values")
        self.cur.execute(
            "INSERT INTO associations (object_id1, atype, object_id2, creation_time, keys_values) VALUES (?, ?, ?, ?, ?)",
            [object_id1, asoc.atype, object_id2, asoc.creation_time, keys_values_json])
        self.con.commit()
        self.add_inverse_association(asoc)

    def add_inverse_association(self, asoc):
        object_id1 = asoc.object_id1
        object_id2 = asoc.object_id2
        keys_values_json = json.dumps(asoc.keys_values)
        atype = invert_assoc(asoc.atype)

        # self.cur.execute("INSERT OR REPLACE INTO associations (object_id1, atype, object_id2, creation_time, "
        #                  "keys_values")
        self.cur.execute(
            "INSERT INTO associations (object_id1, atype, object_id2, creation_time, keys_values) VALUES (?, ?, ?, ?, ?)",
            [object_id2, atype, object_id1, asoc.creation_time, keys_values_json])
        self.con.commit()

    def delete_association(self, object_id1, association_type, object_id2):
        self.cur.execute("DELETE FROM associations WHERE object_id1 = ? AND atype = ? AND object_id2 = ?",
                         [object_id1, association_type, object_id2])
        self.con.commit()

    def change_association_type(self, object_id1, association_old_type, object_id2, association_new_type):
        self.cur.execute("UPDATE associations SET atype = ? WHERE object_id1 = ? AND atype = ? AND object_id2 = ?",
                         [association_new_type, object_id1, association_old_type, object_id2])
        self.con.commit()

    def get_associations(self, object_id1, association_type, objects_ids2, low=None, high=None):
        if low is None and high is None:
            q = 'SELECT creation_time, keys_values FROM associations WHERE object_id1 = ? AND atype = ? AND object_id2 IN (%s)' % ','.join(
                '?' for object_id in objects_ids2)
            arguments = [object_id1, association_type] + objects_ids2
        elif low is not None and high is not None:
            if low < 0 or low > high:
                raise ValueError("Both low and high have to be positive. Also low must be <= high")
            q = 'SELECT creation_time, keys_values FROM associations WHERE object_id1 = ? AND atype = ? AND creation_time >= ?' \
                ' AND creation_time <= ? AND object_id2 IN (%s)' % ','.join('?' for object_id in objects_ids2)
            arguments = [object_id1, association_type, low, high] + objects_ids2
        else:
            raise ValueError("Either both low and high should be none or nor")
        q += ' ORDER BY creation_time DESC'
        self.cur.execute(q, arguments)
        keys_values_json = self.cur.fetchall()
        assocs = []
        if keys_values_json is not None:
            index = 0
            for i in keys_values_json:
                assocs.append(Association(object_id1, association_type, objects_ids2[index], i[0], json.loads(i[1])))
        return assocs

    def count_associations(self, object_id1, association_type):
        q = 'SELECT COUNT(object_id1) FROM associations WHERE object_id1 = ? AND atype = ?'
        arguments = [object_id1, association_type]
        self.cur.execute(q, arguments)
        keys_values_json = self.cur.fetchall()
        if keys_values_json is not None:
            return keys_values_json[0]
        return 0

    def get_associations_range(self, object_id1, association_type, pos, limit):
        if pos < 0 or limit < 0:
            raise ValueError("Both pos and limit have to be negative")
        q = 'SELECT object_id2, creation_time, keys_values FROM associations WHERE object_id1 = ? AND atype = ?'
        q += ' ORDER BY creation_time DESC'
        arguments = [object_id1, association_type]
        self.cur.execute(q, arguments)
        keys_values_json = self.cur.fetchall()
        assocs = []
        if keys_values_json is not None:
            for i in keys_values_json:
                assocs.append(Association(object_id1, association_type, i[0], i[1], json.loads(i[2])))
            assocs = assocs[pos: pos + limit]
        return assocs

    def get_associations_time_range(self, object_id1, association_type, low, high, limit):
        if low < 0 or low > high:
            raise ValueError("Both low and high have to be positive. Also low must be <= high")
        q = 'SELECT object_id2, creation_time, keys_values FROM associations WHERE object_id1 = ? AND atype = ? AND creation_time BETWEEN ? AND ?'
        q += ' ORDER BY creation_time DESC'
        arguments = [object_id1, association_type, low, high]
        self.cur.execute(q, arguments)
        keys_values_json = self.cur.fetchall()
        assocs = []
        if keys_values_json is not None:
            for i in keys_values_json:
                assocs.append(Association(object_id1, association_type, i[0], i[1], json.loads(i[2])))
            if limit < len(assocs):
                return assocs[0: limit]
        return assocs
