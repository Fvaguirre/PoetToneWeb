from app import app, db
from app.models import User, Poem, PoemFeature, PoemTone

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Poem': Poem, 'PoemFeature': PoemFeature, 'PoemTone': PoemTone}
