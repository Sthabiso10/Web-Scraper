from flask import Flask, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    return 'Welcome to the Web Scraper API!'


@app.route('/scrape', methods=['GET'])
def scrape():
    url = "https://www.premierleague.com/about/what-we-do"

    # Make a request to fetch the page content
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find headings and paragraphs
            headings = soup.find_all(
                ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])  # Find headings
            paragraphs = soup.find_all('p')  # Find paragraphs

            # Group the headings with their paragraphs (simple approach)
            scraped_data = []
            # Assuming headings correspond to paragraphs
            for i in range(min(len(headings), len(paragraphs))):
                scraped_data.append({
                    'heading': headings[i].get_text(),
                    'text': paragraphs[i].get_text()
                })

            return jsonify({'scraped_data': scraped_data})
        else:
            return jsonify({'error': 'Failed to retrieve content'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
