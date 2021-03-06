
import json
import pytest
from copy import copy

from fatcat_client import *
from fatcat_client.rest import ApiException
from fixtures import *


def test_lookup_hide_extend(api):

    r = api.lookup_release(doi='10.1371/journal.pmed.0020124')
    assert len(r.refs) >= 2
    assert r.files is None
    assert r.container is None
    assert len(r.container_id) > 10
    assert r.abstracts == []

    r = api.lookup_release(doi='10.1371/journal.pmed.0020124', expand='files', hide='refs,abstracts')
    assert r.refs is None
    assert len(r.files[0].sha1) == 40
    assert r.container is None
    assert r.abstracts is None

    r = api.lookup_release(doi='10.1371/journal.pmed.0020124', expand='container,abstracts')
    assert len(r.refs) >= 2
    assert r.files is None
    assert r.container.issnl
    assert r.abstracts == []

def test_unexpected_body(api):

    eg = quick_eg(api)

    # all the fields!
    f1 = FileEntity(
        sha1="88888888888888892dd2657a1e3c992b5dc45dd2",
    )
    f1.urls = [dict(url="http://thing", rel="repository", asdf="blue")]
    api.create_file(f1, editgroup_id=eg.editgroup_id)

