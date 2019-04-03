"""

"""
import logging, requests, json, time
import xml.dom.minidom
from sickle import Sickle, oaiexceptions
from requests.adapters import HTTPAdapter
# unclear why pylint chokes on this import. Recent 'requests' and 'urllib3' are
# in Pipenv.lock, and there are no errors in QA
from requests.packages.urllib3.util.retry import Retry # pylint: disable=import-error

_LOGGER = logging.getLogger(__name__)

_OAI_SRC_IDS = ('arxiv', 'doajA', 'doajJ', 'pubmed')
_DOI_SRC_IDS = ('crossref', 'datacite')

SRC_IDS = _OAI_SRC_IDS + _DOI_SRC_IDS


def src_oai_id(src_ids):
    """
    The command line arguments contains dict keys corresponding to
    oai source id's.
    :param src_ids: list corresponding to oai source ids
    :return: tuple of oai source id's set to true.
    """
    if 'all' in src_ids:
        return _OAI_SRC_IDS + _DOI_SRC_IDS # return all the id's

    # Only one will be set otherwise
    oai_ids = [id for id in _OAI_SRC_IDS if id in src_ids]
    doi_ids = [id for id in _DOI_SRC_IDS if id in src_ids]
    return tuple(oai_ids + doi_ids)


def _requests_retry_session(retries=10, backoff_factor=3,
                            status_forcelist=(500, 502, 504), session=None):
    """
    From: https://www.peterbe.com/plog/best-practice-with-retries-with-requests
    """
    session = session if session else requests.Session()

    retry = Retry(total=retries, read=retries, connect=retries,
                  backoff_factor=backoff_factor,  status_forcelist=status_forcelist,)

    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def _update_params(params, resp):
    params['cursor'] = resp['message']['next-cursor']
    return params


def _extract_key(obj):
    return obj['DOI'].encode('utf-8')


def _params(date_str, is_update_filter, batch_sz):
    filter_param = 'from-index-date:{},until-index-date:{}'.format(date_str, date_str)

    if is_update_filter is not None:
        filter_param += ',is_update:{}'.format(bool(is_update_filter))

    return {
        'filter': filter_param,
        'rows': batch_sz,
        'cursor': '*',
    }


def _extract_items(resp):
    return resp['message']['items']


class Harvester:
    """

    """

    def __init__(self, src_id, endpoint_url=None, meta_prefix=None, contact_email=None, is_update_filter=None,
                 sleep=30.0, to_stdout=False):
        self._to_stdout = to_stdout
        self._loop_sleep = sleep
        self._metadata_prefix = meta_prefix
        self._endpoint_url = endpoint_url
        self._src_id = src_id
        self._is_update_filter = is_update_filter
        self._contact_email = contact_email
        self._batch_sz = 100
        # Ok this looks like magic but I didn't want to create
        # factories, subclasses or IF THENs to choose between
        # just 2 functions in a limited number of cases.
        if src_id in _OAI_SRC_IDS:
            self.fetch_recs_day = self.fetch_oai_recs_day
            self.to_string = self.to_string_oai
        if src_id in _DOI_SRC_IDS:
            self.fetch_recs_day = self.fetch_doi_recs_day
            self.to_string = self.to_string_doi

    @property
    def sleep(self):
        """
        Sleep interval in seconds
        :return: str
        """
        return self._loop_sleep

    @sleep.setter
    def sleep(self, value):
        """
        Sleep interval in seconds
        :param value: str
        :return:
        """
        self._loop_sleep = value

    @property
    def endpoint_url(self):
        """
        URL of Oai data source
        :return: str
        """
        return self._endpoint_url

    @endpoint_url.setter
    def endpoint_url(self, value):
        """
        URL of Oai data source
        :param value: String
        :return:
        """
        self._endpoint_url = value

    @property
    def metadata_prefix(self):
        """

        :return:
        """
        return self._metadata_prefix

    @metadata_prefix.setter
    def metadata_prefix(self, value):
        """

        :param value: str
        :return: str
        """
        self._metadata_prefix = value

    @property
    def src_id(self):
        return self._src_id

    @src_id.setter
    def src_id(self, value):
        self._src_id = value

    @property
    def to_stdout(self):
        """
        Boolean flag to send output to standard out
        :return:
        """
        return self._to_stdout

    @to_stdout.setter
    def to_stdout(self, value):
        """
        Boolean flag to send output to standard out
        :param value: Boolean
        :return:
        """
        self._to_stdout = value

    @property
    def batch_sz(self):
        """
        Boolean flag to send output to standard out
        :return:
        """
        return self._batch_sz

    @batch_sz.setter
    def batch_sz(self, value):
        """
        Boolean flag to send output to standard out
        :param value: Boolean
        :return:
        """
        self._batch_sz = value

    def to_string_oai(self, rec):
        """
        Convert a rec to a pretty print string.
        :param rec: str
        :return:  str - reformatted
        """
        dom = xml.dom.minidom.parseString(rec)
        return dom.toprettyxml()

    def to_string_doi(self, rec):
        """
        Convert a rec to a pretty print string.
        :param rec: str
        :return:  str - reformatted
        """
        parsed = json.loads(rec)
        return json.dumps(parsed, indent=4, sort_keys=True)

    def fetch_oai_recs_day(self, date):
        """
        Generator that returns the key and full record
        of works deposited on a particular day.

        :param day:
        :return: str key, str rec
        """
        api = Sickle(self.endpoint_url)
        date_str = date.isoformat()
        # this dict kwargs hack is to work around 'from' as a reserved python keyword
        # recommended by sickle docs
        # Question: Why would someone insist on using a keyword for a parameter?
        try:
            records = api.ListRecords(**{
                'metadataPrefix': self.metadata_prefix,
                'from': date_str,
                'until': date_str,
            })
        except oaiexceptions.NoRecordsMatch:
            records = []
            _LOGGER.info('OAI request produced no records.')

        for item in records:
            yield item.header.identifier.encode('utf-8'), item.raw.encode('utf-8')

    def fetch_doi_works(self, day):
        """

        :param day:
        :return:
        """
        date_str = day.isoformat()
        batch_sz = self._batch_sz
        is_update_filter = self._is_update_filter
        params = _params(date_str, is_update_filter, batch_sz)

        http_session = _requests_retry_session()
        http_session.headers.update({
            'User-Agent': 'fatcat_tools/0.1.0 (https://fatcat.wiki; mailto:{}) python-requests'.format(
                self._contact_email),
        })

        while True:
            http_resp = http_session.get(self.endpoint_url, params=params)

            if http_resp.status_code == 503:
                _LOGGER.info('DOI http request backing off due to status 503.')
                # crude backoff; now redundant with session exponential
                # backoff, but allows for longer backoff/downtime on remote end
                time.sleep(self.sleep)
                continue

            http_resp.raise_for_status()
            resp = http_resp.json()
            items = _extract_items(resp)

            for work in items:
                yield work

            if len(items) < self._batch_sz:
                break

            params = _update_params(params, resp)

    def fetch_doi_recs_day(self, day):
        """
        Generator that returns the key and full record
        of works deposited on a particular day.

        :param day:
        :return: str key, str rec
        """
        for work in self.fetch_doi_works(day):
            yield _extract_key(work), json.dumps(work).encode('utf-8')


