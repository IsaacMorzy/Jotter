# outstanding work from the jenga api team to simplify payments reception in Africa.
# the 2 properties of restful apis which make them suitable for modern internet development
# are:
1. stateless = enforces no state-machine thus there is no order of protocol messages enforced
2. cache-less = the protocol will not remember any info across requests/responses. Each request
                is unique and has no relation to previous or next request.

# points to remember while developing rest apis
1. URL  eg.https://graph.facebook.com/v2.3/{photo_id}
2. Message Type [GET, POST, PUT, DELETE]
    import requests
    ret = requests.get(url)
    ret2 = requests.post(url)   # update a resource
    ret3 = requests.put(url)    # create a resource
    ret4 = requests.delete(url) # delete a resource


3. HTTP Headers -- contain info used to process the request and responses. Headers are colon-separated
                    key-value pairs

                    head = {"Content-type": "application/json"}
                    ret = requests.get(url, headers=head)
                    ret.status_code # 200

4. Parameters--pass values in the url parameters
    parameters = {'name': 'saranavan', 'designation': 'Technical Leader'}
    head = {'Content-type': 'application/json'}
    ret = requests.post(url, params=parameters, headers=head)   

5. Payload -- contains the data to be sent in the requests.
    eg. to send a json object in the payload:
    
    import json, requests
    url = 'http://graph.facebook.com/v2.3/12335'
    head = {'Content-type': 'application/json', 'accept': 'application/json'}
    payload = {'name': 'saravan', 'Designation': 'Architect', 'Organization': 'Cisco Systems'}
    payId = json.dumps(payload) # convert dict to json object
    ret = requests.post(url, header=head, data=payId)
    ret.status_code # 200 ok



6. Authentication -- requests lib can support various means of authentication like Basic, Digest Authentication, OAuth, etc
    from requests.auth import HTTPBasicAuth
    url = 'http://www.hostmachine.com/sem/getInstances'
    ret = requests.get(url, auth=HTTPBasicAuth('username': 'password'))
    ret.status_code # 200 ok

#-----------------jenga api endpoint structure----------------------
{protocol}://{host}/{basePath}/{resource}

# to generate an access token where uat.jengahq.io is the host for all resources
https://uat.jengahq.io/identity/v2/token


JengaAPI supports the OAuth 2.0 Authentication Framework, requiring you to provide a username and password, as well as an API key that you generate on Jenga HQ part of HTTP Basic Authentication to generate a Bearer token.

Once you have a token you can make subsequent requests to initiate payments, check completed transactions and more.

To generate your Bearer token, you will need your username, password and the API Key 
that you will pass in the Authorization header of your request.

eg.
    POST /identity-test/v2/token HTTP/1.1
    Authorization: Basic czZCaGRSa3F0MzpnWDFmQmF0M2JW
    Content-type:application/x-www-form-urlencoded

    username=0582910862&password=ce0NHpa7ZaxmOFkbEbULABpu412fS4NQa
# sample response
200 ok
{
    "token-type": "bearer",
    "issued_at": "1443102144106",
    "expires-in": "3599",
    "access-token": "ceTo5RCpluTfGn9B3OZXnnQkDVKM"
}

# generate signatures
To ensure the security of your transactions or requests, 
we have implemented security controls that we ensure that 
transactions can only be initiated by you and no one else. 
To achieve this, we use message signatures.

# All requests other than the identity api will require a signature in the header
Signature:<signature-in-base64>

To generate the signature, you will need to create a key pair of private key and public key. 
You will share the public key with us and use the private key to generate the signature.

# to generate the key pair
openssl genrsa -out privatekey.pem 2048 -nodes  # private key will be generated in your present dir

Proceed to export the publickey from the pair generated.
openssl rsa -in privatekey.pem -outform PEM -pubout -out publickey.pem

If the above command is successful, a new file (publickey.pem) will be created on your present directory. 
Copy the contents of this file and add it on our jengaHQ portal. 
Make sure to copy only the contents of the keyblock and paste as is.

# generating a signature
Prep the data being signed by concatenating particular values within the api request payload

eg (using the opening and closing account balance api)
    {
        "countryCode": "KE",
        "accountId": "0011547896523",
        "date": "2018-08-09"
    }

A SHA-256 signature to prove that this request is coming from the merchant.
Build a String of concatenated values of the request fields with the following order: 
    accountId, countryCode, date. 
The resulting text is then signed with Private Key and Base64 encoded.
We can see that the data to be signed is a concatenation of the values in the fields: 
    accountId, countryCode and date and in that order and from our payload above, 
    that would be: 0011547896523KE2018-08-09. This is the data we will sign.


# to sign the data using python
from base64 import b64encode
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA

message = "0011547896523KE2018-08-09".encode('utf-8')
digest = SHA256.new()   #create a new instance of SHA256 signature
digest.update(message)  # feed message to the signing instance

private_key = False
with open("privatekey.pem", "r") as my_file:
    private_key = RSA.importKey(my_file.read())

signer = PKCS1_v1_5.new(private_key)
sigBytes = signer.sign(digest)
signBase64 = b64encode(sigBytes)

>>>Your generated signature is now a variable 'signBase64'.<<<

You can now include it in your requests:

import json
import requests
from base64 import b64encode
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA

message = "0011547896523KE2018-08-09".encode('utf-8')
digest = SHA256.new()
digest.update(message)

private_key = False
with open("privatekey.pem", "r") as myfile:
    private_key = RSA.importKey(myfile.read())

signer = PKCS1_v1_5.new(private_key)
sigBytes = signer.sign(digest)
signBase64 = b64encode(sigBytes)

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ipARkr578zcp2fYPiZpEL1cpG6qE',
    'signature': signBase64
}

params = {}

payload = {
    "countryCode": "KE",
    "accountId": "0011547896523",
    "date": "2018-08-09"
}

url = "https://sandbox.jengahq.io/account-test/v2/accountbalance/query"

response = requests.post(url, headers=headers, params=params, data=json.dumps(payload))

print(response.text)

# you have completed your first secure api request

# ------------------your first api call------------------
You've initiated a request to get your account opening and closing balance from your application.

You'll call the Opening and Closing Account Balance API and pass the account number (accountId) in the payload, 
as well as the Bearer token and signature in the Authorization Header of your request.

POST /account-test/v2/accountbalance/query HTTP/1.1
Content-Type: application/json
Authorization: Bearer 67ew8n31me
signature: KCfrIYXSQdGPsKdu6yOxkNLmnUKOpT3M89K2p/pfCJRkrvKH9jD5ot/7BHuIYaicFi+CONYB4oiM5bWA8hUpUahmHBRf06LHXKWLEz3CYme+UhJ4W0EozhiMcj94og8QW/Rnnp3F9asBtU1498Y4qnNasW5BtWLR5ZvhRFrn0/kKH2CgopRctKOMBIDD55AzxqlkDdBhT1zsAbVIU9Rk55FXJxEjgw7+A505wqcfStybaZLaEeRxi2n5AZ9B0GcDZQ4G98IVael/M92JrxdZmmfe9xC/9fCANU+g0oQkuv9iwQ+bd0DVx1J5zjmNOI21eJApY2LifKBAyRH/az7AFg==
 
{
   "countryCode": "KE",
   "accountId": "0011547896523",
   "date": "2017-09-29"
}

You're ready to use any of the other APIs. 
All you need to do is pass the parameters of the endpoint and authorize your request 
by passing your Bearer token in the Authorization Header plus signature, where required.















































































