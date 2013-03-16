from BeautifulSoup import BeautifulSoup
import urllib2
import codecs
import re
import os
import sys, string
import urllib




if len(sys.argv) < 2:
    sys.stderr.write('Usage: python <this_file>.py <lesson_text_version_url> \n')
    sys.exit(1)
else:
        url = sys.argv[1]

urllib.urlretrieve(url, 'tmp.txt')

fileString = open('tmp.txt', 'r').read()

#get the title
output = re.sub('\n', '', fileString)
title = output[output.find("<title>")+7:output.find("</title>")]
#print title


#nuke the text
output = re.sub('(.*?)<h1>Key Vocabulary</h1>', '<h1>Key Vocabulary</h1>', output)
output = re.sub('(.*?)<h1>Key Vocabulary</h1><table>', '<h1>Key Vocabulary</h1><table id="keyVocabTable">', output)
output = re.sub('<h1>Supplementary Vocabulary</h1><table>', '<h1>Supplementary Vocabulary</h1><table id="supplementaryVocabTable">', output)
output = re.sub('</body></html>', '', output)

output = re.sub('<span style="font-style:italic;">', '', output)
output = re.sub('</span>', '', output)


'''
fout = open("tmp.txt", 'w')
fout.write('<title>'+title+'</title>')
fout.write(output)
fout.close

#print output


#convert to pleco format
response = urllib2.urlopen('file:///home/steve/dev/bitbucket/pleco-card-generator/tmp.txt')

html = response.read()

'''
html = output
soup = BeautifulSoup(html)

#tag = soup.table
#print(tag)

#title
fileString = open('tmp.txt', 'r').read()
title = fileString[fileString.find("<title>")+7:fileString.find("</title>")]
title = re.sub('Advanced - ', 'Advanced/', title)
title = re.sub('Upper Intermediate - ', 'Upper Intermediate/', title)
title = re.sub('Intermediate - ', 'Intermediate/', title)
title = re.sub('Elementary - ', 'Elementary/', title)
title = re.sub('Newbie - ', 'Newbie/', title)

#print "----------------------" + title

records = [] # store all of the records in this list

#key vocab
keyVocabTableObj = soup.find("table", {"id" : "keyVocabTable"})
for row in keyVocabTableObj.findAll('tr'):
    col = row.findAll('td')
    hanzi = col[0].string.strip()
    pinyin = col[1].string.strip()
    definition = col[2].string
    record = '%s\t%s\t%s' % (hanzi, pinyin, definition) # store the record with a tab between hanzi and pinyin and definition
    #print record
    records.append(record)

#supplementary vocab
supplementaryVocabTableObj = soup.find("table", {"id" : "supplementaryVocabTable"})
for row in supplementaryVocabTableObj.findAll('tr'):
    col = row.findAll('td')
    hanzi = col[0].string.strip()
    pinyin = col[1].string.strip()
    definition = col[2].string
    record = '%s\t%s\t%s' % (hanzi, pinyin, definition) # store the record with a tab between hanzi and pinyin and definition
    #print record
    records.append(record)

#print records

#output
filename = re.sub('/', '-', title)

fl = codecs.open('cards/'+filename+'.txt', 'wb', 'utf8')
fl.write('//' + title + u'\r\n');
line = '\n'.join(records)
fl.write(line + u'\r\n')
fl.close()

os.remove('tmp.txt')