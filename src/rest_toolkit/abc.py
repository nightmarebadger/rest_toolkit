from __future__ import absolute_import
import abc
from .compat import add_metaclass


@add_metaclass(abc.ABCMeta)
class ViewableResource(object):
    """Base class for resources using the default GET view.

    If a resource class is derived from this class it must implement the
    :py:meth:`to_dict` method. Doing this will automatically enable the default
    GET view from rest_toolkit.
    """

    @abc.abstractmethod
    def to_dict(self):
        """Generate a (JSON-compatible) dictionary with resource data.

        This method is used by the default GET, PATCH and PUT views to generate
        the data for the response. It is also used by by the PATCH view
        to complete the (partial) data provided by a client before validation
        is done (see :py:class:`EditableResource` for details).
        """
        raise NotImplemented()


@add_metaclass(abc.ABCMeta)
class EditableResource(object):
    """Base class for resources using the default PATCH and PUT views.

    If a resource class is derived from this class it must implement the
    :py:meth:`to_dict`, :py:meth:`validate` and :py:meth:`update_from_dict`
    methods. Doing this will automatically enable the default GET, PATCH and
    PUT views from rest_toolkit.
    """

    @abc.abstractmethod
    def validate(self, data, partial):
        """Validate new data for the resource.

        This method is called to validate data received from a client before it
        is passed to :py:meth:`update_from_dict`.

        :param dict data: data to validate. The data is usually taken directly
            from JSON send by a client.
        :param bool partial: indicates if data contains the full resource state
            (as received in a PUT request), or only partial state (as received
            in a PATCH request). You can reconstruct the full resource state
            from partial data by using :py:func:`merge
            <rest_toolkit.utils.merge>` to come data the current state as
            returned by :py:meth:`to_dict` with `data`.

            .. code-block:: python
               :linenos:

               full_state = merge(self.to_dict(), data) if partial else data

        :raises HTTPException: if all further request processing should be aborted
            and the exception returned directly.
        """
        raise NotImplemented()

    @abc.abstractmethod
    def to_dict(self):
        """Generate a (JSON-compatible) dictionary with resource data.

        This method is used by the default GET, PATCH and PUT views to generate
        the data for the response. It is also used by by the PATCH view
        to complete the (partial) data provided by a client before validation
        is done.
        """
        raise NotImplemented()

    @abc.abstractmethod
    def update_from_dict(self, data, replace):
        """Update a resource.

        :param dict data: The data to validate. The data is usually taken
            directly from JSON send by a client.
        :param bool replace: Indicates if the provided data should fully
            replace the resource state (as should be done for a PUT request),
            or if only provided keys should be updated (as should be done
            for a PATCH request).
        """
        raise NotImplemented()


@add_metaclass(abc.ABCMeta)
class DeletableResource(object):
    """Base class for resources using the default DELETE views.

    If a resource class is derived from this class it must implement the
    :py:meth:`dlete` method. Doing this will automatically enable the default
    DELETE view from rest_toolkit.
    """

    @abc.abstractmethod
    def delete(self):
        """Delete the resource.

        This method must delete the resource, or mark it as deleted, so that it
        is no longer accessible through the REST API.
        """
        raise NotImplemented()


__all__ = ['DeletableResource', 'EditableResource', 'ViewableResource']
