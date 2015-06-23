"""Service handling managing artifacts in db and index."""

from datetime import datetime
import uuid
import requests
import os
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import desc

import settings
from core.service_template import ServiceTemplate
from core.db.models import River, Measure
from core.perflogger import time_logger

logger = settings.getLogger(__name__)


class RiverService(ServiceTemplate):
    """
    Service for river management.
    """

    def __init__(self, _db_sess):
        super().__init__(_db_sess)

    @time_logger
    def find_river_by_identifier(self, identifier):
        """Find river by identifier"""

        if not identifier:
            raise ValueError(
                "Can't find river without identifier!")
        q = self.sess.query(River).filter(River.identifier == identifier)
        river = q.one()
        if river:
            return river.to_artifact()
        return None

    @time_logger
    def find_measures(self, river_id, start=0, rows=100, db_model=False):
        measures = []
        try:
            q = self.sess.query(Measure)
            q = q.filter(Measure.river_id == river_id)
            db_ms = q.order_by(Measure.measured_at.desc()).offset(start).limit(
                rows)
            if db_model:
                return db_ms
            elif db_ms:
                for s in db_ms:
                    measures.append(s.to_artifact())
        except NoResultFound:
            return None
        return measures

    @time_logger
    def find_rivers(self, start=0, rows=1000, db_model=False):
        """Find and return a list of rivers"""
        rivers = []
        try:
            q = self.sess.query(River)
            db_rivers = q.order_by(River.name).offset(start).limit(rows)
            if db_model:
                return db_rivers
            elif db_rivers:
                for s in db_rivers:
                    if s.source == 'NVE':
                        rivers.append(s.to_artifact())
        except NoResultFound:
            return None
        return rivers

    @time_logger
    def get_river(self, river_id, db_model=False):
        """Find and return a river or None"""
        if not river_id:
            raise ValueError("Need river_id to get river!")

        try:
            q = self.sess.query(River)
            q = q.filter(River.id == river_id)
            db_river = q.one()
            if db_river:
                if db_model:
                    return db_river
                else:
                    return db_river.to_artifact()
        except NoResultFound:
            return None
        return None

    @time_logger
    def get_measure(self, river_id, measured_at, db_model=False):
        """Find and return a measure for river at measured_at or None"""
        if not river_id:
            raise ValueError("Need river_id to get measure!")
        if not measured_at:
            raise ValueError("Need measured_at to get measure!")
        try:
            q = self.sess.query(Measure)
            q = q.filter(Measure.river_id == river_id)
            q = q.filter(Measure.measured_at == measured_at)
            db_measure = q.one()
            if db_measure:
                if db_model:
                    return db_measure
                else:
                    return db_measure.to_artifact()
        except NoResultFound:
            return None
        return None

    @time_logger
    def put_river(self, river, db_model=False):
        """Create or update river"""
        if not river.name or not river.identifier:
            raise ValueError(
                "Can't create river without name and identifier!")
        if river.id:
            q = self.sess.query(River).filter(River.id == river.id)
            db_river = q.one()
        else:
            db_river = River()
        db_river.update_from_artifact(river)
        db_river.modified = datetime.utcnow()
        self.sess.add(db_river)
        self.sess.flush()
        self.sess.refresh(db_river)
        if db_model:
            return db_river
        else:
            return db_river.to_artifact()

    @time_logger
    def sync_river(self, river):
        """
        download measure data and update measures for river
        :param river:
        :return:
        """
        if river.source == 'NVE':
            self.sync_river_nve(river)
        elif river.source == 'GLB':
            self.sync_river_glb(river)
        else:
            raise ValueError("Invalid river source: %s" % river.source)

    def sync_river_nve(self, river):
        data_file = self.download_river_nve(river)
        with open(data_file, 'r') as f:
            for line in f.readlines():
                measure = self.nve_to_measure(river, line)
                if measure:
                    if (not river.latest_measure_at or
                                measure.measured_at > river.latest_measure_at):
                        existing = self.get_measure(
                            river_id=river.id, measured_at=measure.measured_at,
                            db_model=True)
                        if existing:
                            existing.level = measure.level
                            existing.cumecs = measure.cumecs
                            self.sess.add(existing)
                        else:
                            self.sess.add(measure)
                        river.latest_measure_at = measure.measured_at
                        river.latest_level = measure.level
                        river.latest_cumecs = measure.cumecs
        os.remove(data_file)
        return river

    def download_river_nve(self, river):
        data_file = "%s/%s.txt" % (settings.tmp_dir(), str(uuid.uuid4()))
        logger.info("Downloading NVE data for %s to %s" % (
            river.name, data_file))
        rv = requests.get("http://www2.nve.no/h/hd/plotreal/Q/%s/basis.txt" %
                          river.identifier)
        with open(data_file, 'w') as f:
            f.write(rv.text)
        return data_file

    def nve_to_measure(self, river, line):
        if line and line.strip():
            try:
                dl = line.strip()
                if dl and not dl.startswith("#"):
                    data = [ds.strip() for ds in dl.split()]
                    if data:
                        dt = datetime.strptime(data[0], "%d%m%Y/%H%M")
                        level = data[1]
                        try:
                            cumecs = float(data[2])
                        except:
                            cumecs = 0.0
                        return Measure(measured_at=dt, level=level,
                                       cumecs=cumecs, river_id=river.id)
            except Exception as e:
                logger.exception("Error measuring NVE for %s" + river.name)
                return None
            return None

    def sync_river_glb(self, river):
        return river


if __name__ == '__main__':
    from core.db.models import conn

    with conn() as sess:
        rs = RiverService(_db_sess=sess)
        for river in rs.find_rivers(db_model=True):
            rs.sync_river(river)
