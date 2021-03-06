from flask import render_template, current_app, make_response
from app.sitemap import bp
from datetime import datetime, timedelta
from os import listdir


@bp.route('/sitemap.xml', methods=['GET'])
def sitemap():
    pages = []

    # get static routes
    # use arbitary 10 days ago as last modified date
    lastmod = datetime.now() - timedelta(days=10)
    lastmod = lastmod.strftime('%Y-%m-%d')
    for rule in current_app.url_map.iter_rules():
        # omit auth and admin routes and if route has parameters. Only include if route has GET method
        if 'GET' in rule.methods and len(rule.arguments) == 0 \
                and not rule.rule.startswith('/admin'):
            pages.append(['http://localhost:5000' + rule.rule, lastmod])

    sitemap_template = render_template('sitemap/sitemap_template.xml', pages=pages)
    response = make_response(sitemap_template)
    response.headers['Content-Type'] = 'application/xml'
    return response
