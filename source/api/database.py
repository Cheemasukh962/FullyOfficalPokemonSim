"""Database models and initialization for Pokémon Battle Arena."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

db = SQLAlchemy()


class Battle(db.Model):
    """Model for storing battle results."""
    __tablename__ = 'battles'
    
    id = db.Column(db.Integer, primary_key=True)
    winner = db.Column(db.String(100), nullable=False)
    loser = db.Column(db.String(100), nullable=False)
    winner_stats = db.Column(db.Integer, nullable=False)
    loser_stats = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Battle {self.winner} vs {self.loser}>'
    
    def to_dict(self):
        """Convert battle record to dictionary."""
        return {
            'id': self.id,
            'winner': self.winner,
            'loser': self.loser,
            'winner_stats': self.winner_stats,
            'loser_stats': self.loser_stats,
            'created_at': self.created_at.isoformat()
        }


def init_db(app):
    """Initialize database with Flask app."""
    db.init_app(app)
    with app.app_context():
        db.create_all()
