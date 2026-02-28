from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton, Factory

from backend.src.infrastructure.databases.postgresql.session.sessionmanager import DatabaseSessionManager
from backend.src.infrastructure.repository.postgresql.item.uow import PostgreSQLItemRepositoryUOW
from backend.src.infrastructure.repository.postgresql.user.uow import PostgreSQLUserRepositoryUOW


class Container(DeclarativeContainer):
    session_manager = Singleton(DatabaseSessionManager)

    session_item = Factory(PostgreSQLItemRepositoryUOW)
    session_user = Factory(PostgreSQLUserRepositoryUOW)