# -*- coding: utf-8 -*-
# This file is part of tears
#
# SQLAlchemy single connection strategy overwrite to run tests
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

tears - SQLAlchemy single connection strategy overwrite to run tests
        in a super transaction and rollback at teardown.

"""

import sqlalchemy.engine.strategies
import sqlalchemy.engine.base
import logging

__version__ = '0.2'

log = logging.getLogger('tears')


class Connection(sqlalchemy.engine.base.Connection):
    def __init__(self, *args, **kwargs):
        super(Connection, self).__init__(*args, **kwargs)
        self.__transaction = sqlalchemy.engine.base.RootTransaction(self)

    def teardown(self):
        """Rollback the super transaction"""
        self.__transaction.rollback()
        self.__transaction = sqlalchemy.engine.base.RootTransaction(self)

    def begin(self):
        """Ensure that there is a super transaction even after a rollback"""
        if self.__transaction is None:
            self.__transaction = sqlalchemy.engine.base.RootTransaction(self)
        return super(Connection, self).begin()

    def close(self):
        """Do NOT close the connection"""


class Engine(sqlalchemy.engine.base.Engine):

    def __init__(self, *args, **kwargs):
        super(Engine, self).__init__(*args, **kwargs)
        self._tears_connection = Connection(self, **kwargs)

    def connect(self, **kwargs):
        return self._tears_connection

    def contextual_connect(self, **kwargs):
        return self._tears_connection

    def setup(self):
        pass

    def teardown(self):
        self._tears_connection.teardown()


class TearsEngineStrategy(sqlalchemy.engine.strategies.DefaultEngineStrategy):
    """Strategy for configuring an Engine with threadlocal behavior."""

    name = 'plain'
    engine_cls = Engine

TearsEngineStrategy()
