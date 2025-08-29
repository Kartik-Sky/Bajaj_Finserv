from flask import Flask, request, jsonify
from datetime import datetime
import os

app = Flask(__name__)

def is_number(s):
    return s.lstrip('-').isdigit()

def is_alphabet(s):
    return s.isalpha()


def is_special_character(s):
    return not s.isalnum()


def create_alternating_caps(alphabets):
    
    all_chars = []
    for item in alphabets:
        for ch in item:
            if ch.isalpha():
                all_chars.append(ch.lower())

    
    all_chars.reverse()

    
    result = ""
    for i, ch in enumerate(all_chars):
        if i % 2 == 1:
            result += ch.lower()
        else:
            result += ch.upper()

    return result


@app.route('/bfhl', methods=['POST'])
def bfhl_post():
    try:
        data = request.get_json()

        if not data or "data" not in data or not isinstance(data["data"], list):
            return jsonify({
                "is_success": False,
                "error": "Invalid input: 'data' should be an array"
            }), 400

        input_data = data["data"]
        odd_numbers, even_numbers, alphabets, special_chars = [], [], [], []
        total_sum = 0

        for item in input_data:
            item_str = str(item)
            if is_number(item_str):
                num = int(float(item_str))
                if num % 2 == 0:
                    even_numbers.append(item_str)
                else:
                    odd_numbers.append(item_str)
                total_sum += num
            elif is_alphabet(item_str):
                alphabets.append(item_str.upper())
            elif is_special_character(item_str):
                special_chars.append(item_str)

        concat_string = create_alternating_caps(alphabets)

        response = {
            "is_success": True,
            "user_id": "kartik_goyal_18022005",
            "email": "kartik.goyal2022@vitstudent.ac.in",
            "roll_number": "22BCE1638",
            "odd_numbers": odd_numbers,
            "even_numbers": even_numbers,
            "alphabets": alphabets,
            "special_characters": special_chars,
            "sum": str(total_sum),
            "concat_string": concat_string
        }

        return jsonify(response), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({
            "is_success": False,
            "error": "Internal server error"
        }), 500


@app.route('/bfhl', methods=['GET'])
def bfhl_get():
    return jsonify({"operation_code": 1}), 200


@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "Server is running",
        "timestamp": datetime.utcnow().isoformat()
    }), 200


@app.errorhandler(404)
def not_found(e):
    return jsonify({"is_success": False, "error": "Route not found"}), 404


@app.errorhandler(500)
def internal_error(e):
    return jsonify({"is_success": False, "error": "Something went wrong!"}), 500


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port, debug=True)

