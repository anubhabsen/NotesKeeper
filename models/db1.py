# -*- coding: utf-8 -*-

db.define_table('label_category',
                Field('label_name', requires=IS_NOT_EMPTY()),
                auth.signature)

db.define_table('note',
                Field('title', requires=IS_NOT_EMPTY()),
                Field('body', 'text', requires=IS_NOT_EMPTY()),
                Field('other', 'upload'),
                auth.signature)


db.define_table('note_comment',
                Field('note_id', 'reference note', readable=False, writable=False),
                Field('body', requires=IS_NOT_EMPTY()),
                auth.signature)

db.define_table('label',
                Field('note_id', 'reference note'),
                Field('name'),
#                Field('label_category_id', 'reference label_category', requires=IS_IN_DB(db, db.label_category.id, '%(label_name)s')),
                auth.signature)

db.define_table('share_note',
                Field('note_id', 'reference note'),
                Field('user_id', 'reference auth_user'),
                auth.signature)
