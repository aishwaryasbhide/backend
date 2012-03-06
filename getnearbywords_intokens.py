import re,sys
from pprint import pprint
import nltk,urllib2
import doc_freq_class
from pprint import pprint
import doc_freq_class
from bingapi import bingapi
from global_file import getbingid
import json
import cate_mongo_specific1

original ="""The classic adventure novel, The Three Musketeers was written by Alexendre Dumas (1802 1870) and was first published in 1844. The first of three D'Artagnan romance novels, it is a story about international intrigue, assassination and political struggles in 17th century France. This is an intricate story with many plot twists and surprises. The story has many complex and interesting personalities. Among the main characters are:D'Artagnan is a young and dashing nobleman from Gascony who dreams of joining the esteemed musketeers, a force of French royal family bodyguards.

Porthos, Athos and Aramis are three musketeers who befriend D'Artagnan. They share a series of adventures.

Cardinal Richelieu is the main political rival of the King of France. It is said that he has as much power as the King.Milady de Winter is a scheming and evil seductress who was the former wife of the musketeer, Athos. She makes several attempts to kill D'Artagnan. As a teenager, she was former nun who seduced a priest and stole valuables from the church.

Felton is an English official who is seduced by Milady. He commits murder and other crimes at her request.

Rochefort is the other major antagonist of the story. He is a member of the Cardinal's body guards and an ally of Milady.

Constance is the love interest of D'Artagnan.

The story begins with D'Artagnan traveling from his home in Gascony to Paris, the headquarters of the musketeers. D'Artagnan carries a letter of recommendation addressed to captain of the musketeers. During his journey he is attacked by mysterious thieves. His money and recommendation letter are stolen and D'Artagnan is injured. He needs a period of time to recuperate before resuming his journey. He eventually arrives in Paris and meets the musketeers. Unfortunately, without his letter of recommendation the initial meeting goes poorly and D'Artagnan challenges three musketeers to a duel. The musketeers are Athos, Porthos and Aramis. As the duel begins, six of the Cardinal's guards arrive and attempt to arrest the four adversaries. The outnumbered musketeers immediately join forces with D'Artagnan and defeat the Cardinal's guards.

D'Artagnan becomes friends with his previous foes and a series of adventures follow. They recover stolen jewels that belong to the Queen of France, participate in the siege of the town of La Rochelle and engage in espionage in England, among other dangers. An arrest warrant (on false charges) is place on D'Artagnan and several attempts are made on his life. Eventually, the young D'Artagnan is brought before Cardinal Richelieu, who was impressed by his courage and integrity. The Cardinal clears D'Artagnan of all charges and instructs Rochefort to befriend the young musketeer.

The Three Musketeers is one of Alexandre Dumas'earliest works and is widely considered to be his best. Although the plot is intricate and complicated, the story is extremely popular with young people. It was originally written in French, but it translates very well into English. The story has been made into several movies, a TV series, miniseries and even a cartoon. This work was followed in the D'Artagnan trilogy by "Twenty Years After in 1845" and by "The Vicomte of Bragelonne: Ten Years Later in 1850". These sequels depict the further adventures of the four friends.

This work is highly recommended for fans of literature. It is also an excellent way to introduce young people to the joys of reading the classics.

"""
#keywords = ["Alexandre Dumas","Three Musketeers","Cardinal Richelieu"]


#getting context of the keywords
#class of neighbouring element of a keyword
class neighbour:
    def __init__(self,word):  
        self.word = word  
        self.freq_word = 0#freq of the words in document
        self.freq_together = 0# frq of that word occuring with that keyword
        self.doc_freq_obj = doc_freq_class.context()
    def find_doc_freq(self,keyword):
    	self.freq_together = self.doc_freq_obj.get_together_DF(keyword,self.word)
        print keyword,
        print self.word
        print "doc freq:" + str(self.freq_together)
        #print keyword,
        #print "    " + self.word 

