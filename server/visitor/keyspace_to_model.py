from typing import TYPE_CHECKING, Callable, Dict

from sqlalchemy.orm import Query, scoped_session

from models import (
    Keyspace,
    KeyspaceCombinator,
    KeyspaceHybrid,
    KeyspaceMask,
    KeyspaceStraight,
)

if TYPE_CHECKING:
    from schemas import (
        KeyspaceBase,
        KeyspaceCombinatorSchema,
        KeyspaceHybridSchema,
        KeyspaceMaskSchema,
        KeyspaceStraightSchema,
    )

from .ikeyspace import IKeyspaceVisitor


class BaseKeyspaceModelConverter(IKeyspaceVisitor):
    _exclude_fields: Dict

    def _to_dict(self, schema: "KeyspaceBase") -> Dict:
        return {
            k: v for k, v in schema.model_dump(exclude=self._exclude_fields).items()
        }


class KeyspaceModelQueryExecutor(BaseKeyspaceModelConverter):
    _session: scoped_session
    _callback: Callable[[Query], None]

    def __init__(
        self,
        session: scoped_session,
        callback: Callable[[Query], None],
        exclude_fields: Dict,
    ):
        self._session = session
        self._callback = callback
        self._exclude_fields = exclude_fields

    def configure_straight(self, schema: "KeyspaceStraightSchema"):
        self._make_query(KeyspaceStraight, schema)

    def configure_combinator(self, schema: "KeyspaceCombinatorSchema"):
        self._make_query(KeyspaceCombinator, schema)

    def configure_mask(self, schema: "KeyspaceMaskSchema"):
        self._make_query(KeyspaceMask, schema)

    def configure_hybrid(self, schema: "KeyspaceHybridSchema"):
        self._make_query(KeyspaceHybrid, schema)

    def _make_query(self, model: "Keyspace", schema: "KeyspaceBase"):
        keyspace_data = self._to_dict(schema)
        query = self._session.query(model).filter_by(**keyspace_data)
        self._callback(query)


class KeyspaceModelCreator(BaseKeyspaceModelConverter):
    _callback: Callable[[Keyspace], None]

    def __init__(self, callback: Callable[[Keyspace], None], exclude_fields: Dict):
        self._callback = callback
        self._exclude_fields = exclude_fields

    def configure_straight(self, schema: "KeyspaceStraightSchema"):
        self._make_query(KeyspaceStraight, schema)

    def configure_combinator(self, schema: "KeyspaceCombinatorSchema"):
        self._make_query(KeyspaceCombinator, schema)

    def configure_mask(self, schema: "KeyspaceMaskSchema"):
        self._make_query(KeyspaceMask, schema)

    def configure_hybrid(self, schema: "KeyspaceHybridSchema"):
        self._make_query(KeyspaceHybrid, schema)

    def _make_query(self, model: "Keyspace", schema: "KeyspaceBase"):
        keyspace_data = self._to_dict(schema)
        self._callback(model(**keyspace_data))
