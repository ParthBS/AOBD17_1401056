import os
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import simplejson as json
import unicodedata
from collections import Counter

lemmatizer = WordNetLemmatizer()

def dataFiles(directory_name):
    inp_files = []  # List which will store all of the full filepaths.

    for d_path, directories, files in os.walk(directory_name):
        for name in files:
            # Join the two strings in order to form the full filepath.
            f_path = os.path.join(d_path, name)
            inp_files.append(f_path)  # Add it to the list.

    return inp_files

def train(profile):
	inp_files = dataFiles("Candidate Profile Data")

	for file in inp_files:
		final=[]
		if file.endswith(".txt"):
			json1_file = open(str(file))
			json1_str = json1_file.read()

			for json1_data in json.loads(json1_str):
				if isinstance(json1_data['Additional-Info'], str):
					temp = json1_data['Additional-Info']
				else:
					temp = unicodedata.normalize('NFKD', json1_data['Additional-Info']).encode('ascii','ignore')

				lexicon = []

				all_words = word_tokenize(temp)
				lexicon += list(all_words)

				temp=''
				li=[]
				for i in lexicon:
					if i==',' or i=='.' or i=='\n' or i=='*' or i=='/' or i=='&':
						li.append(temp)
						temp=''
					elif i==':' or i=='=':
						temp=''
					else:
						temp=temp+i

				if li==[]:
					lexicon = [lemmatizer.lemmatize(j) for j in lexicon]
				else:
					lexicon = [lemmatizer.lemmatize(j) for j in li]

				final.extend(lexicon)

			final = [i.lower() for i in final]
			profile[file]=Counter(final)


def test(test_file, profile):
	json_file = open(test_file)
	json_str = json_file.read()

	for json_data in json.loads(json_str):

		if isinstance(json_data['Additional-Info'], str):
			temp = json_data['Additional-Info']
		else:
			temp = unicodedata.normalize('NFKD', json_data['Additional-Info']).encode('ascii','ignore')

		lex = []

		all_words = word_tokenize(temp)
		lex += list(all_words)

		temp=''
		li=[]
		for i in lex:
			if i==',' or i=='.' or i=='\n' or i=='*' or i=='/' or i=='&':
				li.append(temp)
				temp=''
			elif i==':' or i=='=':
				temp=''
			else:
				temp=temp+i

		if li==[]:
			lex = [lemmatizer.lemmatize(j) for j in lex]
		else:
			lex = [lemmatizer.lemmatize(j) for j in li]


	ans=[]
	names=[]

	for i in profile:
		cnt=Counter(profile[i])
		ans.append([0,i])
		for j in lex:
			for k in profile[i]:
				if j.lower()==k:
					ans[-1][0]+=cnt[k]

	ans.sort(key=lambda x:x[0], reverse=True)
	return ans

test_file = raw_input("Enter Test File Path: ")

profile={}
train(profile)

ans = test(test_file,profile)

print 
print 'Career Field : ', ans[0][1]
print 
cnt=0
for i in profile[ans[0][1]]:
	cnt+=1
	print i,'  '
	if cnt==len(profile)/4:
		break;
