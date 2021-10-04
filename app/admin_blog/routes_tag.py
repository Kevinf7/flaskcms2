from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from app import db
from app.admin_blog import bp
from app.admin_blog.models import Tag, Tagged
from datetime import datetime
from app.breadcrumb import set_breadcrumb


# ADMIN BLOG TAG routes

@bp.route('/tag',methods=['GET'])
@login_required
@set_breadcrumb('home blog tag')
def tag():
    tab = request.args.get('tab')
    if tab == '2':
        tab = 'false'
    else:
        tab = 'true'
    tag_used = db.session.query(Tag).join(Tagged).all()
    tag_all = Tag.query.all()
    tag_notused = []
    for t in tag_all:
        if t not in tag_used:
            tag_notused.append(t)

    return render_template('admin_blog/tag.html',tag_used=tag_used, tag_notused=tag_notused, tab=tab)


@bp.route('/del_tag',methods=['POST'])
@login_required
def del_tag():
    tag_id = request.form.get('id')
    tag = Tag.query.filter_by(id=tag_id).first()
    if tag is None:
        flash('No such tag','danger')
    else:
        db.session.delete(tag)
        db.session.commit()
        flash('The tag has been deleted','success')
    return redirect(url_for('admin_blog.tag',tab=2))


@bp.route('/edit_tag',methods=['POST'])
@login_required
def edit_tag():
    tag_id = request.form.get('id')
    tag_name = request.form.get('name').lower()
    tag = Tag.query.filter_by(id=tag_id).first()
    if tag is None:
        flash('No such tag','danger')
    else:
        if len(tag_name) > 12:
            flash('Name is too long','danger')
        else:
            name_exist = Tag.query.filter_by(name=tag_name).first()
            if name_exist:
                flash('Name already exists','danger')
            else:
                tag.name = tag_name
                tag.update_date = datetime.utcnow()
                db.session.add(tag)
                db.session.commit()
                flash('The tag has been updated','success')
    return redirect(url_for('admin_blog.tag'))
