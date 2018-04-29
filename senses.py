import re

file = 'interest.acl94.txt'
output_file = 'interestacl94.arff'

recorded_words = []

with open(file) as f:
    for line in f:
        if re.match("^\s*\$\$\s*$", line):
            continue

        new_line = line.rstrip('\n')
        new_line = re.sub('======================================', '', new_line)
        new_line = re.sub("interests*_", 'interest', new_line)
        new_line = new_line.split()
        
        words_tags = [l for l in new_line if "/" in l]
        words_tags = [l.split('/') for l in words_tags]
        words = [re.sub("[^0-9a-zA-Z%]+", "X", p[0]) for p in words_tags]
        tags = [re.sub("[^0-9a-zA-Z%]+", "X", p[1]) for p in words_tags]

        pairs = list(zip(words, tags))

        # TODO select 2 prev and 2 next words + tags
        # remove stopwords?
        for idx, p in enumerate(pairs):
            if re.match("^interest[0-9AB]", p[0]):
                prevword = None
                nextword = None
                prevtag = None
                nexttag = None

                if idx == 0:
                    nextidx = idx+1
                    nextword = pairs[nextidx][0]
                    nexttag = pairs[nextidx][1]
                elif idx == len(pairs)-1:
                    previdx = idx-1
                    prevword = pairs[previdx][0]
                    prevtag = pairs[previdx][1]
                else:
                    previdx = idx-1
                    prevword = pairs[previdx][0]
                    prevtag = pairs[previdx][1]
                    nextidx = idx+1
                    nextword = pairs[nextidx][0]
                    nexttag = pairs[nextidx][1]

                #print(prevword, nextword, prevtag, nexttag, p[0])
                recorded_words.append((prevword, nextword, prevtag, nexttag, p[0]))
            else:
                pass
                
# Output .arff format
with open(output_file, 'w') as f:
    f.write("% interestacl94.arff")
    f.write("\n\n")
    f.write("@relation interest\n\n")
    f.write("@attribute prevwords String\n")
    f.write("@attribute nextwords String\n")
    f.write("@attribute prevtags String\n")
    f.write("@attribute nexttags String\n")
    f.write("@attribute 'Class' {'interest1', 'interest2', 'interest3', 'interest4', 'interest5', 'interest6'}\n\n")
    
    f.write("@data\n")
    for r in recorded_words:
        for v in r:
            if v == None:
                f.write("NULL")
                f.write(",")
            elif re.match("^interest[0-9AB]", v):
                f.write(v)
            else:
                f.write(v)
                f.write(",")
        f.write("\n")
        