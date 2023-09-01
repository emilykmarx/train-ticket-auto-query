import logging
from queries import Query
from scenarios import *
import subprocess
import json
import requests
# Makes assumptions about location of rmq go files

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO) # I think sets it globally

cluster_ip_cmd = 'kubectl get nodes -o \'custom-columns=:.status.addresses[0]\'.address --no-headers'
cluster_ip = subprocess.check_output(cluster_ip_cmd, shell=True, text=True).strip()
url = f"http://{cluster_ip}:32677"

def ticket_workflow(username, password):
  q = Query(url)

  if not q.login(username=username, password=password):
    logging.fatal('login failed')

  query_and_preserve(q)
  query_and_pay(q)
  query_and_collect(q)
  query_and_execute(q)

  # Write to rmq for logstash
  user_info = json.dumps({"user_id": q.uid})
  subprocess.check_output(f"go run wtf/rmq_publisher.go -msg='{user_info}' -json",
                          shell=True, cwd="../rabbitmq-tutorials/go", text=True)

'''
Make a bunch of users, do ticket workflow on each
'''
def main():
  word_site = "https://www.mit.edu/~ecprice/wordlist.10000"
  r = requests.get(word_site)
  if r.ok:
      words = r.text.splitlines()
      random.shuffle(words)
  else:
      logging.fatal("failed to get word list")
      return

  # TODO should probably re-login periodically like in normal_request_manager
  q_admin = Query(url)
  if not q_admin.login(username="admin", password="222222"):
    logging.fatal('login failed')

  i = 0
  n_users = 2
  while i/4 < n_users:
    username = words[i] + "_" + words[i+1]
    password = words[i+2] + "_" + words[i+3]
    q_admin.query_create_user(username=username, password=password)
    logger.info(f"created user {username}")
    i += 4
    ticket_workflow(username=username, password=password)

if __name__ == '__main__':
  main()
