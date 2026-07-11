# gh-copy MCP Tool Inventory

Generated from the MCP connectors exposed in the current session.

## Core distinction

`gh-copy` is a selective GitHub acquisition tool. Its confirmed command shape is:

```bash
gh copy OWNER/REPO PATH DESTINATION
gh copy -r REF OWNER/REPO PATH DESTINATION
```

Examples already established for the repository:

```bash
gh extension install VibeCodingLabs/gh-copy

gh copy cli/cli README.md .
gh copy -r v2.40.0 cli/cli docs/ ./cli-docs/
```

It copies files or directories without cloning the complete repository. It does **not** call a live MCP tool. Use it to pull:

- MCP server implementations
- tool handlers
- JSON Schema or Zod/Pydantic models
- OpenAPI specifications
- examples and fixtures
- tests
- authentication adapters
- README and architecture documentation

Then register, build, test, or transform those acquired files inside your own agent ecosystem.

## URL normalization

For a GitHub URL:

```bash
url='https://github.com/OWNER/REPO'
repo="${url#https://github.com/}"
repo="${repo%.git}"

gh copy "$repo" README.md "./sources/$repo/"
```

## Safe repository-acquisition template

```bash
repo='OWNER/REPO'
dest="./sources/${repo//\//__}"

mkdir -p "$dest"

for path in   README.md   LICENSE   package.json   pyproject.toml   go.mod   Cargo.toml   src   server   tools   schemas   examples   tests
do
  gh copy "$repo" "$path" "$dest/$path" || true
done
```

Missing paths are skipped. Review licenses and provenance before reusing code.

## MCP-native feature recommended for gh-copy

A future command could query a running MCP server directly:

```bash
gh copy mcp list --server ./mcp.json --json > .gh-copy/mcp-tools.json
gh copy mcp schema --server jina --tool sort_by_relevance > schemas/jina.sort_by_relevance.schema.json
gh copy mcp snapshot --all --output .gh-copy/mcp-snapshot/
```

That would use MCP `initialize` and `tools/list`; it is a proposed extension, not a confirmed current command.

## Inventory


### Firecrawl — 26 tools

- **`firecrawl_agent`** — Launch an autonomous web-research job that searches, navigates, and extracts structured results.
- **`firecrawl_agent_status`** — Poll an autonomous research job until it completes or fails.
- **`firecrawl_check_crawl_status`** — Check the progress and results of a previously started crawl.
- **`firecrawl_crawl`** — Crawl multiple related pages from a site with path, depth, and page limits.
- **`firecrawl_extract`** — Extract selected fields from one or more pages into a supplied JSON schema.
- **`firecrawl_feedback`** — Submit quality feedback for scrape, parse, map, or search jobs.
- **`firecrawl_interact`** — Open or reuse a browser session and click, fill, navigate, or extract dynamic page content.
- **`firecrawl_interact_stop`** — Close a Firecrawl browser-interaction session.
- **`firecrawl_map`** — Discover indexed URLs on a website before choosing pages to scrape.
- **`firecrawl_monitor_check`** — Read page-level changes and diffs from one monitor check.
- **`firecrawl_monitor_checks`** — List historical executions for a monitor.
- **`firecrawl_monitor_create`** — Create a recurring page, crawl, or web-search monitor with change detection.
- **`firecrawl_monitor_delete`** — Permanently remove a monitor and stop its schedule.
- **`firecrawl_monitor_get`** — Read one monitor's configuration and status.
- **`firecrawl_monitor_list`** — List configured Firecrawl monitors.
- **`firecrawl_monitor_run`** — Trigger a monitor immediately outside its normal schedule.
- **`firecrawl_monitor_update`** — Patch a monitor's name, schedule, status, targets, goal, or notifications.
- **`firecrawl_parse`** — Parse local documents such as PDF, DOCX, XLSX, or HTML into Markdown or structured JSON.
- **`firecrawl_research_inspect_paper`** — Fetch canonical metadata for a research paper by arXiv, PMID, PMCID, or DOI identifier.
- **`firecrawl_research_read_paper`** — Retrieve the most relevant full-text passages from a specific paper for a question.
- **`firecrawl_research_related_papers`** — Expand from seed papers through citation and similarity relationships.
- **`firecrawl_research_search_github`** — Search GitHub READMEs, issues, and pull-request history.
- **`firecrawl_research_search_papers`** — Semantically search scholarly papers across supported research indexes.
- **`firecrawl_scrape`** — Extract a single known webpage as Markdown, HTML, JSON, screenshot, links, or other formats.
- **`firecrawl_search`** — Search the web, news, images, GitHub, research sources, or PDFs.
- **`firecrawl_search_feedback`** — Submit search-specific relevance feedback and identify useful or missing sources.

### Gmail — 21 tools

