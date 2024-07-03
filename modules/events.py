import re

from argo_sensu_tools.exceptions import ArgoSensuToolsException


class PassiveEvents:
    def __init__(self, message, metricprofiles, voname, namespace, tenant):
        self.message = message
        self.metricprofiles = metricprofiles
        self.voname = voname
        self.namespace = namespace
        self.tenant = tenant

    def _parse(self):
        try:
            messages = re.sub(
                "(\[\d*\] PROCESS_SERVICE_CHECK_RESULT;)", "!!!", self.message
            )
            messages = messages.split("!!!")
            messages = [item for item in messages if item]

            data = list()
            for message in messages:
                message = message.split(";")
                data.append({
                    "hostname": message[0],
                    "metric": message[1],
                    "status": int(message[2]),
                    "output": ";".join(message[3:]).strip()
                })

            return data

        except IndexError:
            raise ArgoSensuToolsException(
                f"Error parsing message '{self.message.strip()}'"
            )

    def _metric_name(self, metric):
        if metric.endswith(f"-{self.voname}"):
            n = -(len(self.voname) + 1)
            metric = metric[:n]

        return metric

    def _servicetypes4metric(self, metric):
        metric = self._metric_name(metric)

        servicetypes = set()
        for metricprofile in self.metricprofiles:
            for service in metricprofile["services"]:
                if metric in service["metrics"]:
                    servicetypes.add(service["service"])

        return sorted(list(servicetypes))

    def create_events(self):
        data = self._parse()

        events = list()
        for item in data:
            servicetypes = self._servicetypes4metric(item["metric"])

            for servicetype in servicetypes:
                entity_name = f"{servicetype}__{item['hostname']}"
                metric_name = self._metric_name(item["metric"])

                events.append({
                    "entity": {
                        "entity_class": "proxy",
                        "metadata": {
                            "name": entity_name,
                            "namespace": self.namespace,
                            "labels": {
                                "tenants": self.tenant
                            }
                        }
                    },
                    "check": {
                        "output": item["output"],
                        "status": item["status"],
                        "handlers": [],
                        "metadata": {
                            "name": metric_name,
                            "annotations": {
                                "attempts": "2"
                            },
                            "labels": {
                                "tenants": self.tenant
                            }
                        },
                        "pipelines": [{
                            "name": "hard_state",
                            "type": "Pipeline",
                            "api_version": "core/v2"
                        }]
                    },
                    "pipelines": [{
                        "name": "hard_state",
                        "type": "Pipeline",
                        "api_version": "core/v2"
                    }]
                })

        return events
