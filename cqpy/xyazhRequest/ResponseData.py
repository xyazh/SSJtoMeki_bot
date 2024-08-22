class ResponseData:
    def __init__(self, raw_response):
        self.raw_response = raw_response
        self.headers = {}
        self.body = ""
        self.status_code = 0
        self.reason_phrase = ""
        self._parseResponse()

    def _parseResponse(self):
        parts = self.raw_response.split("\r\n\r\n", 1)
        headers_part = parts[0]
        self.body = parts[1] if len(parts) > 1 else ""
        headers_lines = headers_part.split("\r\n")
        status_line = headers_lines[0]
        self._parseStatusLine(status_line)

        for header in headers_lines[1:]:
            key, value = header.split(":", 1)
            self.headers[key.strip()] = value.strip()

    def _parseStatusLine(self, status_line):
        parts = status_line.split(" ", 2)
        self.status_code = int(parts[1])
        self.reason_phrase = parts[2]

    def json(self):
        try:
            import json
            return json.loads(self.body)
        except json.JSONDecodeError:
            return None

    def __str__(self):
        return f"HTTP/{self.status_code} {self.reason_phrase}\n{self.headers}\n\n{self.body}"