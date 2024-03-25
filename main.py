import json

from flask import Flask, request, render_template
from database import fetch_messages, fetch_labels, generate_sql_query
from write_json import write_json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        description = request.form.get('description')
        rules = request.form.get('rules')
        fields = request.form.getlist('field')
        predicates = request.form.getlist('predicate')
        values = request.form.getlist('value1')
        move_message = request.form.get('move_message')
        inbox = request.form.get('inbox')
        action = request.form.get('action')
        data_list = []
        for i in range(len(fields)):
            data = {
                "description": description,
                "rules": rules,
                "field": fields[i],
                "predicate": predicates[i],
                "value1": values[i],
                "move_message": move_message,
                "inbox": inbox,
                "action": action
            }
            data_list.append(data)
        write_json("rules.json", data_list)
        with open('rules.json', 'r') as file:
            # Load the JSON data
            data = json.load(file)
        sql_query = generate_sql_query(data[-1])
        messages = fetch_messages(sql_query)
        return render_template('output.html', messages=messages)
    label = fetch_labels()
    return render_template('index.html', label=label)

if __name__ == '__main__':
    app.run(debug=True)
