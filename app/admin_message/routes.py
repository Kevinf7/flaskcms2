from flask import render_template, redirect, request, current_app, url_for, flash
from flask_login import login_required
from app import db
from app.admin_message import bp
from app.admin_message.models import Message
from app.breadcrumb import set_breadcrumb


# ADMIN MESSAGE routes 

@bp.route('/message',methods=['GET'])
@login_required
@set_breadcrumb('home message')
def message():
    page = request.args.get('page',1,type=int)
    messages = Message.query.order_by(Message.create_date.desc()) \
    .paginate(page,current_app.config['MESSAGES_PER_PAGE'],False)

    return render_template('admin_message/message.html',messages=messages)


@bp.route('/message/del_message',methods=['POST'])
@login_required
def del_message():
    msg_id = request.form.getlist('id')
    msg = Message.query.filter_by(id=msg_id).first()
    if not msg:
        flash('No such message','danger')
        return redirect(url_for('admin_message.message'))
    else:
        db.session.delete(msg)
        db.session.commit()
        flash('The message has been deleted','success')
    return redirect(url_for('admin_message.message'))
