from pydantic import Field, BaseModel


class ShortLinkRequest(BaseModel):
    """
    short link 요청 본문 정의
    """

    url: str = Field(description="Short Link를 통해서 Landing이 될 URL")
