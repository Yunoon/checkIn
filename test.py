import base64

test = open("sign_in6.png", "rb").read()
print(str(base64.b64encode(test))[2:-1])
