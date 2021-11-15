from flask import Flask
from flask_restful import Api

from account import Account, AccountList
from mall import Mall, MallList
from unit import Unit, UnitList


app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True

api = Api(app)



api.add_resource(Account, '/account/<int:id>')
api.add_resource(AccountList, '/accounts')

api.add_resource(Mall, '/mall/<int:id>')
api.add_resource(MallList, '/malls')

api.add_resource(Unit, '/unit/<int:id>')
api.add_resource(UnitList, '/units')


if __name__ == '__main__':
    app.run(debug=True)  