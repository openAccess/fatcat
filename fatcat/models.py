
"""
states for identifiers:
- pre-live: points to a rev (during edit/accept period)
- live: points to a rev
- redirect: live, points to upstream rev, also points to redirect id
    => if live and redirect non-null, all other fields copied from redirect target
- deleted: live, but doesn't point to a rev

possible refactors:
- '_rev' instead of '_revision'
"""

from fatcat import db

# TODO: EntityMixin, EntityIdMixin

class WorkContrib(db.Model):
    __tablename__ = "work_contrib"
    work_rev= db.Column(db.ForeignKey('work_revision.id'), nullable=False, primary_key=True)
    creator_id = db.Column(db.ForeignKey('creator_id.id'), nullable=False, primary_key=True)
    type = db.Column(db.String, nullable=True)
    stub = db.Column(db.String, nullable=True)

    creator = db.relationship("CreatorId")
    work = db.relationship("WorkRevision")

class ReleaseContrib(db.Model):
    __tablename__ = "release_contrib"
    release_rev = db.Column(db.ForeignKey('release_revision.id'), nullable=False, primary_key=True)
    creator_id = db.Column(db.ForeignKey('creator_id.id'), nullable=False, primary_key=True)
    type = db.Column(db.String, nullable=True)
    stub = db.Column(db.String, nullable=True)

    creator = db.relationship("CreatorId")
    release = db.relationship("ReleaseRevision")

class ReleaseRef(db.Model):
    __tablename__ = "release_ref"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    release_rev= db.Column(db.ForeignKey('release_revision.id'), nullable=False)
    target_release_id= db.Column(db.ForeignKey('release_id.id'), nullable=False)
    index = db.Column(db.Integer, nullable=True)
    stub = db.Column(db.String, nullable=True)
    doi = db.Column(db.String, nullable=True)

    release = db.relationship("ReleaseRevision")
    target = db.relationship("ReleaseId")

class FileRelease(db.Model):
    __tablename__ = "file_release"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    file_rev= db.Column(db.ForeignKey('file_revision.id'), nullable=False)
    release_id = db.Column(db.ForeignKey('release_id.id'), nullable=False)

    release = db.relationship("ReleaseId")
    file = db.relationship("FileRevision")

class WorkId(db.Model):
    """
    If revision_id is null, this was deleted.
    If redirect_id is not null, this has been merged with the given id. In this
        case revision_id is a "cached" copy of the redirect's revision_id, as
        an optimization. If the merged work is "deleted", revision_id can be
        null and redirect_id not-null.
    """
    __tablename__ = 'work_id'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    live = db.Column(db.Boolean, nullable=False, default=False)
    revision_id = db.Column(db.ForeignKey('work_revision.id'), nullable=True)
    redirect_id = db.Column(db.ForeignKey('work_id.id'), nullable=True)

class WorkLog(db.Model):
    __tablename__ = 'work_log'
    # ID is a monotonic int here; important for ordering!
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    work_id = db.Column(db.ForeignKey('work_id.id'), nullable=False)
    old_revision_id = db.Column(db.ForeignKey('work_revision.id'), nullable=True)
    old_redirect_id = db.Column(db.ForeignKey('work_id.id'), nullable=True)
    new_revision_id = db.Column(db.ForeignKey('work_revision.id'), nullable=True)
    new_redirect_id = db.Column(db.ForeignKey('work_id.id'), nullable=True)
    # TODO: is this right?
    edit_id = db.Column(db.ForeignKey('edit.id'))

class WorkRevision(db.Model):
    __tablename__ = 'work_revision'
    id = db.Column(db.Integer, primary_key=True)
    previous = db.Column(db.ForeignKey('work_revision.id'), nullable=True)
    edit_id = db.Column(db.ForeignKey('edit.id'))
    extra_json = db.Column(db.ForeignKey('extra_json.sha1'), nullable=True)

    title = db.Column(db.String)
    work_type = db.Column(db.String)
    date = db.Column(db.String)

    creators = db.relationship('WorkContrib', lazy='subquery',
        backref=db.backref('works', lazy=True))

class ReleaseId(db.Model):
    __tablename__ = 'release_id'
    id = db.Column(db.Integer, primary_key=True)
    live = db.Column(db.Boolean, nullable=False, default=False)
    revision_id = db.Column(db.ForeignKey('release_revision.id'))
    redirect_id = db.Column(db.ForeignKey('release_id.id'), nullable=True)

