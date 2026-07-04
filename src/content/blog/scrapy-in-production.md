---
title: 'Scrapy in Production: What Nobody Tells You'
date: '2026-07-04'
tags:
  - scrapy
  - python
  - web-scraping
  - spidermon
  - docker
category:
  - python
description: Project structure, per-environment settings, secrets, politeness, error handling beyond try/except, Spidermon monitoring, Docker deployment, and scaling with scrapy-redis.
slug: scrapy-in-production
---

You followed the Scrapy tutorial, your spider runs locally, but the moment you try to run it in production for days on end, things break. You need a well structured project with failure tolerance, logging, and monitoring.

Today, we’ll cover:

- How to organize a project structure that survives growth
- How to create settings for each environment and keep secrets out of your code
- How to be a polite, ban-resistant crawler with AutoThrottle
- Handling errors beyond try/except
- How to add monitoring tools with real metrics
- How to deploy, and how to scale out when one machine isn’t enough

## Project Structure That Actually Scales

Scrapy provides a handy command to set up a project with a basic structure for you to start scraping. The `scrapy startproject` command will create a minimal directory tree for the project.

That default structure is fine, and you should not fight it early. If you have one or two spiders, you really only touch `spiders/` and `settings.py`. Items, pipelines, and middlewares are things you add *when you need them*, not on day one.

So when does the default stop being enough? When you hit one (or several) of these:

- You have more than a handful of spiders that share logic.
- You run in more than one environment (your laptop, staging, production).
- You have secrets (database URLs, proxy credentials, API keys) you cannot commit to git.
- Several people work in the same codebase and step on each other’s `settings.py`.

When that happens, we reorganize. Instead of having all development and production settings in one big `settings.py`, we create a folder named `settings/` with a different file per environment. Instead of one giant `middlewares.py` and `pipelines.py`, we split them into focused modules. And we add a `utils/` package for the shared plumbing (database connections, monitoring helpers) so our pipelines and middlewares stay thin.

```
myproject/
├── myproject/
│   ├── settings/
│   │   ├── base.py        # shared settings
│   │   ├── dev.py         # local overrides
│   │   ├── staging.py     # pre-production
│   │   └── prod.py        # production settings
│   ├── spiders/
│   │   ├── base.py        # BaseSpider with common logic
│   │   └── products.py
│   ├── middlewares/
│   │   ├── retry.py
│   │   └── proxy.py
│   ├── pipelines/
│   │   ├── validation.py
│   │   └── storage.py
│   ├── utils/
│   │   ├── database.py     # connection setup, shared by pipelines
│   │   └── monitoring.py   # custom monitors / helpers
│   ├── items.py
│   └── monitors.py        # Spidermon monitor suites (more on this later)
├── tests/
│   ├── unit/
│   └── integration/
├── Dockerfile
├── requirements.txt
└── scrapy.cfg
```

Note in this example we have a different settings file for each environment. Adding to that, we also have a `base.py` inside `spiders/`, which is great to reuse code and keep everything that is shared between spiders in just one place. The `utils/` package is the part most structures forget: it is where your database connection logic and monitoring helpers live, so a pipeline becomes a thin “call this helper” instead of a tangle of connection code.

## Settings: One Source of Truth Per Environment

Scrapy decides which settings module to load from the `SCRAPY_SETTINGS_MODULE` environment variable (the value is a Python import path, e.g. `myproject.settings.prod`). `scrapy.cfg` sets a default, but in production you typically set this env var explicitly so the same image can run as dev, staging, or prod just by flipping a variable.

Settings files are not supposed to keep your secrets. A `prod.py` committed to git with a hardcoded database password is still a leaked secret. Secrets belong in environment variables, not in any file you commit.

