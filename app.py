from flask import Flask, render_template, request, jsonify
from scraper import check_project_title

app = Flask(__name__)

@app.route('/')
def home():
    
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    
    data = request.json
    title = data.get('title')
    
    result = check_project_title(title)
    
    
    status = 'taken' if 'taken' in result.lower() else 'available'
    return jsonify({'message': result, 'status': status})

if __name__ == '__main__':
    app.run(debug=True)