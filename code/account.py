from typing import Text
from flask_restful import Resource, reqparse
import sqlite3


class Account(Resource):
    TABLE_NAME = 'accounts'

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

   
    def get(self, id):
        account = self.find_by_id(id)
        if account:
            return account
        return {'message': 'Account not found'}, 404

    @classmethod
    def find_by_id(cls, id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table} WHERE id=?".format(table=cls.TABLE_NAME)
        result = cursor.execute(query, (id,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'account': {'id': row[0], 'name': row[1]}}

    def post(self, id):
        if self.find_by_id(id):
            return {'message': "An account with id '{}' already exists.".format(id)}

        data = Account.parser.parse_args()

        account = {'id': id, 'name': data['name']}

        try:
            Account.insert(account)
        except:
            return {"message": "An error occurred inserting the account."}

        return account

    @classmethod
    def insert(cls, account):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO {table} VALUES(?, ?)".format(table=cls.TABLE_NAME)
        cursor.execute(query, (account['id'], account['name']))

        connection.commit()
        connection.close()

    
    def delete(self, id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM {table} WHERE id=?".format(table=self.TABLE_NAME)
        cursor.execute(query, (id,))

        connection.commit()
        connection.close()

        return {'message': 'Account deleted'}

   
    def put(self, id):
        data = Account.parser.parse_args()
        account = self.find_by_id(id)
        updated_account = {'id': id, 'name': data['name']}
        if account is None:
            try:
                Account.insert(updated_account)
            except:
                return {"message": "An error occurred inserting the account."}
        else:
            try:
                Account.update(updated_account)
            except:
                return {"message": "An error occurred updating the account."}
        return updated_account

    @classmethod
    def update(cls, account):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE {table} SET name=? WHERE id=?".format(table=cls.TABLE_NAME)
        cursor.execute(query, (account['name'], account['id']))

        connection.commit()
        connection.close()


class AccountList(Resource):
    TABLE_NAME = 'accounts'

    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table}".format(table=self.TABLE_NAME)
        result = cursor.execute(query)
        accounts = []
        for row in result:
            accounts.append({'id': row[0], 'name': row[1]})
        connection.close()

        return {'accounts': accounts}