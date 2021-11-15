from typing import Text
from flask_restful import Resource, reqparse
import sqlite3


class Unit(Resource):
    TABLE_NAME = 'units'

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

    parser.add_argument('mall_id',
        type=int,
        required=True,
        help="This field cannot be left blank!"
    )

    def get(self, id):
        unit = self.find_by_id(id)
        if unit:
            return unit
        return {'message': 'unit not found'}, 404

    @classmethod
    def find_by_id(cls, id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table} WHERE id=?".format(table=cls.TABLE_NAME)
        result = cursor.execute(query, (id,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'unit': {'id': row[0], 'name': row[1], 'mall_id': row[2]}}

    def post(self, id):
        if self.find_by_id(id):
            return {'message': "A unit with id '{}' already exists.".format(id)}

        data = Unit.parser.parse_args()

        unit = {'id': id, 'name': data['name'], 'mall_id':data['mall_id']}

        try:
            Unit.insert(unit)
        except:
            return {"message": "An error occurred inserting the unit."}

        return unit

    @classmethod
    def insert(cls, unit):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO {table} VALUES(?, ?, ?)".format(table=cls.TABLE_NAME)
        cursor.execute(query, (unit['id'], unit['name'], unit['mall_id']))

        connection.commit()
        connection.close()

    
    def delete(self, id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM {table} WHERE id=?".format(table=self.TABLE_NAME)
        cursor.execute(query, (id,))

        connection.commit()
        connection.close()

        return {'message': 'Unit deleted'}

    
    def put(self, id):
        data = Unit.parser.parse_args()
        unit = self.find_by_id(id)
        updated_unit = {'id': id, 'name': data['name'], 'mall_id': data['mall_id']}
        if unit is None:
            try:
                Unit.insert(updated_unit)
            except:
                return {"message": "An error occurred inserting the unit."}
        else:
            try:
                Unit.update(updated_unit)
            except:
                return {"message": "An error occurred updating the unit."}
        return updated_unit

    @classmethod
    def update(cls, unit):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE {table} SET name=? WHERE id=?".format(table=cls.TABLE_NAME)
        cursor.execute(query, (unit['name'], unit['id'], unit['mall_id']))

        connection.commit()
        connection.close()


class UnitList(Resource):
    TABLE_NAME = 'units'

    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table}".format(table=self.TABLE_NAME)
        result = cursor.execute(query)
        units = []
        for row in result:
            units.append({'id': row[0], 'name': row[1], 'mall_id': row[2]})
        connection.close()

        return {'units': units}