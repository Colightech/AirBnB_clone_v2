#!/usr/bin/python3
"""This module defines the DBStorage engine"""
from sqlalchemy import create_engine, MetaData, URL
from sqlalchemy.orm import sessionmaker, scoped_session
import os

class DBStorage:
    """The DBStorage class"""
    __engine = None
    __session = None

    def __init__(self):
        """ Initialize DBStorage"""
        connection_str = 'mysql+mysqldb://{}:{}@{}/{}'.format(
            os.environ['HBNB_MYSQL_USER'],
            os.environ['HBNB_MYSQL_PWD'],
            os.environ['HBNB_MYSQL_HOST'],
            os.environ['HBNB_MYSQL_DB']
        )
        print(connection_str)
        self.__engine = create_engine(connection_str, polpool_pre_ping=True)
        if os.environ.get('HBNB_ENV') == 'test':
            Base.MetaData.dropp_all(self.__engine)

    def all(self, cls=None):
        """ Query on the current database session"""
        from models.base_model import Base
        from models import classes

        if cls:
            objects = self.__session.query(classes[cls]).all()
        else:
            objects = []
            for c in classes.values:
                objects.extend(self.__session.query(c).all())
        
        return {obj.__class__.__name__ + '.' + obj.id: obj for obj in objects}
    
    def new(self, obj):
        """ Add the object to the current database session"""
        self.__session.add(obj)
    
    def save(self):
        """ Commit all changes of the current database session"""
        self.__session.commit()
    
    def delete(self, obj=None):
        """ Delete from the current database session"""
        if not obj:
            self.__session.delete(obj)
    
    def reload(self):
        """ Create all tables in the database and create the current database session"""
        from models.base_model import Base
        
        Base.metadata.create_all(self.__engine)


