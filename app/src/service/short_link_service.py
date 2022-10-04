from src.models.sqlalchemy.short_link import ShortLinkUrl, Base
from src.common.logger import logger_setting
import string
import secrets
from urllib.request import urlopen
from urllib.error import URLError
import ssl

log = logger_setting("INFO")


def verify_url(url: str) -> None:
    """
    옳바른 url인지 검증
    url open시 status가 200이 아닐 경우 -> 존재하지 않는 url
    url open시 URLError 발생할 경우 -> 존재하지 않는 url
    url open시 ValueError 발생할 경우 -> 잘못된 형식의 url
    :param url: requests url
    :return:
    """
    context = ssl._create_unverified_context()
    url_result = urlopen(url, context=context)
    if url_result.status != 200:
        raise URLError


def create_response(data: Base) -> dict:
    """
    orm model 객체를 받아 response의 데이터를 구성하여 리턴한다.
    :param data: orm model 객체
    :return: response dict
    """
    response = {"data": {}}
    response["data"]["shortId"] = data.short_id
    response["data"]["url"] = data.url
    response["data"]["createdAt"] = data.create_date

    return response


class ShortLinkService:
    def __init__(self, session):
        """
        short link 기능을 수행하기 위한 클래스
        :param session: db 커넥션 객체
        """
        self._session = session

    def search_short_id(self, short_id: str) -> Base:
        """
        short id에 해당되는 데이터 객체를 리턴한다.
        :param short_id: short id
        :return: orm model 객체
        """
        data = self._session.query(ShortLinkUrl).filter(ShortLinkUrl.short_id==short_id).first()
        return data

    def search_url(self, url: str) -> Base:
        """
        url에 해당되는 데이터 객체를 리턴한다.
        :param url: url
        :return: orm model 객체
        """
        data = self._session.query(ShortLinkUrl).filter(ShortLinkUrl.url==url).first()
        return data

    def _create_short_id(self) -> str:
        """
        랜덤한 5자 길이의 alphanumeric 문자열을 생성하여 리턴한다.
        :return: 랜덤 문자열
        """
        alphabet = string.ascii_letters + string.digits
        short_id = ''.join(secrets.choice(alphabet) for i in range(5))
        return short_id

    def insert_url(self, url: str) -> None:
        """
        url을 받아 db에 insert 한다.
        short id가 이미 존재할 경우 중복이 없을때까지 재생성
        :param url: url
        :return:
        """

        while True:
            short_id = self._create_short_id()
            if self.search_short_id(short_id=short_id) is None:
                break

        url_model = ShortLinkUrl(
            short_id=short_id,
            url=url
        )
        self._session.add(url_model)
        self._session.commit()
