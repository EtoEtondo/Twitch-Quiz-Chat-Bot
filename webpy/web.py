#!/usr/bin/env python3

from flask import Flask, render_template, jsonify
import csv
import os
import time

app = Flask(__name__)

def get_answer_counts():
    csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'answer_tmp.csv')
    try:
        with open(csv_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader, None)  # Header
            data = next(reader, None)    # Counter
            percentages = next(reader, None) # Percentage
            if header and data:
                answer_data = dict(zip(header, data))
                percentage_data = dict(zip(header, percentages)) if percentages else {}
                return answer_data, percentage_data
            else:
                return {}, {}
    except FileNotFoundError:
        print(f"File not found: {csv_path}")
        return {}, {}
    except Exception as e:
        print(f"Error reading csv: {e}")
        return {}, {}

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/api/answers")
def api_answers():
    answer_counts, answer_percentages = get_answer_counts()
    try:
        answers_int = {k: int(v) for k, v in answer_counts.items() if k != 'All'}
        all_count = int(answer_counts.get('All', 0))
        percentages_float = {k: float(v) for k, v in answer_percentages.items() if k != 'All'}
        return jsonify({'all': all_count, 'counts': answers_int, 'percentages': percentages_float})
    except ValueError:
        return jsonify({'error': 'Error in converting file'}), 500

if __name__ == '__main__':
    app.run(debug=True)