import logging
import os

from dotenv import load_dotenv
from opentelemetry.instrumentation.requests import RequestsInstrumentor

load_dotenv()
from opentelemetry import trace
from opentelemetry._logs import set_logger_provider, get_logger_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)
from azure.monitor.opentelemetry.exporter import AzureMonitorLogExporter, AzureMonitorTraceExporter
RequestsInstrumentor().instrument()
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)
connection_string = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
if connection_string:
    trace_exporter = AzureMonitorTraceExporter(
        connection_string=os.environ["APPLICATIONINSIGHTS_CONNECTION_STRING"]
    )
    set_logger_provider(LoggerProvider())
    log_exporter = AzureMonitorLogExporter(
        connection_string=os.environ["APPLICATIONINSIGHTS_CONNECTION_STRING"]
    )
    get_logger_provider().add_log_record_processor(BatchLogRecordProcessor(log_exporter))
    handler = LoggingHandler()
    logger = logging.getLogger(__name__)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

else:
    trace_exporter = ConsoleSpanExporter()

processor = BatchSpanProcessor(trace_exporter)
trace.get_tracer_provider().add_span_processor(processor)



# Creates a tracer from the global tracer provider
tracer = trace.get_tracer("ai-chess")
