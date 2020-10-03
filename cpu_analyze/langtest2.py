import tsdbhelper
from datetime import datetime


# tags={"a":"a", "b":"b"}
# fields = {"a":1, "b":2}

# tsdbhelper.put(measurement = 'cpu_prequency', \
#         time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z'), \
#             tags = tags, fields = fields)
from pprint import pprint
for r in tsdbhelper.query('select * from cpu_frequency;'):
    pprint(r)