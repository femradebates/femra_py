
import firebase_admin
from praw.models import Comment, Submission
from praw.models import Redditor as PrawUser

from linkProcessing import isPostLink, isCommentLink

readOnlyPlaceholder=lambda: (_ for _ in ()).throw(Exception("Property is readonly"))

class Redditor:
    def __init__(self, name, db, reddit):
        self._name_=name
        self._reddit_ = reddit
        try:
            self._prawUser_ = reddit.redditor(name)
        except:
            self._prawUser_ = None
        
        self._dbData_ = db.collection("redditors").document("u"+name)
    
    @property
    def flair(self):
        return self._dbData_.get().to_dict()['flairText']
    @property
    def tier(self):
        return self._dbData_.get().to_dict()['tier']
    @tier.setter
    def tier(self,val):
        if not(4<=val<0):
            raise ValueError("Tier must be between 0 and 4")
        self._dbData_.update({'tier':val})
    
    @property
    def name(self):
        return self._name_
    @property
    def prawUser(self):
        return self._prawUser_
    
    @property
    def deletedThings(self):
        for link in self._dbData_.get().to_dict()['deletedThings']:
            if isCommentLink(link):
                yield Comment(self._reddit_,url=link)
                continue
            if isPostLink(link):
                yield Submission(self._reddit_,url=link)
                continue
            yield link

    @property
    def wasModded(self):
        """Tells whether the users has been modded _on this account_"""
        res=False
        for x in self.deletedThings:
            res=True
            break
        return res

    def addDeletedThing(self,newThing):
        currentDeletedThings=self._dbData_.get().to_dict()['deletedThings']

        if not isinstance(newThing,(str,Submission,Comment)):
            raise TypeError("Expected str, Submission, or Comment, got {}".format(type(newThing)))
        
        if isinstance(newThing,str):
            if isPostLink(newThing):
                currentDeletedThings.append(newThing)
            elif isCommentLink(newThing):
                currentDeletedThings.append(newThing)
            else:
                raise ValueError("{} is not an acceptable link".format(newThing))
        else:
            if newThing.subreddit!=self._reddit_.subreddit("femradebates"):
                raise ValueError("/r/{} is not /r/fremadebates".format(newThing.subreddit))
            currentDeletedThings.append("http://reddit.com"+newThing.permalink)
        
        self._dbData_.update({'deletedThings':currentDeletedThings})

    def __str__(self):
        res="{} is at tier {} of the ban system.".format(self.prawUser,self.tier)
        if self.wasModded:
            res+="  They were modded at the following times: "+(', '.join(self.deletedThings))
        return res
            
    


class Redditors:
    def __init__(self, db, reddit):
        self.db=db
        self.reddit=reddit
        self._userNames_=[name[1:] for name in db.collection("redditors").document('allUsers').get().to_dict()['list']]
        self._users_={}
        self._userSet_=set(self._userNames_)
    
    def __contains__(self,userName):
        return userName in self._userSet_

    def __getitem__(self,userName):
        if userName not in self._users_ and userName in self:
            self._users_[userName]=Redditor(userName,self.db,self.reddit)
        return self._users_[userName]
    
    def __iter__(self):
        for name in self.userNames:
            yield self[name]
    @property
    def userNames(self):
        for name in self._userNames_:
            yield name
    @userNames.setter
    def userNames(self,val):
        raise Exception("usernames is read-only")

    def addRedditor(self,newUser, autoApprove=True):
        if not isinstance(newUser,PrawUser):
            raise TypeError("{} is not a reddit user".format(newUser))
        uName=str(newUser)
        if autoApprove:
            self.reddit.subreddit('femradebates').contributor.add(uName)
        
        pos=0
        for i, name in enumerate(self.userNames):
            if name.lower()>uName.lower():
                pos=i
                break
        
        self._userNames_.insert(post,uName)
        self._userSet_.add(uName)
        self._users_[uName]=Redditor(uName, self.db, self.reddit)

    