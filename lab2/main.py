from flask import Flask, render_template, request, make_response

app = Flask(__name__)
application = app


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/args')
def args():
    return render_template('args.html', request=request)


@app.route('/headers')
def headers():
    return render_template('headers.html', request=request)


@app.route('/cookies')
def cookies():
    resp = make_response(render_template('cookies.html', request=request))
    if 'cookie' in request.cookies:
        resp.delete_cookie('cookie')
    else:
        resp.set_cookie('cookie', 'cock')
    return resp


@app.route('/form', methods=['GET', 'POST'])
def form():
    return render_template('form.html', request=request)


def do_calc(operand1, operand2, action):
    if not operand1 or not operand2 or not action:
        return ''
    res = 0
    match action:
        case '+':
            res = int(operand1) + int(operand2)
        case '-':
            res = int(operand1) - int(operand2)
        case '*':
            res = int(operand1) * int(operand2)
        case '/':
            res = int(operand1) / int(operand2)
    return res


@app.route('/calc')
def calc():
    operand1 = request.args.get('operand1')
    operand2 = request.args.get('operand2')
    action = request.args.get('action')

    result = do_calc(operand1, operand2, action)

    return render_template('calc.html', result=result)

@app.route('/form_phone', methods=['GET', 'POST'])
def form_phone():
    error_message = ''
    original_phone_number = ''
    formatted_phone_number = ''

    if request.method == 'POST':
        original_phone_number = request.form['param1']
        
        # Проверка валидности номера телефона
        
        for char in original_phone_number:
            if char not in '0123456789 ()-+.':
                error_message = "Недопустимый ввод. В номере телефона встречаются недопустимые символы."
                break
                
        if not error_message:        
            digits = ''.join(filter(str.isdigit, original_phone_number))
            if original_phone_number.startswith('+7') or original_phone_number.startswith('8'):
                if len(digits) != 11:
                    error_message = "Недопустимый ввод. Неверное количество цифр."
            else:
                if len(digits) != 10:
                    error_message = "Недопустимый ввод. Неверное количество цифр."

        # Форматирование номера телефона
        if not error_message:
            if digits.startswith('+7'):
                digits = digits[2:]
            elif digits.startswith(('7', '8')):
                digits = digits[1:]

            formatted_phone_number = f'8-{digits[:3]}-{digits[3:6]}-{digits[6:8]}-{digits[8:]}'

    return render_template('form_phone.html', error_message=error_message, original_phone_number=original_phone_number, formatted_phone_number=formatted_phone_number)


if __name__ == '__main__':
    app.run(debug=True)
