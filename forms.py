from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from models import User

class RegistrationForm(FlaskForm):
    """Form for new user registration."""
    username = StringField(
        'Username',
        validators=[
            DataRequired(message="Username is required."),
            Length(min=3, max=25, message="Username must be between 3 and 25 characters.")
        ]
    )
    email = StringField(
        'Email Address',
        validators=[
            DataRequired(message="Email is required."),
            Email(message="Please enter a valid email address.")
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message="Password is required."),
            Length(min=6, message="Password must be at least 6 characters long.")
        ]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(message="Please confirm your password."),
            EqualTo('password', message="Passwords must match.")
        ]
    )
    submit = SubmitField('Create Account')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken. Please choose another one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('An account with this email already exists. Please log in.')


class LoginForm(FlaskForm):
    """Form for existing user login."""
    email = StringField(
        'Email Address',
        validators=[
            DataRequired(message="Email is required."),
            Email(message="Please enter a valid email address.")
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message="Password is required.")
        ]
    )
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class PostForm(FlaskForm):
    """Form for creating and editing blog posts."""
    title = StringField(
        'Title',
        validators=[
            DataRequired(message="A post title is required."),
            Length(min=3, max=150, message="Title must be between 3 and 150 characters.")
        ]
    )
    category = SelectField(
        'Category',
        choices=[
            ('Technology', 'Technology'),
            ('Programming', 'Programming'),
            ('Lifestyle', 'Lifestyle'),
            ('Education', 'Education'),
            ('Career', 'Career'),
            ('General', 'General')
        ],
        default='General',
        validators=[DataRequired()]
    )
    tags = StringField(
        'Tags (comma separated, e.g. python, web, beginner)',
        validators=[Optional(), Length(max=100)]
    )
    content = TextAreaField(
        'Content',
        validators=[
            DataRequired(message="Post content cannot be empty."),
            Length(min=10, message="Content must be at least 10 characters long.")
        ]
    )
    submit = SubmitField('Publish Post')


class CommentForm(FlaskForm):
    """Form for posting a comment on an article (Week 5)."""
    content = TextAreaField(
        'Add a comment',
        validators=[
            DataRequired(message="Comment cannot be empty."),
            Length(min=2, max=1000, message="Comments must be between 2 and 1000 characters.")
        ]
    )
    submit = SubmitField('Post Comment')
