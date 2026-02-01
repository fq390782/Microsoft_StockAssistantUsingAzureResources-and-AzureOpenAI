제공된 프로젝트 문서와 발표 자료를 바탕으로 구성한 **Antic Signal (stock-hyper-visioning-app)**의 포트폴리오용 README입니다.

---

# 📈 Antic Signal: AI 주식 비서와 함께하는 건강한 금융 투자

**"개인 투자자의 정보 비대칭과 감정 편향을 줄여주는 클라우드 네이티브 주식 인사이트 플랫폼"**

## 1. 프로젝트 개요

* 
**프로젝트 명**: Antic Signal (MS DATA SCHOOL 2기 1차 프로젝트) 


* 
**기간**: 2025. 11. 10 ~ 2025. 11. 19 (10일) 


* **목적**: 실시간 대규모 데이터 스트리밍이 구현된 MVP(Minimum Viable Product) 개발 및 클라우드 인프라 중심의 데이터 파이프라인 구축
* 
**핵심 가치**: 주식 증권의 실시간/히스토리 데이터와 뉴스 정보를 결합하여 투자자에게 객관적인 인사이트 제공 



## 2. 주요 기능

1. 
**실시간 시그널 탐지**: 거래량 급등 상위 10개 종목 실시간 차트 및 순위 제공 


2. **투자 인사이트 대시보드**:
* 개별 종목의 실시간 시세 및 기간별 가격/거래량 추이 그래프 


* 개인/외국인/기관 등 투자자 매매 동향 분석 




3. 
**AI 기반 감성 분석**: 관련 뉴스 수집 및 Azure OpenAI를 활용한 긍정/부정 감정 분석 결과 제공 



## 3. 서비스 아키텍처

클라우드 네이티브 아키텍처를 기반으로 확장성과 안정성을 확보하였습니다. 

* 
**Data Source**: 한국투자증권 KIS API (시세, 순위, 히스토리), NAVER News API 


* 
**Processing Layer**: Azure Functions (Event Trigger 기반 데이터 수집/가공), Azure Event Hubs 


* **Storage & Serving**:
* 
**Cache**: Azure Managed Redis (실시간 데이터 캐싱) 


* 
**Database**: Azure Database for PostgreSQL (히스토리 데이터 저장) 




* 
**Backend**: Azure App Service (FastAPI) 


* 
**Frontend**: Azure Static Web Apps (HTML/JS/Bootstrap/Chart.js) 



## 4. 기술 스택

| 항목 | 기술 |
| --- | --- |
| **Cloud Infra** | Azure Functions, Event Hubs, App Service, Static Web Apps, OpenAI |
| **Backend** | Python 3.11, FastAPI, PostgreSQL, Redis |
| **Frontend** | HTML5, CSS3, JavaScript, Bootstrap 4, Chart.js 

 |
| **DevOps** | Docker, Git/GitHub, Confluence, Notion |

## 5. 핵심 기술적 특징 및 문제 해결

* 
**책임 있는 AI (Ethical AI)**: 뉴스 본문 무단 스크래핑에 따른 저작권 침해를 방지하기 위해 단문 헤더만 분석하고 외부 링크를 제공하는 방식을 채택하였습니다. 


* 
**트러블슈팅 (CORS)**: 백엔드 API와 프론트엔드 간의 Cross-Origin 자원 공유 오류를 Azure App Service 설정을 통해 해결하였습니다. 


* 
**비용 및 성능 최적화**: Pay-as-you-go 정책 분석을 통해 시장 실현성을 검토하고, Redis 캐싱을 통해 API 호출 부하를 줄였습니다. 



## 6. 발전 방향

* 
**보안 강화**: Azure Key Vault를 활용한 중요 키값 관리 시스템 도입 


* 
**기능 확장**: 기업 공시 자료 기반 지표 추가 및 실시간 투자 알림 서비스 제공 


* 
**개인화**: 사용자 투자 성향 및 매매 방식 분석/조언 기능 추가 



## 7. 팀 구성 및 역할

* 
**김태진**: 파이프라인 기획, 증권 API 수집, 비용/특성 분석 


* 
**김시영**: 데이터 전처리, 실시간 데이터 처리 툴 활용 


* 
**윤장원**: 프론트/백엔드 개발, 시스템 아키텍처 설계 


* 
**이대건**: 파이프라인 구축, 데이터 분석, 백엔드 API 구현 


* 
**신동환**: 뉴스 API 수집, AI 감정 분석 파이프라인 구축, DevOps/백엔드 



---

*본 프로젝트는 MS DATA SCHOOL 2기 교육 과정의 일환으로 제작되었습니다.*

