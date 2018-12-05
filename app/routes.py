from app import app, db
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import LoginForm, RegistrationForm
from app.models import User, Poem, PoemFeature
from werkzeug.urls import url_parse

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    if current_user.liked_poems is None:
        return render_template('')
    return render_template('index.html', title='Home Page')

@app.route('/login', methods=['GET', 'POST'])
def login():
    #if current user is logged in and navigates to /login
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # print(user)
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            if user.liked_poems is None:
                next_page = url_for('index')
            else:
                next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)
    # form = LoginForm()
    # if form.validate_on_submit():
    #     flash('Login requested for user {}, remember_me={}'.format(
    #         form.username.data, form.remember_me.data))
    #     return redirect(url_for('index'))
    # return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        if current_user.liked_poems is None:
            return redirect(url_for('index'))
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account Registered!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/explore/<type>')
@login_required
def explore(type):
    page = request.args.get('page', 1, type=int)

    poemfeatures = PoemFeature.query.order_by(PoemFeature.times_liked.desc()).paginate(
        page, app.config['POEMS_PER_PAGE'], False)
    if type == 'mood':
        return redirect(url_for('index'))
    elif type == 'recommended':
        pass
    next_url = None
    prev_url = None
    if poemfeatures.has_next:
        next_url = url_for('explore', page=poemfeatures.next_num)
    if poemfeatures.has_prev:
        prev_url = url_for('explore', page=poemfeatures.prev_num)
    poems = list(map(lambda x: x.poem, poemfeatures.items))
    return render_template('explore.html', title='Explore', poems=poems, next_url=next_url, prev_url=prev_url)

@app.route('/like/<int:poem_id>/<action>')
@login_required
def like_action(poem_id, action):
    poem = Poem.query.filter_by(id=poem_id).first_or_404()
    if action == 'like':
        poem.likers.append(current_user)
    elif action == 'unlike':
        #Slow bc database not set up correctly to support ths :/
        poem.likers.remove(current_user)
    db.session.commit()
    return redirect(request.referrer + '/#')

