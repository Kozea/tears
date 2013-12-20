# -*- coding: utf-8 -*-
# This file is part of tears
#
# Flask SQLAlchemy single connection extension to run tests
# in a super transaction and rollback at teardown.
# Copyright © 2013 Florian Mounier
#
# This library is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with tears. If not, see <http://www.gnu.org/licenses/>.


"""

tears - Flask SQLAlchemy single connection extension to run tests
        in a super transaction and rollback at teardown.

"""


from flask_sqlalchemy import SQLAlchemy as FlaskSQLAlchemy

__version__ = '0.1'


class SQLAlchemy(FlaskSQLAlchemy):
    """
       This SQLAlchemy class uses an unique connection with an external
       transaction (see: http://www.sqlalchemy.org/docs/orm/session.html
                         #joining-a-session-into-an-external-transaction)

       It overrides the `get_engine` method to return the connection instead
       of the engine in order to prevent other connections creation.

       It exposes two methods:
          `setup` which creates a new external transaction
          `teardown` which rollbacks the external transaction

       This MUST be used only in testing environment for obvious reasons.
       A common pattern would be:
       ````
          if testing:
              from tears import SQLAlchemy
          else:
              from flask_sqlalchemy import SQLAlchemy
       ````

       and in tests:
       ````
           def setUp():
               app.db.setup()

           def tearDown():
               app.db.teardown()
       ````
       """

    def get_engine(self, app, bind=None):
        """Returns the connection and creates it on first call"""

        if not hasattr(self, '_mono_connection'):
            engine = super(SQLAlchemy, self).get_engine(app, bind)
            self._connection = engine.connect()

            # Apparently we cannot use sane row count in this case:
            self._connection.dialect.supports_sane_rowcount = False

            # Start a transaction in case of
            self._transaction = self._connection.begin()

        return self._connection

    def setup(self, *args, **kwargs):
        """If there is an ongoing connection roll it back"""

        if self._transaction:
            self._transaction.rollback()

        # Start a new transaction inside the connection
        self._transaction = self._connection.begin()

    def teardown(self, *args, **kwargs):
        """Rollback the transaction"""

        self._transaction.rollback()
        self._transaction = None
