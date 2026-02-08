from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton, Factory

from infrastructure.databases.postgresql.session.sessionmanager import DatabaseSessionManager
from infrastructure.repository.postgresql.item.uow import PostgreSQLItemRepositoryUOW
from infrastructure.repository.postgresql.user.uow import PostgreSQLUserRepositoryUOW


class Container(DeclarativeContainer):
    session_manager = Singleton(DatabaseSessionManager)

    session_item = Factory(PostgreSQLItemRepositoryUOW)
    session_user = Factory(PostgreSQLUserRepositoryUOW)