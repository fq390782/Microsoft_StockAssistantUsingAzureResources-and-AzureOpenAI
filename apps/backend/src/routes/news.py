import json
from fastapi import Depends, APIRouter, HTTPException
from typing import TYPE_CHECKING
from ..services import (
    NewsFetchAnalysisService
)
from ..core.clients import (
    get_redis_service_client, 
    RedisService
)
from ..modules.az_openai import get_azure_open_ai_instance
from ..services.schema_enums import REDIS_NEWS_STOCK
import logging
if TYPE_CHECKING:
    from openai import AzureOpenAI

router = APIRouter()

REDIS_NEWS_STOCK_EXPIRE_TTL_S = 60 * 30      # 30분


## /api/v1/news/stock
@router.get("/stock/{stock_name}")
async def get_stock_news_data(
        stock_name: str,
        redis_client: RedisService = Depends(get_redis_service_client),
        az_openai: "AzureOpenAI" = Depends(get_azure_open_ai_instance),
):
    """[GET] 해당 주식 종목에 대한 뉴스 감정 분석 데이터를 받도록 합니다.

    Examples
    --------
        GET: ``/api/v1/news/stock/삼성전자``
    
    """
    #
    #   :TODO
    #   - 해당 뉴스 분석 코드 분리 
    #   - 주기적인 트리거/캐시 
    #
    # Redis 캐시 로드 (존재할 경우 즉시 반환)
    cached = redis_client.get(
        REDIS_NEWS_STOCK.format(name=f"{stock_name}")
    )
    if cached:
        try:
            return json.loads(cached)   # type: ignore
        except Exception as e:
            logging.error(e)
            return cached

    # 캐시 없을 경우
    service = NewsFetchAnalysisService()
    data = service.fetch_news_with_naver_api(str(stock_name))
    if data:
        data = service.analyze_news_and_convert_datetime(
            az_openai, data
        )

    # (새로운 데이터) Redis 캐시 저장
    if data:
        try:
            redis_client.set(
                REDIS_NEWS_STOCK.format(name=f"{stock_name}"),
                json.dumps(data, ensure_ascii=False),
                ex=REDIS_NEWS_STOCK_EXPIRE_TTL_S
            )
        except Exception as e:
            logging.error(e)
    return data

