PRODID = "-//AT Content Types//AT Event//EN"

# iCal header and footer
ICS_HEADER = """\
BEGIN:VCALENDAR
PRODID:%(prodid)s
VERSION:2.0
METHOD:PUBLISH
"""

ICS_FOOTER = """\
END:VCALENDAR
"""

# Note: a previous version of event start set "SEQUENCE:0"
# That's not necessary unless we're supporting recurrence.

# iCal event
ICS_EVENT_START = """\
BEGIN:VEVENT
DTSTAMP:%(dtstamp)s
CREATED:%(created)s
UID:ATEvent-%(uid)s
LAST-MODIFIED:%(modified)s
SUMMARY:%(summary)s
DTSTART:%(startdate)s
DTEND:%(enddate)s
"""

# Note: a previous version of event end set "TRANSP:OPAQUE", which would cause
# blocking of the time slot. That's not appropriate for an event
# calendar.
# Also, previous version set "PRIORITY:3", which the RFC interprets as a high
# priority. In absence of a priority field in the event, there's no justification
# for that.

ICS_EVENT_END = """\
CLASS:PUBLIC
END:VEVENT
"""