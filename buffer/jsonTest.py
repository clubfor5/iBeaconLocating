import demjson
import json
data = [{'a':1, 'b':2}]
json = demjson.encode(data)
print(json)
text = demjson.decode(json)
print(text)
print(text[0])
text1 = json.loads(json)
print(text1)
pinrt(text1[0])
WTF