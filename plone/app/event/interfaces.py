from zope import schema
from zope.interface import Interface

from plone.event.utils import default_timezone as fallback_default_timezone
from plone.app.event import messageFactory as _


ISO_DATE_FORMAT = '%Y-%m-%d'


# Controlpanel Interface

class IEventSettings(Interface):
    """ Global settings for eventish content types.
    """

    portal_timezone = schema.Choice(
            title=_(u"Portal default timezone"),
            description=_(u"help_portal_timezone",
                default=u"The timezone setting of the portal. Users can set "
                         "their own timezone, if available timezones are defined."),
            required=True,
            default=fallback_default_timezone(),
            vocabulary="plone.app.event.Timezones"
            )

    available_timezones = schema.List(
            title=_(u"Available timezones"),
            description=_(u"help_available_timezones",
                default=u"The timezones, which should be available for the portal. "
                         "Can be set for users and events"),
            required=False,
            default=[],
            value_type=schema.Choice(
                vocabulary="plone.app.event.Timezones"
                )
            )

    first_weekday = schema.Choice(
            title=_(u'label_first_weekday', default=u'First Weekday'),
            description=_(u'help_first_weekday', default=u'First day in the Week.'),
            required=True,
            default='0',
            vocabulary="plone.app.event.Weekdays"
            )
