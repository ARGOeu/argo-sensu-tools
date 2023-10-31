class PassiveEvents:
    def __init__(self, message, metricprofiles, voname, namespace):
        self.message = message
        self.metricprofiles = metricprofiles
        self.voname = voname
        self.namespace = namespace

    def _parse(self):
        message = self.message.split(";")
        data = {
            "hostname": message[1],
            "metric": message[2],
            "status": int(message[3]),
            "output": message[4].strip()
        }

        return data

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

    def create_event(self):
        item = self._parse()
        servicetypes = self._servicetypes4metric(item["metric"])

        events = list()

        for servicetype in servicetypes:
            entity_name = f"{servicetype}__{item['hostname']}"
            metric_name = self._metric_name(item["metric"])

            events.append({
                "entity": {
                    "entity_class": "proxy",
                    "metadata": {
                        "name": entity_name,
                        "namespace": self.namespace
                    }
                },
                "check": {
                    "output": item["output"],
                    "status": item["status"],
                    "handlers": ["publisher-handler"],
                    "metadata": {
                        "name": metric_name
                    }
                }
            })

        return events
