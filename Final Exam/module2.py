import simplejson as json
from nltk.tokenize import word_tokenize
import unicodedata
from nltk.stem import WordNetLemmatizer
from collections import Counter
import glob,os
import re, math

lemmatizer = WordNetLemmatizer()

def get_filepaths(directory):
    file_paths = []  # List which will store all of the full filepaths.

    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)  # Add it to the list.

    return file_paths  # Self-explanatory.

full_file_paths = get_filepaths("Candidate Profile Data")

final=[]														#Software Architect ,  #

for i in xrange(len(full_file_paths)):
	print i,'.) ',full_file_paths[i][23:-4]
	# print full_file_paths[i][23:-4]

print 
pro = raw_input('Input : '),

json1_file = open('Candidate Profile Data/'+pro[0]+'.txt')
json1_str = json1_file.read()


for json1_data in json.loads(json1_str):

	# json1_data = json.loads(json1_str)[i]
	# print type(json1_data['Additional-Info'])
	if isinstance(json1_data['Additional-Info'], str):
		temp = json1_data['Additional-Info']
	else:
		temp = unicodedata.normalize('NFKD', json1_data['Additional-Info']).encode('ascii','ignore')

	# print temp

	lexicon = []

	all_words = word_tokenize(temp)
	lexicon += list(all_words)

	# print lexicon

	temp=''
	li=[]
	# print lexicon
	for i in lexicon:
		# print i
		if i==',' or i=='.' or i=='\n' or i=='*' or i=='/' or i=='&' or i=='=========':
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

cnt=0
for i in profile:
	cnt+=1
	print i,'  '
	if cnt==len(profile)/4:
		#print 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
		break;





# print "Enter your json formatted resume file path: ",
# test_file = raw_input()




# ans=[]
# names=[]
# for i in profile:
# 	cnt=Counter(profile[i])
# 	ans.append([0,i])
# 	# names.append(i)
# 	for j in lexicon:
# 		for k in profile[i]:
# 			if j.lower()==k:
# 				ans[-1][0]+=cnt[k]

# ans.sort(key=lambda x:x[0], reverse=True)
# print ans[:3]
# # print names[ans.index(max(ans))]
# # for i in names:
# # 	print i
# text1 = 'myapple'
# text2 = 'applemy'

# vector1 = text_to_vector(text1)
# vector2 = text_to_vector(text2)

# cosine = get_cosine(vector1, vector2)

# print 'Cosine:', cosine