class ReleaseRevision(db.Model):
    __tablename__ = 'release_revision'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    previous = db.Column(db.ForeignKey('release_revision.id'), nullable=True)
    edit_id = db.Column(db.ForeignKey('edit.id'))
    extra_json = db.Column(db.ForeignKey('extra_json.sha1'), nullable=True)

    work_id = db.ForeignKey('work_id.id')
    container_id = db.Column(db.ForeignKey('container_id.id'), nullable=True)
    title = db.Column(db.String, nullable=False)
    license = db.Column(db.String, nullable=True)   # TODO: oa status foreign key
    release_type = db.Column(db.String)             # TODO: foreign key
    date = db.Column(db.String, nullable=True)      # TODO: datetime
    doi = db.Column(db.String, nullable=True)       # TODO: identifier table
    volume = db.Column(db.String, nullable=True)
    pages = db.Column(db.String, nullable=True)
    issue = db.Column(db.String, nullable=True)

    creators = db.relationship('ReleaseContrib', lazy='subquery')
        #backref=db.backref('releases', lazy=True))
    refs = db.relationship('ReleaseRef', lazy='subquery')
        #backref=db.backref('backrefs', lazy=True))

class CreatorId(db.Model):
    __tablename__ = 'creator_id'
    id = db.Column(db.Integer, primary_key=True)
    live = db.Column(db.Boolean, nullable=False, default=False)
    revision_id = db.Column(db.ForeignKey('creator_revision.id'))
    redirect_id = db.Column(db.ForeignKey('creator_id.id'), nullable=True)

class CreatorRevision(db.Model):
    __tablename__ = 'creator_revision'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    previous = db.Column(db.ForeignKey('creator_revision.id'), nullable=True)
    edit_id = db.Column(db.ForeignKey('edit.id'))
    extra_json = db.Column(db.ForeignKey('extra_json.sha1'), nullable=True)
    #creator_ids = db.relationship("CreatorId", backref="revision", lazy=False)

    name = db.Column(db.String)
    sortname = db.Column(db.String)
    orcid = db.Column(db.String)            # TODO: identifier table

class ContainerId(db.Model):
    __tablename__ = 'container_id'
    id = db.Column(db.Integer, primary_key=True)
    live = db.Column(db.Boolean, nullable=False, default=False)
    revision_id = db.Column(db.ForeignKey('container_revision.id'))
    redirect_id = db.Column(db.ForeignKey('container_id.id'), nullable=True)

class ContainerRevision(db.Model):
    __tablename__ = 'container_revision'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    previous = db.Column(db.ForeignKey('container_revision.id'), nullable=True)
    edit_id = db.Column(db.ForeignKey('edit.id'))
    extra_json = db.Column(db.ForeignKey('extra_json.sha1'), nullable=True)

    name = db.Column(db.String)
    container_id = db.Column(db.ForeignKey('container_id.id'))
    publisher = db.Column(db.String)        # TODO: foreign key
    sortname = db.Column(db.String)
    issn = db.Column(db.String)             # TODO: identifier table

class FileId(db.Model):
    __tablename__ = 'file_id'
    id = db.Column(db.Integer, primary_key=True)
    live = db.Column(db.Boolean, nullable=False, default=False)
    revision_id = db.Column('revision', db.ForeignKey('file_revision.id'))
    redirect_id = db.Column(db.ForeignKey('file_id.id'), nullable=True)

class FileRevision(db.Model):
    __tablename__ = 'file_revision'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    previous = db.Column(db.ForeignKey('file_revision.id'), nullable=True)
    edit_id = db.Column(db.ForeignKey('edit.id'))
    extra_json = db.Column(db.ForeignKey('extra_json.sha1'), nullable=True)

    size = db.Column(db.Integer)
    sha1 = db.Column(db.Integer)            # TODO: hash table... only or in addition?
    url = db.Column(db.Integer)             # TODO: URL table

    releases = db.relationship('FileRelease', lazy='subquery')
        #backref=db.backref('backrefs', lazy=True))

class Edit(db.Model):
    __tablename__ = 'edit'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    edit_group = db.Column(db.ForeignKey('edit_group.id'), nullable=True)
    editor = db.Column(db.ForeignKey('editor.id'), nullable=False)
    comment = db.Column(db.String, nullable=True)
    extra_json = db.Column(db.ForeignKey('extra_json.sha1'), nullable=True)
    # WARNING: polymorphic. Represents the id that should end up pointing to
    # this revision.
    # TODO: this doesn't work
    entity_id = db.Column(db.Integer, nullable=True)

class EditGroup(db.Model):
    __tablename__ = 'edit_group'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    editor = db.Column(db.ForeignKey('editor.id'))
    description = db.Column(db.String)

class Editor(db.Model):
    __tablename__ = 'editor'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String)

class ChangelogEntry(db.Model):
    # XXX: remove this?
    __tablename__= 'changelog'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    edit_id = db.Column(db.ForeignKey('edit.id'))
    timestamp = db.Column(db.Integer)

class ExtraJson(db.Model):
    __tablename__ = 'extra_json'
    sha1 = db.Column(db.String, primary_key=True)
    json = db.Column(db.String)
