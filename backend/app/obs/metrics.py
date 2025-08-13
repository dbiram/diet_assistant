from prometheus_client import Counter, Histogram

# Counters
llm_requests_total = Counter("llm_requests_total", "Total LLM requests")
llm_errors_total   = Counter("llm_errors_total", "Total LLM errors")

# Token counters (increment with amounts)
llm_tokens_in_total  = Counter("llm_tokens_in_total", "Total input tokens to LLM")
llm_tokens_out_total = Counter("llm_tokens_out_total", "Total output tokens from LLM")

# Latency histogram (seconds)
llm_latency_seconds = Histogram(
    "llm_latency_seconds",
    "LLM call latency in seconds",
    buckets=(0.1, 0.25, 0.5, 1, 2, 4, 8, 16)
)