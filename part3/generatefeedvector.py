# -*- coding: utf-8 -*-
'''
Created on 2015-4-7

@author: hteng
'''
import feedparser
import re

#return RSS title and word dict.
def getwordcounts(url):
    d=feedparser.parse(url)
    wc={}
    
    for e in d.entries:
        if 'summary' in e:
            summary=e.summary
        else:
            summary=e.description
        #print "summary is %s\n" % summary 
        words=getwords(e.title+''+summary)
        #print "words is %s\n"%words
        for word in words:
            wc.setdefault(word,0)
            wc[word]+=1
    return d.feed.title, wc

def getwords(html):
    txt=re.compile(r'<[^>]+>').sub('',html)
    words=re.compile(r'[^A-Z^a-z]+').split(txt)
    return [word.lower() for word in words if word!='']


if __name__=='__main__':
    print getwordcounts('http://blog.outer-court.com/rss.xml')
    print getwordcounts('http://www.tuaw.com/rss.xml')

    apcount={}
    wordcounts={}
    feedlist=[line for line in file('feedlist_1.txt')]
    print "feedlist is %s" % feedlist
    print len(feedlist)
    for feedurl in feedlist:
        title,wc=getwordcounts(feedurl)
        print "wc is %s" % wc
        wordcounts[title]=wc
        for word,count in wc.items():
            apcount.setdefault(word,0)
            if count >= 1:
                apcount[word]+=1
    print apcount         
    wordlist=[]
    for w,bc in apcount.items():
        frac=float(bc)/len(feedlist)
        if frac>0.1 and frac < 0.5:wordlist.append(w)
    
    out=file('blogdata.txt','w')
    out.write('Blog')
    for word in wordlist:
        out.write('\t%s' % word)
    out.write('\n')
    for blog,wc in wordcounts.items():
        out.write(blog)
        for word in wordlist:
            if word in wc:out.write('\t%d' % wc[word])
            else:
                out.write('\t0')
        out.write('\n')
                
