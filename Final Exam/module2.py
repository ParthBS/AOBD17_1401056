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

def getCareerPath(inp):
	json1_file = open('Candidate Profile Data/'+inp[0]+'.txt')
	json1_str = json1_file.read()

	final=[]

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
	profile=Counter(final)

	if profile.has_key('none'):
		profile.pop('none')

	if profile.has_key(''):
		profile.pop('')

	if profile.has_key('('):
		profile.pop('(')

	if profile.has_key(')'):
		profile.pop(')')
		
	return profile


inp_files = dataFiles("Candidate Profile Data")

for i in xrange(len(inp_files)):
	print '(',i,') ',inp_files[i][23:-4]

print 
inp = raw_input('Input : '),

profile = getCareerPath(inp)

cnt=0
for i in profile:
	cnt+=1
	print i,'  '
	if cnt==len(profile)/4:
		break;
