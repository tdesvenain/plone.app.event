from Products.ATContentTypes.interfaces.event import IATEvent
from Products.CMFCore.interfaces import IPropertiesTool
from Products.CMFCore.utils import getToolByName
from Products.contentmigration.archetypes import ATItemMigrator
from Products.contentmigration.walker import CustomQueryWalker
from transaction import savepoint
from zope.component import queryUtility
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent

import transaction
import logging


logger = logging.getLogger('plone.app.event.at migration')


class PAEATMigrator(ATItemMigrator):
    src_portal_type = 'Event'
    src_meta_type = 'ATEvent'
    dst_portal_type = 'Event'
    dst_meta_type = 'ATEvent'

    def migrate_schema(self):
        """Migrate old ATEvent schema to plone.app.event's ATEvent.
        """
        # TODO: assure - if possible - that timezone is set correctly.
        # Call ObjectModifiedEvent to do data_postprocessing on each event
        # object.
        notify(ObjectModifiedEvent(self.new))


def callBefore(oldobj):
    transaction.commit()  # Do a commit before each migration, commiting the
                          # previous changes to avoid running out of space for
                          # large migrations.
    if 'portal_factory' in oldobj.getPhysicalPath():
        logger.info('Skipping factory obj: {0}'.format(
            '/'.join(oldobj.getPhysicalPath())))
        return False
    return True


def upgrade_step_1(context):
    # switch linkintegrity temp off
    ptool = queryUtility(IPropertiesTool)
    site_props = getattr(ptool, 'site_properties', None)
    linkintegrity = site_props.getProperty(
        'enable_link_integrity_checks',
        False
    )
    site_props.manage_changeProperties(enable_link_integrity_checks=False)

    # do migration
    portal = getToolByName(context, 'portal_url').getPortalObject()
    walker = CustomQueryWalker(
        portal, PAEATMigrator,
        query=dict(object_provides=IATEvent.__identifier__),
        callBefore=callBefore)
    savepoint(optimistic=True)
    walker.go()

    # switch linkintegrity back
    site_props.manage_changeProperties(
        enable_link_integrity_checks=linkintegrity
    )

    return walker.getOutput()

from ecreall.helpers.upgrade.interfaces import IUpgradeTool
from Products.Archetypes.interfaces.base import IBaseContent

def upgrade_step_1_bis(context):
    tool = IUpgradeTool(context)
    from plone.app.event.at.content import ATEvent
    from plone.app.event.portlets.portlet_calendar import Assignment as CalendarAssignment
    from plone.app.event.portlets.portlet_events import Assignment as EventsAssignment

    def update_at_class(obj, path):
        if obj.__class__.__module__ == 'plone.app.event.event':
            obj.__class__ = ATEvent
            logger.info("Updated class : %s", path)

    tool.migrateContent('Event', update_at_class)
    tool.runImportStep('plone.app.event', 'plone.app.registry')

    def update_portlets(obj, path):
        right_portlets = obj.restrictedTraverse('++contextportlets++plone.rightcolumn').items()
        left_portlets = obj.restrictedTraverse('++contextportlets++plone.leftcolumn').items()
        for name, assignment in right_portlets + left_portlets:
            if assignment.__class__.__module__ == 'plone.app.event.portlets.calendar':
                assignment.__class__ = CalendarAssignment
                logger.info("Updated portlet : %s at %s", name, path)

            if assignment.__class__.__module__ == 'plone.app.event.portlets.events':
                assignment.__class__ = EventsAssignment
                logger.info("Updated portlet : %s at %s", name, path)

    tool.migrateContent(tool.portal.portal_types.keys(),
                        update_portlets)