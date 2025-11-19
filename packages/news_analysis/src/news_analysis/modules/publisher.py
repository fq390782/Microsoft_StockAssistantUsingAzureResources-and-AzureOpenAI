"""뉴스 기사 URL로부터 언론사 이름을 추출하는 유틸리티."""

from dataclasses import dataclass
from typing import Dict, Optional

__all__ = (
    "PublisherResolverResult",
    "resolve_publisher",
)

_URL_PUBLISHER_MAP: Dict[str, str] = {
    "osen.mt.co.kr": "OSEN",
    "www.wowtv.co.kr": "한국경제TV",
    "www.etnews.com": "전자신문",
    "www.sportschosun.com": "스포츠조선",
    "imnews.imbc.com": "MBC",
    "koreajoongangdaily.joins.com": "중앙데일리",
    "isplus.joins.com": "일간스포츠",
    "www.joongang.co.kr": "중앙일보",
    "www.inews24.com": "아이뉴스24",
    "www.ichannela.com": "채널A",
    "www.hani.co.kr": "한겨레",
    "zdnet.co.kr": "지디넷코리아",
    "biz.chosun.com": "조선비즈",
    "world.kbs.co.kr": "KBS World",
    "www.newstapa.org": "뉴스타파",
    "www.imaeil.com": "매일신문",
    "www.dailian.co.kr": "데일리안",
    "www.edaily.co.kr": "이데일리",
    "www.ytn.co.kr": "YTN",
    "www.khan.co.kr": "경향신문",
    "mbn.mk.co.kr": "MBN",
    "www.sportsseoul.com": "스포츠서울",
    "www.nocutnews.co.kr": "노컷뉴스",
    "asiatoday.co.kr": "아시아투데이",
    "www.mydaily.co.kr": "마이데일리",
    "www.mediatoday.co.kr": "미디어오늘",
    "www.mk.co.kr": "매일경제",
    "www.hankyung.com": "한국경제",
    "www.fnnews.com": "파이낸셜뉴스",
    "www.munhwa.com": "문화일보",
    "www.kmib.co.kr": "국민일보",
    "www.bloter.net": "블로터",
    "www.seoul.co.kr": "서울신문",
    "www.newsis.com": "뉴시스",
    "www.sedaily.com": "서울경제",
    "www.newdaily.co.kr": "뉴데일리",
    "www.dt.co.kr": "디지털타임스",
    "www.hankookilbo.com": "한국일보",
    "www.ohmynews.com": "오마이뉴스",
    "www.pressian.com": "프레시안",
    "www.sisain.co.kr": "시사IN",
    "www.asiae.co.kr": "아시아경제",
    "www.koreaherald.com": "코리아헤럴드",
    "www.segye.com": "세계일보",
    "www.chosun.com": "조선일보",
    "www.yonhapnewstv.co.kr": "연합뉴스TV",
    "news.sbs.co.kr": "SBS",
    "news.jtbc.joins.com": "JTBC",
    "www.heraldbiz.com": "헤럴드경제",
    "www.donga.com": "동아일보",
    "news.kbs.co.kr": "KBS",
    "www.mt.co.kr": "머니투데이",
    "www.yna.co.kr": "연합뉴스",
    "news.skbroadband.com": "B tv news",
    "news.mtn.co.kr": "MTN 뉴스",
    "view.asiae.co.kr": "아시아경제",
    "www.etoday.co.kr": "이투데이",
    "biz.newdaily.co.kr": "뉴데일리 경제",
    "www.metroseoul.co.kr": "메트로서울",
    "www.news1.kr": "뉴스1",
    "biz.heraldcorp.com": "헤럴드경제",
    "www.busan.com": "부산일보",
    "www.joongdo.co.kr": "중도일보",
    "www.joseilbo.com": "조세일보",
    "www.moneys.co.kr": "머니S",
    "www.newspim.com": "뉴스핌",
    "daily.hankooki.com": "데일리한국",
    "www.shinailbo.co.kr": "신아일보",
    "news.tf.co.kr": "더팩트",
    "www.domin.co.kr": "전북도민일보",
    "www.sentv.co.kr": "서울경제TV(SEN)",
    "www.kihoilbo.co.kr": "기호일보",
    "www.kizmom.com": "키즈맘",
    "weekly.hankooki.com": "주간한국",
    "www.kgnews.co.kr": "경기신문",
    "www.topstarnews.net": "톱스타뉴스",
    "www.g-enews.com": "글로벌이코노믹",
    "www.kukinews.com": "쿠키뉴스",
    "www.breaknews.com": "브레이크뉴스",
    "www.digitaltoday.co.kr": "디지털투데이",
}


@dataclass(slots=True)
class PublisherResolverResult:
    """언론사 추출 결과."""

    url: str
    publisher: Optional[str] = None


def _extract_domain(url: str) -> str:
    """URL에서 스킴 이후 첫 `/` 사이의 도메인을 추출한다."""
    if not isinstance(url, str) or "://" not in url:
        raise ValueError("도메인을 추출할 수 있는 유효한 URL이 아닙니다.")

    start = url.index("://") + 3
    end = url.find("/", start)
    if end == -1:
        return url[start:]
    return url[start:end]


def resolve_publisher(url: str) -> PublisherResolverResult:
    """뉴스 기사 URL을 입력 받아 언론사 이름을 반환한다.
    PublisherResolverResult.publisher
    """
    if not isinstance(url, str) or not url:
        raise ValueError("뉴스 URL은 빈 문자열일 수 없습니다.")

    parsed_url = _extract_domain(url)
    publisher = _URL_PUBLISHER_MAP.get(parsed_url, parsed_url)
    return PublisherResolverResult(url=url, publisher=publisher)
