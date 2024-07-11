from flask import Flask, request, render_template, jsonify
import unicodedata

app = Flask(__name__)

keypad = {
    '1': '.,?!:',
    '2': 'abc',
    '3': 'def',
    '4': 'ghi',
    '5': 'jkl',
    '6': 'mno',
    '7': 'pqrs',
    '8': 'tuv',
    '9': 'wxyz',
    '0': ' '
}

reverse_keypad = {char: (key, index + 1) for key, chars in keypad.items() for index, char in enumerate(chars)}

def encrypt(message):
    encrypted_message = ''
    for char in message.lower():
        for key, chars in keypad.items():
            if char in chars:
                encrypted_message += key * (chars.index(char) + 1) + ' '
                break
    return encrypted_message.strip()

def decrypt(encrypted_message):
    decrypted_message = ''
    tokens = encrypted_message.split()
    for token in tokens:
        key = token[0]
        count = len(token)
        for char, (k, cnt) in reverse_keypad.items():
            if k == key and cnt == count:
                decrypted_message += char
                break
    return decrypted_message

def remove_special_characters(message):
    string = unicodedata.normalize('NFKD', message).encode('ASCII', 'ignore').decode('ASCII')
    return string

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    message = request.form['message']
    message = remove_special_characters(message)
    if not all(char.isdigit() or char.isspace() for char in message):
        result = encrypt(message)
    else:
        result = decrypt(message)
    return jsonify(result=result)

if __name__ == '__main__':
    app.run(debug=True)
