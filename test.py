from datetime import datetime,timedelta, timezone
date = "Wed, 24 Apr 2024 19:42:09 +0300"
res = datetime.strptime(date,'%a, %d %b %Y %H:%M:%S %z')
print(datetime.utcnow() - timedelta(days=1) )



