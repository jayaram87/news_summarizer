from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
from demo import Demo

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET', 'POST'])
@cross_origin()
def index():
    if request.method == 'POST':
        keyword = request.form['keyword']
        if not keyword:
            error = 'Please enter a keyword'
            return render_template('index.html', error=error)
        headline, summary, date, keyword = Demo(keyword=keyword).run()
        data = {'headline': headline, 'summary':summary, 'date': date, 'keyword': keyword}
        return render_template('index.html', data=data)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)