#class of context vector 
#initialisation 
class document_frequency:
   def __init__(self,keyword):
       self.keyword = keyword
       self.neighbours = []
       self.cnt = 0 #number of neighbours for that keyword

   def addneighbour(self,word):
       self.neighbours.append(neighbour(word))  #append the neighbour of that keyword
       self.cnt += 1  


class getnearbywords:
    
    def __init__(self):
        print "\nHELLO"

    def scrape(self,url):
        webpage = urllib2.urlopen(sys.argv[1]).read()
    #webpage = str(webpage)
        para = re.compile('<p>(.*)</p>') #collect data in p tags and store in para object
        raw = re.findall(para , webpage)
        rawstr = ' '.join(raw)
        clean_raw = nltk.clean_html(rawstr)
        #print clean_raw
        return clean_raw
   
    def get_words_from_proximity(self,keywords,text):  #think of how to get nouns from sentence only... !!
        #create object of doc_frequency
	#search_web(keywords)
        doc_freq_obj = doc_freq_class.context()
    	
        tokens = nltk.word_tokenize(text)
        #print "tokens:"
        #print tokens
        for i in tokens:
            if i.isalnum()== False:
                tokens.remove(i)
            
        c = nltk.ConcordanceIndex(tokens, key = lambda s: s.lower())
      
        tokens_pos = nltk.pos_tag(tokens)  
        i = 5
        doc_freq = []
        df_cnt = 0

        print "keywords going to loop",
        print keywords
        for kw in keywords:
            print "keyword::::::::",
            print kw
			#split keyword not required as kw is list of strings
            #k = nltk.word_tokenize(kw)
            #print k
            
            #print "keywords in for ", 
            #print kw
            first_word = kw[0]        #1st word in keyword
            #print "first word"
            #print first_word
            keyword_len = len(kw)
            #print "LEN="+str(keyword_len)
            i = 5
            nomatch = 0
            #print "IN KWD LOOP."
            print "offset",
            print c.offsets(first_word)
            
            for offset in c.offsets(first_word):
                print kw
                j = 1
                i = 5
                #print "Keyword=",
                #print kw,
                #print " OFFSET=" + str(offset) 
                nomatch = 0
                while j < keyword_len:
                    #print "in while"
                    #print tokens[offset+j]
                    #print kw[j]
                    
                    if tokens[offset+j].lower() <> kw[j].lower():
                        #print tokens[offset+j]
                        #print k[j]
                	nomatch = 1
                       	break 
                    j = j + 1
                if nomatch == 0:
                    doc_freq.append(document_frequency(kw))
                    #print "matched kwd",
                    #print tokens[offset:offset+j-1]
                    #print tokens[offset-5:offset+5]
                    i = 5
                    while i > 0 :
                	if (offset-i) < 0:
                    	    break
                        
                    	if (tokens_pos[offset-i][1] in ["NN","NNP"]) and (tokens_pos[offset-i][1].lower() not in  nltk.corpus.stopwords.words('english')):
                       		#doc_freq_obj.get_together_DF("")
                            #print "dfcnt:" + str(df_cnt) 
                            #print "i: " + str(i)
                            doc_freq[df_cnt].addneighbour(tokens_pos[offset-i][0])
                       		
                            print tokens_pos[offset-i][0],
                            
                            #pass
                    	i = i - 1
                
                
                    print "\m/ ",
                    print kw,
                    print "\m/ ",
                    i = 1
           
                    while i < 5 :
                        if (offset+i+(keyword_len-1)) >= len(tokens):
                            break
    	
                        if (tokens_pos[offset+i+(keyword_len-1)][1] in ["NN","NNP"]) and (tokens_pos[offset+i+(keyword_len-1)][1].lower() not in  nltk.corpus.stopwords.words('english')): 
                            #pass
                            doc_freq[df_cnt].addneighbour(tokens[offset+i+(keyword_len-1)])
                            print tokens_pos[offset+i+(keyword_len-1)][0],
                
	        
                        i = i + 1
                    k = 0
                    print "\n\n"    
                    while k < doc_freq[df_cnt].cnt:
                        #doc_freq[df_cnt].neighbours[k].freq_word = fd1[context_vectors[CV_cnt].keyword]
                        doc_freq[df_cnt].neighbours[k].find_doc_freq(doc_freq[df_cnt].keyword)
                        k = k + 1

                    doc_freq[df_cnt].neighbours.sort(key=lambda x: x.freq_together, reverse=True)
                    if doc_freq[df_cnt].cnt > 5:
                        doc_freq[df_cnt].neighbours = doc_freq[df_cnt].neighbours[:5]        #take 10 neighbours with highest weight
                        doc_freq[df_cnt].cnt = 5
                    k = 0
                    #while k < doc_freq[df_cnt].cnt:
                    print "keyword: ",
                    for l in doc_freq[df_cnt].keyword: 
                        print  l,
                    print "\n"
                    print  "neighbours: ",
                    for m in doc_freq[df_cnt].neighbours:
                        print m.word,
                        print "\n"
                        #k += 1
                    
                    
                    df_cnt = df_cnt + 1
        search_web(doc_freq)




