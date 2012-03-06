#TODO
#stemming
# -*- coding: utf-8 -*-
from BeautifulSoup import BeautifulSoup
import cate_mongo
import sys,re
import itertools
import urllib2,nltk
import AlchemyAPI
import getnearbywords_intokens
# Create an AlchemyAPI object.
import doc_freq_class



alchemyObj = AlchemyAPI.AlchemyAPI()


# Load the API key from disk.
alchemyObj.loadAPIKey("api_key.txt")


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

class proper_noun:


    def __init__(self):
        print "\nHELLO"

    def get_nnp_ngrams(self,original_text, highlight=5, minsize=0):
       
        #print original_text
        keywords_by_postion = []
        minsize = minsize-1
        if minsize<0:
            minsize = 0 
        tokens = nltk.wordpunct_tokenize(original_text)
        tagged = nltk.word_tokenize(original_text)
        i = 0
        for t in tagged:
        	tagged[i]=str(t)
        	i = i + 1
        	
        tagged =  nltk.pos_tag(tokens)
        #for word in tagged:
        #    print word
        doc_length = len(tokens)
        counter = 0
        counter2 = 0
        if highlight==0:
            concated_test = doc_length # This is set to doc_length but could be anything recommend 3.
        else:
            concated_test = highlight
        list_of_NNPs = []
        while counter < (doc_length-1):
            while counter2 < concated_test:
                counter2 = counter2+1
                counter3 = 0
            #print '--------------------'
                temp_array = []
                all_nnp = True
                while counter3 < counter2:
                    if counter < (doc_length-counter3):
                        #print "\ntoken getting appended"
                        #print tokens[counter+counter3],tagged[counter+counter3][1]
                        temp_array.append(tokens[counter+counter3])
                        if tagged[counter+counter3][1] != 'NNP':
                            all_nnp = False
                    counter3 = counter3+1
                #print "\nOutsied of 3rd inner loop %r"%all_nnp
                counter3 = 0
                if all_nnp == True:
                    if(len(temp_array)>minsize):
                        #print "appending: " ,
                        #print temp_array
                        list_of_NNPs.append(temp_array)
                #print 'added to main array'
            #else:
                #print 'not all NNPs'
            counter2 = 0
            counter = counter+1
       # print "outside of ALL LOOPS"
        #print list_of_NNPs
        
        #for ngram in list_of_NNPs:
        #    for i in ngram:
        #        if i.isalnum() == False:
        #            ngram.remove(i)
        import itertools
        for l in list_of_NNPs:
            str1 = ' '.join(l)
            if len(str1)< 3 or (not str1.isalnum()):
                list_of_NNPs.remove(l)
        #list_of_NNPs.sort()
        unique_NNPs = list(list_of_NNPs for list_of_NNPs,_ in itertools.groupby(list_of_NNPs))
    #for ngram in unique_NNPs:
    #   print ngram
        #discard punctuations
        unique_NNPs = self.discard_words_after_punct(unique_NNPs)
        
        #print "After puctuation removal"
        #print unique_NNPs

        #removal of duplicates
        unique_NNPs.sort()
        unique_NNPs_final = list(unique_NNPs for unique_NNPs,_ in itertools.groupby(unique_NNPs))
        unique_NNPs_final.sort()
        
        #print "\nBEFORE JOIN"
        #for ngram in unique_NNPs_final:
         #   print ngram
        

        #filter list to get max lenght n grams
        unique_NNPs_final = self.get_maxlength_ngram(unique_NNPs_final)
        unique_NNPs_final = self.remove_stopwords(unique_NNPs_final)
        unique_NNPs_final.sort()         ##for removing empty ngrams
        unique_NNPs_final = list(unique_NNPs_final for unique_NNPs_final,_ in itertools.groupby(unique_NNPs_final))
        if not unique_NNPs_final[0]:
            #print "empty"
            #print unique_NNPs_final
            del unique_NNPs_final[0:1]
            #print unique_NNPs_final
        print "Keywords:"
        print unique_NNPs_final
        
        if len(tokens)> 200:
            for kw in unique_NNPs_final:
                print "kw[0]::" + kw[0]
                indx_NNP = tokens.index(kw[0])
                #indx_NNP = indx[0]
                i=1
                flag = 0
                for i in range(len(kw)):
                    if tokens[indx_NNP+i]<> kw[i]:
                        flag = 1
                        break
                    i = i + 1
                if flag == 0:
                    if indx_NNP>0 and indx_NNP<200 :
                        keywords_by_postion.append(kw)
            print "filtered Keywords:"
            print keywords_by_postion 
            unique_NNPs_final = keywords_by_postion
            for ngram in unique_NNPs_final:
		
                for i in ngram:
                    if len(i)==1:
                        ngram.remove(i)
                if len(ngram)== 0:
                    unique_NNPs_final.remove(ngram)
		
        
        return unique_NNPs_final

    def remove_stopwords(self,unique_NNPs_final):
        
        print "\nIN STOP WORDS"
        for ngram in unique_NNPs_final:
            for i in ngram:
                if i.lower() in nltk.corpus.stopwords.words('english'):
                   # print "DETECTED"
                    ngram.remove(i)

					
        return unique_NNPs_final


    def discard_words_after_punct(self,list_of_NNPs):
        
        for ngram in list_of_NNPs:
            for i in ngram:
                if i.isalnum() == False:
                    #print "ngrams:::"
                    #print ngram
                    #print i 
                    index = ngram.index(i)
                    length = len(ngram) 
                    del ngram[index:length]
                    #print ngram
        return list_of_NNPs

    def issubstring(self,thelist,tomatch): #check whether tomatch is part of thelist        
     
        #for sublist in thelist:
            
        if all(item in thelist for item in tomatch):
            return 1
        elif all(item in tomatch for item in thelist):
            return 2
        else:
            return -1
    


    def get_maxlength_ngram(self,list_of_NNPs):

        i = k = 0
        final_list_NNPs = []
        length = len(list_of_NNPs)
