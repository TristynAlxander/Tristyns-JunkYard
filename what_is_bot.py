import praw                             # Reddit Bots
import re                               # Regex
import xml.etree.ElementTree as XML		# XML Files

# Define Constants
SUBREDDIT_LIST = ""
USERNAME = ""
PASSWORD = ""
CLIENT_ID = ""
CLIENT_SECRET = ""
USER_AGENT = 'script:Answer what-is questions users:v0.2:written by /u/'



# Misc XML
COMMAND_TAG             = "command"
EQN_NAME                = "name"
# Index XML
INDEX                   = "index.xml"
INDEX_ROOT              = "index"
INDEX_KEY               = "key"
INDEX_REF               = "file"
# Redundant XML
REDUNDANT               = "redundant.xml"
REDUNDANT_ROOT          = "index"
REDUNDANT_KEY           = "redundant_key"



def authenticate_me():
	print("Authenticating...")
	reddit = praw.Reddit(
		client_id=CLIENT_ID,
		client_secret=CLIENT_SECRET,
		password=PASSWORD,
		user_agent=USER_AGENT,
		username=USERNAME)
	print(reddit.user.me())
	return reddit

def get_question(comment):
    has_search_phrase = re.search("((what(((( is)|( are)|((')?s))(( a)|( the))?)|( a))( equation(s)? for)?)|(define))(:)?",comment)
    if(has_search_phrase):
        start_index = has_search_phrase.end()
        end_index   = comment.find("?",start_index)
        if(end_index != -1):
            return comment[start_index:end_index].strip()
        else: 
            return ""
    else:
        return ""

def latex_processor(latex):
    latex = latex.replace("^", "\^")
    latex = latex.replace("*", "\*")
    latex = latex.replace("_", "\_")
    return "[;"+latex+";]"

def i_am_a_bot(message):
    return message + "\n\n__________________________________ \n\n ^^Disclaimer: ^^I ^^am ^^a ^^bot. ^^| [^^Having ^^trouble ^^reading ^^this?](https://www.reddit.com/r/Physics/wiki/syntax) ^^| [^^Did ^^I ^^get ^^something ^^wrong?](https://www.reddit.com/message/compose?to=TrystynAlxander&subject=Incorrect%20Bot)"

def get_reply(path):
    is_equation = path[-8:]==".eqn.xml"
    is_markdown = path[-9:]==".markdown" or path[-3:]==".md"
    if(is_equation):
        equation_root_element = XML.parse(path).getroot()
        name = "# "+equation_root_element.get(EQN_NAME)+"\n\n"
        latex = latex_processor(equation_root_element[0].text)+" \n\n"
        table = "| Symbol | Math&nbsp;Object | Unit | Name | \n|--|--|--|--| \n"
        
        for var in equation_root_element[1]:
            table = table + "| "+latex_processor(var.get("symbol"))+" | "+var.get("math_object")+" | "+latex_processor(var.get("unit"))+" | "+var.get("name")+" |"
        
        return i_am_a_bot(name + latex + table)
        
    elif(is_markdown):
        with open(path,"r") as markdown:
            return markdown.read()
    else:
        print("Bad Index Reference: "+path)
        return ""
    return "reply"

reddit = authenticate_me()

print('Starting comment stream...')
for comment in reddit.subreddit(SUBREDDIT_LIST).comments(limit=100):
    
    # Non-Questions
    if comment.saved:
        continue
    question = get_question(comment.body.lower())
    if(question == ""):
#        comment.save()
        continue
    
    print("Question Found! "+question)
    # Questions
    redundant_root_element  = XML.parse(REDUNDANT).getroot()
    index_root_element      = XML.parse(INDEX).getroot()
    
    # Search Redundant Index
    index_key = ""
    for command in redundant_root_element.iter(COMMAND_TAG):
        if(command.get(REDUNDANT_KEY) == question):
            index_key = command.get(INDEX_KEY)
            #comment.save()
    
    # Search Index
    if(index_key != ""):                                                # Search Index for Redundant Key
        for index_command in index_root_element.iter(COMMAND_TAG):
            if(index_key == index_command.get(INDEX_KEY)):
                path = index_command.get(INDEX_REF)
                reply = comment.reply(get_reply(path))
    else:                                                           # Search Index for Original Key
        for index_command in index_root_element.iter(COMMAND_TAG):
            if(question == index_command.get(INDEX_KEY)):
                #comment.save()
                path = index_command.get(INDEX_REF)
                reply = comment.reply(get_reply(path))
