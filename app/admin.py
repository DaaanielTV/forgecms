from datetime import datetime
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, abort
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from slugify import slugify
import os
from sqlalchemy.exc import IntegrityError
from . import db
from .models import Post

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('Admin access required')
            return redirect(url_for('blog.index'))
        return f(*args, **kwargs)
    return decorated_function


def _parse_publish_at(value):
    if not value:
        return None
    try:
        return datetime.strptime(value, '%Y-%m-%dT%H:%M')
    except ValueError:
        return None


def _prepare_post_from_form(post):
    title = (request.form.get('title') or '').strip()
    content = (request.form.get('content') or '').strip()
    summary = (request.form.get('summary') or '').strip()
    status = request.form.get('status', Post.STATUS_DRAFT)
    publish_at_raw = request.form.get('publish_at')
    publish_at = _parse_publish_at(publish_at_raw)

    if not title or not content:
        raise ValueError('Title and content are required.')

    if status == Post.STATUS_SCHEDULED and not publish_at:
        raise ValueError('Scheduled posts require a valid publish date/time.')

    base_slug = slugify(title)
    slug = base_slug
    suffix = 1
    while Post.query.filter(Post.slug == slug, Post.id != post.id).first():
        suffix += 1
        slug = f'{base_slug}-{suffix}'

    post.title = title
    post.slug = slug
    post.content = content
    post.summary = summary
    post.set_workflow_status(status, publish_at=publish_at)

@admin_bp.route('/')
@admin_required
def index():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('admin/index.html', posts=posts)

@admin_bp.route('/post/new', methods=['GET', 'POST'])
@admin_required
def create_post():
    if request.method == 'POST':
        post = Post(author=current_user)
        try:
            _prepare_post_from_form(post)
        except ValueError as exc:
            flash(str(exc))
            return render_template('admin/post_form.html', post=post)

        if 'featured_image' in request.files:
            file = request.files['featured_image']
            if file.filename:
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                post.featured_image = filename
        
        db.session.add(post)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash('A post with a similar URL already exists. Please adjust the title.')
            return render_template('admin/post_form.html', post=post)
        flash('Post created successfully!')
        return redirect(url_for('admin.index'))
    
    return render_template('admin/post_form.html')

@admin_bp.route('/post/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_post(id):
    post = Post.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            _prepare_post_from_form(post)
        except ValueError as exc:
            flash(str(exc))
            return render_template('admin/post_form.html', post=post)

        if 'featured_image' in request.files:
            file = request.files['featured_image']
            if file.filename:
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                post.featured_image = filename
        
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash('A post with a similar URL already exists. Please adjust the title.')
            return render_template('admin/post_form.html', post=post)
        flash('Post updated successfully!')
        return redirect(url_for('admin.index'))
    
    return render_template('admin/post_form.html', post=post)

@admin_bp.route('/post/<int:id>/delete', methods=['POST'])
@admin_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully!')
    return redirect(url_for('admin.index'))


@admin_bp.route('/post/<int:id>/preview')
@admin_required
def preview_post(id):
    post = Post.query.get_or_404(id)
    if post.author != current_user and not current_user.is_admin:
        abort(403)
    return render_template('blog/post_detail.html', post=post, is_preview=True)