- **`apply_labels_to_emails`** — Add or remove Gmail labels by display name; optionally create missing labels.
- **`archive_emails`** — Remove the INBOX label while retaining messages in Gmail.
- **`batch_modify_email`** — Add or remove existing label IDs from many individual messages.
- **`batch_read_email`** — Read multiple messages and their bodies in one request.
- **`batch_read_email_threads`** — Read multiple conversation threads by message IDs or thread IDs.
- **`bulk_label_matching_emails`** — Search server-side and label every matching message, optionally archiving them.
- **`create_draft`** — Create a reviewable Gmail draft with optional HTML and attachments.
- **`create_label`** — Create or retrieve a Gmail organizational label.
- **`delete_emails`** — Move messages to Gmail Trash.
- **`forward_emails`** — Forward messages with original attachments and an optional note.
- **`get_profile`** — Read the authenticated Gmail account profile.
- **`list_drafts`** — List pending Gmail drafts with summary metadata.
- **`list_labels`** — List labels and their message/unread counts.
- **`read_attachment`** — Download a supported attachment from a known Gmail message.
- **`read_email`** — Read one message, optionally including raw MIME.
- **`read_email_thread`** — Read an entire Gmail conversation thread.
- **`search_email_ids`** — Return only message IDs matching a Gmail search query.
- **`search_emails`** — Search Gmail and return summarized matching messages.
- **`send_draft`** — Send an existing reviewed Gmail draft.
- **`send_email`** — Send a new email or threaded reply immediately.
- **`update_draft`** — Modify an existing draft without recreating it.

### Google_Calendar — 12 tools

- **`batch_read_event`** — Read multiple calendar events by event ID.
- **`create_event`** — Create a meeting, focus block, status event, recurrence, reminders, or Google Meet.
- **`delete_event`** — Delete or cancel a calendar event.
- **`fetch`** — Fetch one event by ID.
- **`get_availability`** — Return busy windows across one or more calendars.
- **`get_colors`** — Read Google Calendar's supported calendar and event color IDs.
- **`get_profile`** — Read the authenticated Calendar account profile.
- **`read_event`** — Read full details for one calendar event.
- **`respond_event`** — Accept, decline, or tentatively respond to an invitation.
- **`search`** — Broadly search event text within an optional bounded time window.
- **`search_events`** — Find candidate events using time, calendar, query, and pagination filters.
- **`update_event`** — Update event details, attendees, recurrence, scope, reminders, or Meet settings.

### Google_Contacts — 3 tools

- **`get_profile`** — Read the authenticated Google account profile.
- **`read_contact`** — Read one saved contact by Google resource ID.
- **`search_contacts`** — Find contacts or directory entries by name, email, company, or domain.

### Jina_AI — 21 tools

- **`capture_screenshot_url`** — Capture the first screen or full page as a JPEG screenshot.
- **`classify_text`** — Classify text into user-defined labels using Jina embeddings.
- **`deduplicate_images`** — Select a semantically diverse subset of images with CLIP embeddings.
- **`deduplicate_strings`** — Select representative, semantically diverse strings from a redundant list.
- **`expand_query`** — Rewrite one search query into broader and deeper search variants.
- **`extract_pdf`** — Extract figures, tables, and equations from an arXiv paper or PDF URL.
- **`guess_datetime_url`** — Estimate a page's publication or last-updated timestamp.
- **`parallel_read_url`** — Read and convert up to five webpages in parallel.
- **`parallel_search_arxiv`** — Run up to five arXiv searches concurrently.
- **`parallel_search_ssrn`** — Run up to five SSRN searches concurrently.
- **`parallel_search_web`** — Run up to five web searches concurrently.
- **`primer`** — Return session context such as current time, location, or network environment.
- **`read_url`** — Convert one or more webpages or PDFs into clean readable Markdown.
- **`search_arxiv`** — Search arXiv for technical and scientific papers.
- **`search_bibtex`** — Find papers and return ready-to-use BibTeX citations.
- **`search_images`** — Search the web for images and optionally return image URLs and metadata.
- **`search_jina_blog`** — Search official Jina AI news and technical blog content.
- **`search_ssrn`** — Search SSRN for social-science, finance, law, and business papers.
- **`search_web`** — Search the current web for pages, articles, and news.
- **`show_api_key`** — Debug the MCP Authorization bearer token. Treat as secret and never log or publish it.
- **`sort_by_relevance`** — Rerank documents by relevance to a query using Jina Reranker.

## Total

**83 MCP tools across 5 connectors.**

## How gh-copy fits each connector

### Firecrawl

Acquire scraper, search, crawl, browser-interaction, parsing, monitoring, and research modules. Prioritize API schemas, request/response models, job polling, webhook payloads, tests, and rate-limit handling.

### Gmail

Acquire OAuth setup, Gmail query examples, MIME handling, attachment handling, label operations, draft/send flows, and message/thread schemas. Never commit tokens or downloaded private mail.

### Google Calendar

Acquire event schemas, recurrence examples, RFC3339 handling, availability logic, invitation responses, and Google Meet integration. Preserve timezone and recurring-event semantics.

### Google Contacts

Acquire profile/contact schemas and search examples. Treat names, phone numbers, addresses, and emails as sensitive personal data.

### Jina AI

Acquire Reader, Search, Embeddings, Reranker, PDF, screenshot, and research examples. Keep bearer tokens outside the repository. `show_api_key` is debugging-only and should never be included in logs or generated fixtures.

## Recommended extraction pipeline

```text
GitHub repository
      |
      v
gh-copy selective acquisition
      |
      v
license + provenance scan
      |
      v
Tree-sitter / AST analysis
      |
      v
tool signature extraction
      |
      v
JSON Schema / OpenAPI 3.1 / Pydantic v2 / Zod v4
      |
      v
MCP server + CLI + tests + evals
      |
      v
signed manifest and reproducible snapshot
```
