from app import db
from app.main import bp
from app.main.forms import EditProfileForm, PostForm, SearchForm
from app.models import User, Post
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, current_app, g
from flask_login import current_user, login_required


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    """
    View function with route URL decorators
    """
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()

        flash('Your post has been submitted!')
        return redirect(url_for('main.index'))

    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(page, current_app.config['POSTS_PER_PAGE'], False)

    next_url = None
    if posts.has_next:
        next_url = url_for('main.index', page=posts.next_num)

    prev_url = None
    if posts.has_next:
        prev_url = url_for('main.index', page=posts.prev_num)

    return render_template('index.html', title='Home', form=form, posts=posts.items, next_url=next_url, prev_url=prev_url)


@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)

    next_url = None
    if posts.has_next:
        next_url = url_for('main.explore', page=posts.next_num)

    prev_url = None
    if posts.has_next:
        prev_url = url_for('main.explore', page=posts.prev_num)

    return render_template('index.html', title='Explore', posts=posts.items, next_url=next_url, prev_url=prev_url)


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)

    next_url = None
    if posts.has_next:
        next_url = url_for('main.user', username=user.username, page=posts.next_num)

    prev_url = None
    if posts.has_next:
        prev_url = url_for('main.user', username=user.username, page=posts.prev_num)

    return render_template('user.html', user=user, posts=posts.items, next_url=next_url, prev_url=prev_url)


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_login = datetime.utcnow()
        db.session.commit()
        g.search_form = SearchForm()


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(original_username=current_user.username)

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.bio = form.bio.data
        db.session.commit()

        flash('Your changes have been saved')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.bio.data = current_user.bio

    return render_template('edit_profile.html', title='Edit Profile', form=form)


@bp.route('/follow/<username>')
@login_required
def follow(username):
    other_user = User.query.filter_by(username=username).first()
    if other_user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('main.index'))

    if current_user == other_user:
        flash('You cannot follow yourself.')
        return redirect(url_for('main.user', username=username))

    current_user.follow(other_user)
    db.session.commit()

    flash('You are now following {}!'.format(username))
    return redirect(url_for('main.user', username=username))


@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    other_user = User.query.filter_by(username=username).first()
    if other_user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('main.index'))

    if current_user == other_user:
        flash('You cannot unfollow yourself.')
        return redirect(url_for('main.user', username=username))

    current_user.unfollow(other_user)
    db.session.commit()

    flash('You\'ve unfollowed {}.'.format(username))
    return redirect(url_for('main.user', username=username))


@bp.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.explore'))

    page = request.args.get('page', 1, type=int)
    posts, total = Post.search(g.search_form.q.data, page, current_app.config['POSTS_PER_PAGE'])

    next_url = None
    if total > (page * current_app.config['POSTS_PER_PAGE']):
        next_url = url_for('main.search', q=g.search_form.q.data, page=(page + 1))

    prev_url = None
    if page > 1:
        prev_url = url_for('main.search', q=g.search_form.q.data, page=(page - 1))

    return render_template('search.html', title='Search', posts=posts, next_url=next_url, prev_url=prev_url)
