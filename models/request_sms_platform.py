class HTTPRequest:
    def __init__(self, method, url, headers, body):
        self.method = method
        self.url = url
        self.headers = headers
        self.body = body

    def to_bytes(self):
        headers_str = "\r\n".join([f"{k}: {v}" for k, v in self.headers.items()])
        request_line = f"{self.method} {self.url} HTTP/1.1"
        return f"{request_line}\r\n{headers_str}\r\n\r\n{self.body}".encode()
