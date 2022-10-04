from fastapi import APIRouter, Depends
from app.src.models.pydantic.short_link import ShortLinkRequest
from app.src.core.database import get_db
from app.src.service.short_link_service import ShortLinkService, create_response, verify_url
from app.src.common.logger import logger_setting
from starlette.responses import Response
from starlette.status import HTTP_404_NOT_FOUND, HTTP_302_FOUND, HTTP_400_BAD_REQUEST
from starlette.responses import RedirectResponse
from urllib.error import URLError
from sqlalchemy.orm import Session

PREFIX = "/ab180"
short_link_route = APIRouter(prefix=PREFIX, tags=["ShortLink"])
log = logger_setting("INFO")


@short_link_route.post("/short-links")
async def create_short_link(
        request: ShortLinkRequest,
        db: Session = Depends(get_db)
):
    """
    URL을 입력하면 random한 ID를 가지는 short Link를 생성해주는 API
    URL을 검증하고 이미 등록된 URL이라면 등록되어있는 데이터를 리턴
    새로운 URL이라면 등록 후 해당 데이터 리턴
    :param request: 요청 본문
    :param db: db 커넥션 객체
    :return:
    """
    try:
        verify_url(url=request.url)
    except URLError as e:
        log.info(e.args[0])
        return Response(content=f"존재하지 않는 url 입니다. ==> {request.url}", status_code=HTTP_404_NOT_FOUND)
    except ValueError as e:
        log.info(e.args[0])
        return Response(content=f"url 형식이 잘못되었습니다. ==> {request.url}", status_code=HTTP_400_BAD_REQUEST)

    sls = ShortLinkService(session=db)
    url_data = sls.search_url(url=request.url)

    if url_data is not None:
        log.info(f"URL ==> {request.url} :: 이미 등록된 URL")
        response = create_response(data=url_data)

    else:
        log.info(f"URL ==> {request.url} :: 새로운 URL 등록")
        sls.insert_url(url=request.url)
        url_data = sls.search_url(url=request.url)
        response = create_response(data=url_data)

    return response


@short_link_route.get("/short-links/{short_id}")
async def search_short_link(
        short_id: str,
        db: Session = Depends(get_db)
):
    """
    short link 1개를 조회하는 API
    생성되지 않은 short id 받을 경우 404 에러 리턴
    :param short_id: short id
    :param db: db 커넥션 객체
    :return:
    """
    sls = ShortLinkService(session=db)
    short_id_data = sls.search_short_id(short_id=short_id)

    if short_id_data is None:
        return Response(content="생성하지 않은 short link", status_code=HTTP_404_NOT_FOUND)

    return create_response(data=short_id_data)


@short_link_route.get("/r/{short_id}", response_class=RedirectResponse, status_code=HTTP_302_FOUND)
async def redirect_url(
        short_id: str,
        db: Session = Depends(get_db)
):
    """
    short link를 통해 접속했을 때 원래 입력했던 URL로 리다이렉트 해주는 API
    생성되지 않은 short id 받을 경우 404 에러 리턴
    :param short_id: short id
    :param db: db 커넥션 객체
    :return:
    """
    sls = ShortLinkService(session=db)
    short_id_data = sls.search_short_id(short_id=short_id)

    if short_id_data is None:
        return Response(content="생성하지 않은 short link", status_code=HTTP_404_NOT_FOUND)

    return short_id_data.url
