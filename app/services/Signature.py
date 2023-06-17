class CustomSignature(object):
    """Sign given SOAP envelope with WSSE sig using given key and cert."""
    def __init__(self, wsse_list):
        self.wsse_list = wsse_list

    def apply(self, envelope, headers):
        for wsse in self.wsse_list:
            envelope, headers = wsse.apply(envelope, headers)
        return envelope, headers

    def verify(self, envelope):
        pass
