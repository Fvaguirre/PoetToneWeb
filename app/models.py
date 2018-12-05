from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
likes = db.Table('likes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('poem_id', db.Integer, db.ForeignKey('poem.id'))
)
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    # Relationship to child
    liked_poems = db.relationship("Poem", secondary=likes, backref=db.backref('likers', lazy='dynamic'))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):

        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class PoemTone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tone_confidence = db.Column(db.Float)

    #Relationship to parent
    poemfeature_id = db.Column(db.Integer, db.ForeignKey('poem_feature.id'))
    poem_feature = db.relationship("PoemFeature", back_populates="poem_tones")

class PoemFeature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    close_poem = db.Column(db.Integer)
    top_topic = db.Column(db.Integer)
    times_liked = db.Column(db.Integer, default=0)

    #Relationship to parent
    poem_id = db.Column(db.Integer, db.ForeignKey('poem.id'))
    poem = db.relationship("Poem", back_populates="poem_feature")

    #Relationship to child
    poem_tones = db.relationship("PoemTone", back_populates="poem_feature")

    # size features
    num_lines = db.Column(db.Integer)
    num_words = db.Column(db.Integer)
    word_size = db.Column(db.Float)
    width_in_char = db.Column(db.Float)
    repetition_score = db.Column(db.Float)
    obscurity_score = db.Column(db.Float)
    sentence_score = db.Column(db.Float)


class Poem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    text = db.Column(db.String(2500))
    poet = db.Column(db.String(50))
    url = db.Column(db.String(60))
    tags = db.Column(db.String(60))
    source = db.Column(db.String(20))


    #Relationship to child
    poem_feature = db.relationship("PoemFeature", uselist=False, back_populates="poem")