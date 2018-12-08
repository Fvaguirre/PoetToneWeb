from app import app, db
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import LoginForm, RegistrationForm
from app.models import User, Poem
from app.recommender import content_engine
from werkzeug.urls import url_parse

# @app.before_first_request
# def loadRecommender():
#     content_engine.train('app/poems_data.csv')
#     poems = Poem.query.all()
#     count = 1
#     for p in poems:
#         print("On " + str(count) + " out of " + str(len(poems)))
#         print("Getting predictions for poem :" + p.title)
#         predictions = content_engine.predict(p.title, 10)
#         # print(predictions)
#         count += 1
#         for pred in predictions:
#             target = Poem.query.filter_by(title=pred[1]).first()
#             p.similars.append(target)
#             db.session.commit()

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    flash("What are you in the mood for " + current_user.username + " ?")
    # if current_user.liked_poems is None or len(current_user.liked_poems) < 5:
    #     return redirect(url_for('explore', type='popular'))
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
    num_liked = len(current_user.liked_poems)
    poems = Poem.query.order_by(Poem.times_liked.desc()).paginate(
        page, app.config['POEMS_PER_PAGE'], False)
    if type == 'mood':
        return redirect(url_for('index'))
    elif type == 'recommended':
        if current_user.liked_poems is None or num_liked < 5:
            flash("Please like at least " + str(5-num_liked) + " more poems to start getting recommendations!")
            return redirect(url_for('explore', type='popular'))
        else:
            ignore_ids = [poem.id for poem in current_user.liked_poems]
            target_poems = [poem.similars for poem in current_user.liked_poems]
            # for sublist in target_poems:
            #     for item in sublist[0:3]:
            #         flat_list.append(item)
            target_poems = [item for sublist in target_poems for item in sublist[0:3]]
            target_ids = [poem.id for poem in target_poems]

            print(target_poems)
            poems = Poem.query.filter((Poem.id.notin_(ignore_ids)) | (Poem.id.in_(target_ids)))
            # liked = current_user.liked_poems
            # liked_ids = map(lambda x: x.id, liked)
            # poems = Poem.query.filter(~Poem.id.any(Poem.id.in_(liked_ids)))
            poems = poems.paginate(page, app.config["POEMS_PER_PAGE"], False)
    next_url = None
    prev_url = None
    if poems.has_next:
        next_url = url_for('explore', type=type, page=poems.next_num)
    if poems.has_prev:
        prev_url = url_for('explore', type=type, page=poems.prev_num)
    poems = poems.items
    # print(poems[2].text)
    return render_template('explore.html', title='Explore', poems=poems, next_url=next_url, prev_url=prev_url)

@app.route('/like/<int:poem_id>/<action>')
@login_required
def like_action(poem_id, action):
    poem = Poem.query.filter_by(id=poem_id).first_or_404()
    if action == 'like':
        poem.likers.append(current_user)
        poem.times_liked += 1
    elif action == 'unlike':
        poem.likers.remove(current_user)
        poem.times_liked -= 1
    db.session.commit()
    return redirect(request.referrer)



