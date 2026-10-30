import os
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from sqlalchemy import or_
from models import db, User, BlogPost, Comment
from forms import RegistrationForm, LoginForm, PostForm, CommentForm

# Load environment variables from .env file if available
load_dotenv()

# Initialize Flask Application
app = Flask(__name__)

# Security & Database Configurations via Environment Variables (Week 7 Deployment Prep)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///site.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Connect extensions with the app
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    """Flask-Login helper: Loads user object from user_id stored in the session."""
    return db.session.get(User, int(user_id))


# -------------------------------------------------------------------
# CUSTOM JINJA TEMPLATE FILTERS (WEEK 4)
# -------------------------------------------------------------------

@app.template_filter('reading_time')
def reading_time_filter(content):
    """Calculates estimated reading time in minutes based on 200 wpm."""
    if not content:
        return "1 min read"
    words = len(content.split())
    minutes = max(1, round(words / 200))
    return f"{minutes} min read"


# -------------------------------------------------------------------
# PUBLIC & SEARCH ROUTES (WEEK 6)
# -------------------------------------------------------------------

@app.route('/')
def home():
    """Homepage route with search, category filtering, and tag filtering."""
    search_query = request.args.get('q', '').strip()
    selected_category = request.args.get('category', 'All')
    selected_tag = request.args.get('tag', '').strip()

    categories = ['All', 'Technology', 'Programming', 'Lifestyle', 'Education', 'Career', 'General']

    query = BlogPost.query

    # 1. Filter by category if not 'All'
    if selected_category and selected_category != 'All':
        query = query.filter_by(category=selected_category)

    # 2. Filter by specific tag if clicked
    if selected_tag:
        query = query.filter(BlogPost.tags.ilike(f'%{selected_tag}%'))

    # 3. Search across title, content, and tags
    if search_query:
        query = query.filter(
            or_(
                BlogPost.title.ilike(f'%{search_query}%'),
                BlogPost.content.ilike(f'%{search_query}%'),
                BlogPost.tags.ilike(f'%{search_query}%')
            )
        )

    posts = query.order_by(BlogPost.date_posted.desc()).all()

    return render_template(
        'index.html',
        title='Home',
        posts=posts,
        categories=categories,
        active_category=selected_category,
        search_query=search_query,
        active_tag=selected_tag
    )


@app.route('/about')
def about():
    """About page route."""
    return render_template('about.html', title='About Us')


# -------------------------------------------------------------------
# AUTHENTICATION ROUTES (WEEK 2)
# -------------------------------------------------------------------

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handles new user registration."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data.lower())
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash('Your account has been created successfully! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handles user login."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Welcome back, {user.username}!', 'success')

            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Login unsuccessful. Please check your email and password.', 'danger')

    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    """Logs the user out and clears their session."""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))


# -------------------------------------------------------------------
# USER DASHBOARD & BLOG POST CRUD (WEEK 3)
# -------------------------------------------------------------------

@app.route('/dashboard')
@login_required
def dashboard():
    """Protected user dashboard displaying user's published posts and comment metrics."""
    user_posts = BlogPost.query.filter_by(user_id=current_user.id).order_by(BlogPost.date_posted.desc()).all()
    total_comments_received = sum(len(p.comments) for p in user_posts)
    return render_template(
        'dashboard.html',
        title='Dashboard',
        posts=user_posts,
        comments_count=total_comments_received
    )


@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def create_post():
    """CRUD - Create a new blog post."""
    form = PostForm()
    if form.validate_on_submit():
        post = BlogPost(
            title=form.title.data,
            category=form.category.data,
            tags=form.tags.data,
            content=form.content.data,
            author=current_user
        )
        db.session.add(post)
        db.session.commit()
        flash('Your blog post has been published successfully!', 'success')
        return redirect(url_for('post_detail', post_id=post.id))

    return render_template('create_post.html', title='New Post', form=form, legend='Create New Post')


@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post_detail(post_id):
    """CRUD - Read a single blog post and handle new comments (Week 5)."""
    post = BlogPost.query.get_or_404(post_id)
    comment_form = CommentForm()

    if comment_form.validate_on_submit():
        if not current_user.is_authenticated:
            flash('Please log in to leave a comment.', 'info')
            return redirect(url_for('login', next=request.url))

        comment = Comment(
            content=comment_form.content.data,
            author=current_user,
            post=post
        )
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been posted successfully!', 'success')
        return redirect(url_for('post_detail', post_id=post.id))

    return render_template('post_detail.html', title=post.title, post=post, comment_form=comment_form)


@app.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    """CRUD - Update an existing blog post (Author only)."""
    post = BlogPost.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)

    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.category = form.category.data
        post.tags = form.tags.data
        post.content = form.content.data
        db.session.commit()

        flash('Your post has been updated successfully!', 'success')
        return redirect(url_for('post_detail', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.category.data = post.category
        form.tags.data = post.tags
        form.content.data = post.content
        form.submit.label.text = 'Save Changes'

    return render_template('create_post.html', title='Edit Post', form=form, legend=f'Edit: {post.title}')


@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    """CRUD - Delete an existing blog post (Author only)."""
    post = BlogPost.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted successfully.', 'info')
    return redirect(url_for('dashboard'))


# -------------------------------------------------------------------
# COMMENT MANAGEMENT (WEEK 5)
# -------------------------------------------------------------------

@app.route('/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    """Allows comment author OR post author to remove a comment."""
    comment = Comment.query.get_or_404(comment_id)

    if comment.author != current_user and comment.post.author != current_user:
        abort(403)

    post_id = comment.post.id
    db.session.delete(comment)
    db.session.commit()
    flash('The comment has been removed.', 'info')
    return redirect(url_for('post_detail', post_id=post_id))


# -------------------------------------------------------------------
# CUSTOM ERROR HANDLERS (WEEK 7)
# -------------------------------------------------------------------

@app.errorhandler(403)
def forbidden_error(error):
    """Custom 403 Forbidden page."""
    return render_template('errors/403.html', title='Access Denied'), 403


@app.errorhandler(404)
def not_found_error(error):
    """Custom 404 Page Not Found."""
    return render_template('errors/404.html', title='Page Not Found'), 404


@app.errorhandler(500)
def internal_error(error):
    """Custom 500 Internal Server Error."""
    db.session.rollback()  # Rollback session in case of database transaction error
    return render_template('errors/500.html', title='Server Error'), 500


# -------------------------------------------------------------------
# APPLICATION ENTRY POINT & DB CREATION
# -------------------------------------------------------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    # In development mode, debug is enabled; set FLASK_DEBUG=0 for production
    is_debug = os.environ.get('FLASK_DEBUG', '1') == '1'
    app.run(debug=is_debug, port=5000)
