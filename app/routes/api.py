from flask import Blueprint, request, jsonify
from app.models.suggestions import SuggestionManager
from app.utils.validators import validate_suggestion, validate_prefix
from app.utils.helpers import get_client_info
import os

bp = Blueprint('api', __name__)

@bp.route('/autocomplete', methods=['POST'])
def autocomplete():
    suggestion_manager = SuggestionManager(load_trie_on_init=True)
    data = request.get_json()
    prefix = data.get('prefix', '')
    limit = data.get('limit', 10)

    if not validate_prefix(prefix):
        return jsonify({'error': 'Invalid prefix'}), 400

    suggestions = suggestion_manager.get_suggestions(prefix, limit)

    # Log search
    user_agent, ip_address = get_client_info(request)
    suggestion_manager.log_search(
        prefix,
        len(suggestions),
        user_agent,
        ip_address
    )

    return jsonify({
        'suggestions': suggestions,
        'count': len(suggestions)
    })

@bp.route('/suggestion', methods=['POST'])
def add_suggestion():
    suggestion_manager = SuggestionManager(load_trie_on_init=True)
    data = request.get_json()
    text = data.get('text', '')
    category = data.get('category', 'general')

    if not validate_suggestion(text):
        return jsonify({'error': 'Invalid suggestion'}), 400

    success = suggestion_manager.add_suggestion(text, category)

    if success:
        return jsonify({'status': 'success', 'message': 'Suggestion added'})
    else:
        return jsonify({'error': 'Failed to add suggestion'}), 500

@bp.route('/interaction', methods=['POST'])
def log_interaction():
    suggestion_manager = SuggestionManager(load_trie_on_init=True)
    data = request.get_json()
    suggestion = data.get('suggestion', '')
    action = data.get('action', '')

    if suggestion and action:
        suggestion_manager.log_interaction(suggestion, action)

    return jsonify({'status': 'logged'})

@bp.route('/analytics', methods=['GET'])
def get_analytics():
    suggestion_manager = SuggestionManager(load_trie_on_init=True)
    analytics = suggestion_manager.get_analytics()
    return jsonify(analytics)

@bp.route('/import-dataset', methods=['POST'])
def import_dataset():
    suggestion_manager = SuggestionManager(load_trie_on_init=True)
    dataset_type = request.form.get('type', 'names')

    if dataset_type == 'names':
        filepath = 'data/raw/NationalNames.csv'
        if os.path.exists(filepath):
            count = suggestion_manager.import_names_dataset(filepath)
            return jsonify({
                'status': 'success',
                'imported': count,
                'message': f'Imported {count} names'
            })
        else:
            return jsonify({'error': 'Dataset file not found'}), 404

    elif dataset_type == 'emails':
        count_param = request.form.get('count', 1000)
        try:
            count = int(count_param)
            imported = suggestion_manager.generate_synthetic_emails(count)
            return jsonify({
                'status': 'success',
                'imported': imported,
                'message': f'Generated {imported} emails'
            })
        except ValueError:
            return jsonify({'error': 'Invalid count parameter'}), 400

    return jsonify({'error': 'Invalid dataset type'}), 400

@bp.route('/rebuild-trie', methods=['POST'])
def rebuild_trie():
    suggestion_manager = SuggestionManager(load_trie_on_init=True)
    suggestion_manager.rebuild_trie()
    return jsonify({'status': 'success', 'message': 'Trie rebuilt'})