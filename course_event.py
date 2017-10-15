import urllib2
import json
import pymysql.cursors
API_BASE="http://bartjsonapi.elasticbeanstalk.com/api"

def lambda_handler(event, context):
    if (event["session"]["application"]["applicationId"] !=
            "amzn1.ask.skill.3ff5db33-4e40-4071-925c-b0d66b4a553e"):
        raise ValueError("Invalid Application ID")
    
    if event["session"]["new"]:
        on_session_started({"requestId": event["request"]["requestId"]}, event["session"])

    if event["request"]["type"] == "LaunchRequest":
        return on_launch(event["request"], event["session"])
    elif event["request"]["type"] == "IntentRequest":
        return on_intent(event["request"], event["session"])
    elif event["request"]["type"] == "SessionEndedRequest":
        return on_session_ended(event["request"], event["session"])

def on_session_started(session_started_request, session):
    print "Starting new session."

def on_launch(launch_request, session):
    return get_welcome_response()

def on_intent(intent_request, session):
    intent = intent_request["intent"]
    intent_name = intent_request["intent"]["name"]

    if intent_name == "GetStatus":
        return get_system_status()
    elif intent_name == "GetElevators":
        return get_elevator_status()
    elif intent_name == "GetCourseNum":
        return get_course_num(intent)
    elif intent_name == "GetWhen":
        return get_when(intent)
    elif intent_name == "GetInstr":
        return get_instr(intent)
    elif intent_name == "GetSeats":
        return get_seats(intent)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")

def on_session_ended(session_ended_request, session):
    print "Ending session."
    # Cleanup goes here...

def handle_session_end_request():
    card_title = "BART - Thanks"
    speech_output = "Thank you for using the BART skill.  See you next time!"
    should_end_session = True

    return build_response({}, build_speechlet_response(card_title, speech_output, None, should_end_session))

