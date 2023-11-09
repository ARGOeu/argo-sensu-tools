import logging
import os
import signal
import stat
import sys

from argo_sensu_tools.data import WebAPI
from argo_sensu_tools.events import PassiveEvents
from argo_sensu_tools.exceptions import WebAPIException
from argo_sensu_tools.sensu import Sensu


class GracefulKiller:
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, *args):
        self.kill_now = True


class FIFO:
    def __init__(
            self, fifo_path, webapi_url, webapi_token, metricprofiles,
            sensu_url, sensu_token, voname, namespace
    ):
        self.logger = logging.getLogger("argo-sensu-tools.run")
        self.fifo_path = fifo_path
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

    def _create(self):
        try:
            if not os.path.exists(self.fifo_path):
                os.mkfifo(self.fifo_path)

            else:
                if not stat.S_ISFIFO(os.stat(self.fifo_path).st_mode):
                    os.remove(self.fifo_path)
                    os.mkfifo(self.fifo_path)

        except OSError as e:
            self.logger.error(f"Error creating FIFO: {str(e)}")

    def _clean(self):
        try:
            os.remove(self.fifo_path)
            self.logger.info("Exiting...")
            sys.exit(0)

        except OSError as e:
            self.logger.error(f"Error removing FIFO: {str(e)}")
            sys.exit(2)

    def read(self):
        self._create()

        killer = GracefulKiller()

        with open(self.fifo_path) as f:
            while not killer.kill_now:
                data = f.read()

                if data:
                    try:
                        passives = PassiveEvents(
                            message=data,
                            metricprofiles=self.webapi.get_metricprofiles(),
                            voname=self.voname,
                            namespace=self.namespace
                        )

                        for event in passives.create_event():
                            self.sensu.send_event(event=event)

                    except WebAPIException as e:
                        self.logger.error(str(e))
                        self.logger.warning(
                            f"Event {data.strip()} not processed"
                        )
                        continue

            self._clean()
