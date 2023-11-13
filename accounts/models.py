from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, text, func, Date, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TINYINT
from enum import Enum as PythonEnum

from sms.database import Base

class GenderEnum(PythonEnum):
    MALE = 'MALE'
    FEMALE = 'FEMALE'
    OTHERS = 'OTHERS'

class RoleEnum(PythonEnum):
    ADMIN = 'ADMIN'
    TEACHER = 'TEACHER'
    STUDENT = 'STUDENT'

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
    role = Column(Enum(RoleEnum), server_default=text("'STUDENT'"))
    dob = Column(Date)
    address = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def as_dict(self):
        serialized_user = {}
        for column in self.__table__.columns:
            column_name = column.name
            column_value = getattr(self, column_name)

            # Check if the column type is Enum
            if isinstance(column.type, Enum):
                # Convert Enum to its value
                column_value = column_value.value if column_value is not None else None

            serialized_user[column_name] = column_value

        return serialized_user
    
    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True
