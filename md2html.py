import re, sys

#Conver the link in md format to html format
def replace_link(md_string):
	split_link_regex = re.compile(r'[()\[\]]')
	#Split to title and url
	link_title = split_link_regex.split(md_string)[1]
	link_url = split_link_regex.split(md_string)[3]
	return r'<a href="' + link_url + r'">' + link_title + r'</a>'

#Match Headers or Paragraph markdown and convert to  html format
def match_headers(prev_line, md_string, next_line):
	#Dictionary format to store html conversion of md headers tag
	dic = {"#" : ("<h1>", "</h1>"),
		"##" : ("<h2>", "</h2>"),
		"###" : ("<h3>", "</h3>"),
		"####" : ("<h4>", "</h4>"),
		"#####" : ("<h5>", "</h5>"),
		"######" : ("<h6>", "</h6>") }
		#Match the header format
	headers_regex = re.compile(r'#{1,6}')
	match = headers_regex.match(md_string)
	#IF header the add the hearder tag as prefix and postfix of the string
	if match:
		header = match.group()
		start_index = len(header)
		return dic[header][0] + md_string[start_index:] + dic[header][1]
	#IF not header then check if it is paragaph
	else:
		#If the previous line is a newline then add a <p> tag, if the next line is a new line then add </p> tag
		prefix, postfix = r'', r''
		if  prev_line.isspace():
			prefix = r'<p>'
		if next_line.isspace() or "" == next_line :
			postfix = r'</p>'
		return prefix + md_string + postfix

#Match the link format from md file
def match_link(md_string):
	#regex for link in md format
	link_regex = re.compile(r'((\[)[^\]*]+(\])(\s)*(\()\S+(\)))')
	match = link_regex.search(md_string)
	if match:
		print match.group()
		return md_string[:match.start()] + replace_link(md_string[match.start() : match.end()]) + match_link(md_string[match.end():])
	else:
		return md_string

#Read content of markdown file and write to html file after convertion
def parse_md_file(md_file, html_file):
	file_content = md_file.readlines() #get all the lines from the md file
	list_length = len(file_content)-1
	for i in range(0, list_length+1):
		print i, list_length, file_content[i]
		#If first line
		if 0 == i:
			html_file.write(match_link(match_headers("", file_content[i], file_content[i+1])))
		#if last line
		elif list_length > i:
			html_file.write(match_link(match_headers(file_content[i-1], file_content[i], file_content[i+1])))
		#Any other line
		else:
			html_file.write(match_link(match_headers(file_content[i-1], file_content[i], "")))

def main():
	if len(sys.argv) == 3:
		md_file = open(sys.argv[1], "r") #open markdown file
		html_file = open(sys.argv[2], "w") #open html file
		if md_file:
			parse_md_file(md_file, html_file)
		md_file.close()
		html_file.close()
	else:
		print "Error : Invalid format \n Format : markdown.py <Input MD file> <Output HTML File>"

if __name__ == "__main__":
	main()
