from flask import Blueprint, render_template, abort
from .models import Post
from flask_login import current_user

blog_bp = Blueprint('blog', __name__)

@blog_bp.route('/')
def index():
    posts = Post.query.filter(Post.public_filter()).order_by(Post.created_at.desc()).all()
    return render_template('blog/index.html', posts=posts)

@blog_bp.route('/post/<string:slug>')
def post_detail(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    can_preview = current_user.is_authenticated and current_user.is_admin
    if not post.is_publicly_visible and not can_preview:
        abort(404)
    return render_template('blog/post_detail.html', post=post)
