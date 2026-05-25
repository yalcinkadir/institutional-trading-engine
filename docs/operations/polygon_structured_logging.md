# Polygon Structured Logging

Polygon data scripts now emit structured JSON logs for operational observability.

## Implementation

```text
src/observability/structured_logging.py
scripts/build_polygon_universe.py
scripts/download_polygon_daily_bars.py
tests/test_polygon_structured_logging.py
```

## Why this exists

Large Polygon runs can fail or degrade because of rate limits, HTTP errors, unexpected payloads, missing bars or partial batches. Plain text output is hard to parse in GitHub Actions and hard to use for later diagnostics.

Structured logs make these events machine-readable.

## Log shape

Each log line contains JSON fields such as:

```text
timestamp
level
component
event
message
symbol
status_code
bar_count
requested
downloaded
skipped
failed
```

## Universe builder events

```text
polygon_universe_build_started
polygon_ticker_page_request
polygon_page_fetched
polygon_rate_limit
polygon_http_error
polygon_unexpected_payload
polygon_duplicate_symbol_skipped
polygon_duplicate_symbols_summary
polygon_universe_build_completed
polygon_universe_output_written
polygon_universe_coverage_failed
```

## Daily bars downloader events

```text
polygon_universe_symbols_loaded
polygon_bars_download_started
polygon_bars_request
polygon_bars_response
polygon_rate_limit
polygon_http_error
polygon_unexpected_payload
polygon_symbol_skipped_insufficient_bars
polygon_symbol_download_failed
polygon_sleep_between_symbols
polygon_bars_written
polygon_bars_manifest_written
polygon_bars_download_completed
polygon_bars_coverage_failed
```

## Operational rule

During large data runs, logs should answer these questions without manual inspection:

1. Did Polygon rate-limit us?
2. Which symbols failed?
3. Which symbols had insufficient bars?
4. How many symbols were requested, downloaded, skipped and failed?
5. Did the run fail because coverage dropped below the evidence minimum?

These logs are intentionally JSON-line friendly for GitHub Actions, local shell runs and future observability ingestion.
