

import collections
from fatcat_client import ApiClient


def contribs_by_role(contribs, role):
    ret = [c.copy() for c in contribs if c['role'] == role]
    [c.pop('role') for c in ret]
    # XXX:
    [c.pop('literal') for c in ret]
    if not ret:
        return None
    else:
        return ret


def release_to_csl(entity):
    """
    Returns a python dict which can be json.dumps() to get a CSL-JSON (aka,
    citeproc-JSON, aka Citation Style Language JSON)

    This function will likely become an API method/endpoint

    Follows, but not enforced by: https://github.com/citation-style-language/schema/blob/master/csl-data.json
    """
    contribs = []
    for contrib in (entity.contribs or []):
        if contrib.creator:
            # TODO: should we actually be pulling creator metadata? or just
            # using release-local raw metadata?
            c = dict(
                family=contrib.creator.surname,
                given=contrib.creator.given_name,
                #dropping-particle
                #non-dropping-particle
                #suffix
                #comma-suffix
                #static-ordering
                literal=contrib.raw_name, # or display_name?
                #parse-names,
                role=contrib.role,
            )
        else:
            c = dict(
                # XXX: possible inclusion of full name metadata in release_contrib
                family=contrib.raw_name.split()[-1],
                literal=contrib.raw_name,
                role=contrib.role,
            )
        for k in list(c.keys()):
            if not c[k]:
                c.pop(k)
        contribs.append(c)
    abstract = None
    if entity.abstracts:
        abstract = entity.abstracts[0].content

    issued_date = None
    if entity.release_date:
        issued_date = {"date-parts": [[
            entity.release_date.year,
            entity.release_date.month,
            entity.release_date.day,
        ]]}
    elif entity.release_year:
        issued_date = {"date-parts": [[entity.release_year]]}

    csl = dict(
        #id,
        #categories
        type=entity.release_type or "article", # XXX: can't be blank
        language=entity.language,
        #journalAbbreviation
        #shortTitle
        ## see below for all contrib roles
        #accessed
        #container
        #event-date
        issued=issued_date,
        #original-date
        #submitted
        abstract=abstract,
        #annote
        #archive
        #archive_location
        #archive-place
        #authority
        #call-number
        #chapter-number
        #citation-number
        #citation-label
        #collection-number
        #collection-title
        container_title=entity.container and entity.container.name,
        #container-title-short
        #dimensions
        DOI=entity.doi,
        #edition
        #event
        #event-place
        #first-reference-note-number
        #genre
        ISBN=entity.isbn13,
        ISSN=entity.container and entity.container.issnl,
        issue=entity.issue,
        #jurisdiction
        #keyword
        #locator
        #medium
        #note
        #number
        #number-of-pages
        #number-of-volumes
        #original-publisher
        #original-publisher-place
        #original-title
        # TODO: page=entity.pages,
        page_first=entity.pages and entity.pages.split('-')[0],
        PMCID=entity.pmcid,
        PMID=entity.pmid,
        publisher=(entity.container and entity.container.publisher) or entity.publisher,
        #publisher-place
        #references
        #reviewed-title
        #scale
        #section
        #source
        #status
        title=entity.title,
        #title-short
        #URL
        #version
        volume=entity.volume,
        #year-suffix
    )
    for role in ['author', 'collection-editor', 'composer', 'container-author',
            'director', 'editor', 'editorial-director', 'interviewer',
            'illustrator', 'original-author', 'recipient', 'reviewed-author',
            'translator']:
        cbr = contribs_by_role(contribs, role)
        if cbr:
            csl[role] = cbr
    # underline-to-dash
    csl['container-title'] = csl.pop('container_title')
    csl['page-first'] = csl.pop('page_first')
    empty_keys = [k for k,v in csl.items() if not v]
    for k in empty_keys:
        csl.pop(k)
    return csl


def refs_to_csl(entity):
    ret = []
    for ref in entity.refs:
        if ref.release_id and False:
            # TODO: fetch full entity from API and convert with release_to_csl
            raise NotImplementedError
        else:
            issued_date = None
            if ref.year:
                issued_date = [[ref.year]]
            csl = dict(
                title=ref.title,
                issued=issued_date,
            )
        csl['id'] = ref.key or ref.index, # zero- or one-indexed?
        ret.append(csl)
    return ret

