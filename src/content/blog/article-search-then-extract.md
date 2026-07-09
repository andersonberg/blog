---
title: How I Scraped Political News for Academic Research Without Writing a Single Spider
date: '2026-07-05'
tags:
  - python
  - web-scraping
  - serpapi
  - trafilatura
  - data-collection
category:
  - python
description: How a search-then-extract pipeline (SerpAPI + trafilatura + JSONL) replaced eight custom Scrapy spiders for a one-shot academic research collection of Brazilian political news.
slug: article-search-then-extract
---

*The search-then-extract pattern: SerpAPI + trafilatura + JSONL*

---

## The Request That Started It All

A political scientist came to me with a clear but complex request: collect all news articles from Brazilian media outlets about lawsuits filed against presidential and gubernatorial candidates in the 2018 and 2022 elections.

Here's what "clear but complex" looked like in practice:

- **7 candidates**: 3 for president of Brazil(federal); 4 for government of state of Pernambuco
- **6 search term families**: ação, processo, judiciário, judicial, investigação, denúncia + justiça eleitoral
- **8 news portals**: 3 regional (NE10, JC, Diário de Pernambuco) + 5 national (G1, Folha, UOL, Estadão, R7)
- **Specific date windows** per candidate, tied to each election cycle
- **720 unique search queries** to run in total

This wasn't a "scrape a product page" problem. It was a research data collection problem — and that distinction changed everything about how I designed the solution.

---



## The Spider Trap

My first instinct was to build one Scrapy spider per portal. That's the "right" web scraping answer, isn't it? A spider for G1, one for Folha, one for NE10, one for each of the 8 portals.

I've been doing web scraping professionally for years. I know exactly what happens next:

- Each portal has a different search endpoint — or no public search at all
- Anti-bot measures vary wildly between outlets
- Some paginate differently, some use infinite scroll, some require JavaScript
- The HTML structure changes without warning, breaking your CSS selectors
- You're now maintaining 8 separate spiders for a **one-time** research collection

That last point is the killer. This was a historical, one-shot collection — not ongoing monitoring. Spending weeks building and testing custom spiders for 8 news sites made no sense.

But the bigger realization was this: the real problem wasn't crawling. It was **URL discovery with date filtering**. I didn't need to index entire news sites. I needed to find which articles mentioned specific candidates during specific time windows. That's a search problem, not a scraping problem.

---



## The Search-Then-Extract Pattern

Instead of building spiders to crawl news sites, this pipeline works in two stages:

1. **Search**: Use SerpAPI (backed by Google News) to discover the URLs of relevant articles
2. **Extract**: Fetch each URL and use trafilatura to pull clean article text

The insight: Google has already solved news indexing, date-filtered search, and ranking. SerpAPI gives you structured API access to that index. Your job is to query it intelligently, then extract text from what comes back.

This pattern isn't the right choice for every project. It works best when you have:

- **Specific search criteria** (named entities, search terms)
- **Date windows** you want to filter by
- **Targeted portals** you care about
- A **one-shot or infrequent** collection need

For broad crawling or real-time monitoring, you'd want a different approach. But for focused research with well-defined parameters, it's surprisingly powerful.

---



## Architecture: A Config-Driven Pipeline

The pipeline has four steps:

```
searches.yaml → expand-queries → discover-serpapi → fetch-articles
                     ↓                  ↓                 ↓
           queries.expanded.jsonl   urls_pending.jsonl  articles.jsonl
```

Each step produces a JSONL file that feeds the next. This design is:

- **Interruptible**: stop at any point and resume without restarting
- **Reproducible**: the same config always produces the same job list
- **Auditable**: every article carries a complete provenance chain

Let's walk through each piece.

---



## Step 1: YAML as the Source of Truth

The `searches.yaml` file defines the entire research design:

