from sqlalchemy.ext.declarative import declarative_base

# declarative_base will return a class, other class can inherit this Base class, then become a database class
Base = declarative_base()