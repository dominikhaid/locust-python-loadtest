import time
from locust import HttpUser, task, between

import logging
from locust import events

import locust.stats

locust.stats.CSV_STATS_INTERVAL_SEC = 5 # default is 1 second
locust.stats.CSV_STATS_FLUSH_INTERVAL_SEC = 60 # Determines how often the data is flushed to disk, default is 10 seconds


@events.quitting.add_listener
def _(environment, **kw):
    if environment.stats.total.fail_ratio > 0.01:
        logging.error("Test failed due to failure ratio > 1%")
        environment.process_exit_code = 1
    elif environment.stats.total.avg_response_time > 200:
        logging.error("Test failed due to average response time ratio > 200 ms")
        environment.process_exit_code = 1
    elif environment.stats.total.get_response_time_percentile(0.95) > 800:
        logging.error("Test failed due to 95th percentile response time > 800 ms")
        environment.process_exit_code = 1
    else:
        environment.process_exit_code = 0




class QuickstartUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def index_page(self):
        self.client.get("/")
    
    @task(3)
    def blog(self):
        self.client.get("/blog/")

    @task(1)
    def api(self):
        self.client.get("/api/")

    #ONFIGURATION FOR A USER LOGIN
    # def on_start(self):
    #     self.client.post("/login", json={"username":"foo", "password":"bar"})