```yaml
search_terms:
  - id: processo
    keywords: [processo]

  - id: denuncia_je
    keywords: [denúncia]
    extra_keywords: [justiça eleitoral]

candidates:
  - id: candidato_1_2022
    name: Candidato 1
    office: presidente
    election_year: 2022
    query_window:
      start: "2022-08-05"
      end: "2022-10-30"
    search_name_variants:
      - Candidato 1

portals:
  - id: g1
    name: G1
    domain: g1.globo.com
    tier: 2
    enabled: true
```

This file is validated against a JSON Schema before anything runs:

```bash
uv run news-scraping-pe validate-config
# INFO: Configuração válida: config/searches.yaml
```

Catching misconfiguration early matters here — every mistake you find after this point could mean wasted API credits. The validation step costs nothing.

There's another reason to keep the research design in YAML: the political scientist reviewed this file directly. The date windows, candidate names, and search terms are visible and auditable by non-engineers. No spreadsheets, no back-and-forth emails about which candidates to include. The config **is** the research protocol, and it's version-controlled.

---



## Step 2: Job Expansion (720 Queries)

The `expand-queries` command generates every combination the pipeline needs to run:

```bash
uv run news-scraping-pe expand-queries
# INFO: Expansão concluída: 720 jobs → data/queries.expanded.jsonl
```

Each job is a line in a JSONL file:

```json
{
  "job_id": "candidato_1_2022__processo__g1",
  "candidate_id": "candidato_1_2022",
  "search_query": "\"Candidato 1\" processo",
  "portal_id": "g1",
  "site_domain": "g1.globo.com",
  "query_window_start": "2022-08-05",
  "query_window_end": "2022-10-30",
  "office": "presidente",
  "election_year": 2022
}
```

720 jobs came from: (7 name variants for presidential candidates + 8 for state candidates) × 6 search terms × 8 portals. The expansion handles all the combinations so you don't have to track them manually or risk missing one.

This file also acts as a metadata index for later steps. When `fetch-articles` processes a URL, it looks up the job that discovered that URL by `job_id` and copies the research context (candidate, election year, search term) into the article record.

---



## Step 3: SerpAPI for URL Discovery

This is where the pattern earns its keep. Instead of scraping news portals directly, each job triggers one SerpAPI call to Google News:

```python
def build_serpapi_params(job: Mapping[str, Any]) -> dict[str, str]:
    query = str(job["search_query"])
    site_domain = job.get("site_domain")
    if site_domain:
        query = f"{query} site:{site_domain}"

    window_start = str(job["query_window_start"])
    window_end = str(job["query_window_end"])
    tbs = (
        f"cdr:1,cd_min:{_format_date_for_tbs(window_start)},"
        f"cd_max:{_format_date_for_tbs(window_end)}"
    )

    return {
        "engine": "google_news",
        "q": query,
        "tbs": tbs,
        "gl": "br",
        "hl": "pt",
    }
```

The `tbs` parameter is the non-obvious part. It restricts Google News results to a custom date range. Combine that with `site:g1.globo.com` in the query string, and you get articles about a specific candidate, from a specific outlet, during a specific window.

For the Candidato 1/processo/G1 job, Google News receives:

```
"Candidato 1" processo site:g1.globo.com
```

...with date filtering applied. SerpAPI returns structured JSON with `news_results` and `organic_results`. The pipeline extracts URLs from both:

```python
def extract_urls_from_response(payload: Mapping[str, Any]) -> list[str]:
    urls = []
    for section in ("news_results", "organic_results"):
        for item in payload.get(section, []):
            link = item.get("link")
            if isinstance(link, str) and link.strip():
                urls.append(link.strip())
    return urls
```

**Cost**: 1 SerpAPI credit per job. At 720 jobs, that's 720 credits for a full run. The `--limit` flag makes testing cheap:

```bash
# Test a single job (1 credit)
uv run news-scraping-pe -v discover-serpapi \
  --job-id candidato_1_2022__processo__g1

# Test 5 jobs for one candidate
uv run news-scraping-pe discover-serpapi \
  --candidate-id candidato_1_2022 --limit 5
```

