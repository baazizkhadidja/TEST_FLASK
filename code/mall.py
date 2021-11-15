from typing import Text
from flask_restful import Resource, reqparse
import sqlite3


class Mall(Resource):
    TABLE_NAME = 'malls'

    parser = reqparse.RequestParser()
    parser.add_argument('id',
        type=int,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument('name',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument('id_account',
        type=int,
        required=True,
        help="This field cannot be left blank!"
    )


    def get(self, id):
        mall = self.find_by_id(id)
        if mall:
            return mall
        return {'message': 'Mall not found'}, 404

    @classmethod
    def find_by_id(cls, id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table} WHERE id=?".format(table=cls.TABLE_NAME)
        result = cursor.execute(query, (id,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'mall': {'id': row[0], 'name': row[1], 'id_account': row[2]}}

    def post(self, id):
        if self.find_by_id(id):
            return {'message': "A mall with id '{}' already exists.".format(id)}

        data = Mall.parser.parse_args()

        mall = {'id': id, 'name': data['name'], 'id_account': data['id_account']}

        try:
            Mall.insert(mall)
        except:
            return {"message": "An error occurred inserting the mall."}

        return mall

    @classmethod
    def insert(cls, mall):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO {table} VALUES(?, ?, ?)".format(table=cls.TABLE_NAME)
        cursor.execute(query, (mall['id'], mall['name'], mall['id_account']))

        connection.commit()
        connection.close()

    
    def delete(self, id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM {table} WHERE id=?".format(table=self.TABLE_NAME)
        cursor.execute(query, (id,))

        connection.commit()
        connection.close()

        return {'message': 'Mall deleted'}

    
    def put(self, id):
        data = Mall.parser.parse_args()
        mall = self.find_by_id(id)
        updated_mall = {'id': id, 'name': data['name'], 'account_id': data['account_id']}
        if mall is None:
            try:
                Mall.insert(updated_mall)
            except:
                return {"message": "An error occurred inserting the mall."}
        else:
            try:
                Mall.update(updated_mall)
            except:
                return {"message": "An error occurred updating the mall."}
        return updated_mall

    @classmethod
    def update(cls, mall):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE {table} SET name=? WHERE id=?".format(table=cls.TABLE_NAME)
        cursor.execute(query, (mall['name'], mall['id'], mall['account_id']))

        connection.commit()
        connection.close()


class MallList(Resource):
    TABLE_NAME = 'malls'

    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table}".format(table=self.TABLE_NAME)
        result = cursor.execute(query)
        malls = []
        for row in result:
            malls.append({'id': row[0], 'name': row[1], 'account_id':row[2]})
        connection.close()

        return {'malls': malls}