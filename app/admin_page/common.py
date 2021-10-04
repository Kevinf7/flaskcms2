from flask import flash, request, current_app
from flask_login import current_user
from app.admin_page.models import Page, PageStatus
from app.admin_media.models import ImageType, Images
from app.admin_media.routes import process_image
from app import db
from datetime import datetime


def getImage(page, num_images):
    for r in range(1,num_images+1):
        image_id = request.form.get('image_id'+str(r))
        if image_id:
            if image_id == 'none':
                pass
            elif image_id == 'del':
                setattr(page,'image_id'+str(r),None)
            else:
                setattr(page,'image_id'+str(r),int(image_id))
        else:
            new_path = request.form.get('new_path'+str(r))
            if new_path:
                i = new_path.rsplit('/',1)
                img = Images.query.filter_by(filename=i[1]).first()
                setattr(page,'image'+str(r),img)
            else:
                reqfile = request.files
                img_key = 'new_image'+str(r)
                if img_key in reqfile:
                    new_image = reqfile[img_key]
                    if new_image:
                        upload_path = current_app.config['UPLOAD_PATH_PAGE']
                        upload_path_thumb = current_app.config['UPLOAD_PATH_THUMB_PAGE']
                        img_type_obj = ImageType.query.filter_by(name='page').first()
                        resp = process_image(new_image,upload_path,upload_path_thumb,img_type_obj)
                        if resp['status'] == 'error':
                            flash(resp['msg'],'danger')
                            return False
                        else:
                            img = Images.query.filter_by(filename=resp['msg']).first()
                            setattr(page,'image'+str(r),img)
                    else:
                        flash('Image key no value','danger')
                        return False
                else:
                    flash('Image key not found','danger')
                    return False
    return True


def page_post(page_model, page_name, fields, num_images):
    edit_ver = None
    if request.method == 'POST':
        page_id = request.form.get('id')
        page = page_model.query.filter_by(id=int(page_id)).first()
        if page:
            data = {}
            for f in fields:
                if f['type'] == 'int':
                    data[f['name']] = request.form.get(f['name'], type=int)
                else:
                    data[f['name']] = request.form.get(f['name'])
    
            action = request.form.get('action')
            if action == 'Delete':
                if page.page_status.name == 'draft':
                    db.session.delete(page)
                    db.session.commit()
                    flash('Draft deleted', 'success')
                else:
                    flash('This page is not a draft', 'danger')
            elif action == 'Save':
                if page.page_status.name == 'draft':
                    if getImage(page, num_images):
                        for f in fields:
                            setattr(page,f['name'],data[f['name']])
                        page.author = current_user
                        page.update_date = datetime.utcnow()
                        page.create_date = datetime.utcnow()
                        db.session.add(page)
                        db.session.commit()
                        flash('Draft saved', 'success')
                else:
                    flash('This page is not a draft', 'danger')
            elif action == 'Save as draft':
                page = page_model.query.filter_by(page_status=PageStatus.getStatus('draft')).first()
                if not page:
                    page = page_model(page_id=Page.getPage(page_name).id, \
                        page_status=PageStatus.getStatus('draft'), author=current_user, \
                        update_date=datetime.utcnow(), create_date = datetime.utcnow())
                    for r in range(1,num_images+1):
                        image_id=request.form.get('image_id'+str(r))
                        if (image_id != 'none' and image_id != 'del'):
                            setattr(page,'image_id'+str(r),image_id)
                    for f in fields:
                        setattr(page,f['name'],data[f['name']])
                    db.session.add(page)
                    db.session.commit()
                    flash('Saved as draft', 'success')
                else:
                    for r in range(1,num_images+1):
                        image_id=request.form.get('image_id'+str(r))
                        if (image_id != 'none' and image_id != 'del'):
                            setattr(page,'image_id'+str(r),image_id)
                    for f in fields:
                        setattr(page,f['name'],data[f['name']])
                    page.author = current_user
                    page.update_date = datetime.utcnow()
                    page.create_date = datetime.utcnow()
                    db.session.add(page)
                    db.session.commit()
                    flash('Saved as draft', 'success')
            elif action == 'Publish':
                if page.page_status == PageStatus.getStatus('published'):
                    flash('Page already published', 'danger')
                elif page.page_status == PageStatus.getStatus('draft'):
                    # there should only be 1 published.. this is just to make 100% sure
                    page_pub = page_model.query.filter_by(page_status=PageStatus.getStatus('published')).all()
                    for p in page_pub:
                        db.session.delete(p)

                    if getImage(page, num_images):
                        for f in fields:
                            setattr(page,f['name'],data[f['name']])
                        page.page_status = PageStatus.getStatus('published')
                        page.author = current_user
                        page.update_date = datetime.utcnow()
                        page.page.last_publish_by = current_user
                        page.page.last_publish_date = datetime.utcnow()
                        db.session.add(page)
                        db.session.commit()
                        flash('Page published', 'success')
                else:
                    flash('Status error', 'danger')
            elif action == 'Edit this version':
                edit_ver = page_model.query.filter_by(id=page_id).first()
            else:
                flash('Submit button error', 'danger')
        else:
            flash('id error', 'danger')

    if not edit_ver:
        page_draft = page_model.query.filter_by(page_status=PageStatus.getStatus('draft')).first()
        if page_draft:
            edit_ver = page_draft
        else:
            edit_ver = page_model.query.filter_by(page_status=PageStatus.getStatus('published')).first()
    
    all_ver = page_model.query.order_by(page_model.update_date.desc()).all()
    return([edit_ver, all_ver])