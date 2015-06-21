"""
Service template
"""
from sqlalchemy.orm.exc import NoResultFound
from core.errors import CoreError, UnauthorizedError
from core.perflogger import time_logger
import settings


logger = settings.getLogger(__name__)


class ServiceException(CoreError):

    """Exception related to problems with feature operations."""

    pass


class ServiceTemplate(object):

    """
    Template for inheriting services

    service takes database session injected as dependency and lets
    the user of it to handle commits. Typically in app/blueprints.

    """

    def __init__(self, _db_sess):
        if not _db_sess:
            raise ValueError("Can't use service without db session. "
                             "Transactions should be controlled by caller")
        self.sess = _db_sess

    @time_logger
    def get_model(self, model_cls, model_id, db_model=False):
        """Find and return a site or None"""
        if not model_id:
            raise ValueError("Need model_id to get model!")
        try:
            q = self.sess.query(model_cls)
            q = q.filter(model_cls.id == model_id)
            db_site = q.one()
            if db_site:
                if db_model:
                    return db_site
                else:
                    return db_site.to_artifact()
        except NoResultFound:
            return None
        return None

    @time_logger
    def put_model(self, model_cls, model, db_model=False):
        """Create or update model"""

        if model.id:
            q = self.sess.query(model_cls).filter(model_cls.id == model.id)
            db_mod = q.one()
        else:
            db_mod = model_cls()
        db_mod.update_from_artifact(model)

        self.sess.add(db_mod)
        self.sess.flush()
        self.sess.refresh(db_mod)
        if db_model:
            return db_mod
        else:
            return db_mod.to_artifact()

    @time_logger
    def delete_model(self, model_cls, model_id):
        """delete model"""
        if not model_id:
            raise ValueError("Can't delete model %s without id" % model_cls)
        q = self.sess.query(model_cls).filter(model_cls.id == model_id)
        try:
            db_mod = q.one()
            if db_mod:
                self.sess.delete(db_mod)
                self.sess.flush()
                return True
        except NoResultFound:
            return False

    @time_logger
    def find_model_by_name(self, model_cls, name, db_model):
        try:
            q = self.sess.query(model_cls)
            q = q.filter(model_cls.name == name)
            db_mod = q.one()
            if db_model:
                return db_mod
            else:
                return db_mod.to_artifact()
        except NoResultFound:
            return None