The pattern almost everyone converges on is dead simple: read secrets from environment variables with the standard library’s `os.getenv`, and during local development load them from a `.env` file (which you `.gitignore`). The tiny [python-dotenv](https://pypi.org/project/python-dotenv/) library handles the loading. `load_dotenv()` reads `.env` and injects the values into `os.environ`. It does *not* override variables already present in the environment, so in production the real env vars your platform injects always win over any stray file.

Commit a `.env.example` with dummy values as living documentation for your team, and keep the real `.env` out of git.

Let’s check the settings files:

### base.py

```python
import os

from dotenv import load_dotenv

# Loads a local .env during development. In production your platform
# (Docker, fly.io, a CI runner, ...) injects these as real env vars,
# and load_dotenv() won't clobber them.
load_dotenv()

BOT_NAME = "myproject"

SPIDER_MODULES = ["myproject.spiders"]
NEWSPIDER_MODULE = "myproject.spiders"

# A real, identifiable User-Agent. "myproject (+https://example.com/bot)"
USER_AGENT = os.getenv("USER_AGENT", "myproject (+https://example.com)")

# Be a good web citizen by default.
ROBOTSTXT_OBEY = True

# Politeness / throttling (tuned further per environment).
DOWNLOAD_DELAY = 1
CONCURRENT_REQUESTS = 8
CONCURRENT_REQUESTS_PER_DOMAIN = 8

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 2.0

# Retry transient failures.
RETRY_ENABLED = True
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 408, 429]

# Secrets come from the environment, never hardcoded.
DATABASE_URL = os.getenv("DATABASE_URL", "")
```

This is the base settings file that is shared between all environments. Notice the secrets (`DATABASE_URL`) and anything environment-specific are pulled from `os.getenv(...)`, not written inline. One thing to keep in mind: environment variables are always strings, so cast as you read them: `int(os.getenv("CONCURRENT_REQUESTS", "8"))` for a number, or `os.getenv("DEBUG", "false").lower() == "true"` for a boolean. If that manual casting starts to sprawl, that’s the signal to graduate to a typed config layer like [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/), which validates and coerces everything at startup.

### dev.py

```python
from .base import *

LOG_LEVEL = "DEBUG"
LOG_FILE = "scrapy.log"
LOG_FORMAT = "%(asctime)s [%(name)s]%(levelname)s:%(message)s"
LOG_DATEFORMAT = "%Y-%m-%d %H:%M:%S"
LOG_ENCODING = "utf-8"

# Cache responses locally so you don't hammer the target while developing.
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 3600

# Go gentle locally.
CONCURRENT_REQUESTS = 4
```

This is the development settings file, used when running the spider locally: verbose logs, an HTTP cache so you can iterate on selectors without re-fetching, and low concurrency.

### prod.py

```python
from .base import *

LOG_LEVEL = "INFO"
LOG_ENCODING = "utf-8"
# In production prefer structured logs (JSON) so they're queryable in your log aggregator.
# Plug in a JSON formatter via LOG_FORMATTER or a logging config here.

# The HTTP cache is a development tool; never serve stale data in prod.
HTTPCACHE_ENABLED = False

# Push harder, but let AutoThrottle keep you polite.
CONCURRENT_REQUESTS = 16
CONCURRENT_REQUESTS_PER_DOMAIN = 16
```

This is the production settings file. The point of keeping `dev.py` and `prod.py` genuinely different (rather than near-identical copies) is that each environment now *means* something: dev is verbose and cached and slow; prod is quiet, structured, and faster.

### Read settings the typed way

One small thing that bites people: settings passed from the command line (`scrapy crawl spider -s RETRY_TIMES=5`) arrive as **strings**. When you read settings in your own components, use the typed getters instead of dict access:

```python
def from_crawler(cls, crawler):
    settings = crawler.settings
    max_retries = settings.getint("RETRY_TIMES")     # not settings["RETRY_TIMES"]
    enabled = settings.getbool("AUTOTHROTTLE_ENABLED")
    codes = settings.getlist("RETRY_HTTP_CODES")
    ...
```

### Secrets in the cloud

A `.env` file is a local-development convenience, not a production mechanism, you should never bake one into your image. In production you inject environment variables through the platform itself, and your `os.getenv` calls pick them up unchanged. No code difference between environments; only where the values come from changes.

On a PaaS like fly.io that means the `fly secrets` command:

```bash
fly secrets set DATABASE_URL=postgres://... PROXY_PASSWORD=...
```

Fly encrypts these at rest, injects them as environment variables into every machine at runtime, and triggers a rolling restart when they change. Non-sensitive config (log level, feature flags) can live in the `[env]` block of `fly.toml`; anything secret goes through `fly secrets set`. The same idea maps to every platform: `docker run -e` and Compose’s `environment:`, Kubernetes Secrets mounted as env vars, GitHub Actions secrets in CI, or a dedicated secret manager (AWS Secrets Manager, GCP Secret Manager, HashiCorp Vault) for larger setups.

One gotcha that bites people: on fly.io (and most platforms) injected secrets are only available at **runtime, not during the Docker build**. If a build step tries to read one, you get a “not found” error. Either move that work to runtime (an entrypoint script, not a `RUN` line), or use the platform’s dedicated build-secrets mechanism.

## Being Polite (and Not Getting Banned)

This is the section nobody writes, and it’s the one that actually keeps your spider alive for days. A static `DOWNLOAD_DELAY` is a blunt instrument: too high and you’re slow, too low and you get banned. **AutoThrottle** watches how fast the target server responds and adapts your request rate on the fly. That adaptive balance between speed and politeness is not optional at volume; it’s survival.

In my experience, AutoThrottle may let the spider very slow, which in some situations is not the desired behavior. That becomes a tradeoff between AutoThrottle settings and CONCURRENT_REQUESTS. You have to try and decide by yourself what’s the best combination of those configurations.

The canonical production block (already in our `base.py`):

```python
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 2.0

RETRY_ENABLED = True
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 408, 429]

DOWNLOAD_DELAY = 1
ROBOTSTXT_OBEY = True
```

### A war story: 92% → 61% with zero code changes

Here’s the part that surprises people. A developer ran a Reddit scraper that held a 92% success rate. A month later it had collapsed to 61% (with no code change on their side). It was pure IP-reputation decay against `www.reddit.com`. More retries didn’t help; you can’t out-rotate a poisoned proxy pool.

The fix was architectural, not tactical: switch the target host from `www.reddit.com` to `old.reddit.com` (same JSON API, same response shape, but dramatically more permissive bot-detection because most human traffic moved off it years ago). Combined with:

- A browser-like header set (`Sec-Ch-Ua`, `Sec-Ch-Ua-Mobile`, `Sec-Ch-Ua-Platform`, `Sec-Fetch-Dest`, `Sec-Fetch-Mode`, `Sec-Fetch-Site`, `Accept-Encoding`, `Referer`), anti-bot systems fingerprint unusual combinations, and anything missing is a tell.
- 300–900ms of random jitter before each request, so you don’t hit at a perfectly steady, machine-like rate.
- A genuinely diverse User-Agent pool (Firefox + Safari on top of Chrome variants) so rotation doesn’t degenerate into the same string 90% of the time.

Success rate went back to 92%+. The lesson worth tattooing on your monitor: **the architectural fix beats the tactical fix every time.** When you’re getting blocked, ask whether there’s a friendlier endpoint or approach before you reach for more retries and more proxies.

## Handling Errors Beyond try/except

In a spider, the most important failures happen at the network layer, and a `try/except` around your parsing code never sees them. Scrapy gives you four better tools.

### 1. Let RetryMiddleware do the boring retries

`RetryMiddleware` is enabled by default and automatically retries failures caused by temporary problems: connection timeouts, DNS issues, and the HTTP codes in `RETRY_HTTP_CODES`. Failed pages are collected and rescheduled at the *end* of the crawl, after the normal pages are done. For most transient errors, you configure it and forget it:

```python
RETRY_ENABLED = True
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 408, 429]
```

### 2. Catch what try/except can’t: errback

Attach an `errback` to a request to handle exceptions raised anywhere in the request lifecycle (including 404s and connection failures). It receives a Twisted `Failure`, and you branch on the failure type with `failure.check(...)`:

```python
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TimeoutError

def start_requests(self):
    for url in self.start_urls:
        yield scrapy.Request(url, callback=self.parse, errback=self.errback)

def errback(self, failure):
    # Always log the failure so it's visible in production.
    self.logger.error(repr(failure))

    if failure.check(HttpError):
        response = failure.value.response
        self.logger.error("HttpError%s on%s", response.status, response.url)
    elif failure.check(DNSLookupError):
        self.logger.error("DNSLookupError on%s", failure.request.url)
    elif failure.check(TimeoutError):
        self.logger.error("TimeoutError on%s", failure.request.url)
```

### 3. Retry from inside a callback with get_retry_request

Sometimes you only discover a request was bad *after* you parsed it (an empty results page, a soft block that returns 200). You can manually reschedule it:

```python
from scrapy.downloadermiddlewares.retry import get_retry_request

def parse(self, response):
    if not response.css("div.product"):
        new_request = get_retry_request(
            response.request, spider=self, reason="empty_product_list"
        )
        if new_request:           # None once retries are exhausted
            yield new_request
        return
    ...
```

### 4. Stop Scrapy from silently dropping status codes

By default Scrapy ignores non-2xx responses. When you actually want to *process* a 404 or 403 (to mark a product as gone, or to detect a block), tell the spider to hand them to you:

```python
class ProductSpider(scrapy.Spider):
    handle_httpstatus_list = [404, 403]
```

For error types specific to your stack (say, a proxy or fake-user-agent library raising its own exception), you can subclass `RetryMiddleware` and override `process_exception` to retry on those too.

## Monitoring With Real Metrics

Seeing `FAILED` scroll past in the logs is useful while developing. In production, where you might run hundreds of jobs, it’s useless, unless someone is watching. The community standard here is **Spidermon**, an open-source monitoring extension built by the same people who maintain Scrapy.

Spidermon is built around four concepts:

- **Monitors** — unit-test-style checks that run against your job’s stats.
- **MonitorSuites** — groups of monitors that run at a defined moment: when the spider opens, when it closes, or periodically during long crawls.
- **Actions** — what happens on pass/fail: Slack, Discord, email (via Amazon SES), Sentry, or a custom action.
- **Validation** — checking each scraped item against a schema (jsonschema/schematics) so malformed data is caught before it flows downstream.

Enabling it is just two lines:

```python
# settings.py
SPIDERMON_ENABLED = True
EXTENSIONS = {
    "spidermon.contrib.scrapy.extensions.Spidermon": 500,
}
```

Then you define a suite in `monitors.py` and register it (for example via `SPIDERMON_SPIDER_CLOSE_MONITORS` for post-crawl checks, or `SPIDERMON_PERIODIC_MONITORS` for interval checks).

Useful built-in monitors to start with:

- `ItemCountMonitor` — fail if fewer than N items were scraped.
- `FieldCoverageMonitor` — fail if, say, fewer than 95% of items have a `name`, or any item is missing a `price`.
- `ItemValidationMonitor` — fail if too many items failed schema validation.
- `ErrorCountMonitor` / `WarningCountMonitor` — fail above an error/warning threshold.
- `RetryCountMonitor` — fail if requests are hitting max retries and getting dropped.
- `FinishReasonMonitor` — fail if the job didn’t finish for the reason you expected.

The metrics worth alerting on, generally:

- Items extracted.
- Successful vs. failed responses.
- Requests dropped/discarded.
- Crawl duration.
- Log error count.
- Ban count.
- Field coverage and item validation errors.

One especially powerful production move: **compare a run against previous runs** to catch regressions. “Did this spider return significantly fewer items than last time?” usually means the site changed its markup or started blocking you — and you want to know that before your data consumers do.

## Deploying to Production

There are some options to deploy spiders to a production environment:

- **Scrapyd** — open-source service that gives you an HTTP API to deploy, schedule, and monitor spiders. You deploy with `scrapyd-deploy` (from the `scrapyd-client` package). It’s free but self-hosted, and in practice you’ll want a dashboard (ScrapeOps, Scrapyd-web) on top of it.
- **Zyte Scrapy Cloud** — a hosted, managed service from the company behind Scrapy. Nice UI for scheduling, logs, items, and stats; you deploy with `shub`. Zero servers to babysit, but it’s paid (the cost is per “Scrapy unit”, one concurrent job per unit). It reads the same `scrapy.cfg` as Scrapyd, so you can switch between them.
- **Docker + docker-compose / Kubernetes** — the default when you want full control and horizontal scaling. This is what we’ll focus on.

### Docker: one job, one service

The single most-repeated production design principle is to keep the **spider** and the **datastore** in separate containers. The spider is a short-lived job; the database is a long-running service.

```mermaid
flowchart LR
    Trigger["Cron / CI trigger"] --> Scrapy
    subgraph compose [docker-compose network]
        Scrapy["Scrapy container (one-shot job)"] --> DB[("PostgreSQL (persistent service)")]
        Scrapy -.->|"stats / alerts"| Mon["Spidermon -> Slack / Sentry"]
    end
    DB --> Grafana["Grafana (optional dashboards)"]
```



The key ideas:

- **The spider is a one-shot job**: it starts, crawls, stores its data, and exits.
- **The database is a service**: it stays running, with a persistent volume so data survives restarts.
- They share a Docker network, so the spider reaches the database by its **service name** as hostname (e.g. `postgres`).
- `depends_on` declares ordering so the database is up before the spider runs.

A minimal `docker-compose.yml` for that shape. Notice the secrets are *not* written inline: non-sensitive config (the settings module) stays in the file, while anything secret is referenced from the environment with `${VAR}` and supplied by an `env_file` locally (or by the platform’s injected vars in production). Compose reads a `.env` sitting next to the compose file automatically, so `${POSTGRES_PASSWORD}` and friends resolve without ever being committed.

```yaml
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: scraped_data
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}   # from .env / platform, never inline
    volumes:
      - pgdata:/var/lib/postgresql/data

  scrapy:
    build: .
    depends_on:
      - postgres
    environment:
      # Non-sensitive config is fine to keep here.
      SCRAPY_SETTINGS_MODULE: myproject.settings.prod
    # Secrets come from a gitignored .env (or injected by your platform),
    # not hardcoded into the compose file.
    env_file:
      - .env
    command: ["scrapy", "crawl", "products"]

volumes:
  pgdata:
```

Your `.env` (gitignored) and a committed `.env.example` would then hold the values, for example:

```bash
POSTGRES_PASSWORD=super-secret
DATABASE_URL=postgresql://postgres:super-secret@postgres:5432/scraped_data
```

In production you skip the `.env` file entirely and let the platform inject those same variables (`fly secrets set ...`, Kubernetes Secrets, and so on) — the compose file and your `os.getenv` calls don’t change.

One gotcha that will cost you an afternoon: setting `SCRAPY_SETTINGS_MODULE` in the container (as we do above) changes how Scrapy bootstraps. When you run `scrapy` from your project directory locally, Scrapy adds the project root to `sys.path` for you (but it only does that when `SCRAPY_SETTINGS_MODULE` is *not* already set in the environment). Pre-set it, and Scrapy skips that step, so your project package never lands on the path and you get a `ModuleNotFoundError: No module named 'myproject'` even though the code is sitting right there in the image. The fix is to make the package importable explicitly, e.g. `ENV PYTHONPATH=/app` in your Dockerfile (alongside `WORKDIR /app`). It works locally precisely because you *didn’t* set the variable there.

Want scheduled scraping? Trigger the job via cron or CI. Want a different database? Swap the image. Want dashboards? Add a Grafana container. Each component is isolated and replaceable, which is exactly why this scales.

If you go the **Scrapyd** route instead, the documented pattern is a multi-stage Dockerfile: one stage builds an egg of your project with `scrapyd-deploy --build-egg`, and a slim runtime stage runs `scrapyd` and serves it on port 6800.

## Scaling Out: When One Machine Isn’t Enough

Tune one machine first (`CONCURRENT_REQUESTS`, AutoThrottle, HTTP caching during development) before throwing hardware at the problem. But when a single machine can’t keep up, the standard move is to replace Scrapy’s in-memory scheduler with a shared queue.

[scrapy-redis](https://scrapeops.io/python-scrapy-playbook/scrapy-redis/) lets multiple spider instances across machines pull from the same Redis-backed request queue, with deduplication so the same URL isn’t crawled twice. Two big wins:

- **Crash recovery / resumability.** Because the queue lives in Redis, a crashed or paused spider can be resumed by a new worker from exactly where it left off, instead of restarting the whole job.
- **Horizontal scale.** Backlogged? Add more workers against the same queue.

For very large setups, Scrapy Cluster offers a memorable rule of thumb: run spiders **thin, not thick** — only 5–10 spider processes per machine, and scale out by adding machines rather than stacking processes. Thin spiders give you better per-IP rate limits and fewer bans, and you’d be surprised how fast a small fleet can crawl.

## A Few More Things Nobody Tells You

- **Items vs. plain dicts.** Dicts are genuinely fine for small spiders. The moment you want validation, field-coverage monitoring, or structure shared across spiders, switch to `Item`/`ItemLoader` (or dataclasses). Don’t adopt them on day one just because a tutorial did.
- **Pipelines are separation of concerns.** One concern per stage: validate → clean → transform → dedup → store, each running in priority order. You can bolt on or rip out a stage without ever touching spider code — which matters a lot when several engineers share the codebase.
- **Open connections once, not per item.** Use `open_spider`/`close_spider` in your pipeline to set up and tear down the database connection a single time. Opening a connection inside `process_item` (once per item) is a classic production-killer.
- **Run under process supervision.** In production, run spiders/Scrapyd under systemd, supervisord, or PM2 so a crash restarts automatically instead of silently going dark.
- **Make re-runs idempotent.** Production crawls re-run on a schedule. Dedup in a pipeline (or via scrapy-redis fingerprints), and upsert instead of blind-insert, so a second run doesn’t duplicate rows.

## Sources and Further Reading

- Scrapy docs: [Settings](https://docs.scrapy.org/en/latest/topics/settings.html), [Downloader Middleware / RetryMiddleware](https://docs.scrapy.org/en/latest/topics/downloader-middleware.html), [Deploying Spiders](https://docs.scrapy.org/en/latest/topics/deploy.html)
- Zyte: [Building a production-style scraper with Scrapy, Docker, and PostgreSQL](https://www.zyte.com/learn/building-a-production-style-web-scraper-with-scrapy-docker-and-postgre-sql/), [Spidermon: battle-tested spider monitoring](https://www.zyte.com/blog/spidermon-scrapy-spider-monitoring/)
- [Spidermon documentation](https://spidermon.readthedocs.io/en/latest/monitors.html)
- ScrapeOps: [The Scrapy Redis Guide](https://scrapeops.io/python-scrapy-playbook/scrapy-redis/), [Scrapy Cloud alternatives](https://scrapeops.io/python-scrapy-playbook/scrapy-cloud-alternatives/)
- [Scrapy Cluster: production setup](https://scrapy-cluster.readthedocs.io/en/latest/topics/advanced/productionsetup.html)
- [Single Scrapy project vs. multiple projects (StackOverflow)](https://stackoverflow.com/questions/57861326/single-scrapy-project-vs-multiple-projects)
- [Why my Reddit scraper went from 92% to 61% (DEV)](https://dev.to/perufitlife/why-my-reddit-scraper-went-from-92-to-61-success-rate-in-30-days-and-the-one-line-fix-3013)
- Environment variables and secrets: [python-dotenv](https://pypi.org/project/python-dotenv/), [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/), [Fly.io: Secrets and Fly Apps](https://fly.io/docs/apps/secrets/), [Fly.io: Build secrets](https://fly.io/docs/reference/build-secrets/)

