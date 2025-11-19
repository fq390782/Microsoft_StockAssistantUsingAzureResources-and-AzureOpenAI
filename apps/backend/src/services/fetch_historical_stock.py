"""SQL DB로 부터 누적 주식 데이터를 `Query`합니다.
"""
from typing import Optional, Sequence, Any
from antic_extensions import PsqlDBClient
from ..settings import api_settings

__all__ = (
    'HistoricalStockDataQueryService',
    'PsqlDBClient'
)

class HistoricalStockDataQueryService:
    """누적 주식 데이터와 뉴스 데이터 등 실시간성이 아닌 데이터를 조회하고 
    적절하게 반환하도록 한다. 내부적으로 PostgreSQL에 접속하여 쿼리를 수행한다.  
    """
    _QUERY_STOCK_HISTORY = """
        SELECT 
            stck_bsop_date,
            stck_clpr,
            acml_vol
        FROM anticsignal.stock_history
        WHERE fid_input_iscd = %s
        ORDER BY stck_bsop_date;
    """

    def __init__(self, sql_client: Optional[PsqlDBClient]) -> None:
        """누적 주식 데이터나 뉴스 데이터 등 비실시간성 데이터를 PostgreSQL에서 
        쿼리하기 위한 서비스 클래스를 생성한다. 이미 기존에 생성된 client를 주입할 
        경우 해당 클라이언트를 강제 적용하지만, `None`으로 미지정시 ``settings.api_settings``의 
        설정 값에 따라 자동으로 생성한다. (`SQL_HOST`, `SQL_USER`, `SQL_DATABASE`... 등)  

        >>> client = PsqlDBClient(...)
            service = HistoricalStockDataQueryService(client)
            data = service.query_historical_stock_data("505050")
            ...

        Args:
            sql_client (PsqlDBClient, optional): sql_client를 입력할 경우 해당 클라이언트를 이용합니다.
                                                `None`으로 미기입시 자동으로 내부적으로 새로운 클라이언트를 
                                                생성합니다. 이때는 ``settings.api_settings``의 설정 값을 
                                                따라 자동으로 생성됩니다.  
        """
        if api_settings.SQL_PASSWORD is None:
            raise EnvironmentError("SQL_PASSWORD is not provided.")
        self._sql_client = sql_client
        if not self._sql_client:
            self._sql_client = PsqlDBClient(
                api_settings.SQL_HOST, 
                api_settings.SQL_USER,
                api_settings.SQL_PASSWORD,
                api_settings.SQL_DATABASE
            )

    @property
    def sql_client(self) -> PsqlDBClient:
        if not self._sql_client:
            raise RuntimeError("SQL client is not initialized.")
        return self._sql_client

    def _normalize_rows(self, columns: Sequence[str], rows: Sequence[Sequence[Any]]):
        """쿼리 결과를 Key-Value 리스트로 가공"""
        normalized = []
        for row in rows:
            normalized.append({
                column: str(value) if value is not None else None
                for column, value in zip(columns, row)
            })
        return normalized

    def query_historical_stock_data(
            self,
            stock_unique_id: str
    ):
        """해당 종목의 주식 누적 데이터를 Psql로 부터 받아온다.  
        
        :param stock_unique_id: (str) 주식 종목 코드 입력.  
        
        return example
        [{'acml_vol': '48095234', 'stck_bsop_date': '2024-11-18', 'stck_clpr': '56700'},
        {'acml_vol': '31539632', 'stck_bsop_date': '2024-11-19', 'stck_clpr': '56300'},
        {'acml_vol': '20864667', 'stck_bsop_date': '2024-11-20', 'stck_clpr': '55300'},
        {'acml_vol': '19096850', 'stck_bsop_date': '2024-11-21', 'stck_clpr': '56400'},
        {'acml_vol': '15281543', 'stck_bsop_date': '2024-11-22', 'stck_clpr': '56000'}]
        """
        if not stock_unique_id:
            raise ValueError("stock_unique_id is required.")

        with self.sql_client.cursor() as cursor:
            cursor.execute(
                self._QUERY_STOCK_HISTORY,
                (stock_unique_id,)
            )
            description = cursor.description or []
            columns = [desc[0] 
                       for desc in description]
            rows = cursor.fetchall()

        return self._normalize_rows(columns, rows)
