class HTTPResponse:

    def __init__(self, status_code, headers, body):
        self.status_code = status_code
        self.headers = headers
        self.body = body

    @classmethod
    def from_bytes(cls, binary_data):
        data = binary_data.decode()
        headers, body = data.split("\r\n\r\n", 1)
        status_line, *header_lines = headers.split("\r\n")
        status_code = int(status_line.split(" ")[1])
        headers_dict = dict(line.split(": ", 1) for line in header_lines)
        return cls(status_code, headers_dict, body)
