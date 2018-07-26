# coding: utf-8

"""
    fatcat

    A scalable, versioned, API-oriented catalog of bibliographic entities and file metadata  # noqa: E501

    OpenAPI spec version: 0.1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from fatcat_client.models.editgroup_edits import EditgroupEdits  # noqa: F401,E501


class Editgroup(object):
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
        'id': 'str',
        'editor_id': 'str',
        'description': 'str',
        'extra': 'object',
        'edits': 'EditgroupEdits'
    }

    attribute_map = {
        'id': 'id',
        'editor_id': 'editor_id',
        'description': 'description',
        'extra': 'extra',
        'edits': 'edits'
    }

    def __init__(self, id=None, editor_id=None, description=None, extra=None, edits=None):  # noqa: E501
        """Editgroup - a model defined in Swagger"""  # noqa: E501

        self._id = None
        self._editor_id = None
        self._description = None
        self._extra = None
        self._edits = None
        self.discriminator = None

        if id is not None:
            self.id = id
        self.editor_id = editor_id
        if description is not None:
            self.description = description
        if extra is not None:
            self.extra = extra
        if edits is not None:
            self.edits = edits

    @property
    def id(self):
        """Gets the id of this Editgroup.  # noqa: E501

        base32-encoded unique identifier  # noqa: E501

        :return: The id of this Editgroup.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Editgroup.

        base32-encoded unique identifier  # noqa: E501

        :param id: The id of this Editgroup.  # noqa: E501
        :type: str
        """
        if id is not None and len(id) > 26:
            raise ValueError("Invalid value for `id`, length must be less than or equal to `26`")  # noqa: E501
        if id is not None and len(id) < 26:
            raise ValueError("Invalid value for `id`, length must be greater than or equal to `26`")  # noqa: E501
        if id is not None and not re.search('[a-zA-Z2-7]{26}', id):  # noqa: E501
            raise ValueError("Invalid value for `id`, must be a follow pattern or equal to `/[a-zA-Z2-7]{26}/`")  # noqa: E501

        self._id = id

    @property
    def editor_id(self):
        """Gets the editor_id of this Editgroup.  # noqa: E501

        base32-encoded unique identifier  # noqa: E501

        :return: The editor_id of this Editgroup.  # noqa: E501
        :rtype: str
        """
        return self._editor_id

    @editor_id.setter
    def editor_id(self, editor_id):
        """Sets the editor_id of this Editgroup.

        base32-encoded unique identifier  # noqa: E501

        :param editor_id: The editor_id of this Editgroup.  # noqa: E501
        :type: str
        """
        if editor_id is None:
            raise ValueError("Invalid value for `editor_id`, must not be `None`")  # noqa: E501
        if editor_id is not None and len(editor_id) > 26:
            raise ValueError("Invalid value for `editor_id`, length must be less than or equal to `26`")  # noqa: E501
        if editor_id is not None and len(editor_id) < 26:
            raise ValueError("Invalid value for `editor_id`, length must be greater than or equal to `26`")  # noqa: E501
        if editor_id is not None and not re.search('[a-zA-Z2-7]{26}', editor_id):  # noqa: E501
            raise ValueError("Invalid value for `editor_id`, must be a follow pattern or equal to `/[a-zA-Z2-7]{26}/`")  # noqa: E501

        self._editor_id = editor_id

    @property
    def description(self):
        """Gets the description of this Editgroup.  # noqa: E501


        :return: The description of this Editgroup.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this Editgroup.


        :param description: The description of this Editgroup.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def extra(self):
        """Gets the extra of this Editgroup.  # noqa: E501


        :return: The extra of this Editgroup.  # noqa: E501
        :rtype: object
        """
        return self._extra

    @extra.setter
    def extra(self, extra):
        """Sets the extra of this Editgroup.


        :param extra: The extra of this Editgroup.  # noqa: E501
        :type: object
        """

        self._extra = extra

    @property
    def edits(self):
        """Gets the edits of this Editgroup.  # noqa: E501


        :return: The edits of this Editgroup.  # noqa: E501
        :rtype: EditgroupEdits
        """
        return self._edits

    @edits.setter
    def edits(self, edits):
        """Sets the edits of this Editgroup.


        :param edits: The edits of this Editgroup.  # noqa: E501
        :type: EditgroupEdits
        """

        self._edits = edits

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
        if not isinstance(other, Editgroup):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
