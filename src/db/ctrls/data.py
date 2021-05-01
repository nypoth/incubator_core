import logging

from src.db.config import get_session
from src.db.models.data import Config, ConfigSchema, Atmospheric, AtmosphericSchema
from src.db.utils import SessionScope

logger = logging.getLogger(__name__)

db_session = get_session()


def get_settings():
    with SessionScope(db_session) as s:
        query = s.session.query(Config).first()

    if s.exit_status:
        logger.error(f'Errore Query {s.exit_status}')
        return []

    return query


def insert_data(data: Atmospheric):
    with SessionScope(db_session) as s:
        query = s.session.add(data)

    if s.exit_status:
        logger.error(f'Errore Query {s.exit_status}')
        return []

    return query
