tears
=====


Description
-----------


SQLAlchemy single connection strategy overwrite to run tests in a super transaction and rollback at teardown.

This SQLAlchemy class uses an unique connection with an external transaction (see: http://www.sqlalchemy.org/docs/orm/session.html#joining-a-session-into-an-external-transaction)

It overrides the plain strategy to implement custom `Engine` and `Connection`


It exposes two methods:
   - `setup` which creates a new external transaction
   - `teardown` which rollbacks the external transaction

This **MUST** be used only in testing environment for obvious reasons.


Usage
-----


A common pattern would be:

````python
   if testing:
     import tears
   import sqlalchemy
   # sqlalchemy stuff
````

and in tests:

````python
    def setUp():
        app.db.session.bind.setup()

    def tearDown():
        app.db.session.bind.rollback()
````
