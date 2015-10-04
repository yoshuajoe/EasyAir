#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#This is your Twitter Access 
access_token = "389991595-dKUVgcidmWcgoM4QKW4rt7iDJ7X1T4W71gQeA0S9"
access_token_secret = "u8NkgMpZvUGcgHqvGyHk57vlNKt0PelO5vDUPWZLPOp31"
consumer_key = "cQCwkkl0rQw7JJV1eKSs9TTft"
consumer_secret = "sGUjtns4aC5Djm6C1aQUYxGTRnb2k5A180aS423Q0K7nosi7Bx"


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
	def on_data(self, data):
		print data
		#return True
	def on_error(self, status):
		print status


if __name__ == '__main__':
	#This handles Twitter authetification and the connection to Twitter Streaming API
	l = StdOutListener()
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	stream = Stream(auth, l)
	
	#This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
	stream.filter(track=['jokowi', 'prabowo'])