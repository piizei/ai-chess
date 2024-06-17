import os
import logging

from dotenv import load_dotenv
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.trace.export import BatchSpanProcessor

load_dotenv()
from opentelemetry import trace
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import (
    LoggerProvider,
    LoggingHandler,
)
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.trace import TracerProvider

from azure.monitor.opentelemetry.exporter import AzureMonitorLogExporter, AzureMonitorTraceExporter
RequestsInstrumentor().instrument()
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)
logger_provider = LoggerProvider()
set_logger_provider(logger_provider)

exporter = AzureMonitorLogExporter(
    connection_string=os.environ["APPLICATIONINSIGHTS_CONNECTION_STRING"]
)
#trace_exporter = AzureMonitorTraceExporter(
#    connection_string=os.environ["APPLICATIONINSIGHTS_CONNECTION_STRING"]
#)
#processor = BatchSpanProcessor(trace_exporter)
#trace.get_tracer_provider().add_span_processor(processor)

logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))

# Attach LoggingHandler to namespaced logger
handler = LoggingHandler()
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
