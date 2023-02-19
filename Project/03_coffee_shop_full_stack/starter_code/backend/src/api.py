import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS


from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
   uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
# db_drop_and_create_all()

# ROUTES
'''
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks")
def get_drinks():
    try:
        drinks = Drink.query.order_by(Drink.id).all()
        short_drinks = [drink.short() for drink in drinks]
        if len(drinks) == 0:
            abort(404)
        return jsonify(
            {
                "success": True,
                "drinks": short_drinks,
            }
        )
    except Exception as e:
        if hasattr(e, 'code') and e.code == 404:
            abort(404)
        else:
            abort(422)

'''
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks-detail")
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    try:
        drinks = Drink.query.order_by(Drink.id).all()
        long_drinks = [drink.long() for drink in drinks]
        if len(drinks) == 0:
            abort(404)
        return jsonify(
            {
                "success": True,
                "drinks": long_drinks,
            }
        )
    except Exception as e:
        if hasattr(e, 'code') and e.code == 401:
            abort(401)
        if hasattr(e, 'code') and e.code == 404:
            abort(404)
        else:
            abort(422)

'''
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks", methods=["POST"])
@requires_auth('post:drinks')
def create_drink(payload):
    try:
        body = request.get_json()
        new_drink_title = body.get("title", None)
        new_drink_recipe = body.get("recipe", None)
        if new_drink_title is None or new_drink_title == "":
            abort(422)
        if new_drink_recipe is None or new_drink_recipe == "":
            abort(422)
        drink_entity = Drink(title=new_drink_title, recipe=json.dumps(new_drink_recipe))
        drink_entity.insert()
        return jsonify(
            {
                "success": True,
                "drinks": drink_entity.long()
            }
        )
    except Exception as e:
        if hasattr(e, 'code') and e.code == 401:
            abort(401)
        if hasattr(e, 'code') and e.code == 404:
            abort(404)
        else:
            abort(422)

'''
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks/<drink_id>", methods=["PATCH"])
@requires_auth('patch:drinks')
def update_drink(payload, drink_id):
    try:
        drink_id = int(drink_id)
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
        if drink is None:
            abort(404)
        body = request.get_json()
        new_drink_title = body.get("title", None)
        new_drink_recipe = body.get("recipe", None)
        if new_drink_title is None and new_drink_recipe is None:
            abort(422)
        if new_drink_title != "":
            drink.title = new_drink_title
        if new_drink_recipe != "":
            drink.recipe = json.dumps(new_drink_recipe)
        drink.update()
        return jsonify(
            {
                "success": True,
                "drinks": [drink.long()]
            }
        )
    except Exception as e:
        if hasattr(e, 'code') and e.code == 401:
            abort(401)
        if hasattr(e, 'code') and e.code == 404:
            abort(404)
        else:
            abort(422)


'''
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks/<drink_id>", methods=["DELETE"])
@requires_auth('delete:drinks')
def delete_question(payload, drink_id):
    try:
        drink_id = int(drink_id)
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
        if drink is None:
            abort(404)
        drink.delete()
        return jsonify(
            {
                "success": True,
                "delete": drink_id,
            }
        )
    except Exception as e:
        if hasattr(e, 'code') and e.code == 404:
            abort(404)
        else:
            abort(422)


'''
error handlers using the @app.errorhandler(error) decorator
each error handler should return (with approprate messages):
            jsonify({
                "success": False,
                "error": 404,
                "message": "resource not found"
                }), 404

'''

# Error Handling
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

'''
    error handler for 404
    error handler should conform to general task above
'''
@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

'''
    error handler for AuthError
    error handler should conform to general task above
'''

@app.errorhandler(AuthError)
def auth_error(ex):
    return jsonify({
        "success": False,
        "error": ex.code,
        "message": str(ex.description) # did not manage to extract the description only
    }), ex.code