#        import pdb;pdb.set_trace();
        
       
        for i in range(length-3):#******************
         
           
            return_val = self.issubstring(list_of_NNPs[i+1],list_of_NNPs[i])
            #print "value %d"%(return_val)
            inloop = 0
            #k = i
            while(self.issubstring(list_of_NNPs[i+1],list_of_NNPs[i]) == 1):
                #return_val = self.issubstring(list_of_NNPs[i+1],list_of_NNPs[i])
                #print "value %d"%(return_val)
               # k = i
                #inloop = 1
                i += 1
                
            #if inloop == 1:
            #    del list_of_NNPs[k:k+1]
            flag = 0
            for (index,nnp) in enumerate(final_list_NNPs):
            	if_sub = self.issubstring(nnp,list_of_NNPs[i])
            	if if_sub == 1:
                    flag = 1
                    break
            	if if_sub == 2:
            	    flag = 1
                    del final_list_NNPs[index]
                    final_list_NNPs.append(list_of_NNPs[i])
                else: 
                    continue       	
            	
            if(flag == 0):	
            	final_list_NNPs.append(list_of_NNPs[i])

            	
            	
            i = i + 1 
            print "\nADDED TO NEW LIST"
            print list_of_NNPs[i]
        print "\nAt the end of get_max_lenght function"
        for i in final_list_NNPs:
            print i
        
    
        return final_list_NNPs
                            

    def scrape(self,url):
        # Extract page text from a web URL (ignoring navigation links, ads, etc.).
        result = alchemyObj.URLGetText(url)
        
        soup = BeautifulSoup(result)
        raw = soup('text')
        raw = [text.text for text in raw]
        
        rawstr = ' '.join(raw)
        return rawstr
   
def main():
    obj = proper_noun()
    text = obj.scrape(sys.argv[1])
    title = alchemyObj.URLGetTitle(sys.argv[1])
    soup = BeautifulSoup(title)
    raw = soup('title')
    tokens_title_first = [str(title.text) for title in raw]
    #tokens_title = ['Three', 'Musketeers']
    print "title::",
    print tokens_title_first
    #text = original
    ### Take nouns in title
    tokens_title_first = str(tokens_title_first[0])
    print tokens_title_first
    tokens_title_temp = nltk.word_tokenize(tokens_title_first)
    tokens_title_pos = nltk.pos_tag(tokens_title_temp)
    print "tokens_title_temp::",
    print tokens_title_temp

    tokens_title = []      ##create duplicate list
    for t in tokens_title_temp:
    	index = tokens_title_temp.index(t)
        print "t::" + t
        print "index::" + str(index) 
        print "tag::" + tokens_title_pos[index][1]
        print "len" + str(len(t))
    	if (t.isalpha() and (tokens_title_pos[index][1] == "NNP") and (len(t) >= 3)):
           # tokens_title.remove(t)
            tokens_title.append(t)
    tokens_title.sort()
    tokens_title = list(tokens_title for tokens_title,_ in itertools.groupby(tokens_title))
    print "title::",
    print tokens_title 
    list_of_NNPs = obj.get_nnp_ngrams(text,5,0)
    
    #list_of_NNPs = [['Three','Musketeers'],['Alexandre', 'Dumas']]#,['Cardinal', 'Richelieu'],['Athos'],['Although'],['Porthos'] ]
    print "list of NNPs: ",
    print list_of_NNPs
    if len(list_of_NNPs)>3: ######
        list_of_NNPs = list_of_NNPs[0:3] ########
    doc_freq_obj = doc_freq_class.context()
    print "getting doc freq"
    max_df = []
    for n in list_of_NNPs:
        print "got n"
        max_freq = 0
        for t in tokens_title:
            print "got t"
            df = doc_freq_obj.get_together_DF(n,t)
            if df > max_freq:
                max_freq = df
            print "ngram:",
            print n
            print "title word:",
            print t
            print "df:",
            print df
        max_df.append(max_freq)
    i = 0
    for df in max_df:
        for i in range(len(max_df)-1):
            if max_df[i]<max_df[i+1]:
                t = list_of_NNPs[i]
                list_of_NNPs[i]=list_of_NNPs[i+1]
                list_of_NNPs[i+1]= t
                t1 = max_df[i]
                max_df[i]=max_df[i+1]
                max_df[i+1] = t1
    #i = 0
    for i in range(len(list_of_NNPs)):
        print "keyword: ",
        print list_of_NNPs[i] 
        print "df:",
        print max_df[i]
    if len(list_of_NNPs)>3:
        list_of_NNPs = list_of_NNPs[0:3]#*********
    #list_of_NNPs.sort()
    #list_of_NNPs_final = list(list_NNPs for list_NNPs,_ in itertools.groupby(list_of_NNPs))
    #list_of_NNPs_final.sort()
    print "\n\nfinal list:",
    print list_of_NNPs
    nearbywordsObj = getnearbywords_intokens.getnearbywords()
    nearbywordsObj.get_words_from_proximity(list_of_NNPs,text) 
        

      
    

if __name__ == "__main__":
    main()
