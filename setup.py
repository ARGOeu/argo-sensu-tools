from distutils.core import setup

NAME = "argo-sensu-tools"


def get_ver():
    try:
        for line in open(f"{NAME}.spec"):
            if "Version:" in line:
                return line.split()[1]

    except IOError:
        raise SystemExit(1)


setup(
    name=NAME,
    version=get_ver(),
    author="SRCE",
    author_email="kzailac@srce.hr",
    description="Package that contains service used for conversion of passive "
                "metrics results written in a socket into Sensu events",
    url="https://github.com/ARGOeu/argo-sensu-tools",
    package_dir={"argo_sensu_tools": "modules"},
    packages=["argo_sensu_tools"],
    data_files=[
        ("/etc/argo-sensu-tools/", ["config/argo-sensu-tools.conf"]),
        ("/usr/lib/systemd/system/", ["init/passive2sensu.service"])
    ],
    scripts=["bin/passive2sensud"]
)
