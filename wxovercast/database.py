import sqlalchemy

import wxovercast.settings as settings
db_settings = settings.get("database")

connection_url = "%s://%s:%s@%s:%s/%s" %(db_settings['type'], 
                                         db_settings['username'], 
                                         db_settings['password'],
                                         db_settings['host'],
                                         db_settings['port'],
                                         db_settings['database'],)

engine = sqlalchemy.create_engine(connection_url)