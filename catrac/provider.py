# -*- coding: utf-8 -*-

from trac.core import *
from trac.env import IEnvironmentSetupParticipant
from trac.db import Table, Column, Index


class CatracProvider(Component):
    """
    Class responsible for creating the database tables in the installation of the plugin
    """
    implements(IEnvironmentSetupParticipant)
    
    SCHEMA = [
        Table('catrac', key = ('name','internalid'))[
              Column('name','varchar'),
              Column('internalid','int'),                            
        ]        
    ]

    # IEnvironmentSetupParticipant methods
    def environment_created(self):
        self._upgrade_db(self.env.get_db_cnx())

    def environment_needs_upgrade(self, db):
        cursor = db.cursor()
        #if self._need_migration(db):
        #    return True
        try:
            cursor.execute("select count(*) from catrac")
            cursor.fetchone()
            return False
        except:
            db.rollback()
            return True

    def upgrade_environment(self, db):
        self._upgrade_db(db)
        
    def _upgrade_db(self, db):
        try:
            try:
                from trac.db import DatabaseManager
                db_backend, _ = DatabaseManager(self.env)._get_connector()
            except ImportError:
                db_backend = self.env.get_db_cnx()

            cursor = db.cursor()
            for table in self.SCHEMA:
                for stmt in db_backend.to_sql(table):
                    self.env.log.debug(stmt)
                    cursor.execute(stmt)                              
            cursor.execute("INSERT INTO permission (username,action)VALUES('authenticated','CATRAC_VIEW');")
            db.commit()

        except:
            db.rollback()
            raise
