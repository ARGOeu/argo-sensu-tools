import os
import socket
import threading

from argo_sensu_tools.events import PassiveEvents
from argo_sensu_tools.exceptions import SensuException
from argo_sensu_tools.sensu import Sensu


class SocketListen:
    def __init__(
            self, socket_path, metricprofiles, sensu_url, sensu_token,
            voname, namespace
    ):
        self.socket_path = socket_path
        self.metricprofiles = metricprofiles
        self.sensu = Sensu(
            url=sensu_url,
            token=sensu_token,
            namespace=namespace
        )
        self.voname = voname
        self.namespace = namespace

    def _handle_client(self, connection):
        try:
            while True:
                data = connection.recv(1024).decode("utf-8")

                if data:
                    passives = PassiveEvents(
                        message=data,
                        metricprofiles=self.metricprofiles,
                        voname=self.voname,
                        namespace=self.namespace,
                    )

                    for event in passives.create_event():
                        self.sensu.send_event(event=event)

                else:
                    break

        except Exception as e:
            print(f"Error handling client: {e}")

        except SensuException as e:
            print(f"Error sending event to Sensu backend: {e}")

        finally:
            connection.close()

    def run_server(self):
        server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            server.bind(self.socket_path)
            os.chmod(self.socket_path, 0o777)
            server.listen()

            while True:
                connection, client_address = server.accept()

                thread = threading.Thread(
                    target=self._handle_client, args=(connection,)
                )
                thread.start()

        except Exception as e:
            print(f"Error: {e}")

        finally:
            server.close()
