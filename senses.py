import argparse
import re

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ws', 
                        default=3, type=int,
                        help='Window size (Number of preceding and following words to consider). (default: %(default)s)')
    parser.add_argument('--stopwords', 
                        action='store_true',
                        help='Boolean flag indicating if stopwords should be ignored.')
    args = parser.parse_args()
    return args

args = parse_args()

WINDOW_SIZE = args.ws

input_file = 'interest.acl94.txt'
output_file = 'interestacl94.arff' if not args.stopwords else 'interestacl94stopwords.arff'
stoplist_file = 'stoplist-english.txt'

if args.stopwords:
    stopwords = []

    with open(stoplist_file) as f:
        stopwords = f.readlines()
    stopwords = [w.strip() for w in stopwords]

recorded_words = []

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

        if args.stopwords:
            pairs = [p for p in pairs if p[0] not in stopwords]

        for idx, p in enumerate(pairs):
            if re.match("^interest[0-9AB]", p[0]):
                prev_words = [None] * WINDOW_SIZE
                next_words = [None] * WINDOW_SIZE
                prev_tags = [None] * WINDOW_SIZE
                next_tags = [None] * WINDOW_SIZE

                for n in range(1,WINDOW_SIZE+1):
                    i = idx+n
                    if i <= len(pairs)-1:
                        next_words[n-1] = pairs[i][0]
                        next_tags[n-1] = pairs[i][1]
                    j = idx-n
                    if j >= 0:
                        prev_words[n-1] = pairs[j][0]
                        prev_tags[n-1] = pairs[j][1]
                
                word_list = prev_words[::-1] + next_words + prev_tags[::-1] + next_tags
                word_list.append(p[0])
                recorded_words.append(word_list)

# Output .arff format
with open(output_file, 'w') as file:
    file.write(f"% {output_file}")
    file.write("\n\n")
    file.write("@relation interest\n\n")
    for i in range(WINDOW_SIZE, 0, -1):
        file.write(f"@attribute prevword_{i} String\n")
    for i in range(WINDOW_SIZE):
        file.write(f"@attribute nextword_{i+1} String\n")
    for i in range(WINDOW_SIZE, 0, -1):
        file.write(f"@attribute prevtag_{i} String\n")
    for i in range(WINDOW_SIZE):
        file.write(f"@attribute nexttag_{i+1} String\n")
    file.write("@attribute 'Class' {'interest1', 'interest2', 'interest3', 'interest4', 'interest5', 'interest6'}\n\n")
    
    file.write("@data\n")
    for word_list in recorded_words:
        for word in word_list:
            if word == None:
                file.write("'NULL'")
                file.write(",")
            elif re.match("^interest[0-9AB]", word):
                file.write(f"'{word}'")
            else:
                file.write(f"'{word}'")
                file.write(",")
        file.write("\n")