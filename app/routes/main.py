from flask import Blueprint, render_template, request, session
from app.models.suggestions import SuggestionManager

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    suggestion_manager = SuggestionManager(load_trie_on_init=True)
    analytics = suggestion_manager.get_analytics()
    return render_template('index.html', analytics=analytics)

@bp.route('/form')
def form():
    return render_template('form.html')

@bp.route('/analytics')
def analytics():
    suggestion_manager = SuggestionManager(load_trie_on_init=True)
    analytics_data = suggestion_manager.get_analytics()
    return render_template('analytics.html', data=analytics_data)

@bp.route('/admin')
def admin():
    return render_template('admin.html')