URLs are stored with full provenance:

```json
{
  "url": "https://g1.globo.com/politica/...",
  "job_id": "candidato_1_2022__processo__g1",
  "discovered_via": "serpapi"
}
```

The `discovered_via` field is there for a future expansion. If at some point, we need to add Scrapy spiders for some portals, that field will be important to know which discovery method found each article.

---



## Step 4: URL Deduplication

SerpAPI often returns the same article URL for multiple jobs. The same piece may match "Candidato 1 processo" on G1 and "Candidato 1 judicial" on G1 — two different jobs, one article. Deduplication happens before writing to `urls_pending.jsonl`.

The dedup goes beyond naive string comparison — it normalizes URLs first:

```python
_TRACKING_QUERY_PARAMS = frozenset({
    "utm_source", "utm_medium", "utm_campaign", "utm_content",
    "fbclid", "gclid", "ref", "referrer", ...
})

def normalize_url(url: str) -> str:
    parsed = urlparse(url.strip())
    filtered_query = {
        key: values for key, values in parse_qs(parsed.query).items()
        if key.lower() not in _TRACKING_QUERY_PARAMS
    }
    # normalize scheme/host to lowercase, strip trailing slash
    ...
```

The same article shared via Facebook (`?fbclid=...`) and via email (`?utm_source=newsletter`) resolves to the same canonical URL. This alone typically cuts the URL list by 15–20%.

Running the same job twice also doesn't produce duplicates — useful when you're testing incrementally and running the same `--job-id` multiple times.

---



## Step 5: trafilatura for Text Extraction

Once you have a deduplicated list of article URLs, `fetch-articles` downloads and extracts each one:

```python
def fetch_raw_text(url: str, *, client: httpx.Client | None = None) -> str | None:
    http_client = client or create_http_client()
    try:
        html = fetch_html(url, http_client)
        if html is None:
            return None
        return extract_raw_text_from_html(html, url)
    finally:
        if client is None:
            http_client.close()

def extract_raw_text_from_html(html: str, url: str) -> str | None:
    text = trafilatura.extract(
        html,
        url=url,
        include_comments=False,
        include_tables=False,
    )
    return text.strip() if text else None
```

Why trafilatura instead of BeautifulSoup or custom CSS selectors?

News sites are structurally inconsistent. Different CMS platforms, different HTML layouts, different approaches to ads, navigation, and paywalls. Writing a custom parser for each portal would require maintaining 8+ extraction patterns that break when sites redesign.

trafilatura handles all of that automatically. It identifies the main content block, strips navigation, ads, comments, and sidebar content, and returns clean article text. It uses heuristics trained on a large corpus of news articles — which is exactly what this use case needs.

It's not perfect. PDFs, paywalled articles, and JavaScript-heavy pages will fail. That's expected:

```
WARNING: Falha ao baixar https://folha.uol.com.br/paywall-article/...: HTTP 403
WARNING: Trafilatura não extraiu texto de https://estadao.com.br/...
```

Failed extractions are warnings, not errors. You expect some failures in news scraping. The goal is maximum coverage, not 100% guaranteed extraction.

Each successfully extracted article is stored with its full research context:

```json
{
  "article_id": "a1b2c3d4e5f6",
  "url": "https://g1.globo.com/politica/...",
  "portal_id": "g1",
  "title": "Candidato 1 responde a processo na Justiça Eleitoral",
  "published_at": "2022-09-15",
  "raw_text": "...",
  "candidate_id": "candidato_1_2022",
  "election_year": 2022,
  "office": "presidente",
  "search_term_id": "processo",
  "discovered_via": "serpapi",
  "extraction_method": "trafilatura",
  "collected_at": "2026-06-01T10:00:00Z"
}
```

Every article carries the research provenance: which candidate, which election, which search term triggered discovery, which method found and extracted it. This is what makes the dataset reproducible and traceable for academic use.

