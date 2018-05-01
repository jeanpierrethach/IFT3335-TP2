import re

input_file = 'interest.acl94.txt'
output_file = 'interestacl94.arff'
stoplist_file = 'stoplist-english.txt'

recorded_words = []

#stopwords = []

#with open(stoplist_file) as f:
#    stopwords = f.readlines()
#stopwords = [w.strip() for w in stopwords]

# TODO make 1,2,3 context words possible
# or just takes 3 next and prev then in weka remove by filtering

with open(input_file) as f:
    for line in f:
        if re.match("^\s*\$\$\s*$", line):
            continue

        new_line = line.rstrip('\n')
        new_line = re.sub('======================================', '', new_line)
        new_line = re.sub("interests?_", 'interest', new_line)
        new_line = new_line.split()
        
        words_tags = [l.split('/') for l in new_line if "/" in l]
        words = [re.sub("[^0-9a-zA-Z%]+", "X", p[0]) for p in words_tags]
        tags = [re.sub("[^0-9a-zA-Z%]+", "X", p[1]) for p in words_tags]

        pairs = list(zip(words, tags))
        #pairs = [p for p in pairs if p[0] not in stopwords]

        for idx, p in enumerate(pairs):
            if re.match("^interest[0-9AB]", p[0]):
                prevword = None
                prevword_2 = None
                nextword = None
                nextword_2 = None
                prevtag = None
                prevtag_2 = None
                nexttag = None
                nexttag_2 = None

                for n in range(1,3):
                    i = idx+n
                    if i > len(pairs)-1:
                        continue
                    
                    if n == 1:
                        nextword = pairs[i][0]
                        nexttag = pairs[i][1]
                    elif n == 2:
                        nextword_2 = pairs[i][0]
                        nexttag_2 = pairs[i][1]
                for n in range(1,3):
                    j = idx-n
                    if j < 0:
                        continue
                   
                    if n == 1:
                        prevword = pairs[j][0]
                        prevtag = pairs[j][1]
                    elif n == 2:
                        prevword_2 = pairs[j][0]
                        prevtag_2 = pairs[j][1]

                recorded_words.append((prevword_2, prevword, nextword, nextword_2, prevtag_2, prevtag, nexttag, nexttag_2, p[0]))
            
# Output .arff format
with open(output_file, 'w') as f:
    f.write("% interestacl94.arff")
    f.write("\n\n")
    f.write("@relation interest\n\n")
    f.write("@attribute prevword_2 String\n")
    f.write("@attribute prevword String\n")
    f.write("@attribute nextword String\n")
    f.write("@attribute nextword_2 String\n")
    f.write("@attribute prevtag_2 String\n")
    f.write("@attribute prevtag String\n")
    f.write("@attribute nexttag String\n")
    f.write("@attribute nexttag_2 String\n")
    f.write("@attribute 'Class' {'interest1', 'interest2', 'interest3', 'interest4', 'interest5', 'interest6'}\n\n")
    
    f.write("@data\n")
    for r in recorded_words:
        for v in r:
            if v == None:
                f.write("'NULL'")
                f.write(",")
            elif re.match("^interest[0-9AB]", v):
                f.write("'{}'".format(v))
            else:
                f.write("'{}'".format(v))
                f.write(",")
        f.write("\n")