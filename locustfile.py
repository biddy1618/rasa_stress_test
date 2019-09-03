from locust import HttpLocust, TaskSequence, task, seq_task
import random
import string
import resource

fauth_url = 'http://xmpp-qa.forte.kz:8089/api'
fdomain = 'xmpp-qa.forte.kz'
fpass = 'test'

resource.setrlimit(resource.RLIMIT_NOFILE, (999999, 999999))


class UserBehavior(TaskSequence):

    def on_start(self):
        self.number = self.genNumber()

    @seq_task(1)
    def send_message(self):
        self.client.request(
            method='POST', url=f'{fauth_url}/messages', auth=(f'{self.number}@{fdomain}', fpass),
            json={'to': 'fortebot@{fdomain}',  'body': '{ "type" : "text", "text" : "Привет! как дела?" }'}
        )

    @seq_task(2)
    def get_message(self):
        self.client.request(
            method='GET', url = f'{fauth_url}/messages', 
            auth=(f'{self.number}@{fdomain}', fpass),
        )
    
    def genNumber(self):
        return ''.join(random.SystemRandom().choice(string.ascii_letters + \
            string.digits) for _ in range(10))



class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    # wait_function = lambda self: random.expovariate(1)*1000
    min_wait = 2000
    max_wait = 5000