from flask import current_app, flash, redirect, render_template, request, url_for, jsonify, make_response
from flask_login import login_required
from app import db, csrf
from app.admin_media import bp
from app.admin_media.models import Images, ImageType
from app.breadcrumb import set_breadcrumb
from PIL import Image
from math import ceil
import os
from pathlib import Path


# ADMIN_MEDIA routes

@bp.route('/media', methods=['GET'])
@login_required
@set_breadcrumb('home media')
def media():
    page = request.args.get('page',1,type=int)
    if current_app.config['ADMIN_PAGE'] and not current_app.config['ADMIN_BLOG']:
        show = 'page'
    elif current_app.config['ADMIN_BLOG'] and not current_app.config['ADMIN_PAGE']:
        show = 'blog'
    else:
        show = request.args.get('show')
    # True means 404 error is returned if page is out of range. False means an empty list is returned
    if (show != 'blog' and show != 'page'):
        images = Images.query.order_by(Images.create_date.desc()) \
                            .paginate(page,current_app.config['IMAGES_PER_PAGE'],False)
    else:
        images = db.session.query(Images).join(ImageType) \
                            .filter(ImageType.name==show) \
                            .order_by(Images.create_date.desc()) \
                            .paginate(page,current_app.config['IMAGES_PER_PAGE'],False)
    if show:
        return render_template('admin_media/media.html',images=images,show=show)
    else:
        return render_template('admin_media/media.html',images=images)


@bp.route('/media/del_image', methods=['POST'])
@login_required
def del_image():
    show = request.form.get('show')
    id = request.form.get('id')
    image = Images.getImage(id)

    if image is None:
        flash('No such image.','danger')
    else:
        upload_path = current_app.config['UPLOAD_PATH_PAGE']
        upload_path_thumb = current_app.config['UPLOAD_PATH_THUMB_PAGE']
        if image.image_type.name == 'blog':
            upload_path = current_app.config['UPLOAD_PATH_BLOG']
            upload_path_thumb = current_app.config['UPLOAD_PATH_THUMB_BLOG']
        try:
            img_fullpath = os.path.join(upload_path, image.filename)
            tmb_fullpath = os.path.join(upload_path_thumb, image.thumbnail)
            os.remove(img_fullpath)
            os.remove(tmb_fullpath)
            db.session.delete(image)
            db.session.commit()
            flash('The image has been successfully deleted','success')
        except OSError:
            flash('System error, image not deleted','danger')
    if show:
        return redirect(url_for('admin_media.media',show=show))
    else:
        return redirect(url_for('admin_media.media'))


def process_image(file, upload_path, upload_path_thumb, img_type_obj):
    if file:
        filename = file.filename.lower()
        fn, ext = filename.split('.')
        if ext in ['jpg', 'gif', 'png', 'jpeg']:
            # truncate filename (excluding extension) to 30 characters
            fn = fn[:24]
            filename = fn + '.' + ext
            img_file = upload_path / filename
            if img_file.is_file():
                for i in range (1,11):
                    new_fn = fn + '-' + str(i)
                    filename = new_fn + '.' + ext
                    img_file = upload_path / filename
                    if not img_file.is_file():
                        break
            if not img_file.is_file():
                try:
                    # everything looks good, save file
                    img_fullpath = os.path.join(upload_path, filename)
                    file.save(img_fullpath)
                    # get the file size to save to db
                    file_size = ceil(os.stat(img_fullpath).st_size / 1024)
                    size = 200, 200
                    # read image into pillow
                    im = Image.open(img_fullpath)
                    # get image dimension to save to db
                    file_width, file_height = im.size
                    # convert to thumbnail
                    im.thumbnail(size)
                    thumbnail = fn + '-thumb.jpg'
                    tmb_fullpath = os.path.join(upload_path_thumb, thumbnail)
                    # PNG is index while JPG needs RGB
                    if not im.mode == 'RGB':
                        im = im.convert('RGB')
                    # save thumbnail
                    im.save(tmb_fullpath, "JPEG")

                    # save to db
                    img = Images(filename=filename, thumbnail=thumbnail, file_size=file_size, \
                                file_width=file_width, file_height=file_height, image_type=img_type_obj)
                    db.session.add(img)
                    db.session.commit()
                    return {'status': 'success','msg':filename}
                except IOError:
                    return {'status':'error','msg':'Cannot create thumbnail'}
            else:
                return {'status':'error','msg':'Filename already exists'}
        else:
            return {'status':'error','msg':'Filename needs to be JPG, JPEG, GIF or PNG'}
    return {'status':'error','msg':'File is empty'}


# imageuploader for tinyMCE
@bp.route('/imageuploader/<image_type>', methods=['POST'])
@login_required
@csrf.exempt
def imageuploader(image_type):
    if image_type != 'blog' and image_type != 'page':
        return make_response('image type is not correct', 400)
    upload_path = current_app.config['UPLOAD_PATH_PAGE']
    upload_path_thumb = current_app.config['UPLOAD_PATH_THUMB_PAGE']
    if image_type == 'blog':
        upload_path = current_app.config['UPLOAD_PATH_BLOG']
        upload_path_thumb = current_app.config['UPLOAD_PATH_THUMB_BLOG']
    img_type_obj = ImageType.query.filter_by(name=image_type).first()

    file = request.files.get('file')
    resp = process_image(file, upload_path, upload_path_thumb, img_type_obj)
    if resp['status'] == 'success':
        return jsonify({'location' : resp['msg']})
    elif resp['status'] == 'error':
        return make_response(resp['msg'], 400)
