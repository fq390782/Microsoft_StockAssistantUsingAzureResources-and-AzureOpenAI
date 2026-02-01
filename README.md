# StockAssistantUsingAzureResources-and-AzureOpenAI
개인 투자자의 정보 비대칭과 감정 편향을 줄여주는 클라우드 네이티브 AI 주식 비서

## 1. 프로젝트 개요 (Project Overview)
- **배경**: 개인 투자자들은 기관에 비해 실시간 정보 접근성이 낮고, 시장의 노이즈(이슈성 뉴스 등)에 휩쓸려 감정적인 매매를 하기 쉽습니다.
- **목표**: 실시간 대규모 데이터 스트리밍 기술과 AI 감정 분석을 결합하여, 투자자에게 객관적인 시각 자료와 정제된 인사이트를 제공하는 클라우드 기반 MVP를 구축합니다.
- **기간**: 2025. 11. 10 ~ 2025. 11. 20 (MS DATA SCHOOL 1차 프로젝트)

## 2. 서비스 아키텍처 (Architecture)
클라우드 네이티브 환경에서 확장성과 실시간성을 확보하기 위해 **이벤트 기반 아키텍처(Event-Driven Architecture)**를 채택하였습니다.

### Data Pipeline Flow
1. **Collection**: Azure Functions가 주기적으로 한국투자증권(KIS) 및 Naver News API에서 데이터를 수집합니다.
2. **Streaming**: 수집된 데이터는 Azure Event Hubs를 통해 실시간으로 전달됩니다.
3. **Storage**:
    - **Hot Data**: 실시간 시세 및 순위 정보는 Azure Cache for Redis에 저장되어 초고속 조회를 보장합니다.
    - **Warm Data**: 히스토리 차트 및 종목 메타 데이터는 Azure Database for PostgreSQL에 저장됩니다.
4. **Intelligence**: Azure OpenAI를 연동하여 수집된 뉴스 헤드라인의 긍정/부정 감성을 분석합니다.
5. **Serving**: FastAPI(Backend)와 Static Web Apps(Frontend)를 통해 사용자에게 최종 대시보드를 제공합니다.

## 3. 핵심 기능 (Key Features)

### 🚀 실시간 시그널 탐지 (Real-time Signal Tracking)
- 거래량 급등 및 가격 변동 상위 10개 종목을 실시간으로 추적하여 리스트업합니다.
- Redis 캐싱을 활용하여 API 응답 속도를 최적화했습니다.

### 📊 심층 분석 대시보드 (Insight Dashboard)
- Chart.js 기반의 인터랙티브 차트(가격, 거래량)를 제공합니다.
- 개인/외국인/기관 등 투자자별 매매 동향을 시각화하여 수급 분석을 돕습니다.

### 🤖 AI 뉴스 감성 분석 (News Sentiment Analysis)
- 종목 관련 최신 뉴스를 스캔하고, AI가 분석한 **'투자 심리 점수'**를 제공합니다.
- 책임 있는 AI(Ethical AI) 원칙에 따라 뉴스 본문을 직접 노출하지 않고 요약 및 링크를 제공하여 저작권을 준수합니다.

## 4. 기술 스택 (Tech Stack)

| 구분 | 기술 |
| :--- | :--- |
| **Infrastructure** | Azure Functions, Event Hubs, App Service, Static Web Apps, Bicep |
| **Backend** | Python 3.11, FastAPI, SQLAlchemy, Pydantic |
| **Database** | PostgreSQL, Azure Cache for Redis |
| **Frontend** | JavaScript (Vanilla), Bootstrap 4, Chart.js |
| **DevOps** | GitHub Actions (CI/CD), Git, Docker |

## 5. 주요 도전 과제 및 해결 (Troubleshooting)

### 1. 대규모 실시간 데이터 처리 부하
- **문제**: 수많은 종목의 실시간 시세를 매번 외부 API로 요청할 경우 속도 저하와 할당량(Quota) 문제가 발생했습니다.
- **해결**: Azure Cache for Redis를 도입하여 한 번 조회한 실시간 데이터는 일정 시간 캐싱함으로써 API 호출 수를 획기적으로 줄이고 조회 속도를 0.1초 미만으로 단축했습니다.

### 2. Cross-Origin (CORS) 이슈
- **문제**: Static Web Apps에서 App Service API를 호출할 때 브라우저 보안 정책으로 인한 통신 오류가 발생했습니다.
- **해결**: Azure App Service의 CORS 설정에 프론트엔드 도메인을 명시하고, FastAPI의 CORSMiddleware를 적절히 설정하여 보안을 유지하면서도 안정적인 통신을 구현했습니다.

### 3. 뉴스 저작권 및 리소스 최적화
- **문제**: 전체 뉴스 본문을 분석하는 것은 연산 비용이 높고 저작권 침해 우려가 있었습니다.
- **해결**: 뉴스 헤드라인(Heading)만을 사용하여 감성 분석을 수행하는 경량화된 모델 프롬프트를 설계하여 처리 속도를 높이고 법적 리스크를 해소했습니다.

## 6. 팀 구성 (Team)
- **김태진**: 파이프라인 기획, 증권 API 수집, 비용/특성 분석
- **김시영**: 데이터 전처리, 실시간 데이터 처리 모듈 개발
- **윤장원**: 프론트엔드/백엔드 총괄 개발, 시스템 아키텍처 설계
- **이대건**: 인프라 구축, PostgreSQL 스키마 설계, 데이터 분석
- **신동환**: 뉴스 API 연동, AI 감정 분석 모듈 구현, 배포 자동화

## 7. 실행 방법 (Getting Started)

### Prerequisites
- Python 3.11+
- Azure 구독 및 관련 서비스 설정

### Installation
1. 저장소를 클론합니다.
   ```bash
   git clone https://github.com/AnticSignal/stock-hyper-visioning-app.git
   ```

2. 백엔드 패키지를 설치합니다.
   ```bash
   cd apps/backend
   pip install -r requirements.txt
   ```

3. 환경 변수(.env)를 설정합니다. (KIS API Key, DB Connection, OpenAI Key 등)

4. 서비스를 실행합니다.
   ```bash
   uvicorn main:app --reload
   ```

