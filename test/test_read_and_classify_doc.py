import pandas as pd
from py2neo import Graph
import spacy
from spacy.matcher import PhraseMatcher
import itertools

# set spacy properties
nlp = spacy.load("en_core_web_sm")
# use 'lower' to create case insensitive matches
matcher = PhraseMatcher(nlp.vocab, attr="LOWER")

graph = Graph(host="localhost", port=7687, auth=('neo4j', 'admin'))

txt = """
Minutes and actions
AAM – Technical Design Authority
Meeting date	October 4, 2021
Venue	MS Teams
Attendees
Present highlighted


















	Steve Harker
Wouter Peters 
Monique Schurgers
Angel Payne
Carrie Olmstead
Christine Newlin
Graham Hopper
Jeroen de Lange
Katrina Stuart
Linda Nisbet
Lorri Fettkether
Nicole Sandig
Robert Hol
Ross Macleod
Sarah Tjaden
Stephen Payton-hale
Sue Haldeman, scribe
Others:
Anitha Gururaja
Bill Mehmen
Brent Kohlenberg
Doug Kennedy
Erin Baker
Gary Logan
Kathryn Burnside
Kelly Stutzman
Matt Marion
Mark Daams
Sandie Lovie
Solomon Smith
Trevor Atkinson
Ann Enneking
Katheryn Waller, guest




	

AGENDA

►	For Approval
►	Snowflake Architecture Follow Up: Intermediate State – Steve Peyton-Hale
Non-Aladdin data needed for Aladdin Client Reporting must be loaded into Aladdin Data Cloud because BRS will not have the facility to directly access AAM Snowflake Data Cloud directly available for go-live because it is subject to internal development in their systems.
Input TDA 20211004 - Aladdin Data Distribution and Reporting Intermediate State Vision.png
►	Snowflake Architecture Follow Up: Retrospective Waiver – Graham Hopper
Architecture Waiver: RAFT Data Feeds built in AWS but not using Snowflake
►	MEDM Retention Use case 2 – Erin Baker/Graham Hopper/Ross Macleod
MEDM Retention Paper
►	Areas for Discussion / AOB
►	Follow up on pricing (ASAP)


September 14, 2021 Previous Actions 
No.	ACTIONS	Who	Deadline	Status
2	On the solution for the reference and mapping tables, it is the ones not needed in MEDM, Ross will explore AWS resource opportunities, as new resources were recently added to the team. AWS solution was ruled out in the past due timeline constraints and resource issues. 	Ross	9/20/2021 extended	9/15 Ross is taking discussion to Computacenter.  Ideally on Wednesday morning, 9/22, Ross will receive a download from them.  He will provide an update then.  
10/4 Ross spoke with the Computacenter and has a follow up call tomorrow for an update.  He will prepare an update after tomorrow’s call and inform Graham.   


September 20, 2021 Previous Actions 
No.	ACTIONS	Who	Deadline	Status
1	Clarify where the non-PII non-native data sets will go.  Where will be delivered.  (Carrie - Anything that is non-PII, non-Aladdin data, we still have to put in an Aladdin data set so can be put in ADC so ACR can read.  Sarah – we need to understand if it gets moved later or stay there. )
Stephen will bring more clarity on paper on the non-native, non-PII ACR differences and Phases.  See what needs to be done for US implementation and afterwards the final state to show.  Stephen is unsure if will be in the signoff position next TDA.  We want to bring in Snowflake consultants and training as part of the Snowflake contract.  The model needs to be agreed before bringing to the TDA.
	Stephen	9/27/2021	

September 27, 2021 Previous Actions 
No.	ACTIONS	Who	Deadline	Status
1	From Nicole: Platform for access – need to design and comeup with a support model and have to fact base it because it is alot easier – can turn on and off, get reporting on it. This is exactly what we need to know in order to understand the effort and this is going to Cloud IT versus another way of logging the access.  This is an interfacing tool.  			
2	From Bill and Nicole: Timeline agreement for builds needed.	Nicole, Bill, Architecture		
3	From Nicole: Waiver requested by Bill for IT training.  (Power BI accesses.  ADC for training) 	Nicole, Bill, Architecture	ASAP	
4	From Nicole & Wouter:  Need to understand credits – Aladdin does not use the same.  Also credit calculations needed while we are still in project mode.	Architecture		
5	Create waiver(s) on what we’ve built so far and anything we say needs to continue, we create a waiver to cover.	Graham	10/4/2021	COMPLETE
6	Nicole recommended additing a note to the architecture and double check with Snowflake.  Her assumption that needs to validate is the whole replication is event based which means triggered as soon as they change something in the Data Cloud – weither a field / an event based replicates it so confirm it is an event based architecture.  She asked Stephen to check	Stephen		
7	Role based data access sort out between Nicole, Carrie and developers. 	Nicole, Ross, Bill		




New Actions
No.	ACTIONS	Who	Deadline	Status
1	Erin, Graham, Monique, and Sarah will meet and discuss what is needed to move forward on AWS pricing.   Erin will set this up.	Erin, Graham, Monique, Sarah  	10/11	



For Approval
•	Snowflake Architecture Follow Up: Intermediate State – Steve Peyton-Hale
Non-Aladdin data needed for Aladdin Client Reporting must be loaded into Aladdin Data Cloud because BRS will not have the facility to directly access AAM Snowflake Data Cloud directly available for go-live because it is subject to internal development in their systems.
•	Monique stated we need to have an intermediate approach and Steve will walk us through.  Graph Input TDA 2021104 – Aladdin Data Distribution and Reporting Intermediate State Vision was viewed.  Steve noted this is what we approved on the outline design.  Issue #2 we would make non-Aladdin data which we need for client reports available to BlackRock via inside/outside of Snowflake.  We would have the data, replicate to AWS, they can then read the data directly.  This will be in the contract but they cannot deliver on Day 1.  BlackRock explained in Aladdin Studio it does much orchestration – time needed to work out.  Steve explained further in the near term temporarily what we will need to do.
o	Discussion:
o	There are no use cases in the US for implementation.  Nicole stated Blackrock has been clear for standard, business card information on fund managers contact details, they have a business card functionality in Aladdin client reporting.  Not considered a need to using the solutions.  It should be noted will be stored in Aladdin Client Reporting.  
o	Steve pointed out Snowflake Data Cloud being replicated in AWS so can read.  BlackRock is committed to do beginning Day 1.  We are the first client in doing this.  Nicole added this is standard AWS Snowflake out of the box replication. It may take longer since they will need to turn on.  This is a process issue.
o	Solomon is scoping the penetration test now.  Nicole said from a timing perspective Aladdin Data Cloud will be available in a production like system when we sign the contact.  We sign the contract and turn on first before we can do a penetration test otherwise it will not load the data.   From a go live perspective, it means we can access that data as we build reports but should agree on the penetration tests.  We also need to lean on warranties, data protection, controls, etc. between that period.  Sarah – also another timing is the internal people getting trained.  There will be dependency on BlackRock.
•	Approval
•	Monique stated there are no further questions.  It is clear to all we have an intermediate approach and intermediate builds depending on timelines and EU requirements.  Approved. 

•	Snowflake Architecture Follow Up: Retrospective Waiver – Graham Hopper
•	Monique stated as we discussed last week, we will have a retrospective waiver on the builds currently done for US based on the new Snowflake architecture.  All viewed the 0 Architecture Waiver: RAFT Data Feeds built in AWS but not using Snowflake.  Graham stated this is not just for US based.  Waiver is to cover any piece of work with RAFT where we previously made the decision to use AWS strategy before introduced Snowflake.  He read the Question/Current Problem.  This is to allow the draft RAFT deadlines to be met.  Graham pointed out the diagrams.  As-Is State is the original agreed diagram.  He walked through Waiver State and To-Be Architecture.  This is to cover any work in order to continue.  Monique added existing links already in the program that will impact as well – US reference.   This was Graham’s action from last week’s TDA meeting.  He asked for questions.  
o	Discussion
o	Jeroen asked why waiver is shown as a major impact.  Have we translated into the business case of RAFT?  Graham responded potentially the waivers we have in place to build in Legacy and the Legacy tools we want to retire is more of a major that this.  He could change to a minor impact. Nicole stated it is minor if using AWS technology.  It would be major if using Informatica for rebuild.  
o	Sarah asked if this was still an in-project waiver. There are features (Clearwater examples) when started early for Canoe, we kept Informatica to get to an S3 bucket so go to Clearwater and planned to do during RAFT.   She asked if some is a waiver for a while not for the life of the company but for later into RAFT.   Monique responded “yes”.   The ones mentioned are those we provided the links that old Legacy technology patterns.
	Monique said these waivers were granted to use Legacy patterns.  Legacy patterns so Legacy technology.  Lorri said Graham has waivers in AWS people are working on now.  Here are those using Legacy technology and here are those using 
o	Nicole stated there should be a limit on the duration of the waivers.  Her understanding is we would do the rebuild as part of RAFT.   This means from the development side, RAFT moved in June 2022.  Monique agreed and added the waivers listed are recognized as such – features are already defined.  We are saying the future state that we indicated in those waivers is changing because we are changing towards Snowflake.  They are on the list to be dealt with in RAFT.     
o	Lorri is not in favor or removing any and having all the RAFT waivers shown.
o	Monique asked on the waiver we are now discussing, AWS versus Snowflake, do we plan to copy that waiver also within RAFT?  “Yes” was the response.  Monique - we need to discuss Sarah how to put into Jira.  Nicole believes it is a principle.  If we deliver a project, we do not deliver a project with the definition of done.  It is purely to hit go live dates.  Also noted the data governance layer (red boxes) is an add on.    
o	Monique stated it would be good to address that we discussed those use cases two weeks ago to give an idea on thinking about, likely future state will look like in certain types of use cases, not indicating we are fully complete in those use cases.  We cannot move further until we go into training and have support from consultants to verify solutions to those use cases.   
•	Approval
o	Monique asked to be complete, I assume this waiver is confirmed?  All accepted the waiver.  Approved.   


•	MEDM Retention Use case 2 – Erin Baker/Graham Hopper/Ross Macleod
•	Graham stated we agreed Use case 1 last week.  The Architecture Decision: Post-RAFT Use of Markit EDM was shown.  Do we want to agree to retain MEDM for RAFT to maintain data?  Ross has an action to look at the potential of doing in AWS and Graham is waiting for a response.  
	Ross has spoken with the Computacenter and has a follow up call tomorrow for an update.  Their indication was they have seen it done when MEDM itself was hosted in AWS and was a seamless integration but what we are asking is different.  ACTION Update:  Ross will get other solutions indicated after tomorrow’s call and prepare an update.   
o	Discussion
o	Ross also spoke just with the AWS team.  They have workarounds to get to UAT using static files.  
o	Sarah asked for clarification.  We are talking about the reference data that is not already in Markit but needs to be somewhere because BlackRock cannot manage?  Graham said “yes”.  Any sort of portfolio attributes for whatever reason, we will not be able to store in Aladdin we need to distribute them.  Carrie in the US we do not do today.  Sarah – what reference data are we trying to solve?  Are we trying to solve putting more reference data in Markit than we have today?  Graham – globally we use MEDM for quite a lot. This is whether if we should continue to do in order to support RAFT.   Sarah said continue assumes later it will go somewhere else.  Continue in a system we are going to keep – Markit US – may be a different answer.  She understands continuing for the next six months but once implemented in Aladdin, would the pattern be to be the same as the US?  
o	Nicole responded – this is about a pattern that currently exists in the EU instance of Markit.  Graham – there are reference tables used as lookups in MEDM in the EU.  MEDM is the integration layer in EU.  This is somewhere to maintain information – solutions where they need to do.  Nicole – this is to turn off one instance and turn on another.  Sarah – you have a different data flow in the EU than in the US and are not yet implemented.  Graham pointed to the graph – this is for just those done manually and spoke of different options of doing.   Monique spoke of the mapping tables that are static and said Ross was looking at alternatives for AWS if needing UI.  
o	Erin asked if this was a one-by-one review.  Knowing what we know now, could we approve these or not?  Then move forward and approve as an option?  Graham – we could approve as an option knowing we have deadlines to meet in RAFT and bring the actual use case when we know it.  
o	Carrie – our new contract is effective at the end of September/October 2022.    If we want to continue to support EU Legacy systems by using Markit EDM, we need to decide when we are beginning EU enterprise accounting and performance and also reporting how much do we need to build.  Did we contract with Markit EDM to do this in the new contract?  
o	Erin stated this is in the contract.  This is a use case.  There will be things done in the EU market today that are not going to be required because Aladdin landscape will help manage.  Approve as an option, potentially look at each use case, as we migrate to Aladdin review, to keep moving forward.  
o	Carrie – we need a business ownership conversation.  Who is the business owner to make changes and which team owns? 
o	Nicole – we need to add to the discussion with Snowflake architects to see alternate solution.  This is temporary.  Graham indicated it is on the list.  
•	Approval
•	Monique – wrap up: We recommend and approve as a solution direction but we will decide on a case by case basis since we need to double check on contracts and on effort we need to do.  The assumption is based on Ross’ conversation as a follow up, there is no alternative at this point in time in AWS.   
	Monique asked - Is this correct?  All agreed this is the conclusion for now.  Approved.  


Areas for Discussion / AOB
•	Follow up on pricing (ASAP)
•	Monique stated we still need to follow up on the ASAP pricing discussion.  She asked Erin for the exact functionalities that we need to move onto solutioning.  Erin gave an update.  
o	Erin put these together a while back and are now needed more granular.  We layered out five different requirements which she shared with Graham, Steve Harker and Steve Saperstein.  She also pulled functionality from ASAP as well to see what we would need to eliminate/enhance.  If this additional detail in needed, she will provide.  ACTION: Erin, Graham, Monique, and Sarah will meet and discuss what is needed to move forward.   Erin will set this up. 
"""

