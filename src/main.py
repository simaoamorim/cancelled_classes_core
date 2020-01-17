#! /usr/bin/env python3
import http.server
import json
import logging
import signal
import cc_db
from urllib.parse import urlparse, parse_qs, parse_qsl

logger = logging.Logger
httpd = http.server.HTTPServer
db = cc_db.CancelledClassesDB


def handle_exit_signal(sig, frame):
    logger.info("Shutting down the server")
    httpd.shutdown()
    httpd.server_close()


class RequestDispatcher(http.server.CGIHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(http.HTTPStatus.OK)
            self.end_headers()
            resp = {"result": "Staying Alive!"}
            self.wfile.write(json.dumps(resp, indent=4).encode("UTF-8"))
        elif self.path == "/get_all":
            try:
                result = json.dumps(db.get_all(), indent=4)
                self.send_response(http.HTTPStatus.OK)
                self.end_headers()
                self.wfile.write(result.encode("UTF-8"))
                self.wfile.flush()
            except db.Error:
                self.send_error(http.HTTPStatus.INTERNAL_SERVER_ERROR)
        elif self.path.startswith("/get?"):
            try:
                query_components = dict(parse_qsl(urlparse(self.path).query))
                if query_components.__len__() == 0:
                    raise ValueError
                result = db.get_filtered(query_components)
                result.update(query_components)
                self.send_response(http.HTTPStatus.OK)
                self.end_headers()
                self.wfile.write(json.dumps(result, indent=4).encode("UTF-8"))
            except db.Error as e:
                self.send_error(http.HTTPStatus.INTERNAL_SERVER_ERROR)
                logger.error(e)
            except ValueError:
                self.send_error(http.HTTPStatus.BAD_REQUEST)
        elif self.path == "/delete_all":
            self.send_error(http.HTTPStatus.NOT_IMPLEMENTED)
        else:
            self.send_error(http.HTTPStatus.INTERNAL_SERVER_ERROR)

    def do_POST(self):
        if self.path == "/add":
            try:
                if self.headers.get_content_type() == "application/json":
                    length = int(self.headers['Content-Length'])
                    print(json.loads(self.rfile.read(length)))
                    self.send_response(http.HTTPStatus.OK)
                    self.end_headers()
                    self.wfile.write(json.dumps({'result': 'Failure'}).encode("UTF-8"))
                else:
                    self.send_error(http.HTTPStatus.BAD_REQUEST)
            except Exception as e:
                self.send_error(http.HTTPStatus.INTERNAL_SERVER_ERROR)
                logger.error(e)
        else:
            self.send_error(http.HTTPStatus.INTERNAL_SERVER_ERROR)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, handle_exit_signal)
    signal.signal(signal.SIGTERM, handle_exit_signal)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.info("App started")
    db = cc_db.CancelledClassesDB("cancelled_classes.db")
    httpd = http.server.HTTPServer(('', 8080), RequestDispatcher)
    httpd.serve_forever()
    db.close()
    logger.info("Exiting")
