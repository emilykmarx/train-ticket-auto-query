import logging
from queries import Query
from scenarios import query_and_preserve
import subprocess

def main():
  cluster_ip_cmd = 'kubectl get nodes -o \'custom-columns=:.status.addresses[0]\'.address --no-headers'
  cluster_ip = subprocess.check_output(cluster_ip_cmd, shell=True, text=True).strip()
  url = f"http://{cluster_ip}:32677"
  q = Query(url)
  # login train-ticket and store the cookies
  if not q.login():
    logging.fatal('login failed')


if __name__ == '__main__':
  main()
