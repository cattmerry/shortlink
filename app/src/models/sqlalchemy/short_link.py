from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, TEXT, DateTime, VARCHAR
import datetime

Base = declarative_base()


class ShortLinkUrl(Base):
    __tablename__ = "short_link_url"

    short_id = Column(VARCHAR, primary_key=True, comment="short id")
    create_date = Column(
        DateTime, nullable=False, default=datetime.datetime.utcnow, comment="생성시간"
    )
    update_date = Column(
        DateTime,
        nullable=False,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        comment="변경시간",
    )
    url = Column(TEXT, unique=True, nullable=False, comment="url")
