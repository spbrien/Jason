# -*- coding: utf-8 -*-

import multiprocessing
import json

import click
import falcon
from wsgiref import simple_server

from models import Connection


@click.command()
@click.option(
    '--database',
    prompt=True,
    help='Database name.'
)
@click.option(
    '--username',
    prompt=True,
    default='root',
    help='Database username.'
)
@click.option(
    '--password',
    prompt=True,
    default='root',
    help='Database password.'
)
@click.option(
    '--hostname',
    prompt=True,
    default='192.168.33.133',
    help='Hostname for the database server.'
)
@click.option(
    '--port',
    prompt=True,
    default='3306',
    help='Port for the running MySQL instance.'
)
def main(database, username, password, hostname, port):
    """Console script for turning your database into JSON"""

    db_string = 'mysql+mysqldb://%s:%s@%s:%s/%s' % (username, password, hostname, port, database)
    connection = Connection(db_string)

    class DatabaseResource:
        def on_get(self, req, resp, table, column=None, identifier=None):
            """Handles GET requests"""
            data = connection.get_entity(table, column, identifier)
            if data['success']:
                resp.status = falcon.HTTP_200
                resp.body = json.dumps(data['content'])
            else:
                resp.status = falcon.HTTP_404
                resp.body = json.dumps(data['content'])

    class MapResource:
        def on_get(self, req, resp):
            """Outputs a map of the database structure"""
            resp.status = falcon.HTTP_200
            resp.body = json.dumps(connection.get_tables())

    class HomeResource:
        def on_get(self, req, resp):
            """Outputs usage instructions"""
            resp.status = falcon.HTTP_200
            resp.body = 'Visit /api/map to list Database tables and column \
                         \nVisit /api/TABLE_NAME/COLUMN_NAME/VALUE to filter results to a specific database entry'

    # Application
    app = falcon.API()
    # Init resources
    resource = DatabaseResource()
    db_map = MapResource()
    home = HomeResource()
    # Create routes
    # this response can be giant -- need to create pagination
    app.add_route('/api/{table}', resource)
    # ---
    app.add_route('/', home)
    app.add_route('/api/{table}/{column}/{identifier}', resource)
    app.add_route('/api/map', db_map)

    httpd = simple_server.make_server('127.0.0.1', 8000, app)

    try:
        click.echo(click.style("\n[+] API available at http://127.0.0.1:8000\n", fg="white", bold=True))
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.shutdown()
        httpd.server_close()

if __name__ == "__main__":
    main()
