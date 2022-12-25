import urllib.request

fp = urllib.request.urlopen("https://www.newbalance.com/pd/550/BB550V1-36007.html")
mybytes = fp.read()

mystr = mybytes.decode("utf8")
fp.close()

print(mystr)
