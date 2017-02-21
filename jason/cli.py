# -*- coding: utf-8 -*-

import json

import click

from models import Connection


# TODO: Change defaults to env variables
@click.command()
@click.option(
    '--database',
    default='scotchbox',
    help='Database name.'
)
@click.option(
    '--username',
    default='root',
    help='Database username.'
)
@click.option(
    '--password',
    default='root',
    help='Database password.'
)
@click.option(
    '--hostname',
    default='192.168.33.133',
    help='Hostname for the database server.'
)
@click.option(
    '--port',
    default='3306',
    help='Port for the running MySQL instance.'
)
def main(database, username, password, hostname, port):
    """Console script for turning your database into JSON"""

    db_string = 'mysql+mysqldb://%s:%s@%s:%s/%s' % (
        username,
        password,
        hostname,
        port,
        database
    )
    connection = Connection(db_string)
    connection.query(table="nonsense")


if __name__ == "__main__":
    main()
