"""
Class for working with dict based generic artifact as object and json.
"""

from datetime import datetime
import json


class DictWrapper(dict):
    """Wrapper class for dict enabling access to elements object attributes."""

    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)

    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            return None  # Artifact.empty_attr

    def __setattr__(self, name, value):
        if name:
            self[name] = value

    def __delattr__(self, name):
        del self[name]

    @classmethod
    def _json_serializer_hook(cls, obj):
        # DIMU java format for dates in json: yyyyMMdd-HHmmss-S
        if isinstance(obj, datetime):
            if obj is not None:
                try:
                    return obj.strftime('%Y%m%d-%H%M%S-%f')
                except:
                    return None
            return None
        else:
            return json.JSONEncoder.encode(obj)

    def to_json(self, pretty=False):
        """ Return json representation. """
        if pretty:
            return json.dumps(self, indent=4, sort_keys=True,
                              default=self._json_serializer_hook,
                              separators=(',', ':'))
        else:
            return json.dumps(self, default=self._json_serializer_hook,
                              separators=(',', ':'))


class Artifact(DictWrapper):
    """Artifact wrapper class

        Proxy class for dict, to be able to access
        elements as object attributes
        ie: artifact.identifier.id, as well as artifact['identifier']['id']
    """
    empty_attr = DictWrapper()
    DATE_ATTRIBUTES = ['created_at', 'updated_at', 'published_at',
                       'archived_at', 'end_at', 'start_at', 'expires_at',
                       'latest_measure_at']

    def __init__(self, *args, **kwargs):
        DictWrapper.__init__(self, *args, **kwargs)

    @classmethod
    def from_json(cls, artifact_json):
        """Builds struct-dict of json """
        res = json.loads(artifact_json,
                         object_hook=cls._json_deserializer_hook)
        # convert date attributes to datetime
        for da in Artifact.DATE_ATTRIBUTES:
            if da in res and res[da] is not None:
                res[da] = datetime.strptime(res[da], '%Y%m%d-%H%M%S-%f')
        return res

    @classmethod
    def is_date(cls, name):
        """ Return True if name is date attribute. """
        return name and name in Artifact.DATE_ATTRIBUTES

    @classmethod
    def to_date(cls, value):
        """ Return datetime object """
        try:
            if isinstance(value, datetime):
                return value
            else:
                return datetime.strptime(value, '%Y%m%d-%H%M%S-%f')
        except:
            return None

    @classmethod
    def date_to_str(cls, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y%m%d-%H%M%S-%f')
        return obj

    @classmethod
    def _json_deserializer_hook(cls, dct):
        return Artifact(dct)

    @classmethod
    def traverse(cls, o):
        """
        Traverses and yields dicts in o
        """
        if isinstance(o, dict):
            yield o
            for v in o.values():
                if isinstance(v, dict) or isinstance(v, list):
                    for nv in cls.traverse(v):
                        yield nv
        elif isinstance(o, list):
            for l in o:
                for ores in cls.traverse(l):
                    yield ores

