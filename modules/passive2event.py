class Passive2Event:
    def __init__(self, filename, metricprofiles, voname, namespace):
        self.filename = filename
        self.metricprofiles = metricprofiles
        self.voname = voname
        self.namespace = namespace

    def _parse(self):
        with open(self.filename, "r") as f:
            lines = f.readlines()

        lines = [line for line in lines if line.strip()]

        data = list()
        for line in lines:
            line = line.split(";")
            data.append({
                "hostname": line[1],
                "metric": line[2],
                "status": int(line[3]),
                "output": line[4].strip()
            })

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

    def _create_event(self, item):
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
                    "metadata": {
                        "name": metric_name
                    }
                },
                "pipelines": [
                    {
                        "name": "hard_state",
                        "type": "Pipeline",
                        "api_version": "core/v2"
                    }
                ]
            })

        return events
