import argparse
from DynamicChart.final import AAstock


help_doc = {
    "description": "WIP, some general stuff",
    "--url": "the target website, string, a must",
    "--headless": "Selenium webdriver with headless mode, \
        if called, the driver is running in headless mode, default False",
    "add more flags or details": "call them using this dict"
}

parser = argparse.ArgumentParser(description=help_doc["description"])
parser.add_argument("--url", action="store", required=True,
                    help=help_doc["--url"])
parser.add_argument("--headless", action="store_true",
                    help=help_doc["--headless"])
flags = parser.parse_args()


def argparse_to_dict(argparse_namespace: argparse.Namespace) -> dict:
    return vars(argparse_namespace)


def main(*args, **kwargs):
    AAstock(**kwargs)


if __name__ == "__main__":
    main(**argparse_to_dict(flags))
