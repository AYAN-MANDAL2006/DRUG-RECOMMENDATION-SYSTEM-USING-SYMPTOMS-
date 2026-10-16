"""
app.py
------
Main Flask Application for Drug Recommendation System Based on Symptoms.
Includes all multi-page routes, NLP recommendation engine integration,
feedback handling, database stats dashboard, and error handlers.
"""

import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from config import Config
from src.database import (
    get_dashboard_stats, search_medicines, get_medicine_by_id, insert_feedback
)
from src.recommender import SymptomRecommender
from src.symptom_search import search_symptoms
from src.utils import sanitize_input

app = Flask(__name__)
app.config.from_object(Config)

# Initialize Recommendation Engine
recommender = SymptomRecommender()


@app.context_processor
def inject_global_data():
    """Injects mandatory safety disclaimer into all template contexts."""
    return {
        'global_disclaimer': Config.DISCLAIMER_TEXT
    }


# 1. HOME PAGE
@app.route('/')
def home():
    stats = get_dashboard_stats()
    return render_template('index.html', stats=stats)


# 2. SYMPTOM ANALYZER INPUT PAGE
@app.route('/analyzer')
def analyzer():
    search_query = sanitize_input(request.args.get('q', ''))
    search_results = search_symptoms(search_query) if search_query else []
    example_symptoms = [
        "Fever", "Headache", "Cough", "Cold", "Sore throat",
        "Stomach pain", "Body pain", "Runny nose", "Heartburn"
    ]
    return render_template(
        'analyzer.html',
        example_symptoms=example_symptoms,
        search_query=search_query,
        search_results=search_results
    )


# API: SYMPTOM SEARCH ENDPOINT (JSON)
@app.route('/api/symptoms/search')
def api_symptom_search():
    query = sanitize_input(request.args.get('q', ''))
    results = search_symptoms(query)
    return jsonify({
        'query': query,
        'count': len(results),
        'results': results
    })


# 3. ANALYZE SYMPTOMS ACTION (POST) & RESULTS DISPLAY
@app.route('/analyze', methods=['POST'])
def analyze():
    symptom_input = sanitize_input(request.form.get('symptoms', ''))

    if not symptom_input:
        flash("Please enter at least one symptom to analyze.", "warning")
        return redirect(url_for('analyzer'))

    # Run NLP Recommender Engine
    result = recommender.recommend(symptom_input)

    return render_template('results.html', result=result)


# 4. MEDICINE INFORMATION DIRECTORY
@app.route('/medicines')
def medicines():
    query = sanitize_input(request.args.get('q', ''))
    medicine_list = search_medicines(query)
    return render_template('medicines.html', medicines=medicine_list, query=query)


# 5. MEDICINE DETAIL PAGE
@app.route('/medicine/<int:med_id>')
def medicine_detail(med_id):
    med = get_medicine_by_id(med_id)
    if not med:
        return render_template('404.html'), 404
    return render_template('medicine_detail.html', medicine=med)


# 6. ABOUT PAGE
@app.route('/about')
def about():
    return render_template('about.html')


# 7. HOW IT WORKS PAGE
@app.route('/how-it-works')
def how_it_works():
    return render_template('how_it_works.html')


# 8. SAFETY / DISCLAIMER PAGE
@app.route('/disclaimer')
def disclaimer():
    return render_template('disclaimer.html')


# 9. FEEDBACK PAGE
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        name = sanitize_input(request.form.get('name', ''))
        email = sanitize_input(request.form.get('email', ''))
        rating = request.form.get('rating', '5')
        message = sanitize_input(request.form.get('message', ''))

        if not name or not email or not message:
            flash("Please fill in all required fields.", "danger")
            return redirect(url_for('feedback'))

        try:
            rating_val = int(rating)
            insert_feedback(name, email, rating_val, message)
            flash("Thank you! Your feedback has been recorded.", "success")
            return redirect(url_for('feedback'))
        except Exception as e:
            flash("Error recording feedback. Please try again.", "danger")
            return redirect(url_for('feedback'))

    return render_template('feedback.html')


# 10. ADMIN / DATABASE TELEMETRY PAGE
@app.route('/admin/stats')
def admin_stats():
    stats = get_dashboard_stats()
    return render_template('admin_stats.html', stats=stats)


# ERROR HANDLERS
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    import socket
    def get_local_ip():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"

    local_ip = get_local_ip()
    print("=" * 60)
    print(" DRUG RECOMMENDATION SYSTEM IS LIVE")
    print(f" Local URL:   http://127.0.0.1:5000")
    print(f" Phone/Wi-Fi: http://{local_ip}:5000")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5000, debug=True)
