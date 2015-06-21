# coding: utf-8
import uuid
from datetime import datetime
from contextlib import contextmanager

from sqlalchemy import Column, DateTime, ForeignKey, Float
from sqlalchemy import Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, backref
from sqlalchemy.orm import relationship, class_mapper, ColumnProperty
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine

from core.errors import DBError
from core.models.artifact import Artifact
import settings

engine = create_engine(settings.db_connection())
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
Base.metadata.bind = engine
metadata = Base.metadata


def next_uuid():
    return str(uuid.uuid4())


def create_session():
    """Create and return session for db."""
    return scoped_session(Session)


@contextmanager
def conn(session=None, commit=True):
    close_sess = session is None
    if close_sess:
        session = create_session()
    try:
        yield session
        if commit:
            session.commit()
    except SQLAlchemyError as e:
        if commit is not None:
            session.rollback()
        raise DBError(
            "A database error happened during db operation", e)
    except Exception as e:
        if commit:
            session.rollback()
        raise DBError(
            "An general error happened during db operation", e)
    finally:
        if close_sess:
            session.close()


class ModelTemplate(object):

    """Mixin that maps model objects to and from Artifact."""
    hidden_fields = ["digest_pass", "password"]

    @classmethod
    def hidden_field(cls, field_name):
        return field_name in cls.hidden_fields

    @classmethod
    def column_names(cls):
        res = []
        for prop in class_mapper(cls).iterate_properties:
            if (isinstance(prop, ColumnProperty) and
                    not cls.hidden_field(prop.key)):
                res.append(prop.key)
        return res

    def to_artifact(self):
        """Maps model to Artifact."""
        return ModelTemplate.model_to_artifact(self)

    @classmethod
    def model_to_artifact(cls, model):
        """Maps model to Artifact."""
        a = Artifact()
        for col in type(model).column_names():
            value = getattr(model, col)
            if value:
                a[col] = value
        return a

    def update_from_artifact(self, artifact):
        """Maps and loads model from Artifact."""
        if artifact is not None:
            for col in type(self).column_names():
                if col in artifact.keys():
                    value = artifact[col]
                    setattr(self, col, value)


class River(Base, ModelTemplate):
    __tablename__ = 'rivers'

    id = Column(Integer, primary_key=True)
    identifier = Column(String(length=255), nullable=False, unique=True)
    source = Column(String(length=255), nullable=False, unique=False)
    name = Column(String(length=255), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    latest_measure_at = Column(DateTime, nullable=True)
    latest_level = Column(String(length=20), nullable=True)
    latest_cumecs = Column(Float, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow,
                        onupdate=datetime.utcnow)


class Measure(Base, ModelTemplate):
    __tablename__ = 'measures'

    id = Column(Integer, primary_key=True)
    measured_at = Column(DateTime, nullable=False, index=True)
    level = Column(String(length=20), nullable=False)
    cumecs = Column(Float, nullable=False)
    river_id = Column(ForeignKey('rivers.id', deferrable=True),
                      nullable=False, index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True,
                        default=datetime.utcnow, onupdate=datetime.utcnow)

    river = relationship("River", backref=backref("measures"))