def search_web(doc_freq):    
    txt= '{"result":'
    #txt += json.dumps(doc_freq)
    txt += "}"
    print "\n\n\n"
    print txt
    return_string ='{"final_results":['
    i=0
    cate_obj = cate_mongo_specific1.categorization()
    #bing = bingapi.Bing(app_ID)
    bing = getbingid()
    print "\n\nKEYWORDS:"
    film =" "
    books=" "
    people = " "
    location =" "
    for l in doc_freq:
    	
        str1 = ' '.join(l.keyword)
        print "keyword:" + str1

    	category = cate_obj.get_category(str1) #get category of keyword
    	print category
	
        for n in l.neighbours:
            str1 = str1 + " " + n.word
        
	search_query = str1
        print "search_query::::::::" + str1

        #for neighbour in df.neighbours:
        #    print neighbour.word
        #    search_query = search_query + neighbour.word + " "

	
	if "film" in category:
		
		#if c is "film":
            print "\n\n in film:"
            film = cate_obj.search_film(search_query)
            print film
	if "books" in category:
            books = cate_obj.search_books(search_query)
        if "people" in category:
            people = cate_obj.search_people(search_query)
        if "location" in category:
            location = cate_obj.search_location(search_query)
	
		
       # else:
        #    film ="empty"
        
            
        res = bing.do_web_search(search_query)
        dump_res = json.dumps({"keyword":search_query,"category":category,"search_res":res["SearchResponse"]["Web"]["Results"],"film":film,"books":books,"people":people,"location":location}) 
        return_string += dump_res + ","
    return_string +='{"test":"dummy_res"}' #Add dummy result for comma after last result
    return_string += "]}"

   
    #return_string ='{"final_results":['
    #i=0
    #bing = bingapi.Bing(app_ID)
    #bing = getbingid()
    #Getting Search results for each keywords and this loop builds json object. structure final_results:[array whr each element is {keyword:value, search_res:[arr of search res]}]
   # obj = CT()
  #  for kw in keywords:
    #    category = obj.get_category(kw)
 #       search_query = ' '.join(kw.neighbours)
#	category= "cat"
      #  res = bing.do_web_search(search_query)
     #   dump_res = json.dumps({"keyword":kw,"category":category,"search_res":res["SearchResponse"]["Web"]["Results"]}) 
    #    return_string += dump_res + ","
   # return_string +='{"test":"dummy_res"}' #Add dummy result for comma after last result
   # return_string += "]}"

    print return_string
    return return_string     
        
            
        



def main():
    print "\nIN THE MAIN"
    obj = getnearbywords()
    #text = obj.scrape(sys.argv[1])
    #print text
    obj.do_web_search()



if __name__ =="__main__":
    main()




    
