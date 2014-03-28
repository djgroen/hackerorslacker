#! /usr/bin/env python

# probably will need to install the github3 python module as is not standard
import github3
import urllib2
# import shelve

def create_github_rawurl(url):
	'''returns a URL that only displays the raw code of the file'''
	
	# reformat the URL so the URL only prints the raw code
	url = url.replace("api","raw")
	url = url.replace("github","raw.githubusercontent")
	url = url.replace("blob/","")
	
	return url

# login to GitHub (add your own USERNAME and PASSWORD here or use something a bit better..) 
gh = github3.login('USERNAME',password='PASSWORD')

# FIXME: the search assumes you have a list of users, which in the long term is inappropriate. 
users = ["apawlik", "alex-konovalov", "bmpvieira", "djgroen", "DevasenaInupakutika", "dimazest", "dorchard", "hogliux", "ninebynine", "jamespjh", "janepipistrelle", "jenshnielsen", "jure", "ktakeda1", "lgatto", "libertyf", "anthrowalla", "njall", "hainesr", "sgibb", "shoaibsufi", "steve-crouch", "npch", "Clyde", "markbasham", "jsspencer", "lingruby", "robintw"]

retrievedCode = {}
# retrievedCode = shelve.open("hacker-code-snippets.db")
counter=0

# iterate over the list of users
for user in users:

	# set up the search string
	# FIXME: this is ONLY for python at present and also assumes you have a list of users (see above). If other languages are added, different parsers will need to be added too.
	# Expect the search of GitHub will have to be narrowed somehow as just searching for all python will return too much...
	# Perhaps such by "starred" or date.
	# You can work out the search string from looking at https://github.com/search/advanced
	# Also check out http://github3py.readthedocs.org/en/latest/api.html
	searchString = "in:file language:Python user:" + user

	# search GitHub and iterate through the results (http://github3py.readthedocs.org/en/latest/search_structs.html)
	for result in gh.search_code(searchString):
	
		# reformat the GitHub URL so that it only displays the raw code
		githubURL = create_github_rawurl(result.html_url)

		try: 
			# open the raw GitHub URL
			response = urllib2.urlopen(githubURL)
			
			# read the code into a string
			code = response.read()

			# add to the dictionary (ugly index was because it was originally shelved)
			retrievedCode[str(counter)]={"code": code, "user": user}
			counter+=1

		except: 
			pass
			# raise Exception, "failed to open modified GitHub URL " + githubURL

codeSnippets = {}

# now iterate through the collected code and parse out one def 
# FIXME: would make more sense to separate this from the GitHub searching if more languages are added
for key in retrievedCode:
	
	code = retrievedCode[key]["code"]
	user = retrievedCode[key]["user"]

	# split the string on new lines so we can look line-by-line
	lines = code.split("\n")
	
	snippet = ""
	keep_going=False
	snippet_length=0
	
	# work through the code, line-by-line
	# FIXME: this will only pull out the FIRST snippet from each file, rather than fragment each file 
	for i in lines:

		# if we are collecting code..
		if keep_going:
			# ..and bump into another def, stop
			if 'def ' in i:
				break
			# ..or if we bump into the protected main code (FIXME: deal with classes and probably other declarations too)
			elif "__name__" in i:
				break
			# otherwise keep collecting a code snippet	
			else:
				snippet += i
				snippet += "\n"
				snippet_length+=1
		
		# aha, we've found a def or the protected code, so start collecting the snippet
		if ("def " in i) or ("__name__" in i):			
			snippet += i
			snippet += "\n"
			keep_going = True
			snippet_length+=1

	# only keep snippets of the "right size"
	if len(snippet)>0 and snippet_length > 7 and snippet_length < 20:

		# again using a clunky key as was setup for shelving
		codeSnippets[str(counter)] = {"user":user,"fragment":snippet}
		counter+=1
	
# just write it all to STDOUT
# FIXME: interface this with the backend database somehow.....	
print codeSnippets