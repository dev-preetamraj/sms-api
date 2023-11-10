from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, text, func, Date, Text
from sqlalchemy.dialects.mysql import TINYINT
from enum import Enum as PythonEnum

from sms.database import Base

class GenderEnum(PythonEnum):
    MALE = 'male'
    FEMALE = 'female'
    OTHERS = 'others'

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), unique=True, index=True)
    username = Column(String(20), unique=True, index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    password = Column(String(255), nullable=False)
    profile_picture = Column(String(255), server_default=text("'https://res.cloudinary.com/dxgl4eyhq/image/upload/v1699608195/sms/profile/default_profile.jpg'"))
    is_active = Column(TINYINT, server_default=text('1'))
    gender = Column(Enum(GenderEnum))
    dob = Column(Date)
    address = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
    
    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True