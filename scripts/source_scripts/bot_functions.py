import feedparser
import praw                             # Reddit Bots
import time
import random
import os
import sys

# Add Source Scripts to Path                                        # Add Source Scripts to Path
current_dir = os.path.dirname(os.path.realpath(__file__))+"/"       # Current Directory
source__dir = current_dir+"../source_scripts/"                      # Relative Position of Source
sys.path.insert(0, source__dir)                                     # Add to Path
# Source Imports
from str_functions import StringFunctions as str_f
from str_functions import HTMLStrParser as html_to_txt

class BotFunctions:
    DOI_KEYS = ['dc_identifier','prism_doi']
    
    def authenticate_me(bot_dict):
        try:
            print("Authenticating...")
            reddit = praw.Reddit(
                client_id       = bot_dict['client_id']     ,
                client_secret   = bot_dict['client_secret'] ,
                password        = bot_dict['password']      ,
                user_agent      = bot_dict['user_agent']    ,
                username        = bot_dict['username']      ,)
            print(reddit.user.me())
            return reddit
        except Exception as e:
            print(e)
            time.sleep(60)
        
    def print_tags(rss_link):
        [print(v) for v in feedparser.parse(rss_link)['entries'][0]]
    
    def try_submit_entries(reddit,subs,entries):
        while(len(entries) > 0):
            try:
                entry = entries.pop(random.randrange(len(entries)))                             # Pop Entry
                title = ''.join(html_to_txt(entry['title']).md_data)                            # Convert Title to Text
                title = ''.join(str_f.remove_brackets(title)[0])                                # Fix Title by Removing Brackets
                post  = reddit.subreddit(subs).submit(title, url=entry['link'],resubmit=False)  # Make Post
                print(str_f.truncate("Posted:  "+title))                                        # Print Post
                return (post,entry)                                                             # Return Post & Entry
            except praw.exceptions.APIException as e:                                           # Exceptions
                if(e.error_type == "ALREADY_SUB"):
                    print("No Reposts.")
                    continue
                if(e.error_type == "RATELIMIT"):
                    print("Rate Limit, Waiting...")
                    time.sleep(60*10)
                    print("Trying again.")
                elif(e.error_type == "DOMAIN_BANNED"):
                    print("Banned Link: "+entry['link'])
                else: 
                    print(e.error_type)
            except Exception as e:
                print("Other Exception: "+e)
        return None
        
    def try_submit_rss_links(reddit,subs,rss_links):
        while(len(rss_links) > 0):
            rss_link = random.choice(rss_links)
            rss_links.remove(rss_link)
            entries  = feedparser.parse(rss_link)['entries']
            post = BotFunctions.try_submit_entries(reddit,subs,entries)
            if(post==None):
                continue
            else:
                return post
        return None
    
    def find_entry(rss_links, title):
        for rss_link in rss_links:
            entries  = feedparser.parse(rss_link)['entries']
            for entry in entries:
                if( title in entry['title']):
                    print(entry)

    
    def has_doi_key(feed):
        has_doi_key = None
        for doi_key in BotFunctions.DOI_KEYS:
            if(doi_key in feed['entries'][0]):
                return doi_key
        return has_doi_key