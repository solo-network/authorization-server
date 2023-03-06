
conf = ...
api = AuthleteApiImpl(conf)

req = AuthorizationRequest()
req.parameters = ...

api.authorization(req)
