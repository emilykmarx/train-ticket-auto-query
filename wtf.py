import logging
from queries import Query
from scenarios import *
import subprocess
from http.client import HTTPConnection

def verbose_requests():
  # Log lots of info on http requests
  HTTPConnection.debuglevel = 1
  requests_log = logging.getLogger("requests.packages.urllib3")
  requests_log.setLevel(logging.DEBUG)
  requests_log.propagate = True

def main():
  logging.basicConfig()
  logging.getLogger().setLevel(logging.DEBUG) # I think sets it globally

  cluster_ip_cmd = 'kubectl get nodes -o \'custom-columns=:.status.addresses[0]\'.address --no-headers'
  cluster_ip = subprocess.check_output(cluster_ip_cmd, shell=True, text=True).strip()
  url = f"http://{cluster_ip}:32677"
  q = Query(url)
  # login train-ticket and store the cookies
  if not q.login():
    logging.fatal('login failed')

  query_and_preserve(q)
  query_and_pay(q)
  query_and_collect(q)
  query_and_execute(q)

if __name__ == '__main__':
  main()
