from ecreall.helpers.upgrade.interfaces import IUpgradeTool
from Products.Archetypes.interfaces.base import IBaseContent

import logging
LOG = logging.getLogger("plone.app.event.upgrade")

def update_to_main(context):
    tool = IUpgradeTool(context)
    from plone.app.event.at.content import ATEvent
    def update_contents(obj, path):
        if IBaseContent.providedBy(obj):
            obj.__class__ = ATEvent
            LOG.info("Updated class : %s", path)

    tool.migrateContent('ATEvent', update_to_main)

