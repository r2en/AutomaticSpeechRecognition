#!/usr/bin/env python

import cgi
from datetime import datetime

html_body="""
<html><meta charset="utf-8"><body>
%s
</body></html>"""

content=''

form = cgi.FieldStorage()
year_str = form.getvalue('year','')

if not year_str.isdigit():
    content=u'input A.D.'
else:
    year = int(year_str)
    friday13 = 0
    date = datetime(year, month, 13)
    if date.weekday()==4:
        friday13+=1
        content+=u"%d year %d month % day is Friday" % (year,date.month)
        content+=u"<br>"
    if friday13:
        content+=u"%d year, there are total %d in 13 days in friday" % (year,friday13)
    else:
        content+=u"%d year, nothing 13 day in Friday"

print "Content-type: text/html; charset=utf-8\n"
print (html_body % content).encode('utf-8')


        