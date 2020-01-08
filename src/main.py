#! /usr/bin/env python3
import http.server
import json
import logging
import signal
import cc_db

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
                # TODO: format the response as expected
                result = db.get_all()
                self.send_response(http.HTTPStatus.OK)
                self.end_headers()
                self.wfile.write(result.encode("UTF-8"))
                self.wfile.flush()
            except db.Error:
                self.send_error(http.HTTPStatus.INTERNAL_SERVER_ERROR)
        elif self.path.startswith("/get?"):
            self.send_error(http.HTTPStatus.NOT_IMPLEMENTED)
        elif self.path == "/delete_all":
            self.send_error(http.HTTPStatus.NOT_IMPLEMENTED)
        else:
            self.send_error(http.HTTPStatus.INTERNAL_SERVER_ERROR)

    def do_POST(self):
        if self.path == "/add":
            self.send_error(http.HTTPStatus.NOT_IMPLEMENTED)
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
