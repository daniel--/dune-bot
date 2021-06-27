# custom sqlalchemy column type for a pendulum datetime - https://pendulum.eustace.io/
from datetime import datetime

import pendulum
import sqlalchemy as sa

from sqlalchemy.types import TypeDecorator as _TypeDecorator

from sqlalchemy_utils.types.scalar_coercible import ScalarCoercible as _ScalarCoercible


class PendulumType(_TypeDecorator, _ScalarCoercible):

    impl = sa.TIMESTAMP

    def __init__(self, *args, **kwargs):
        if "timezone" not in kwargs:
            kwargs["timezone"] = True

        super().__init__(*args, **kwargs)

    def process_bind_param(self, value, dialect):
        if value:
            utc_val = self._coerce(value).in_tz("UTC")
            return utc_val if self.impl.timezone else utc_val.naive()
        return value

    def process_result_value(self, value, dialect):
        if value:
            return pendulum.instance(value)
        return value

    def process_literal_param(self, value, dialect):
        return str(value)

    def _coerce(self, value):
        if value is None:
            return None
        elif isinstance(value, str):
            value = pendulum.parse(value, strict=False)
        elif isinstance(value, datetime):
            value = pendulum.instance(value)
        return value

    @property
    def python_type(self):
        return self.impl.type.python_type
