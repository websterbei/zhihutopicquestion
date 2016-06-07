import requests
import codecs
import re
from lxml import etree

topics = ["https://www.zhihu.com/topic/19566004/hot"]

header = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/50.0.2661.102 Chrome/50.0.2661.102 Safari/537.36",
"Accept-Language":"en-US,en;q=0.8",
"Cookie":"d_c0=\"AJDAVmfJ-gmPTtVW7sAIJCgxTlYAv0M8sRI=|1464228835\"; q_c1=22e751837a66479fac77504346ad3faa|1464228835000|1464228835000; _za=4d93740c-bc14-459a-94ff-c3a5b1b06540; _zap=a4f3ec44-b881-462d-85e8-e0d88d1e5e22; _xsrf=97932a122b9943954ff940a7444c4fec; l_cap_id=\"ZmRmN2RhYWU5ODAyNDE5NWI3YTA4OTFiMDIzZjA3NDc=|1464770717|8b2e4f73be4a02edfaac2c1de879187185b900ff\"; cap_id=\"ZGYzOTIyYjlmMTM3NDM5ZDk5MjI3MjI4MjA3MmJiYzk=|1464770717|fbdfdb9a47dd0546bd92021749603e7a1df62657\"; login=\"NjAyOTgyMGYxYmVlNDcwOTkyOWRiN2E3OTU0MzU0Mzg=|1464770726|6cf626673bc9779f3f0aa619aa378ffed4f876d5\"; a_t=\"2.0AACAj8wbAAAXAAAAuC12VwAAgI_MGwAAAJDAVmfJ-gkXAAAAYQJVTbctdlcA_lYEHThrwwB5eDPKc6PuovC97WtQmhO7r6UT7MuLogi5hhD2vLu1aQ==\"; z_c0=Mi4wQUFDQWo4d2JBQUFBa01CV1o4bjZDUmNBQUFCaEFsVk50eTEyVndELVZnUWRPR3ZEQUhsNE04cHpvLTZpOEwzdGF3|1464770744|593be068649d422b55e1f1e44163dc14af8e9aea; n_c=1; __utma=51854390.95921595.1464771320.1464771320.1464771320.1; __utmb=51854390.6.10.1464771320; __utmc=51854390; __utmz=51854390.1464771320.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=51854390.100-1|2=registration_date=20130606=1^3=entry_date=20130606=1"}

data = {"start":0,
"offset":0,
"_xsrf":"97932a122b9943954ff940a7444c4fec"}

def loadtopics():
	f = open('topiclist','r')
	reobj = re.compile(r'\d+')
	topiclist = []
	topicidlist = []
	for line in f.readlines():
		topiclist.append(line.replace('\n',''))
		topicidlist.append(reobj.findall(line)[0])
	f.close()
	return topiclist,topicidlist

def obtain_data_score(data):
	page = etree.HTML(data)
	data_scores = page.xpath(u"//div[@data-type='Answer']")
	return data_scores[-1].attrib.get('data-score')

def request_content(url,data_score):
	payload = data
	payload['offset'] = data_score
	#print(payload)
	content = requests.post(url,data = payload, headers = header).text
	return content


topics,topicid = loadtopics()
#print(topics)
#print(topicid)

for num in range(len(topics)):
	content = requests.get(topics[num]).text
	data_score = obtain_data_score(content)
	f = open(topicid[num],'w')
	page = etree.HTML(content)
	result = page.xpath(u"//a[@class='question_link']")
	data_scores = page.xpath(u"//div[@data-type='Answer']")
	questions = []
	for x in result:
		question = x.text + " https://www.zhihu.com"+x.attrib.get("href")
		if not questions:
			questions.append(question)
		elif question != questions[-1]:
			questions.append(question)
	for question in questions:
		f.write(question + '\n')
	while True:
	#while True:
		try:
			content = request_content(topics[num],data_score)
			print(data_score)
			page = etree.HTML((eval(content))['msg'][1].replace("\/",'/'))
			result = page.xpath(u"//a[@class='question_link']")
			data_scores = page.xpath(u"//div[@data-type='Answer']")
			questions = []
			for x in result:
				question = x.text + " https://www.zhihu.com"+x.attrib.get("href")
				if not questions:
					questions.append(question)
				elif question != questions[-1]:
					questions.append(question)
			for question in questions:
				f.write(question + '\n')
			data_score = data_scores[-1].attrib.get('data-score')
		except:
			print('Error')
			break
	f.close()