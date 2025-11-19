import json
import logging
import os
from collections import defaultdict
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from typing import Any, Dict, Iterable, List, Optional, Sequence

from antic_extensions import PsqlDBClient, RedisService
from news_analysis import NewsDataPipelineAPI
import azure.functions as func

############################################################
# #   :NOTE
# #
# #   현재 미사용 코드입니다.
# #
# #     해당 관련 기능은 backend에 FastAPI 부분을 살펴보세요.
# #
############################################################


app = func.FunctionApp(
    http_auth_level=func.AuthLevel.FUNCTION
)  # type: ignore

DEFAULT_EVENT_HUB_NAME = os.environ["AnticSignalEventHubName"]
EVENT_HUB_CONNECTION_STRING = os.environ["AnticSignalEventConnectionString"]

@app.function_name(name="StockTop10EventHubTrigger")
@app.event_hub_message_trigger(arg_name="myhub", 
                               event_hub_name=DEFAULT_EVENT_HUB_NAME,
                               connection=EVENT_HUB_CONNECTION_STRING) 
def stock_top10_eventhub_trigger(myhub: func.EventHubEvent):
    logging.info('Python EventHub trigger processed an event: %s',
                myhub.get_body().decode('utf-8'))

# @app.function_name(name="cronTimer")
# @app.timer_trigger(schedule="0 */5 * * * *", 
#               arg_name="cronTimer",
#               run_on_startup=False) 
# def test_function(cronTimer: func.TimerRequest) -> None:
#     utc_timestamp = datetime.utcnow().replace(
#         tzinfo= timezone.utc).isoformat()
#     if cronTimer.past_due:
#         logging.info('The timer is past due!')
#     logging.info('Python timer trigger function ran at %s', utc_timestamp)


# @app.event_hub_message_trigger(
#     arg_name="event", 
#     event_hub_name=DEFAULT_EVENT_HUB_NAME, 
#     connection="EventHubConnection"
# )
# def eventhub_trigger(event: eh.EventData):
#     logging.info(
#         "Python EventHub trigger processed an event %s",
#         event.body_as_str()
#     )
