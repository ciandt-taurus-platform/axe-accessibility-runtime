import docker
import sys
import json

image_name = "axe-accessibility-runtime"

def read_url_list(path: str) -> list[str]:
    f = open(path, "r")
    return f.readlines()


def run_analysis_for_url(url: str):
    cli = docker.from_env()
    return cli.containers.run(
        image=image_name,
        remove=True,
        command=url)


def run_analysis_for_list(urls: list):
    
    result = {}
    
    for url in urls:
        output = run_analysis_for_url(url)
        output_json = json.loads(output)
        result[url] = output_json
    
    return result

file_name = sys.argv[len(sys.argv) - 1]
urls = read_url_list(file_name)
data = run_analysis_for_list(urls)
print(data)

