#!/usr/bin/python

def dp(x):
	print x


MODES={
	0:'Player',
	1:'Viewer',
}
class GAME():
	def __init__(self):
		self.members={}
		self.STATE=0
		self.HANDS_OK=0
	def register_member(self,mode=0):
		member_id=len(self.members.keys())
		self.members[member_id]={
					'id':member_id,
					'pos':member_id,
					'cards':0,
					'mode':mode
					}
		dp("Register Member %d as %s"%(member_id,MODES[mode]))
		return member_id
		
	def get_tasks(self,member_id):
		if not self.members.has_key(member_id):
			return ['register_member']
		else:
			member=self.members[member_id]
			if member['mode']==0:
				return getattr(self,"state"+str(self.STATE))(member)
			else:
				dp("No such mode!!! %(id)d"%member)
				return []
	def get_card(self,member_id):
		member=self.members[member_id]
		member['cards']+=1
	def check_hand(self,member_id,cards):
		import collections as cl
		member=self.members[member_id]
		if max(cl.Counter([card.get_suit() for card in cards]).values())>4 or len(cards)!=6:
			self.STATE=9999
		self.HANDS_OK+=1
		if self.HANDS_OK==len(filter(lambda x: x['mode']==0,self.members.values())):
			self.STATE=10
		
		
	def state9999(self,m):
		raise Exception("fuck you ")
	def state0(self,m):
		if m['cards']<6:
			return ['get_card']
		else:
			return ['check_hand']
	def state10(self,m):
			return ['print_status']


