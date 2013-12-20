tears
=====


Description
-----------


Flask SQLAlchemy single connection extension to run tests in a super transaction and rollback at teardown.

This SQLAlchemy class uses an unique connection with an external transaction (see: http://www.sqlalchemy.org/docs/orm/session.html#joining-a-session-into-an-external-transaction)

It overrides the `get_engine` method to return the connection instead
of the engine in order to prevent other connections creation.

It exposes two methods:
   - `setup` which creates a new external transaction
   - `teardown` which rollbacks the external transaction

This **MUST** be used only in testing environment for obvious reasons.


Usage
-----


A common pattern would be:

````python
   if testing:
       from tears import SQLAlchemy
   else:
       from flask_sqlalchemy import SQLAlchemy
````

and in tests:

````python
    def setUp():
        app.db.setup()

    def tearDown():
        app.db.teardown()
````
