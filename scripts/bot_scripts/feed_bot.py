# Python Imports
import sys
import os
import feedparser
import praw                             # Reddit Bots
import random
import time
import datetime

# Add Source Scripts to Path                                        # Add Source Scripts to Path
current_dir = os.path.dirname(os.path.realpath(__file__))+"/"       # Current Directory
source__dir = current_dir+"../source_scripts/"                      # Relative Position of Source
sys.path.insert(0, source__dir)                                     # Add to Path
# Source Imports
from dat_functions import DatFileDict
from dat_functions import DatFileList
from bot_functions import BotFunctions as bot
from str_functions import StringPath as path
from str_functions import StringFunctions as str_f
from str_functions import HTMLStrParser as html_to_md


# Instance Variables
bot_login_path = "/mnt/d/bot_data/feed_bot.dic.dat"
rss_links_path = "/mnt/d/bot_data/rss_links.dat"
i_am_bot_path  = "/mnt/d/bot_data/i_am_a_bot.txt"


rss_link = "http://onlinelibrary.wiley.com/rss/journal/10.1002/(ISSN)1469-896X"
entries  = feedparser.parse(rss_link)['entries']
for i in range(0,len(entries)):
    entry = entries[i]
    summary = ''.join(html_to_md(entry['summary']).md_data)                             # Convert Summary to Markdown
    a = "Abstract"
    summary = summary.split(a)[1] if len(summary.split(a))>1 else summary.split(a)[0]   # Remove Pre-Abstract
    summary = str_f.less_whitespace(summary)                                            # Remove Excess White space
    summary = str_f.truncate_over(summary)                                              # Truncate Copyright
    print(summary)






now = datetime.datetime.now().time()
today800 = now.replace(hour=6, minute=0, second=0, microsecond=0)
today1800 = now.replace(hour=18, minute=0, second=0, microsecond=0)

while(datetime.datetime.now().time() > today800 and datetime.datetime.now().time() < today1800):
    # Log in to Reddit.
    bot_login_dict = DatFileDict(bot_login_path).data
    reddit = bot.authenticate_me(bot_login_dict)

    # Submit from RSS links
    rss_links  = DatFileList(rss_links_path).data
    post_entry = bot.try_submit_rss_links(reddit,"structural",rss_links)
    if(post_entry != None):                                                                         # If Post was Made.
        
        post,entry=post_entry
        
        summary = ''.join(html_to_md(entry['summary']).md_data)                             # Convert Summary to Markdown
        a = "Abstract"
        summary = summary.split(a)[1] if len(summary.split(a))>1 else summary.split(a)[0]   # Remove Pre-Abstract
        summary = str_f.less_whitespace(summary)                                            # Remove Excess White space
        summary = str_f.truncate_over(summary)                                              # Truncate Copyright
        
        if(len(summary) > 300):                                                                     # If Summary is Proper
            comment_text = "**Summary:**\n\n>"+summary+"\n\n"+path(i_am_bot_path).file_to_str()     # Comment
            post.reply(comment_text)                                                                # 
            print("Commented")
        else:
            print("Bad Summary: "+summary)
        
    time.sleep(60*60)


# TODO: Handle Feed burnner bullshit? Maybe or just fucking not? Half these links aren't even structural.   Don't bother with this shit.
# I'd have to add a filter for [whatever]   Do this anyway. 
#http://feeds.feedburner.com/JBC_MolecularBiophysics
#http://feeds.feedburner.com/JBC_ProteinStructureAndFolding
# Figure out how to make this work
#http://emboj.embopress.org/collection/structural-biology
#http://msb.embopress.org/collection/structural-biology
# https://nsaunders.wordpress.com/2010/06/17/create-your-own-google-scholar-rss-feed/
# Add Email Alerts 

# Some Titles have <> in them need to remove that completely from titles.