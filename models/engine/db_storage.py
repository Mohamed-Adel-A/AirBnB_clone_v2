#!/usr/bin/python3
""""""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv


class DBStorage():
    """"""
    __engine = None
    __session = None

    def __init__(self) -> None:

        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                getenv('HBNB_MYSQL_USER'),
                getenv('HBNB_MYSQL_PWD'),
                getenv('HBNB_MYSQL_HOST'),
                getenv('HBNB_MYSQL_DB')), pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            from models.base_model import Base
            from models.base_model import BaseModel
            from models.user import User
            from models.place import Place
            from models.state import State
            from models.city import City
            from models.amenity import Amenity
            from models.review import Review

            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        objects = None
        objects_dict = {}
        if cls is not None:
            objects = self.__session.query(cls).all()
        else:
            from models import base_model, user, place, state
            from models import city, amenity, review
            objects = self.__session.query(
                base_model.BaseModel,
                user.User,
                city.City,
                place.Place,
                state.State,
                amenity.Amenity,
                review.Review
            ).all()

        for obj in objects:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            objects_dict[key] = obj
        return objects_dict

    def new(self, obj):
        """add the object to the current database session"""
        if obj is not None:
            self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """
        create all tables in the database and
        create the current database session
        """
        from models.base_model import Base
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """
        call remove() method
        on the private session attribute (self.__session) 
        or close() on the class Session
        """
        return (self.__session.remove())
