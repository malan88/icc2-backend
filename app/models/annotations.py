from datetime import datetime as dt

from sqlalchemy.orm import backref

from app import db
from app.models.mixins import Base

class Annotation(Base):
    bookid = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', backref=backref('annotations', lazy='dynamic'))

    created = db.Column(db.DateTime)

    edits = db.relationship('Edit', back_populates='annotation')

    HEAD = db.relationship('Edit',
                           primaryjoin='Edit.annotation_id==Annotation.id',
                           uselist=False)

    def __init__(self, book, author, start, end, text, *args, **kwargs):
        self.created = dt.now()
        self.bookid = book
        self.author = author
        super().__init__(*args, **kwargs)
        self.edits.append(Edit(author, start, end, text))


class Edit(Base):
    annotation_id = db.Column(db.Integer, db.ForeignKey('annotation.id'),
                              index=True)
    text = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    editor = db.relationship('User', backref=backref('edits', lazy='dynamic'))

    start = db.Column(db.Integer)
    end = db.Column(db.Integer)

    created = db.Column(db.DateTime)

    annotation = db.relationship('Annotation', back_populates='edits')

    def __init__(self, editor, start, end, text, *args, **kwargs):
        self.editor = editor
        self.start, self.end = start, end
        self.text = text
        self.created = dt.utcnow()
        super().__init__(*args, **kwargs)
