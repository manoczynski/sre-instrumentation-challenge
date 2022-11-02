from prometheus_client import Counter, Enum, Gauge, Info, Summary


info = Info(name="StorageAPI", documentation="Information about the application")
info.info({"version":"1.0", "language":"python"})


request_total = Counter(
    name="app_request_total",
    documentation="Total number of various requests.",
    labelnames=["endpoint", "method"],
)

response_status_code_total = Counter(
    name="response_status_code_total",
    documentation="Total number of various status requests.",
    labelnames=["endpoint", "method", "code"],
)


response_status_code = Enum(
    name="app_response_status_code",
    documentation="Status code",
    labelnames=["endpoint", "method"],
    states=["200", "404", "500"],
)

