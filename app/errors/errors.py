from flask import render_template, request, jsonify, redirect
from . import bp
from flask_wtf.csrf import CSRFError


@bp.app_errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('errors/csrf_error.html', reason=e.description), 400


@bp.app_errorhandler(400)
def bad_request(e):
    header = request.headers.get('Content-Type')
    if header == 'application/json':
        response = jsonify({'error': 'bad request'})
        response.status_code = 400
        return response
    else:
        return render_template('errors/400.html'), 400


@bp.app_errorhandler(404)
def not_found(e):
    # Only use this if your site is a SPA
    return redirect('/')
    # return render_template('errors/404.html'), 404


@bp.app_errorhandler(500)
def internal_server_error(e):
    header = request.headers.get('Content-Type')
    if header == 'application/json':
        response = jsonify({'error': 'internal server error'})
        response.status_code = 500
        return response
    else:
        return render_template('errors/500.html'), 500


@bp.app_errorhandler(405)
def method_not_allowed(e):
    response = jsonify({'error': 'method not allowed'})
    response.status_code = 405
    return response