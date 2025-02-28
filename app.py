from flask import Flask, render_template, request, jsonify
from scraper import WebScraper
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape_data():
    try:
        scraper_type = request.form['scraperType']
        scraper = WebScraper(headless=True)
        
        result = {}
        start_time = time.time()
        
        if scraper_type == 'jobs':
            result = scraper.scrape_jobs(
                request.form['jobs_url'],
                request.form['container_selector'],
                {
                    'title': request.form['title_selector'],
                    'company': request.form['company_selector'],
                    'location': request.form['location_selector']
                }
            )
        elif scraper_type == 'news':
            result = scraper.scrape_news(
                request.form['news_url'],
                request.form['news_container_selector'],
                {
                    'title': request.form['news_title_selector'],
                    'content': request.form['content_selector'],
                    'source': request.form['source_selector']
                }
            )
        elif scraper_type == 'stocks':
            result = scraper.scrape_stock_price(
                request.form['stock_symbol']
            )
        
        execution_time = round(time.time() - start_time, 2)
        scraper.close()
        
        return render_template('results.html', 
                             data=result,
                             scraper_type=scraper_type,
                             execution_time=execution_time)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
