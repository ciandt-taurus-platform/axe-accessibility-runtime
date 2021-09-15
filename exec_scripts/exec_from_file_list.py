# Requirements
# The python script uses the running docker client to execute the image
# Therefore, it's mandatory to have a valid docker client with a valid
# connection to a docker engine

import docker
import sys
import json
import getopt


def read_url_list(path: str) -> list[str]:
    f = open(path, "r")
    return f.readlines()


def run_analysis_for_url(url: str, image_name: str):
    cli = docker.from_env()
    return cli.containers.run(
        image=image_name,
        remove=True,
        command=url)


def run_analysis_for_list(urls: list, image_name: str):
    
    result = {}
    
    for url in urls:
        output = run_analysis_for_url(url, image_name)
        output_json = json.loads(output)
        result[url] = output_json
    
    return result

def main(argv):
   
    usage_msg = "Usage: python exec_from_file_list.py -f <inputfile> -i <scanner_docker_image_name>"

    input_file = ''
    image_name = "axe-accessibility-runtime"
    try:
        opts, args = getopt.getopt(argv,"hf:i:",["file=","image="])
    except getopt.GetoptError:
        print(usage_msg)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(usage_msg)
            sys.exit()
        elif opt in ("-f", "--file"):
            input_file = arg
        elif opt in ("-i", "--image"):
            image_name = arg
    
    if input_file == "":
        print(usage_msg)
        sys.exit()
    
    urls = read_url_list(input_file)
    urls = [x.replace("\n","") for x in urls if len(x) > 1]
    data = run_analysis_for_list(urls, image_name)
    data["input_file"] = input_file
    data["scanner_image"] = image_name

    print(json.dumps(data))

if __name__ == "__main__":
   main(sys.argv[1:])