import os
import re

def load_dictionary():
	with open("data/dict.txt") as f:
		dictEntries = f.readlines() 
	dictEntries = dictEntries[9:]
	return dictEntries
	
def lookup_meaning(word):
	dictEntries = load_dictionary()
	#pattern =  "^" + word + " "
	#match_pattern = re.compile(pattern)
	if(word.istitle()): # maybe Nomen
		matching = [i for i in dictEntries if i.startswith(word+" {")] 
		if(len(matching)==0):
			matching = [i for i in dictEntries if word in i] 
	else:
		matching = [i for i in dictEntries if i.startswith(word+" ")] 
		if(len(matching)==0):
			matching = [i for i in dictEntries if word+" " in i] 
		elif(len(matching)==0):
			matching = [i for i in dictEntries if word in i]
	matching_as_string = '\n'.join(matching[:5])
	#for i in matching:
		#print(i)
		
	with open("lookups.txt", "a+") as myfile:
		myfile.write(word+ "\n\t" + '\t'.join(matching[:10]))
	return matching_as_string
	
if __name__ == '__main__':
	
	out = lookup_meaning('rasant')
	print(out)
	
