from random import randint

from raven import Client

client = Client('http://634b3d6a4c084d53823626a51acb9bee:f1a1889f88f5428babafe85aa8814659@sentry.devmeter/2')


try:
    raise Exception('Random exception %s' % randint(1, 1000))
except:
        client.captureException()
