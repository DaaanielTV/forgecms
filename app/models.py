# Import required extensions
from datetime import datetime
from sqlalchemy import and_, or_
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, login_manager

"""
This module contains the database models for the BlogForge application.
Any changes to these models should be followed by:
1. flask db migrate -m "Description of changes"
2. flask db upgrade
"""

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Post(db.Model):
    STATUS_DRAFT = 'draft'
    STATUS_SCHEDULED = 'scheduled'
    STATUS_PUBLISHED = 'published'
    STATUS_ARCHIVED = 'archived'
    ALLOWED_STATUSES = {
        STATUS_DRAFT,
        STATUS_SCHEDULED,
        STATUS_PUBLISHED,
        STATUS_ARCHIVED,
    }

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    featured_image = db.Column(db.String(200))
    summary = db.Column(db.String(300))
    published = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), nullable=False, default=STATUS_DRAFT)
    publish_at = db.Column(db.DateTime, nullable=True)
    published_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def set_workflow_status(self, status, publish_at=None):
        normalized_status = (status or self.STATUS_DRAFT).strip().lower()
        if normalized_status not in self.ALLOWED_STATUSES:
            raise ValueError('Invalid post status')

        self.status = normalized_status
        self.publish_at = publish_at
        self.published = normalized_status == self.STATUS_PUBLISHED

        if normalized_status == self.STATUS_PUBLISHED and not self.published_at:
            self.published_at = datetime.utcnow()
        if normalized_status != self.STATUS_PUBLISHED:
            self.published_at = None

    @property
    def is_publicly_visible(self):
        now = datetime.utcnow()

        if self.status == self.STATUS_PUBLISHED:
            return True
        if self.status == self.STATUS_SCHEDULED and self.publish_at:
            return self.publish_at <= now

        # Backward compatibility for existing rows created before workflow states.
        return bool(self.published)

    @classmethod
    def public_filter(cls):
        now = datetime.utcnow()
        return or_(
            cls.status == cls.STATUS_PUBLISHED,
            and_(cls.status == cls.STATUS_SCHEDULED, cls.publish_at.isnot(None), cls.publish_at <= now),
            and_(cls.status.is_(None), cls.published.is_(True)),
        )

    def __repr__(self):
        return f'<Post {self.title}>'
