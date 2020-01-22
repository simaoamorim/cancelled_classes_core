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
            resp = json.dumps({"result": "Staying Alive!"}, indent=4)
            self.send_ok_response(resp)
        elif self.path == "/get_all":
            try:
                resp = json.dumps(db.get_all(), indent=4)
                self.send_ok_response(resp)
            except db.Error as e:
                self.send_error(http.HTTPStatus.INTERNAL_SERVER_ERROR)
                logger.error(f"Error in database: {e}")
        elif self.path.startswith("/get?"):
            try:
                query_components = dict(parse_qsl(urlparse(self.path).query))
                if query_components.__len__() == 0:
                    raise ValueError
                result = db.get_filtered(query_components)
                result.update(query_components)
                resp = json.dumps(result, indent=4)
                self.send_ok_response(resp)
            except db.Error as e:
                self.send_error(http.HTTPStatus.INTERNAL_SERVER_ERROR)
                logger.error(f"Error in database: {e}")
        elif self.path == "/delete_all":
            resp = json.dumps(db.clear(), indent=4)
            self.send_ok_response(resp)
        else:
            self.send_error(http.HTTPStatus.INTERNAL_SERVER_ERROR)
            logger.error(f"Requested path is not valid: {self.path}")

    def do_POST(self):
        if self.path == "/add":
            try:
                if self.headers.get_content_type() == "application/json":
                    length = int(self.headers['Content-Length'])
                    data = json.loads(self.rfile.read(length))
                    resp = json.dumps(db.add(data))
                    self.send_ok_response(resp)
                else:
                    self.send_error(http.HTTPStatus.BAD_REQUEST)
                    logger.error(f"Content-Type is not supported: {self.headers.get_content_type()}")
            except Exception as e:
                self.send_error(http.HTTPStatus.INTERNAL_SERVER_ERROR)
                logger.error(e)
        else:
            self.send_error(http.HTTPStatus.INTERNAL_SERVER_ERROR)
            logger.error(f"Requested path is not valid: {self.path}")

    def send_ok_response(self, data):
        self.send_response(http.HTTPStatus.OK)
        self.end_headers()
        self.wfile.write(data.encode("UTF-8"))
        self.wfile.flush()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, handle_exit_signal)
    signal.signal(signal.SIGTERM, handle_exit_signal)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.info("App started")
    db = cc_db.CancelledClassesDB("db/cancelled_classes.db")
    httpd = http.server.HTTPServer(('', 8080), RequestDispatcher)
    httpd.serve_forever()
    db.close()
    logger.info("Exiting")
