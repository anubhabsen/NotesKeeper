# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
#########################################################################


def index():
    return locals()


@auth.requires_login()
def welcome():
    return locals()


@auth.requires_login()
def add_note():
    form_note = SQLFORM(db.note).process()
    if form_note.accepted:
        session.flash = "New Note Created"
    return locals()


@auth.requires_login()
def add_label():
    form_label = SQLFORM(db.label_category).process()
    if form_label.accepted:
        session.flash = "New Label Created"
    return locals()


@auth.requires_login()
def attach_label():
    nt = db.note(request.args(0, cast=int))
    db.label.note_id.default = nt.id
    label_category_allowed = db(db.label_category.created_by == auth.user_id).select()
    label_category_set = []
    for lbl in label_category_allowed:
        label_category_set.append(lbl.label_name)
    db.label.name.requires = IS_IN_SET(label_category_set)
    form = SQLFORM(db.label).process()
    if form.accepted:
        session.flash = "New label attached"
    return locals()


@auth.requires_login()
def show_note():
    row = db.note(request.args(0, cast=int))
    db.note_comment.note_id.default = row.id
    form_comment = SQLFORM(db.note_comment).process()
    comments = db(db.note_comment.note_id == row.id).select(orderby=~db.note_comment.created_on)
    return locals()


@auth.requires_login()
def share_note():
    row = db.note(request.args(0, cast=int))
    db.share_note.note_id.default = row.id
    form_share = SQLFORM(db.share_note).process()
    return locals()


@auth.requires_login()
def shared_notes():
    rows = db(db.share_note.user_id == auth.user_id).select(orderby=~db.share_note.created_on)
    return locals()

@auth.requires_login()
def my_notes():
    notes = db(db.note.created_by == auth.user_id).select(orderby=~db.note.created_on)
    """note_id = []
    note_title = []
    note_labels = []
    for nt in notes:
        note_id.append(nt.id)
        note_title.append(nt.title)
        labels = db(db.label.note_id == nt.id).select()
        label_list = []
        for tag in labels:
            label_list.append(tag.name)
        note_labels.append(label_list)
    label_category_allowed = db(db.label_category.created_by == auth.user_id).select()
    label_category_set = []
    for lbl in label_category_allowed:
        label_category_set.append(lbl.label_name)
    """
    return locals()


@auth.requires_login()
def my_notes2():
    all_notes = db(db.note.created_by == auth.user_id).select(orderby=~db.note.created_on).as_list()
    tag_notes = []
    tag_names = db(db.label_category.created_by == auth.user_id).select(orderby=db.label_category.label_name).as_list()
    for tag_name in tag_names:
        tag = db(db.label.name == tag_name.label_name).select()
        tag_notes += tag
    return locals()


@auth.requires_login()
def edit_note():
    the_note = db.note(request.args(0, cast=int))
    form_note = SQLFORM(db.note, the_note, deletable=True).process()
    if form_note.accepted:
        session.flash = "Note Updated"
        redirect(URL('my_notes'))
    return locals()


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow
    administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
