import grp
import logging
import os
import pwd
import socket
import threading

from argo_sensu_tools.data import WebAPI
from argo_sensu_tools.events import PassiveEvents
from argo_sensu_tools.exceptions import WebAPIException
from argo_sensu_tools.sensu import Sensu


class SocketListen:
    def __init__(
            self, socket_path, webapi_url, webapi_token, metricprofiles,
            sensu_url, sensu_token, voname, namespace
    ):
        self.logger = logging.getLogger("argo-sensu-tools.run")
        self.socket_path = socket_path
        self.sensu = Sensu(
            url=sensu_url,
            token=sensu_token,
            namespace=namespace
        )
        self.webapi = WebAPI(
            url=webapi_url,
            token=webapi_token,
            metricprofiles=metricprofiles
        )
        self.voname = voname
        self.namespace = namespace
        self.user = "sensu"

    def _handle_client(self, connection):
        try:
            while True:
                data = connection.recv(1024).decode("utf-8")

                if data:
                    try:
                        passives = PassiveEvents(
                            message=data,
                            metricprofiles=self.webapi.get_metricprofiles(),
                            voname=self.voname,
                            namespace=self.namespace,
                        )

                        for event in passives.create_event():
                            self.sensu.send_event(event=event)

                    except WebAPIException as e:
                        self.logger.error(str(e))

                else:
                    break

        except Exception as e:
            self.logger.error(f"Error handling client: {e}")
            connection.close()

        finally:
            connection.close()

    def run_server(self):
        server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            server.bind(self.socket_path)
            os.chmod(self.socket_path, 0o777)
            try:
                uid = pwd.getpwnam(self.user).pw_uid

            except KeyError:
                self.logger.error(
                    f"Unable to change ownership on socket {self.socket_path}: "
                    f"no user named {self.user}"
                )
                server.close()

            else:
                try:
                    gid = grp.getgrnam(self.user).gr_gid

                except KeyError:
                    self.logger.error(
                        f"Unable to change group ownership on socket "
                        f"{self.socket_path}: no group named {self.user}"
                    )
                    server.close()

                else:
                    os.chown(self.socket_path, uid, gid)

                    server.listen()

                    while True:
                        connection, client_address = server.accept()

                        thread = threading.Thread(
                            target=self._handle_client, args=(connection,)
                        )
                        thread.start()

        except Exception as e:
            self.logger.error(str(e))
            server.close()

        finally:
            server.close()
