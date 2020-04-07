import sqlite3
import os
import json
from src.structs import Object, Association

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

    def close(self):
        self.con.close()

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

    # def add_inverse_association(self, asoc):
    #     object_id1 = asoc.object_id1
    #     object_id2 = asoc.object_id2
    #     keys_values_json = json.dumps(asoc.keys_values)
    #
    #     # self.cur.execute("INSERT OR REPLACE INTO associations (object_id1, atype, object_id2, creation_time, "
    #     #                  "keys_values")
    #     self.cur.execute(
    #         "INSERT INTO associations (object_id1, atype, object_id2, creation_time, keys_values) VALUES (?, ?, ?, ?, ?)",
    #         [object_id1, asoc.atype, object_id2, asoc.creation_time, keys_values_json])
    #     self.con.commit()

    def delete_association(self, object_id1, association_type, object_id2):
        self.cur.execute("DELETE FROM associations WHERE object_id1 = ? AND atype = ? AND object_id2 = ?",
                         [object_id1, association_type, object_id2])
        self.con.commit()

    def change_association_type(self, object_id1, association_old_type, object_id2, association_new_type):
        self.cur.execute("UPDATE associations SET atype = ? WHERE object_id1 = ? AND atype = ? AND object_id2 = ?",
                         [association_new_type, object_id1, association_old_type, object_id2])
        self.con.commit()

    def get_associations(self, object_id1, association_type, objects_ids2, high, low):
        q = 'SELECT creation_time, keys_values FROM associations WHERE object_id1 = ? AND atype = ? AND object_id2 IN (%s)' % ',' \
            .join('?' for object_id in objects_ids2)
        arguments = [object_id1, association_type] + objects_ids2
        self.cur.execute(q, arguments)
        keys_values_json = self.cur.fetchall()
        assocs = []
        print(keys_values_json)
        if keys_values_json is not None:
            index = 0
            for i in keys_values_json:
                assocs.append(Association(object_id1, association_type, objects_ids2[index], i[0], json.loads(i[1])))
                #assocs.append(json.loads(i[0]))
        return assocs
