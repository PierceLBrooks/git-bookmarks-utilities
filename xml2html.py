
# Author: Pierce Brooks

import os
import sys
import xml.etree.ElementTree as xml_tree

def write(path, name, content):
	if not (os.path.isdir(path)):
		os.makedirs(path)
	full = str(os.path.join(path, name))+".html"
	try:
		handle = open(full, "wb")
		handle.write(content.encode("utf-8"))
		handle.close()
	except:
		return False
	return True

def convert(target, node, level, parent):
	content = ""
	content += "<html>"
	content += "<head>"
	content += "<title>"
	if (node.tag == "bookmarks"):
		content += "0"
	else:
		if (node.tag == "bookmark"):
			index = node.attrib["index"]
			content += index
		else:
			return False
	content += "</title>"
	content += "</head>"
	content += "</body>"
	if (node.tag == "bookmarks"):
		for child in node:
			head = ""
			tail = ""
			grands = 0
			for grand in child:
				grands += 1
			if (grands == 0):
				head = "("
				tail = ")"
			else:
				head = "&lt;"
				tail = "&gt;"
			content += "<br>&nbsp;*&nbsp;"+head+"<a href=\""
			content += child.attrib["index"]
			content += ".html\">"
			if ("name" in child.attrib):
				content += child.attrib["name"]
			else:
				if ("url" in child.attrib):
					content += child.attrib["url"]
				else:
					content += child.attrib["index"]
			content += "</a>"
			content += tail
			if not (convert(target, child, level+1, node)):
				return False
		content += "</body>"
		content += "</html>"
		if not (write(target, "0", content)):
			return False
		return True
	if not (parent == None):
		head = "("
		tail = ")"
		content += head
		content += "<a href=\""
		if ("index" in parent.attrib):
			content += parent.attrib["index"]
		else:
			content += "0"
		content += ".html\">"
		if ("name" in parent.attrib):
			content += parent.attrib["name"]
		else:
			if ("url" in parent.attrib):
				content += parent.attrib["url"]
			else:
				if ("index" in parent.attrib):
					content += parent.attrib["index"]
				else:
					content += "0"
		content += "</a>"
		content += tail
		content += "<br>"
	if ("name" in node.attrib):
		if ("url" in node.attrib):
			content += "<a href=\""
			content += node.attrib["url"]
			content += "\">"
			content += node.attrib["name"]
			content += "</a>"
		else:
			content += node.attrib["name"]
	else:
		if ("url" in node.attrib):
			content += "<a href=\""
			content += node.attrib["url"]
			content += "\">"
			content += node.attrib["url"]
			content += "</a>"
	content += "<br>"
	for child in node:
		head = ""
		tail = ""
		grands = 0
		for grand in child:
			grands += 1
		if (grands == 0):
			head = "["
			tail = "]"
		else:
			head = "&lt;"
			tail = "&gt;"
		content += "<br>&nbsp;*&nbsp;"+head+"<a href=\""
		content += child.attrib["index"]
		content += ".html\">"
		if ("name" in child.attrib):
			content += child.attrib["name"]
		else:
			if ("url" in child.attrib):
				content += child.attrib["url"]
			else:
				content += child.attrib["index"]
		content += "</a>"
		content += tail
		if not (convert(target, child, level+1, node)):
			return False
	content += "</body>"
	content += "</html>"
	if not (write(target, index, content)):
		return False
	return True

def run(source, destination):
	print(source)
	print(destination)
	tree = xml_tree.parse(source)
	base = tree.getroot()
	result = convert(destination, base, 0, None)
	return result

if (__name__ == "__main__"):
	arguments = sys.argv
	if (len(arguments) > 2):
		print(str(run(arguments[1], arguments[2])))
