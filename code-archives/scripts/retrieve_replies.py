# @author: Adithya Narayanan
# @task:  Retrieves replies to tweets posted by news org. handles from a list of conversation ids obtained from retrieve_tweets.py
# Code used heavily from TwitterAPI Examples: https://github.com/geduldig/TwitterAPI
# See sample_output/replies.csv for sample output

import pandas as pd
from TwitterAPI import TwitterAPI, TwitterOAuth, TwitterRequestError, TwitterConnectionError, TwitterPager

consumer_key= ""
consumer_secret= ""
access_token_key= ""
access_token_secret= ""


# Authotizing TwitterAPI
api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret, api_version='2')

# A Tree Data Structure that captures replies and replies of replies heirarchically
class TreeNode:
	def __init__(self, data):
		"""data is a tweet's json object"""
		self.data = data
		self.children = []

	def id(self):
		"""a node is identified by its author"""
		return self.data['author_id']

	def reply_to(self):
		"""the reply-to user is the parent of the node"""
		return self.data['in_reply_to_user_id']

	def find_parent_of(self, node):
		"""append a node to the children of it's reply-to user"""
		if node.reply_to() == self.id():
			self.children.append(node)
			return True
		for child in self.children:
			if child.find_parent_of(node):
				return True
		return False

	def print_tree(self, level):
		"""level 0 is the root node, then incremented for subsequent generations"""
		# print(f'{level*"_"}{level}: {self.id()}')
		level += 1
		for child in self.children:
			child.print_tree(level)

	def list_l1(self):
		conv_id = []
		child_id = []
		text = []
		# print(self.data['id'])
		for child in self.children:
			conv_id.append(self.data['id'])
			child_id.append(child.data['id'])
			text.append(child.data['text'])
		return conv_id, child_id, text




"""
Retrieves level 1 replies fora given conversation id
Returns lists conv_id, child_id, text tuple which shows every reply's tweet_id and text in the last two lists
"""
def retrieve_replies(conversation_id):
    try:
        # GET ROOT OF THE CONVERSATION
        r = api.request(f'tweets/:{conversation_id}',
                        {
                            'tweet.fields': 'author_id,conversation_id,created_at,in_reply_to_user_id'
                        })

        for item in r:
            root = TreeNode(item)
            # print(f'ROOT {root.id()}')

        # GET ALL REPLIES IN CONVERSATION

        pager = TwitterPager(api, 'tweets/search/recent',
                             {
                                 'query': f'conversation_id:{conversation_id}',
                                 'tweet.fields': 'author_id,conversation_id,created_at,in_reply_to_user_id'
                             })

        orphans = []

        for item in pager.get_iterator(wait=2):
            node = TreeNode(item)
            # print(f'{node.id()} => {node.reply_to()}')
            # COLLECT ANY ORPHANS THAT ARE NODE'S CHILD
            orphans = [orphan for orphan in orphans if not node.find_parent_of(orphan)]
            # IF NODE CANNOT BE PLACED IN TREE, ORPHAN IT UNTIL ITS PARENT IS FOUND
            if not root.find_parent_of(node):
                orphans.append(node)

        conv_id, child_id, text = root.list_l1()

        assert len(orphans) == 0, f'{len(orphans)} orphaned tweets'

    except TwitterRequestError as e:
        print(e.status_code)
        for msg in iter(e):
            print(msg)

    except TwitterConnectionError as e:
        print(e)

    except Exception as e:
        print(e)

    return conv_id, child_id, text


"""
Retrieves replies for a list of conversation ids (conv_ids
Returns a dataframe with columns [conv_id, child_id, text] tuple which shows every reply's tweet_id and text in the last two columns
"""
def reply_thread_maker(conv_ids):
    conv_id = []
    child_id = []
    text = []
    for id in conv_ids:
        conv_id1, child_id1, text1 = retrieve_replies(id)
        conv_id.extend(conv_id1)
        child_id.extend(child_id1)
        text.extend(text1)

    replies_data = {'conversation_id' : conv_id,
               'child_id': child_id,
               'tweet_text' : text}

    replies= pd.DataFrame(replies_data)
    return replies


### Testing Method Definitions

conv_ids = ['1349843764408414213', '1349838775967490049'] # Can replace this with conversation IDs from retrieve_tweets.py
replies = reply_thread_maker(conv_ids)
print(replies.head())

# UNCOMMENT TO WRITE TO DESIRED FILE NAME
# replies.to_csv("replies.csv")