doc = nlp(txt)


def read_from_neo4j():
    """
    # todo: selection should come from the API instead of a neo query
    """
    query = "match(n)-[:has_alias]-(a) return labels(n) as nodetype, a.name as name, labels(a) as node2"
    df = pd.DataFrame.from_dict(graph.run(query).data(), orient='columns')

    return df


def get_parentnode_from_neo4j(nodetype, nodename):
    """
    description
    """
    query = "match (n:{})-[:has_alias]-(a:alias) where a.name = '{}' return n.name as name".format(nodetype, nodename)
    return graph.run(query).data()[0]['name']


def prepare_neo4j_dataframe(df):
    """
    remove alias nodes from dataframe and drop duplicates
    param df: dataframe
    return: dataframe
    """
    df.nodetype = [a[0] for a in df.nodetype]
    df.node2 = [a[0] for a in df.node2]
    df = df[df.nodetype != 'alias']
    df.drop(columns=['node2'], inplace=True)
    df.drop_duplicates(inplace=True)

    return df


def remove_duplicates_from_list(lst):
    lst.sort()
    output = list(k for k, _ in itertools.groupby(lst))
    return output


def populate_matcher(df):
    """
    description
    """
    for nodetype in df.nodetype.unique():
        df_selection = df[df.nodetype == nodetype]
        nodelist = df_selection.name.to_list()
        patterns = [nlp.make_doc(name) for name in nodelist]
        matcher.add(nodetype, patterns)


def get_entities_from_text():
    """
    get entities and entity typing from text
    """
    matches = matcher(doc)
    result_list = []
    for match_id, start, end in matches:
        rule_id = nlp.vocab.strings[match_id]
        span = doc[start:end]
        result = [rule_id, span.text.lower()]
        result_list.append(result)

    return remove_duplicates_from_list(result_list)


def get_cleansed_entities_from_text(txt):
    lst = get_entities_from_text()
    newlist = []
    for idx, item in enumerate(lst):
        new_item_name = get_parentnode_from_neo4j(item[0], item[1])
        newlist.append([item[0], new_item_name])

    return remove_duplicates_from_list(newlist)


def get_missing_entities():
    missing_entity_list = []
    existing_entity_list = df.name.to_list()
    for entity in doc.ents:
        if entity.text.lower() not in existing_entity_list:
            if entity.label_ not in ['DATE', 'TIME', 'CARDINAL', 'ORDINAL']:
                missing_entity_list.append([entity.label_, entity.text])

    return remove_duplicates_from_list(missing_entity_list)


df = read_from_neo4j()
df = prepare_neo4j_dataframe(df)
populate_matcher(df)
x = get_cleansed_entities_from_text(txt)
y = get_missing_entities()
