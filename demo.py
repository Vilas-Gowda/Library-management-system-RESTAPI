from datetime import date, timedelta

today = date.today()
enddate = date.today() + timedelta(days=30)
d1 = today.strftime("%d/%m/%Y")
d2 = enddate.strftime("%d/%m/%Y")