---



## Running the Full Pipeline

A minimal test run — end to end, one job, 5 articles:

```bash
# Install
uv sync

# Configure
cp config/searches.example.yaml config/searches.yaml
cp .env.example .env
# Add SERPAPI_API_KEY to .env

# Validate config
uv run news-scraping-pe validate-config

# Generate 720 jobs
uv run news-scraping-pe expand-queries

# Discover URLs for one job (costs 1 SerpAPI credit)
uv run news-scraping-pe -v discover-serpapi \
  --job-id candidato_1_2022__processo__g1

# Extract text from first 5 articles
uv run news-scraping-pe -v fetch-articles \
  --job-id candidato_1_2022__processo__g1 \
  --limit 5

# Inspect results
wc -l data/articles.jsonl
head -n 1 data/articles.jsonl | python -m json.tool
```

The `-v` flag enables DEBUG logging so you can see what's happening at each step. The `--limit` flag keeps test runs cheap. Go from one job to everything by dropping the flags.

---



## Lessons Learned

**Always start with** `--limit 1`. SerpAPI credits aren't expensive, but burning 720 credits on a misconfigured YAML is an unpleasant feeling. Test one job end-to-end before scaling.

**Store** `discovered_via` **from day one**. When you add a second discovery method — Scrapy spiders for selected portals, GDELT, manual URLs — you'll want to know which articles came from where. Retrofitting provenance into an existing dataset is painful. Start with it.

**JSONL is underrated for research pipelines**. Append-only, human-readable, trivially inspectable with `head`/`tail`/`wc -l`. No schema migrations, no database setup, no service to run. The Phase 2 data science work will read these files with a single line of pandas:

```python
import pandas as pd
df = pd.read_json("data/articles.jsonl", lines=True)
```

And you're in business. For research collection, that simplicity is a feature.

**Separate discovery from extraction**. Keeping `urls_pending.jsonl` between `discover-serpapi` and `fetch-articles` means you can re-extract articles without spending more API credits. If trafilatura fails on a URL today, you can retry tomorrow without calling SerpAPI again.

**Config-driven means research-driven**. The political scientist reviewed `searches.yaml` directly. The date windows, candidate names, and search terms are all visible, version-controlled, and auditable — not hidden inside spider code. This is the kind of transparency that academic research requires.

---



## What's Next

This implementation covers the SerpAPI + trafilatura path. Three things are planned:

**Scrapy spiders for regional portals** (NE10, JC, Diário de Pernambuco). For regional news with limited Google News coverage, crawling each portal's internal search endpoint will be the better discovery method. These spiders will write to the same `urls_pending.jsonl` format with `discovered_via: ne10_spider` — so the rest of the pipeline doesn't change.

**GDELT as a complementary source**. GDELT indexes global news coverage and exposes a public API. It'll act as a fallback for candidates with low article counts from SerpAPI — particularly candidates from smaller parties who may not appear heavily in Google News.

**Phase 2**: Once collection is complete, a separate data science project will analyze correlation between media coverage intensity (frequency of mentions, framing) and voter intent data from election polls. That's the actual research question this pipeline was built to answer.

---



## The Pattern Is Reusable

The search-then-extract architecture isn't specific to political research. Any time you need to collect news articles about specific entities or topics with date filtering, this pattern applies:

- Financial news about specific companies during earnings periods
- Coverage of product launches or PR incidents
- Monitoring news sentiment around a brand or event
- Collecting domain-specific articles for fine-tuning an LLM

The core insight is simple: **Google has already solved news indexing and date-filtered search**. SerpAPI gives you structured access to that index. Your job is to query it intelligently and extract clean text from the results.

If you're building a targeted news collection pipeline, you probably don't need to write a spider at all.

---

*If this was useful, you'll also enjoy [Scrapy in Production: What Nobody Tells You](/blog/scrapy-in-production/) — a breakdown of the patterns that actually keep Scrapy spiders alive in production.*