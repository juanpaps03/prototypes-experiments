# Basic usage of alembic

In order to run any of the following commands you should be in the directory
`data-access/event-sourcing-example/event_sourcing_example`

Create a new migration running `alembic revision -m "some new table"`

Updating the DB `alembic upgrade head` head makes reference to the latest version, alembic run all the migration needed

In case of a specific version, you can do `alembic upgrade ae1` being ae1 the first letter of the uuid created for 
this migration, we can also do `alembic upgrade +2` or even `alembic updgrade -1` to move forward or backwards

