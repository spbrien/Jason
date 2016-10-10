from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import json


class Connection():
    
    def __init__(self, db_string):
        self.base = automap_base()
        self.engine = create_engine(db_string)
        self.base.prepare(self.engine, reflect=True)
        self.session = Session(self.engine)

    def format_out(self, data):
        return json.dumps(
                            data,
                            sort_keys=True,
                            indent=4,
                            separators=(',', ': ')
                         )


    def table_to_dict(self, c):
        return [
                    {
                         str(col).split('.')[1]: str(getattr(item, str(col).split('.')[1]))
                         for col in c.__table__.columns
                    }
                    for item in self.session.query(c).all()
                ]

    def all_json(self):
        return self.format_out({c.__name__: table_to_dict(c) for c in self.base.classes})


    def all_dict(self):
        return {c.__name__: self.table_to_dict(c) for c in self.base.classes}


    def get_tables(self):
        tables = {c.__name__: [item.name for item in c.__table__.columns]
                  for c in self.base.classes
                  }
        return tables


    def get_entity(self, table=None, column=None, identifier=None):
        req_table_class = next(
                (c for c in self.base.classes if c.__name__.lower() == table.lower()),
                None
            )

        if not req_table_class:
            return {
                    'success': False,
                    'content': {
                        'error': 404,
                        'msg': 'No such database table exists'
                    }
                }

        if column is None:
            return {
                    'success': True,
                    'content': table_to_dict(req_table_class)
                }
        else:
            try:
                result = self.session.query(req_table_class).filter(
                    getattr(req_table_class, column) == identifier
                ).first()
            except AttributeError:
                return {
                        'success': False,
                        'content': {
                            'error': 404,
                            'msg': 'Are you sure that column exists? Column names are case-sensitive...'
                        }
                    }

            if result:
                return {
                        'success': True,
                        'content': {
                             str(col).split('.')[1]: str(getattr(result, str(col).split('.')[1]))
                             for col in result.__table__.columns
                        }
                    }
            else:
                return {
                        'success': False,
                        'content': {
                            'error': 404,
                            'msg': 'No such entity exists'
                        }
                    }

