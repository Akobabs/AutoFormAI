from flask import Blueprint, render_template, request, jsonify
from app.models import load_trie_from_pickle, add_suggestion

bp = Blueprint('main', __name__)
trie = load_trie_from_pickle()  # Load from saved model

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/form')
def form():
    return render_template('form.html')

@bp.route('/autocomplete', methods=['POST'])
def autocomplete():
    prefix = request.json.get('prefix', '')
    suggestions = trie.search_prefix(prefix)[:5]
    return jsonify(suggestions)

@bp.route('/add_suggestion', methods=['POST'])
def add_suggestion_route():
    text = request.json.get('text')
    if text:
        add_suggestion(text)
        trie.insert(text)
    return jsonify({'status': 'success'})
