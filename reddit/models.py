from reddit import app,db
from flask_login import UserMixin

#table of users with unique ID, name, and password
class UserDB(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(48), unique=True, nullable=False)
    username = db.Column(db.String(24), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

# Table of posts with unique ID, title, content, author, the number of like, and the time it was posted. Note how author is described as "db.ForeignKey('users.username')". This is because this database column is defined in terms of a primary key column in a different table to ensure data integrity.

class PostDB(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    author = db.Column(db.String(24), db.ForeignKey('users.username'), nullable=False)
    num_likes = db.Column(db.Integer, nullable=False)
    time = db.Column(db.DateTime, nullable=False)

# Table of comments with a unique ID, content, author, the post that this comment belongs to, the number of likes, and the time of commenting.
class CommentDB(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    content = db.Column(db.String(250), nullable=False)
    author = db.Column(db.String(24), db.ForeignKey('users.username'), nullable=False) #has to be from the other table
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False) #has to be from the other table
    num_likes = db.Column(db.Integer, nullable=False)
    time = db.Column(db.DateTime, nullable=False)

# Table of likes with a unique ID, the person who liked, whether the like is attached to a post or a comment, the comment ID if it's under a comment, the post ID if it's under a post, and the like type (either positive or negative)
class LikeDB(db.Model):
    __tablename__ = 'likes'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(24), db.ForeignKey('users.username'), nullable=False)
    post_or_comment = db.Column(db.Integer, nullable=False)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=True)
    like_type = db.Column(db.Boolean, nullable=False)

# Table with the tags that users created with a unique ID and name of the tag. This is similar to subreddits.
class TagDB(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(30), nullable=False)

# Table of posts that belong to certain tags. This lets us query between both tables.
class PostTagDB(db.Model):
    __tablename__ = 'posts_tags'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

#Table of tags that users will see
class UserTagDB(db.Model):
        __tablename__ = 'users_tags'
        id = db.Column(db.Integer, primary_key=True, nullable=False)
        tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), nullable=False)
        username = db.Column(db.String(24), db.ForeignKey('users.username'), nullable=False)
        weight = db.Column(db.Integer, nullable=False)

