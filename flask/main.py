import flask
from flask_cors import CORS
from math import sqrt
from flask import jsonify, request

app = flask.Flask(__name__)
CORS(app)

def calculate(a, b, c) -> dict:
    output = 'Equation solution:\n\nax^2 + bx + c = 0\n\n---\n\n'

    if a == 0:
        output += 'bx + c = 0\n\n'
        output += f'{b}x + {c} = 0\n\n'
        output += f'{b}x = {-c}\n\n'
        output += f'x = {-c}/{b}\n\n'
        output += f'x = {-c/b}\n\n'
        
        print(output)
        return {'text': output}
    
    output += 'x = (-b +- sqrt( b^2 - 4 * a * c )) / (2 * a)\n\n'
    output += f'x = (-{b} +- sqrt( {b}^2 - 4 * {a} * {c} )) / (2 * {a})\n\n'
    
    minus_b = -b
    b_sqr = b*b
    two_a = 2 * a
    output += f'x = ({minus_b} +- sqrt( {b_sqr} - ({4 * a * c}) )) / ({two_a})\n\n'
    
    delta = b_sqr - (4 * a * c)
    output += f'x = ({minus_b} +- sqrt( {delta} )) / ({two_a})\n\n'

    if delta >= 0:

        output += f'x = {minus_b / two_a} +- {sqrt(delta) / two_a}\n\n'
        output += f'x1 = {minus_b / two_a} + {sqrt(delta) / two_a}\n\n'
        output += f'x1 = {minus_b / two_a + sqrt(delta) / two_a}\n\n'
        output += f'x2 = {minus_b / two_a} - {sqrt(delta) / two_a}\n\n'
        output += f'x2 = {minus_b / two_a - sqrt(delta) / two_a}\n\n'
        
    else:
        
        output += f'x = ({minus_b} +- sqrt( {-delta} * -1 )) / ({two_a})\n\n'
        output += f'x = ({minus_b} +- sqrt({-delta}) * i) / ({two_a})\n\n'
        output += f'x = {minus_b / two_a} +- {sqrt(-delta) / two_a} * i\n\n'
        output += f'x1 = {minus_b / two_a} + {sqrt(-delta) / two_a} * i\n\n'
        output += f'x2 = {minus_b / two_a} - {sqrt(-delta) / two_a} * i\n\n'

    print(output)
    return {'text': output}


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