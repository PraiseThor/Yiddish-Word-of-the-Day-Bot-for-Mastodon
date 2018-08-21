from wiktionaryparser import WiktionaryParser
from mastodon import Mastodon
import json, time

# Register app - only once!
'''
Mastodon.create_app(
     'pytooterapp',
     api_base_url = 'https://botsin.space',
     to_file = 'pytooter_clientcred.secret'
)
'''

# Log in - either every time, or use persisted

mastodon = Mastodon(
    client_id = 'pytooter_clientcred.secret',
    api_base_url = 'https://botsin.space'
)
mastodon.log_in(
    'email',
    'password',
    to_file = 'pytooter_usercred.secret'
)

# Create actual API instance
mastodon = Mastodon(
    access_token = 'pytooter_usercred.secret',
    api_base_url = 'https://botsin.space'
)


def define_word(word):
	parser = WiktionaryParser()
	json_word = parser.fetch(word, 'yiddish')
	d=[]
	try:	#error handling for when wiktionaryparse returns an empty set/list
		d=json_word[0]
		return d["definitions"]
	except:
		#print("d="+str(d))
		#print(type(d))
		#print("json_word="+str(json_word))
		#print(type(json_word))
		return False
	

#happens once
word_file=open("no-nikkud-test.txt","r")
iter_file=open("counter.txt","r+")
i=int(float(iter_file.read()))
word_list=word_file.readlines()
localtime=time.localtime(time.time())


if i==len(word_list)-1: #if the program reaches the end of list, returns to the begining
	i=-1
	print(i)
	iter_file.seek(0)
	iter_file.truncate()
	iter_file.write(str(i))

while i<len(word_list)-1:
	
	i+=1
	print(i)
	word=word_list[i].strip('\n')
	iter_file.seek(0)
	iter_file.truncate()
	iter_file.write(str(i))	

	if not bool(define_word(word)):
		print("no definition for "+word)
		continue
	else:
		msg=str(localtime.tm_mon)+"/"+str(localtime.tm_mday)+" - "+define_word(word)[0]["text"]
		print(msg)
		mastodon.toot(msg)
		#print(define_word(word)[0]["partOfSpeech"])
	
		break
	break

iter_file.close()
