from models import user_model
from sqlalchemy import (
    ARRAY,
    TIMESTAMP,
    Boolean,
    ForeignKey,
    Integer,
    SmallInteger,
    String,
    Text,
    func,
)
from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship


class Base(DeclarativeBase):
    pass


# TODO: add info for admin row
class User(Base):
    __tablename__ = "users"

    id = mapped_column(String(41), primary_key=True)
    email = mapped_column(String(255), nullable=False)
    phone = mapped_column(String(20), nullable=False)
    password = mapped_column(String(255), nullable=False)
    first_name = mapped_column(String(100), nullable=False)
    middle_name = mapped_column(String(100), nullable=False)
    last_name = mapped_column(String(100), nullable=False)
    verify = mapped_column(Boolean, default=False)
    role = mapped_column(SmallInteger, default=0)
    created_at = mapped_column(TIMESTAMP, default=func.current_timestamp())

    organization = relationship("Organization", back_populates="user")
    tender = relationship("Tender", back_populates="user")

    def to_model(self) -> user_model.User:
        return user_model.User(
            id=self.id,
            email=self.email,
            phone=self.phone,
            password=self.password,
            first_name=self.first_name,
            middle_name=self.middle_name,
            last_name=self.last_name,
            verify=self.verify,
            role=self.role,
            create_date=self.created_at,
        )


class Organization(Base):
    __tablename__ = "organizations"

    id = mapped_column(String(40), primary_key=True)
    brand_name = mapped_column(String(255), nullable=False)
    short_name = mapped_column(String(50), nullable=False)
    inn = mapped_column(String(12), nullable=False)
    okpo = mapped_column(String(12), nullable=False)
    orgn = mapped_column(String(12), nullable=False)
    kpp = mapped_column(String(12), nullable=False)
    tax_code = mapped_column(Integer, nullable=False)
    real_address = mapped_column(String(255), nullable=False)
    registered_address = mapped_column(String(255), nullable=False)
    mail_address = mapped_column(String(255), nullable=False)
    user_id = mapped_column(String(40), ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="organization")
    documents = relationship("Document", back_populates="organization")


class Document(Base):
    __tablename__ = "documents"

    id = mapped_column(String(40), primary_key=True)
    url = mapped_column(String(255), nullable=False)
    organization_id = mapped_column(String(40), ForeignKey("organizations.id"))

    organization = relationship("Organization", back_populates="documents")


class Tender(Base):
    __tablename__ = "tender"

    id = mapped_column(String(40), primary_key=True)
    name = mapped_column(String(255), nullable=False)
    price = mapped_column(Integer, nullable=False)
    is_contract_price = mapped_column(Boolean, nullable=False)
    regions = mapped_column(ARRAY(Text), nullable=False)
    floor_space = mapped_column(Integer, nullable=False)
    description = mapped_column(String(400))
    wishes = mapped_column(String(400))
    attachments = mapped_column(ARRAY(Text))
    services_groups = mapped_column(ARRAY(Integer))
    services_types = mapped_column(ARRAY(Integer))
    active = mapped_column(Boolean, default=False, nullable=False)
    reception_start = mapped_column(
        TIMESTAMP, server_default=func.current_timestamp()
    )
    reception_end = mapped_column(
        TIMESTAMP, server_default=func.current_timestamp()
    )
    work_start = mapped_column(
        TIMESTAMP, server_default=func.current_timestamp()
    )
    work_end = mapped_column(
        TIMESTAMP, server_default=func.current_timestamp()
    )
    object_group_id = mapped_column(Integer, ForeignKey("objects_groups.id"))
    object_type_id = mapped_column(Integer, ForeignKey("objects_types.id"))
    user_id = mapped_column(String(40), ForeignKey("users.id"), nullable=False)
    created_at = mapped_column(
        TIMESTAMP, server_default=func.current_timestamp()
    )

    user = relationship("User", back_populates="tender")
    object_group = relationship("ObjectGroup", back_populates="tender")
    object_type = relationship("ObjectType", back_populates="tender")


class ObjectGroup(Base):
    __tablename__ = "objects_groups"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(40))

    object_type = relationship("ObjectType", back_populates="object_group")
    tender = relationship("Tender", back_populates="object_group")


class ObjectType(Base):
    __tablename__ = "objects_types"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(40))
    object_group_id = mapped_column(Integer, ForeignKey("objects_groups.id"))

    object_group = relationship("ObjectGroup", back_populates="object_type")
    tender = relationship("Tender", back_populates="object_type")


class ServiceGroup(Base):
    __tablename__ = "services_groups"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(40))

    service_type = relationship("ServiceType", back_populates="service_group")


class ServiceType(Base):
    __tablename__ = "services_types"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(90))
    service_group_id = mapped_column(Integer, ForeignKey("services_groups.id"))

    service_group = relationship("ServiceGroup", back_populates="service_type")


class Logs(Base):
    __tablename__ = "logs"

    id = mapped_column(String(40), primary_key=True)
    method = mapped_column(String(6), nullable=False)
    url = mapped_column(String(255), nullable=False)
    body = mapped_column(Text, nullable=False)
    code = mapped_column(SmallInteger, nullable=False)
    msg = mapped_column(Text, default="")
    created_at = mapped_column(TIMESTAMP, default=func.current_timestamp())
