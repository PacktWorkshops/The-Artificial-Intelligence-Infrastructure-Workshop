import socket
import tweepy
from tweepy import OAuthHandler

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_SECRET = ''


def connect_to_twitter():
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)

    my_stream_listener = MyStreamListener()
    my_stream = tweepy.Stream(auth=api.auth, listener=my_stream_listener)

    # select a (limited) tweet stream
    my_stream.filter(track=['#AI'])
    
    
class MyStreamListener(tweepy.StreamListener):
    def on_error(self, status_code):
        if status_code == 420:
            return False

    def on_data(self, data):
        print(data)

        # send the entire tweet to the socket on localhost where pySpark is listening
        client_socket.sendall(bytes(data, encoding='utf-8'))
        return True


s = socket.socket()
s.bind(("localhost", 1234))
print("Waiting for connection...")

s.listen(1)  # wait for client connection, this should come from pySpark
client_socket, address = s.accept()  # connect to the pySpark client
print("Received request from: " + str(address))

connect_to_twitter()  # now that we have a connection to pySpark, connect to Twitter
