from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from slugify import slugify
import os
from . import db
from .models import Post

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('Admin access required')
            return redirect(url_for('blog.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/')
@admin_required
def index():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('admin/index.html', posts=posts)

@admin_bp.route('/post/new', methods=['GET', 'POST'])
@admin_required
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        summary = request.form['summary']
        published = 'published' in request.form
        
        post = Post(
            title=title,
            slug=slugify(title),
            content=content,
            summary=summary,
            published=published,
            author=current_user
        )
        
        if 'featured_image' in request.files:
            file = request.files['featured_image']
            if file.filename:
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                post.featured_image = filename
        
        db.session.add(post)
        db.session.commit()
        flash('Post created successfully!')
        return redirect(url_for('admin.index'))
    
    return render_template('admin/post_form.html')

@admin_bp.route('/post/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_post(id):
    post = Post.query.get_or_404(id)
    
    if request.method == 'POST':
        post.title = request.form['title']
        post.slug = slugify(request.form['title'])
        post.content = request.form['content']
        post.summary = request.form['summary']
        post.published = 'published' in request.form
        
        if 'featured_image' in request.files:
            file = request.files['featured_image']
            if file.filename:
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                post.featured_image = filename
        
        db.session.commit()
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