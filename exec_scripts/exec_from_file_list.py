import docker
import sys
import json

image_name = "axe-accessibility-runtime"


def run_analysis_for(url: str):
    cli = docker.from_env()
    return cli.containers.run(
        image=image_name,
        remove=True,
        command=url)


file_name = sys.argv[len(sys.argv) - 1]
output = run_analysis_for(file_name)
data = json.loads(output)
print(data)
