import base64
coded_string = '''VmlsYXMxOndLZEhrWEdrd1ZUVWloaUpsck5FWXc='''
a = base64.b64decode(coded_string)
c = 'Basic ZGVtbzpkZW1vMTIz'
username =  c.split()[1]
username = str(base64.b64decode(c))
username = c.split(':')[0][2:]
print(c)