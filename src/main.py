import time
import logging
import io
import queue
import threading
import asyncio

try:
    import tornado
    import tornado.web
    import tornado.websocket
except ImportError:
    raise ImportError("Install tornado, example: #pip3 install tornado")

try:
    import picamera
except ImportError:
    raise ImportError("Install picamera, example: #pip3 install picamera, are you on a Raspberry Pi?")

frames = queue.Queue(5)
connectedWsClients = []


class StreamingOutput(object):

    def __init__(self, showFPS=False):
        self._showFPS = showFPS
        self._buffer = io.BytesIO()

        # FPS
        self._count = 0
        self._stx = time.time()
        self.FPS = -1

    def _detectFPS(self):
        self._count += 1
        if self._count == 60:
            self.FPS = self._count / (time.time() - self._stx)
            logging.info("FPS: {}".format(self.FPS))
            # Reset counters
            self.count = 0
            self.stx = time.time()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):  # New Frame available
            if self._showFPS:
                self._detectFPS()
            self._buffer.truncate()
            try:
                frames.put(self._buffer.getvalue(), False)
            except queue.Full:
                logging.debug("Queue is FULL, free 1 place")
                frames.get()
                frames.task_done()
            self._buffer.seek(0)
        return self._buffer.write(buf)


def dispatcherThread():
    aloop = asyncio.new_event_loop()  # Create an async loop for the current Thread
    asyncio.set_event_loop(aloop)
    while True:
        for client in connectedWsClients:
            try:
                client.write_message(bytes(frames.get()), True)
                frames.task_done()
            except tornado.websocket.WebSocketClosedError:
                logging.info("client disconnected")
                if client in connectedWsClients:
                    connectedWsClients.remove(client)
            except:
                logging.error("exc", exc_info=True)


class WebSocket(tornado.websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True

    def open(self, *args, **kwargs):
        logging.info("Connected client")
        if self not in connectedWsClients:
            connectedWsClients.append(self)

    def close(self, code=None, reason=None):
        logging.info("client disconnected")
        if self in connectedWsClients:
            connectedWsClients.remove(self)


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )

    with picamera.PiCamera(resolution='640x480', framerate=30) as camera:
        camera.rotation = 180
        camera.start_recording(StreamingOutput(), format='mjpeg')

        th = threading.Thread(target=dispatcherThread);
        th.start()

        handlers = [(r"/ws", WebSocket), (r"/(.*)", tornado.web.StaticFileHandler, {"path": "./documentRoot",
                                                                                    "default_filename": "index.html"})]
        application = tornado.web.Application(handlers)
        application.listen(8000)

        try:
            tornado.ioloop.IOLoop.instance().start()
        except KeyboardInterrupt:
            logging.info("CTRL+C detected.")
            tornado.ioloop.IOLoop.instance().stop()
        except:
            logging.error("exc", exc_info=True)
        finally:
            camera.stop_recording()
            logging.info("Streaming Stopped.")


if __name__ == "__main__":
    main()
