# coding: utf-8

"""
    fatcat

    A scalable, versioned, API-oriented catalog of bibliographic entities and file metadata  # noqa: E501

    OpenAPI spec version: 0.2.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class ContainerEntity(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'wikidata_qid': 'str',
        'issnl': 'str',
        'publisher': 'str',
        'container_type': 'str',
        'name': 'str',
        'edit_extra': 'object',
        'extra': 'object',
        'redirect': 'str',
        'revision': 'str',
        'ident': 'str',
        'state': 'str'
    }

    attribute_map = {
        'wikidata_qid': 'wikidata_qid',
        'issnl': 'issnl',
        'publisher': 'publisher',
        'container_type': 'container_type',
        'name': 'name',
        'edit_extra': 'edit_extra',
        'extra': 'extra',
        'redirect': 'redirect',
        'revision': 'revision',
        'ident': 'ident',
        'state': 'state'
    }

    def __init__(self, wikidata_qid=None, issnl=None, publisher=None, container_type=None, name=None, edit_extra=None, extra=None, redirect=None, revision=None, ident=None, state=None):  # noqa: E501
        """ContainerEntity - a model defined in Swagger"""  # noqa: E501

        self._wikidata_qid = None
        self._issnl = None
        self._publisher = None
        self._container_type = None
        self._name = None
        self._edit_extra = None
        self._extra = None
        self._redirect = None
        self._revision = None
        self._ident = None
        self._state = None
        self.discriminator = None

        if wikidata_qid is not None:
            self.wikidata_qid = wikidata_qid
        if issnl is not None:
            self.issnl = issnl
        if publisher is not None:
            self.publisher = publisher
        if container_type is not None:
            self.container_type = container_type
        if name is not None:
            self.name = name
        if edit_extra is not None:
            self.edit_extra = edit_extra
        if extra is not None:
            self.extra = extra
        if redirect is not None:
            self.redirect = redirect
        if revision is not None:
            self.revision = revision
        if ident is not None:
            self.ident = ident
        if state is not None:
            self.state = state

    @property
    def wikidata_qid(self):
        """Gets the wikidata_qid of this ContainerEntity.  # noqa: E501


        :return: The wikidata_qid of this ContainerEntity.  # noqa: E501
        :rtype: str
        """
        return self._wikidata_qid

    @wikidata_qid.setter
    def wikidata_qid(self, wikidata_qid):
        """Sets the wikidata_qid of this ContainerEntity.


        :param wikidata_qid: The wikidata_qid of this ContainerEntity.  # noqa: E501
        :type: str
        """

        self._wikidata_qid = wikidata_qid

    @property
    def issnl(self):
        """Gets the issnl of this ContainerEntity.  # noqa: E501


        :return: The issnl of this ContainerEntity.  # noqa: E501
        :rtype: str
        """
        return self._issnl

    @issnl.setter
    def issnl(self, issnl):
        """Sets the issnl of this ContainerEntity.


        :param issnl: The issnl of this ContainerEntity.  # noqa: E501
        :type: str
        """
        if issnl is not None and len(issnl) > 9:
            raise ValueError("Invalid value for `issnl`, length must be less than or equal to `9`")  # noqa: E501
        if issnl is not None and len(issnl) < 9:
            raise ValueError("Invalid value for `issnl`, length must be greater than or equal to `9`")  # noqa: E501
        if issnl is not None and not re.search('\\d{4}-\\d{3}[0-9X]', issnl):  # noqa: E501
            raise ValueError("Invalid value for `issnl`, must be a follow pattern or equal to `/\\d{4}-\\d{3}[0-9X]/`")  # noqa: E501

        self._issnl = issnl

    @property
    def publisher(self):
        """Gets the publisher of this ContainerEntity.  # noqa: E501


        :return: The publisher of this ContainerEntity.  # noqa: E501
        :rtype: str
        """
        return self._publisher

    @publisher.setter
    def publisher(self, publisher):
        """Sets the publisher of this ContainerEntity.


        :param publisher: The publisher of this ContainerEntity.  # noqa: E501
        :type: str
        """

        self._publisher = publisher

    @property
    def container_type(self):
        """Gets the container_type of this ContainerEntity.  # noqa: E501

        Eg, 'journal'  # noqa: E501

        :return: The container_type of this ContainerEntity.  # noqa: E501
        :rtype: str
        """
        return self._container_type

    @container_type.setter
    def container_type(self, container_type):
        """Sets the container_type of this ContainerEntity.

        Eg, 'journal'  # noqa: E501

        :param container_type: The container_type of this ContainerEntity.  # noqa: E501
        :type: str
        """

        self._container_type = container_type

    @property
    def name(self):
        """Gets the name of this ContainerEntity.  # noqa: E501

        Required for valid entities  # noqa: E501

        :return: The name of this ContainerEntity.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ContainerEntity.

        Required for valid entities  # noqa: E501

        :param name: The name of this ContainerEntity.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def edit_extra(self):
        """Gets the edit_extra of this ContainerEntity.  # noqa: E501


        :return: The edit_extra of this ContainerEntity.  # noqa: E501
        :rtype: object
        """
        return self._edit_extra

    @edit_extra.setter
    def edit_extra(self, edit_extra):
        """Sets the edit_extra of this ContainerEntity.


        :param edit_extra: The edit_extra of this ContainerEntity.  # noqa: E501
        :type: object
        """

        self._edit_extra = edit_extra

    @property
    def extra(self):
        """Gets the extra of this ContainerEntity.  # noqa: E501


        :return: The extra of this ContainerEntity.  # noqa: E501
        :rtype: object
        """
        return self._extra

    @extra.setter
    def extra(self, extra):
        """Sets the extra of this ContainerEntity.


        :param extra: The extra of this ContainerEntity.  # noqa: E501
        :type: object
        """

        self._extra = extra

    @property
    def redirect(self):
        """Gets the redirect of this ContainerEntity.  # noqa: E501

        base32-encoded unique identifier  # noqa: E501

        :return: The redirect of this ContainerEntity.  # noqa: E501
        :rtype: str
        """
        return self._redirect

    @redirect.setter
    def redirect(self, redirect):
        """Sets the redirect of this ContainerEntity.

        base32-encoded unique identifier  # noqa: E501

        :param redirect: The redirect of this ContainerEntity.  # noqa: E501
        :type: str
        """
        if redirect is not None and len(redirect) > 26:
            raise ValueError("Invalid value for `redirect`, length must be less than or equal to `26`")  # noqa: E501
        if redirect is not None and len(redirect) < 26:
            raise ValueError("Invalid value for `redirect`, length must be greater than or equal to `26`")  # noqa: E501
        if redirect is not None and not re.search('[a-zA-Z2-7]{26}', redirect):  # noqa: E501
            raise ValueError("Invalid value for `redirect`, must be a follow pattern or equal to `/[a-zA-Z2-7]{26}/`")  # noqa: E501

        self._redirect = redirect

    @property
    def revision(self):
        """Gets the revision of this ContainerEntity.  # noqa: E501

        UUID (lower-case, dash-separated, hex-encoded 128-bit)  # noqa: E501

        :return: The revision of this ContainerEntity.  # noqa: E501
        :rtype: str
        """
        return self._revision

    @revision.setter
    def revision(self, revision):
        """Sets the revision of this ContainerEntity.

        UUID (lower-case, dash-separated, hex-encoded 128-bit)  # noqa: E501

        :param revision: The revision of this ContainerEntity.  # noqa: E501
        :type: str
        """
        if revision is not None and len(revision) > 36:
            raise ValueError("Invalid value for `revision`, length must be less than or equal to `36`")  # noqa: E501
        if revision is not None and len(revision) < 36:
            raise ValueError("Invalid value for `revision`, length must be greater than or equal to `36`")  # noqa: E501
        if revision is not None and not re.search('[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', revision):  # noqa: E501
            raise ValueError("Invalid value for `revision`, must be a follow pattern or equal to `/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/`")  # noqa: E501

        self._revision = revision

    @property
    def ident(self):
        """Gets the ident of this ContainerEntity.  # noqa: E501

        base32-encoded unique identifier  # noqa: E501

        :return: The ident of this ContainerEntity.  # noqa: E501
        :rtype: str
        """
        return self._ident

    @ident.setter
    def ident(self, ident):
        """Sets the ident of this ContainerEntity.

        base32-encoded unique identifier  # noqa: E501

        :param ident: The ident of this ContainerEntity.  # noqa: E501
        :type: str
        """
        if ident is not None and len(ident) > 26:
            raise ValueError("Invalid value for `ident`, length must be less than or equal to `26`")  # noqa: E501
        if ident is not None and len(ident) < 26:
            raise ValueError("Invalid value for `ident`, length must be greater than or equal to `26`")  # noqa: E501
        if ident is not None and not re.search('[a-zA-Z2-7]{26}', ident):  # noqa: E501
            raise ValueError("Invalid value for `ident`, must be a follow pattern or equal to `/[a-zA-Z2-7]{26}/`")  # noqa: E501

        self._ident = ident

    @property
    def state(self):
        """Gets the state of this ContainerEntity.  # noqa: E501


        :return: The state of this ContainerEntity.  # noqa: E501
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """Sets the state of this ContainerEntity.


        :param state: The state of this ContainerEntity.  # noqa: E501
        :type: str
        """
        allowed_values = ["wip", "active", "redirect", "deleted"]  # noqa: E501
        if state not in allowed_values:
            raise ValueError(
                "Invalid value for `state` ({0}), must be one of {1}"  # noqa: E501
                .format(state, allowed_values)
            )

        self._state = state

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ContainerEntity):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
