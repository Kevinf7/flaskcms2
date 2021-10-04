from flask import render_template, redirect, url_for, flash, request, current_app, session
from flask_login import current_user, login_required
from app import db
from app.admin_blog import bp
from app.admin_blog.models import Post, Tag, Tagged
from app.admin_media.models import ImageType, Images
from app.admin_media.models import Images
from app.admin_media.routes import process_image
from datetime import datetime
from slugify import slugify
from app.breadcrumb import set_breadcrumb


# ADMIN BLOG routes

@bp.route('/blog',methods=['GET', 'POST'])
@login_required
@set_breadcrumb('home blog')
def blog():
    if 'blog_show_type' in session:
        show_type = session['blog_show_type']
    else:
        show_type = 'all'
    if request.method == 'POST':
        s = request.form.get('show_type')
        if s!= 'all' and s!= 'published' and s!= 'draft':
            flash('Show type error', 'danger')
        else:
            show_type = s
    page = request.args.get('page',1,type=int)
    if show_type == 'all':
        session['blog_show_type'] = 'all'
        posts = Post.query.order_by(Post.active.desc(), Post.create_date.desc()) \
        .paginate(page,current_app.config['POSTS_PER_PAGE'],False)
    elif show_type == 'published':
        session['blog_show_type'] = 'published'
        posts = Post.query.filter_by(active=True) \
        .order_by(Post.create_date.desc()) \
        .paginate(page,current_app.config['POSTS_PER_PAGE'],False)
    elif show_type == 'draft':
        session['blog_show_type'] = 'draft'
        posts = Post.query.filter_by(active=False) \
        .order_by(Post.create_date.desc()) \
        .paginate(page,current_app.config['POSTS_PER_PAGE'],False)

    return render_template('admin_blog/blog.html',posts=posts,show_type=show_type)


def processTags(tags_new,post):
    tags_current = post.getTagNames()
    # check if any tags should be deleted
    for tag in tags_current:
        if tag not in tags_new:
            id = Tag.getTagId(tag)
            Tagged.query.filter_by(post_id=post.id,tag_id=id).delete()
            changed=True
    # is there tags to add?
    if not(len(tags_new) == 1 and tags_new[0] == ''):
        for tag in tags_new:
            if Tag.getTagId(tag) == -1:
                t = Tag(name=tag)
                db.session.add(t)
                changed=True
        #check if any tags should be added
        for tag in tags_new:
            if tag not in tags_current:
                id = Tag.getTagId(tag)
                t = Tagged(post_id=post.id, tag_id=id)
                db.session.add(t)


def getUploadedImage(img_num):
    r = request.files
    img_key = 'new_image'+str(img_num)
    if img_key in r:
        new_image = request.files[img_key]
        if new_image:
            upload_path = current_app.config['UPLOAD_PATH_BLOG']
            upload_path_thumb = current_app.config['UPLOAD_PATH_THUMB_BLOG']
            img_type_obj = ImageType.query.filter_by(name='blog').first()
            resp = process_image(new_image,upload_path,upload_path_thumb,img_type_obj)
            if resp['status'] == 'error':
                flash(resp['msg'])
                return False
            else:
                return Images.query.filter_by(filename=resp['msg']).first()
    return False


@bp.route('/post',methods=['GET','POST'])
@login_required
@set_breadcrumb('home blog post')
def post():
    new_tags=''
    if request.method=='POST':
        title = request.form.get('title')
        slug = slugify(title)
        if Post.getPostBySlug(slug) is None:
            post_data = request.form.get('post')
            post = Post(title=title,slug=slug,post=post_data,author=current_user)
            
            new_path = request.form.get('new_path1')
            if new_path:
                i = new_path.rsplit('/',1)
                img = Images.query.filter_by(filename=i[1]).first()
                setattr(post,'image1',img)
            else:
                img = getUploadedImage(1)
                if img:
                    setattr(post,'image1',img)

            db.session.add(post)
            tags = request.form.get('tags')
            tag_list = [t.strip() for t in tags.split(',')]
            processTags(tag_list,post)
            db.session.commit()
            new_tags = post.getTagNamesStr()
            flash('Your post has been published','success')
            return redirect(url_for('admin_blog.edit_post',id=post.id))
        else:
            flash('Title already exists on another post','danger')
    return render_template('admin_blog/post.html',tags=new_tags)


@bp.route('/edit_post',methods=['GET','POST'])
@login_required
@set_breadcrumb('home blog edit-post')
def edit_post():
    id = request.args.get('id')
    if not id:
        flash('id is missing','danger')
        return redirect(url_for('admin_blog.blog'))

    post = Post.query.filter_by(id=id).first()
    if not post:
        flash('Post not found','danger')
        return redirect(url_for('admin_blog.blog',not_used=True))

    if request.method=='POST':
        title = request.form.get('title')
        slug = slugify(title)
        check_post = Post.getPostBySlug(slug)
        if (check_post is not None and check_post.id != post.id):
            flash('Title already exists on another post','danger')
        else:
            image_id = request.form.get('image_id1')
            if image_id:
                pass
            else:
                new_path = request.form.get('new_path1')
                if new_path:
                    i = new_path.rsplit('/',1)
                    img = Images.query.filter_by(filename=i[1]).first()
                    setattr(post,'image1',img)
                else:
                    img = getUploadedImage(1)
                    if img:
                        setattr(post,'image1',img)

            post.title = title
            post.slug = slug
            post.post = request.form.get('post')
            post.update_date = datetime.utcnow()
            db.session.add(post)
            tags = request.form.get('tags')
            tag_list = [t.strip() for t in tags.split(',')]
            processTags(tag_list,post)
            db.session.commit()
            flash('Post has been updated','success')

    tags = post.getTagNamesStr()
    return render_template('admin_blog/edit_post.html',post=post,tags=tags)


@bp.route('/del_post',methods=['POST'])
@login_required
def del_post():
    post_id = request.form.get('id')
    del_type = request.form.get('del_type')
    post = Post.query.filter_by(id=post_id).first()
    if post is None:
        flash('No such post exist','danger')
    elif del_type != 'soft' and del_type != 'hard' and del_type != 'restore':
        flash('Delete type error','danger')
    else:
        if del_type == 'restore':
            post.active=True
            db.session.add(post)
            flash('The post has been restored','success')
        else:
            tagged = Tagged.query.filter_by(post_id=post.id).all()
            for t in tagged:
                db.session.delete(t)
            if del_type == 'soft':
                post.active=False
                db.session.add(post)
                flash('The post has been soft deleted','success')
            elif del_type == 'hard':
                db.session.delete(post)
                flash('The post has been hard (permanently) deleted','success')
        db.session.commit()
        
    return redirect(url_for('admin_blog.blog'))

