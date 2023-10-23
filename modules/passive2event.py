class Passive2Event:
    def __init__(self, filename):
        self.filename = filename

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
