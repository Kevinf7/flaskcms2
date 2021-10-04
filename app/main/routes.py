from flask import render_template
from app.main import bp
from app.admin_page.models import PageHomeMain, PageStatus


@bp.route('/')
def index():
    main = PageHomeMain.query.filter_by(page_status=PageStatus.getStatus('published')).first()
    return render_template('index.html', main=main)