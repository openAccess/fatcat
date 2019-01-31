
## In Progress

## Prod Metadata Checks

- edit and editgroup metadata
- longtail_oa flag getting set on GROBID imports
- crossref citation not saving 'article-title' or 'unstructured', and 'author'
  should be 'authors' (list)
- crossref not saving 'language' (looks like iso code already)
- grobid reference should be under extra (not nested): issue, volume, authors
- uniqueness of:
    sha1 - via SQL dump
    doi - via SQL dump
    issnl - via JSON dump
    orcid - via JSON dump

## Next Up

- bootstrap_bots script should set -ex and output admin and webface tokens
- regression test imports for missing orcid display and journal metadata name
- serveral tweaks/fixes to webface (eg, container metadata schema changed)
- container count "enrich"
- changelog elastic stuff (is there even a fatcat-export for this?)
- QA sentry has very little host info; also not URL of request
- start prod crossref harvesting (from ~start of 2019)
- 158 "NULL" publishers in journal metadata
- should elastic release_year be of date type, instead of int?
- QA/prod needs updated credentials
- ansible: ISSN-L download/symlink
- searching 'N/A' is a bug
- formalize release_status:
    => https://wiki.surfnet.nl/display/DRIVERguidelines/DRIVER-VERSION+Mappings

## Production public launch blockers

- handle 'wip' status entities in web UI
- guide updates for auth
- webface 4xx and 5xx pages
- privacy policy, and link from: create account, create edit
- refactors and correctness in rust/TODO
- update /about page

## Production Tech Sanity

- postgresql replication
- pg_dump/load test
- haproxy somewhere/how
- logging iteration: larger journald buffers? point somewhere?

## Ideas

- write up notes on biblio metadata in general
    => "extensibility" and extra keys
    => proliferation of arrays vs. concrete values
    => various ways to record history/progeny
    => "subtitle", "short-title", "full-title" complexity
    => human names
    => translated metadata: titles/names/abstracts
    => "typing" for metadata (eg, math in titles)
- 'hide' flag for exporter (eg, to skip abstracts and refs in some release dumps)
- https://tech.labs.oliverwyman.com/blog/2019/01/14/serialising-rust-tests/
- use https://github.com/codelucas/newspaper to extract fulltext+metadata from
  HTML crawls
- changelog elastic index (for stats)
- import from arabesque output (eg, specific crawls)
- more logins: orcid, wikimedia
- `fatcat-auth` tool should support more caveats, both when generating new or
  mutating existing tokens
- fast path to skip recursive redirect checks for bulk inserts
- when getting "wip" entities, require a parameter ("allow_wip"), else get a
  404
- consider dropping CORE identifier
- maybe better 'success' return message? eg, "success: true" flag
- idea: allow users to generate their own editgroup UUIDs, to reduce a round
  trips and "hanging" editgroups (created but never edited)
- API: allow deletion of empty, un-accepted editgroups
- refactor API schema for some entity-generic methos (eg, history, edit
  operations) to take entity type as a URL path param. greatly reduce macro
  foolery and method count/complexity, and ease creation of new entities
    => /{entity}/edit/{edit_id}
    => /{entity}/{ident}/redirects
    => /{entity}/{ident}/history
- investigate data quality by looking at, eg, most popular author strings, most
  popular titles, duplicated containers, etc

## Metadata Import

- web.archive.org response not SHA1 match? => need /<dt>id_/ thing
- XML etc in metadata
    => (python) tests for these!
    https://qa.fatcat.wiki/release/search?q=xmlns
    https://qa.fatcat.wiki/release/search?q=%24gt
- bad/weird titles
    "[Blank page]", "blank page"
    "Temporary Empty DOI 0"
    "ADVERTISEMENT"
    "Full title page with Editorial board (with Elsevier tree)"
    "Advisory Board Editorial Board"
- better/complete reltypes probably good (eg, list of IRs, academic domain)
- 'expand' in lookups (derp! for single hit lookups)
- include crossref-capitalized DOI in extra
- some "Elsevier " stuff as publisher
    => also title https://fatcat.wiki/release/uyjzaq3xjnd6tcrqy3vcucczsi
- crossref import: don't store citation unstructured if len() == 0:
    {"crossref": {"unstructured": ""}}
- try out beautifulsoup? (https://stackoverflow.com/a/34532382/4682349)
- manifest: multiple URLs per SHA1
- crossref: relations ("is-preprint-of")
- crossref: two phase: no citations, then matched citations (via DOI table)
- special "alias" DOIs... in crossref metadata?

new importers:
- pubmed (medline) (filtered)
    => and/or, use pubmed ID lookups on crossref import
- arxiv.org
- DOAJ
- CORE (filtered)
- semantic scholar (up to 39 million; includes author de-dupe)

## Guide / Book / Style

- release_type, release_status, url.rel schemas (enforced in API)
- more+better terms+policies: https://tosdr.org/index.html

## Fun Features

- "save paper now"
    => is it in GWB? if not, SPN
    => get hash + url from GWB, verify mimetype acceptable
    => is file in fatcat?
    => what about HBase? GROBID?
    => create edit, redirect user to editgroup submit page
- python client tool and library in pypi
    => or maybe rust?
- bibtext (etc) export

## Metadata Harvesting

- datacite ingest seems to have failed... got a non-HTTP-200 status code, but also "got 50 (161950 of 21084)"

## Schema / Entity Fields

- elastic transform should only include authors, not editors (?)
- `doi` field for containers (at least for "journal" type; maybe for "series"
  as well?)
- `retracted`, `translation`, and perhaps `corrected` as flags on releases,
  instead of release_status?
    => use extra flags and release_status for now
- 'part-of' relation for releases (release to release) and possibly containers
- `container_type` field for containers (journal, conference, book series, etc)

## Other / Backburner

- refactor webface views to use shared entity_view.html template
- shadow library manifest importer
- book identifiers: OCLC, openlibrary
- ref from guide: https://creativecommons.org/2012/08/14/library-catalog-metadata-open-licensing-or-public-domain/
- test redirect/delete elasticsearch change
- fake DOI (use in examples): 10.5555/12345678
- refactor elasticsearch inserter to be a class (eg, for command line use)
- document: elastic query date syntax is like: date:[2018-10-01 TO 2018-12-31]
- fileset/webcapture webface anything
- display abstracts better. no hashes or metadata; prefer plain or HTML,
  convert JATS if necessary
- switch from slog to simple pretty_env_log
- format returned datetimes with only second precision, not millisecond (RFC mode)
    => burried in model serialization internals
- refactor openapi schema to use shared response types
- consider using "HTTP 202: Accepted" for entity-mutating calls
- basic python hbase/elastic matcher
  => takes sha1 keys
  => checks fatcat API + hbase
  => if not matched yet, tries elastic search
  => simple ~exact match heuristic
  => proof-of-concept, no tests
- add_header Strict-Transport-Security "max-age=3600";
    => 12 hours? 24?
- haproxy for rate-limiting

better API docs
- readme.io has a free open source plan (or at least used to)
- https://github.com/readmeio/api-explorer
- https://github.com/lord/slate
- https://sourcey.com/spectacle/
- https://github.com/DapperDox/dapperdox

CSL:
- https://citationstyles.org/
- https://github.com/citation-style-language/documentation/blob/master/primer.txt
- https://citeproc-js.readthedocs.io/en/latest/csl-json/markup.html
- https://github.com/citation-style-language/schema/blob/master/csl-types.rnc
- perhaps a "create from CSL" endpoint?