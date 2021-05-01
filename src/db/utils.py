import logging

from sqlalchemy.orm import Session, sessionmaker

logger = logging.getLogger(__name__)

FORCE_DETAIL_LOG = True
SUPPRESS_EXCEPTION = True

# region EXCEPTIONS


class QueryException:
    """Eccezione query"""

    def __init__(self, exception):
        self._exception = exception

    @property
    def exception(self):
        return repr(self._exception)

    @property
    def exception_obj(self):
        return self._exception

    def __repr__(self):
        return str(self._exception[0].__name__) + ' - ' + str(self._exception[1])

    @property
    def json(self):
        return str(self._exception[0].__name__) + ' - ' + str(self._exception[1])


def is_query_exception(query) -> bool:
    return isinstance(query, QueryException)
# endregion


class SessionScope:
    """Provide a transactional scope around a series of operations."""

    def __init__(self, session_conf, suppress_exception=None):
        self.session: Session = session_conf()
        self.suppress_exception = suppress_exception
        self._exec = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        if exc_type is None:
            self._exec = None

            try:
                self.session.commit()
            except Exception as e:
                self.session.rollback()
                logger.exception('Rollback for exception on session commit!')
                self._exec = (type(e), e, e.__traceback__)
        else:
            self.session.rollback()
            logger.exception('Rollback for exception during session')
            self._exec = (exc_type, exc_val, exc_tb)

        self.session.close()

        return self.suppress_exception or SUPPRESS_EXCEPTION

    @property
    def exit_status(self):
        return self._exec