def get_welcome_response():
    session_attributes = {}
    card_title = "BART"
    speech_output = "Welcome to the course for Department of Computer Science skill. " \
                    "You can ask me a course number from any class, or " \
                    "ask me for system status or elevator status reports."
    reprompt_text = "Please ask me a course number, " \
                    "for example what is 16950."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_system_status():
    session_attributes = {}
    card_title = "BART System Status"
    reprompt_text = ""
    should_end_session = False

    response = urllib2.urlopen(API_BASE + "/status")
    bart_system_status = json.load(response)   

    speech_output = "There are currently " + bart_system_status["traincount"] + " trains operating. "

    if len(bart_system_status["message"]) > 0:
        speech_output += bart_system_status["message"]
    else:
        speech_output += "The trains are running normally."

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_elevator_status():
    session_attributes = {}
    card_title = "BART Elevator Status"
    reprompt_text = ""
    should_end_session = False

    response = urllib2.urlopen(API_BASE + "/elevatorstatus")
    bart_elevator_status = json.load(response) 

    speech_output = "BART elevator status. " + bart_elevator_status["bsa"]["description"]

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_course_num(intent):
    session_attributes = {}
    card_title = "CourseNum"
    speech_output = "I'm not sure which course you wanted for. " \
                    "Please try again."
    reprompt_text = "I'm not sure which course you wanted for. " \
                    "Try asking about 1110 or 2110 for example."
    should_end_session = False

    if "CourseNum" in intent["slots"]:
        course_num = intent["slots"]["CourseNum"]["value"]
        card_title = "CourseNum is " + course_num.title()
        if(course_num != None):
            # Connect to the database
            connection = pymysql.connect(
                   host="uvaclasses.martyhumphrey.info",
                         user='UVAClasses',
                         password='WR6V2vxjBbqNqbts',
                         db='uvaclasses',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
            
            try:
                with connection.cursor() as cursor:
                    # Read a single record
                    sql = "SELECT `Title` FROM `CompSci1178Data` WHERE `Number`=%s"
                    cursor.execute(sql,(str(course_num)))
                    result = cursor.fetchone()
                    speech_output = "It is " + str(result['Title'])
                    reprompt_text = ""
            finally:
                connection.close()
                
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
    
def get_when(intent):
    session_attributes = {}
    card_title = "CourseNum"
    speech_output = "I'm not sure which course you wanted for. " \
                    "Please try again."
    reprompt_text = "I'm not sure which course you wanted for. " \
                    "Try asking about 1110 or 2110 for example."
    should_end_session = False

    if "CourseNum" in intent["slots"]:
        course_num = intent["slots"]["CourseNum"]["value"]
        card_title = "CourseNum is " + course_num.title()
        if(course_num != None):
            # Connect to the database
            connection = pymysql.connect(
                   host="uvaclasses.martyhumphrey.info",
                         user='UVAClasses',
                         password='WR6V2vxjBbqNqbts',
                         db='uvaclasses',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
            
            try:
                with connection.cursor() as cursor:
                    # Read a single record
                    sql = "SELECT `Days` FROM `CompSci1178Data` WHERE `Number`=%s"
                    cursor.execute(sql,(str(course_num)))
                    result = cursor.fetchone()
                    speech_output = "It is " + str(result['Days'])
                    reprompt_text = ""
            finally:
                connection.close()
                
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
    
def get_instr(intent):
    session_attributes = {}
    card_title = "CourseNum"
    speech_output = "I'm not sure which course you wanted for. " \
                    "Please try again."
    reprompt_text = "I'm not sure which course you wanted for. " \
                    "Try asking about 1110 or 2110 for example."
    should_end_session = False

    if "CourseNum" in intent["slots"]:
        course_num = intent["slots"]["CourseNum"]["value"]
        card_title = "CourseNum is " + course_num.title()
        if(course_num != None):
            # Connect to the database
            connection = pymysql.connect(
                   host="uvaclasses.martyhumphrey.info",
                         user='UVAClasses',
                         password='WR6V2vxjBbqNqbts',
                         db='uvaclasses',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
            
            try:
                with connection.cursor() as cursor:
                    # Read a single record
                    sql = "SELECT `Instructor` FROM `CompSci1178Data` WHERE `Number`=%s"
                    cursor.execute(sql,(str(course_num)))
                    result = cursor.fetchone()
                    speech_output = "It is " + str(result['Instructor'])
                    reprompt_text = ""
            finally:
                connection.close()
                
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
    
def get_seats(intent):
    session_attributes = {}
    card_title = "CourseNum"
    speech_output = "I'm not sure which course you wanted for. " \
                    "Please try again."
    reprompt_text = "I'm not sure which course you wanted for. " \
                    "Try asking about 1110 or 2110 for example."
    should_end_session = False

    if "CourseNum" in intent["slots"]:
        course_num = intent["slots"]["CourseNum"]["value"]
        card_title = "CourseNum is " + course_num.title()
        if(course_num != None):
            # Connect to the database
            connection = pymysql.connect(
                   host="uvaclasses.martyhumphrey.info",
                         user='UVAClasses',
                         password='WR6V2vxjBbqNqbts',
                         db='uvaclasses',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
            
            try:
                with connection.cursor() as cursor:
                    # Read a single record
                    sql = "SELECT `EnrollmentLimit` - `Enrollment` AS `seats` FROM `CompSci1178Data` WHERE `Number`=%s"
                    cursor.execute(sql,(str(course_num)))
                    result = cursor.fetchone()
                    if(int(result['seats']) == 1):
                        speech_output = "There is only " + str(result['seats'])
                    elif(int(result['seats']) < 1):
                        speech_output = "There is no seat at all"
                    else:
                        speech_output = "There are " + str(result['seats'])
                    
                    reprompt_text = ""
            finally:
                connection.close()
                
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        "outputSpeech": {
            "type": "PlainText",
            "text": output
        },
        "card": {
            "type": "Simple",
            "title": title,
            "content": output
        },
        "reprompt": {
            "outputSpeech": {
                "type": "PlainText",
                "text": reprompt_text
            }
        },
        "shouldEndSession": should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        "version": "1.0",
        "sessionAttributes": session_attributes,
        "response": speechlet_response
    }
