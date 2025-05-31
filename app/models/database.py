from app import db
from datetime import datetime
from sqlalchemy import func

class Suggestion(db.Model):
    __tablename__ = 'suggestions'
    
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False, unique=True, index=True)
    category = db.Column(db.String(50), default='general')
    frequency = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<Suggestion {self.text}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'category': self.category,
            'frequency': self.frequency,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'is_active': self.is_active
        }

class SearchLog(db.Model):
    __tablename__ = 'search_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    query = db.Column(db.String(255), nullable=False)
    results_count = db.Column(db.Integer, default=0)
    user_agent = db.Column(db.String(500))
    ip_address = db.Column(db.String(45))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f'<SearchLog {self.query}>'

class UserInteraction(db.Model):
    __tablename__ = 'user_interactions'
    
    id = db.Column(db.Integer, primary_key=True)
    suggestion_id = db.Column(db.Integer, db.ForeignKey('suggestions.id'))
    action = db.Column(db.String(50))  # 'click', 'select', 'submit'
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    suggestion = db.relationship('Suggestion', backref='interactions')
    
    def __repr__(self):
        return f'<UserInteraction {self.action}>'