import flask
from flask_cors import CORS
import math
from flask import jsonify, request

app = flask.Flask(__name__)
CORS(app)

def calculate(a, b, c) -> dict:
    if a == b == c == 0:
        return {
            'x1': 0,
            'delta': 0,
            'n_results': 0,
            'complex': False
        }
    
    delta = b * b - (4 * a * c)
    is_complex = False
        
    if a == 0:
        x1 = -c / b

        return {
            'x1': x1,
            'delta': delta,
            'n_results': 1,
            'complex': is_complex
        }

    if delta < 0:
        real = -b / (2 * a)
        im = math.sqrt(-delta) / (2 * a)
        is_complex = True

        return {
            'real': real,
            'imaginary': im,
            'delta': delta,
            'n_results': 2,
            'complex': is_complex
        }
    
    elif delta == 0:
        x1 = -b / (2 * a)

        return {
            'x1': x1,
            'delta': delta,
            'n_results': 1,
            'complex': is_complex
        }

    sqrt_delta = math.sqrt(delta)
    x1 = (-b + sqrt_delta) / (2 * a)
    x2 = (-b - sqrt_delta) / (2 * a)
    
    return {
        'x1': x1,
        'x2': x2,
        'delta': delta,
        'n_results': 2,
        'complex': is_complex
    }

def valid_and_calc(a, b, c):
    coefs = ['a', 'b', 'c']
    
    for i, x in enumerate([a, b, c]):
        if x == '' or x == None:
            print(x)
            return (
                jsonify({
                    'error': f'Missing required field: {coefs[i]} = {x}'
                }),
                400
            )
        
        try:
            float(x)
        except:
            return (
                jsonify({
                    'error': f'Not a number: {coefs[i]} = {x}'
                }),
                400
            )

    a = float(a)
    b = float(b)
    c = float(c)

    if a == b == 0 and not c == 0:
        return (
            jsonify({
                'error': f'Absurd: {c} = 0'
            }),
            400
        )
    
    results = calculate(a, b, c)

    return (
        jsonify(results),
        200
    )

@app.route('/', methods=['GET'])
def get():
    args = request.args
    a, b, c = args.get('a'), args.get('b'), args.get('c')

    if a == b == c == None:
        return (
            jsonify({
                'message': 'This is the quadratic calculator API. To calculate, use GET or POST method and pass the coefficients a, b and c'
            }),
            200
        )
    
    return valid_and_calc(a, b, c)

@app.route('/', methods=['POST'])
def post():
    json = request.json
    a, b, c = json.get('a'), json.get('b'), json.get('c')
    
    return valid_and_calc(a, b, c)

if __name__ == '__main__':
    app.run(debug=True)