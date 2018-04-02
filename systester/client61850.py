import threading
import iec61850
import logging


class IECClient(threading.Thread):
    def __init__(self, ip='192.168.56.102', tcp_port=102):
        super().__init__()
        self._ip = ip
        self._tcp_port = tcp_port
        self.logger = logging.getLogger(type(self).__name__)
        self.logger.debug("client 61850 initialization")

    def run(self):
        self.logger.debug("trying to connect...")
        try:
            self._con = iec61850.IedConnection_create()
            self._timeout = iec61850.IedConnection_setConnectTimeout(
                self._con,
                2000
            )
            self._error = iec61850.IedConnection_connect(
                self._con,
                self._ip,
                self._tcp_port
            )

            if(self._error == iec61850.IED_ERROR_OK):
                self.logger.debug("connection established")
            else:
                self.logger.debug("no connection")
        except Exception as e:
            self.logger.debug("problem with connection %s", e)

    def stop(self):
        self.logger.debug("stopping iec-61850 client")
        iec61850.IedConnection_close(self._con)
        iec61850.IedConnection_destroy(self._con)

    def get_connection_state(self):
        return iec61850.IedConnection_getState(self._con)


if __name__ == "__main__":
    client = IECClient()
    client.start()
