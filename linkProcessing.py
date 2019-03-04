def isRedditLink(url):
    redditStart=url.lower().find("reddit.com")
    if redditStart<0:
        return False
    if redditStart>0:
        prefix = url[:redditStart]
        if len(prefix)<2:
            return False
        try:
            if prefix[:-2]!='np' and prefix[:-3]!='www' and prefix[:-3]!='old' and prefix[:-3]!='new' and prefix[:-7]!='http://' and prefix[:-8]!="https://":
                return False
        except:
            return False
    return True

def isSubLink(url):
    if not isRedditLink(url):
         return False
    redditStart=url.lower().find("reddit.com")
    return url[redditStart+10:].lower().find("/r/femradebates")==0

def isPostLink(url):
    if not isSubLink(url):
        return False
    postStart=url.lower().find("/r/femradebates")+16
    postLink=url[postStart:].lower()
    if postLink.find('comments')!=0:
        return False
    return len(postLink)>len('comments')+1

def isCommentLink(url):
    if not isPostLink(url):
        return False
    postStart=url.lower().find("/r/femradebates")+16
    if url[postStart:].count('/')!=4:
        return False

    
    