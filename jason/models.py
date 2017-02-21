import operator

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from utils import format_json


# TODO: Add function to process filters
def parse_filters(filters):
    if 'filter' in filters:
        filters['filter'] = [
            get_operator(f) for f in filters['filter']
        ]
    return filters


# TODO: Add function to get operators
def get_operator(string):
    operator_map = {
        '==': operator.eq,
        '!=': operator.ne,
        '>=': operator.ge,
        '<=': operator.le,
        '>': operator.gt,
        '<': operator.lt,
    }
    for op in operator_map:
        if op in string:
            plan = {
                'operator': operator_map[op],  # Will be function
                'property_name': string.split(op)[0],
                'proptery_value': string.split(op)[1]
            }
    return plan


class Connection():

    def __init__(self, db_string):
        self.base = automap_base()
        self.engine = create_engine(db_string)
        self.base.prepare(self.engine, reflect=True)
        self.session = Session(self.engine)

    def get_database_map(self):
        tables = {
            table_class.__name__: [
                column_class.name for column_class
                in table_class.__table__.columns
            ] for table_class in self.base.classes
        }
        format_json(tables)

    def get_table_contents(
        self,
        table_class,
        filters=None
    ):
        # function to get the column name
        def column_name(column):
            return str(column).split('.')[1]

        # function to get the column contents
        def column_contents(table, column):
            return str(getattr(table, column_name(column)))

        # function to collect query results
        def collect_results(query):
            return [
                {
                     column_name(col): column_contents(item, col)
                     for col in table_class.__table__.columns
                }
                for item in query
            ]
        # def construct_query_with_filters(query_base):
        #     for item in filters:
        #         return getattr(query_base, item)()

        # if we don't have any filters, return all results
        # else return filtered results
        if table_class and not any(filters):
            q = self.session.query(table_class).all()
            return collect_results(q)

        return None

    def query(self, table=None, column=None, filters=None):
        # get query filters
        query_filters = parse_filters(filters)
        # Try to find the requested table, return None if non-existant fs
        table_to_query_class = next(
            (
                table_class for table_class
                in self.base.classes
                if table_class.__name__.lower() == table.lower()
            ),
            None
        )
        if not table_to_query_class:
            format_json({
                'error': 'The %s table does not exist' % table
            })

        if table_to_query_class and not column:
            format_json(
                self.get_table_contents(table_to_query_class, query_filters)
            )
