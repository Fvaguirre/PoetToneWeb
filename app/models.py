from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

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