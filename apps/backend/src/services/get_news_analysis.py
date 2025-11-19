"""뉴스 데이터 분석 및 반환
"""
import json
from typing import Optional, Union, TYPE_CHECKING, TypedDict
from news_analysis import NewsDataPipelineAPI
from news_analysis.service.news_preprocess import NaverNewsContentTDict, NaverNewsApiResultTDict
from ..modules.az_openai import (
    send_conversation_to_openai
)
from ..modules.date_time import time_ago
from ..settings import api_settings
if TYPE_CHECKING:
    from openai import AzureOpenAI
import logging

__all__ = (
    'NewsFetchAnalysisService',
)

class NaverNewsAnalyzedDict(TypedDict):
    """분석과 처리를 거친 데이터 
    >>> [
        {
            "index: 0,
            "link": "https://n.news.naver.com/mnews/article/030/0003369731?sid=105",
            "originallink": "https://www.etnews.com/20251110000159",
            "title": "리벨리온, 美 법인 설립…오라클 출신 임원 영입",
            "content": "리벨리온은 글로벌 시장 공략을 위해 미국에 법인을 설립하고, 오라클 출신 반도체 전문가를 영입했다고 13일 밝혔다.",
            "timeAgo": "1시간 전",
            "sentiment": "긍정"
            "
        },
        ...
    ]
    """
    index: int
    link: str
    originallink: str
    title: str
    content: str
    timeAgo: str
    sentiment: str


class NewsFetchAnalysisService:
    """뉴스 데이터 분석 및 반환 
    """
    def __init__(self) -> None:
        self._service = NewsDataPipelineAPI(
            api_settings.NAVER_API_CLIENT_ID, 
            api_settings.NAVER_API_SECRET_KEY
        )

    def fetch_news_with_naver_api(self, stock_name: str):
        """뉴스를 Fetch하고 데이터를 반환.

        :param stock_name: (str) 종목 한글 명 입력. (예: 삼성전자, LG)
        
        """
        DISPLAY_AMOUNT = 10
        fetched = self._service.fetch_news_from_naver_api(
            stock_name, display=DISPLAY_AMOUNT
        )
        return fetched
    

    def analyze_news_and_convert_datetime(self, az_openai: "AzureOpenAI",
                                data: Union[list[NaverNewsContentTDict], 
                                            list[NaverNewsApiResultTDict]]
    ) -> list[NaverNewsAnalyzedDict]:
        """[감정 분석] 해당 데이터를 LLM Context로 바꾸고 컨텍스트 전송

        Args:
            data (list[NaverNewsContentTNaverNewsAnalyzedDictDict])
        """
        system = """
당신은 탁월한 감정 분석가입니다.  
각 항목의 뉴스 title과 description을 보고 해당 뉴스 텍스트에 대해 주식 투자를 위한 감정 분석을 하면 됩니다.  
각 항목의 순서대로 '긍정', '중립', '부정'을 리스트 형식으로 출력해주세요. 단 한 항목도 빠뜨리지 말고 채워주세요.  
분석하기 모호한 경우 반드시 '중립'이라 표시하세요. 절대로 추측성으로 하지 마세요.

JSON 응답 예시:
    ["중립", "긍정", "부정", "중립"]
"""
        _context_data = [ {
                            "title": item["title"], 
                            "description": item['content'] if 'content' in item else item.get('description', 'null'),
                        }
                        for item in data]
        _sentiment_sequence = send_conversation_to_openai(
            az_openai,
            api_settings.AZURE_OPENAI_MODEL or '',
            system,
            json.dumps(_context_data, ensure_ascii=False),
            response_json_format=False
        )
        try:
            jsonify_sentiment_seq = json.loads(_sentiment_sequence)
        except Exception as e:
            jsonify_sentiment_seq = ['중립'] * len(data)
            logging.error(e)

        analzyed_result: list[NaverNewsAnalyzedDict] = []
        for i, item in enumerate(data):
            try:
                _sentiment = jsonify_sentiment_seq[i]
            except IndexError as e:
                _sentiment = '중립'
                logging.error(e)
            
            try:
                _time_ago = time_ago(item['pubDate'])
            except Exception as e:
                _time_ago = 'Unknown Date'
                logging.error(e)

            analzyed_result.append(
                {
                    'index': i,
                    'link': item['link'],
                    'originallink': item['originallink'],
                    'title': item['title'],
                    'content': item['content'] if 'content' in item else item.get('description', 'null'),
                    'timeAgo': _time_ago,
                    'sentiment': _sentiment
                }
            )

        return analzyed_result

