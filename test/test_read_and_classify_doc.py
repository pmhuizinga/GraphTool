import pandas as pd
from py2neo import Graph
import spacy
from spacy.matcher import PhraseMatcher
import itertools
import logging

logger = logging.getLogger(__name__)  # initialize logger
logger.handlers = []
c_handler = logging.StreamHandler()  # Create handlers
c_format = logging.Formatter('%(levelname)s - %(message)s')
c_handler.setFormatter(c_format)  # Create formatters and add it to handlers
logger.addHandler(c_handler)  # Add handlers to the logger
logger.setLevel(logging.INFO)

# set spacy properties
nlp = spacy.load("en_core_web_sm")
# use 'lower' to create case insensitive matches
matcher = PhraseMatcher(nlp.vocab, attr="LOWER")

graph = Graph(host="localhost", port=7687, auth=('neo4j', 'admin'))

txt = "Aegon asset management is part of aegon"
txt = """
Thanks Simon

It would also be useful to see examples of the different flavours of daily reports currently sent to the client(s) as well as the number of clients who currently receive these on a daily basis.

Mike

From: Moss, Simon - INV <smoss3@aegonam.com> 
Sent: 28 March 2022 12:14
To: Lee, Alan <alan.c.lee@blackrock.com>; Ritchie, Mike <Mike.Ritchie@blackrock.com>; Woodhead, David <david.woodhead@blackrock.com>; Connolly, Stephen <stephen.connolly@blackrock.com>
Cc: Harker, Steve <steve.harker@aegonam.com>; Huizinga, Paul <huizinga.p@aegonam.com>; Eisenhart, Jennifer <jeisenha@aegonam.com>
Subject: RE: ADC / ACR - Technical Discussion [EXTERNAL]

External Email: Use caution with links and attachments
All – please see internal review and questions on the “Transaction” reporting implementation within ACR.
I will caveat this as “draft” as our Dual triage remains ongoing. Also thought it best to get you this ASAP so quality can be appropriately considered within the go-live deliberations.

I would appreciate an Ack from one of the BR recipients and will send a separate email to confirm. Some concern that zips might not be getting through.

Simon

From: Moss, Simon - INV 
Sent: 15 March 2022 09:27
To: Lee, Alan <alan.c.lee@blackrock.com>; Ritchie, Mike <Mike.Ritchie@blackrock.com>; Woodhead, David <david.woodhead@blackrock.com>; Connolly, Stephen <stephen.connolly@blackrock.com>
Cc: Harker, Steve <steve.harker@aegonam.com>; Huizinga, Paul <huizinga.p@aegonam.com>; Eisenhart, Jennifer <jeisenha@aegonam.com>
Subject: RE: ADC / ACR - Technical Discussion [EXTERNAL]

Gents, 
I’m distributing this as an early draft as I’d appreciate your feedback on whether it is going to be enough to drive the technical conversations we need to have.
Within the zip you will find examples of the components referenced in the word doc and the sql used within the GEM Views.

If this will suffice then we’ll extend to a couple of other examples which draw out other facets of the Data challenges across ACR and ADC.
•	Active Analytics – requires a non-trivial wire up of accounting positions to investment index analytics in ADC to approximate consistency with the Gem datasets.
•	Transactions – includes a brittle and verbose Transaction Types transformation in the GEM View SQL.

Additional comments:
1.	The attached includes requirements to report prelim and daily holdings as consistently as possible with the closed period publication from Aladdin Accounting. Direction we received from Ashish was that the daily AA Balance Sheet should support this, but this requires non-trivial logic to achieve an approximation to the AA Pos Analytics. Further advice will be required on this. I’d also like to understand whether this could be achieved within ACR (previous advice was that is could not) and if not why not.
2.	One of the aggravating factors for the teams in querying the ADC data is that the definitions in Aladdin Studio are incomplete. I’ve previously raised this with Gurps, but haven’t got a response.
E.g. for AA_POS….
 
 

Please feedback ASAP and we’ll then get additional material over to you in the next couple of days and agree a schedule for technical follow-up.

Simon

From: Lee, Alan <alan.c.lee@blackrock.com> 
Sent: 11 March 2022 02:03
To: Moss, Simon - INV <smoss3@aegonam.com>
Cc: Ritchie, Mike <Mike.Ritchie@blackrock.com>; Harker, Steve <steve.harker@aegonam.com>; Woodhead, David <david.woodhead@blackrock.com>
Subject: Re: ADC / ACR - Technical Discussion [EXTERNAL]

Simon, 
It was Sam who mentioned APIs, but it was framed as a possible technical option once we better understand #3.  I believe #2 and #3 are definitely connected in trying to understand your client reporting leaf of your decision tree and how the population of reports flowed through it.  

I know that Steve was willing to share the tree; you all have obviously put a lot of thought into this.  I am definitely interested in studying it further before our next meeting.  

Alan
Sent from my iPhone

On Mar 9, 2022, at 4:43 PM, Moss, Simon - INV <smoss3@aegonam.com> wrote:
 
External Email: Use caution with links and attachments
Gents, 
I hope I’ve distilled the various points we covered earlier.
 
1.	RAFT needs to ensure it has implementation processes in place that effectively drive down EUC retention and maximise on platform tool adoption. This needs to be done in a way that embeds good practice and knowledge within the firm in order to maintain and improve levels of platform adoption and not regress to EUC solutions.
2.	Steve’s decision flow had, as I recall it, a leaf in every branch that required access to data through Snowflake. I think this is ultimately realistic and AAM’s data\architecture strategy needs to enable this, supported by Aladdin’s evolving data platform.
3.	There is a “here and now” problem for Client Reporting and reporting more generally where we need to confirm we have a solution we can stand behind and communicate how this will evolve through the programme and into the future. This solution needs to enable increased adoption of ACR and drive down need for non-ACR reporting.
4.	The firm’s roadmap includes enhanced digital engagement with clients. This should inform the direction taken in responding to 2 and 3over the near to medium term, but is not a primary consideration for what we do within RAFT through to M3.
 
I believe this group (+ a few others) need to drive forward on 3 and to some extent 2. I personally don’t think these two items should be fully divorced as in combination they talk directly to the data governance concerns that have been a constant thread in our discussions.
 
The approach outlined earlier in this email thread still stands. Let’s identify a small sample of things we have already done for the US across ACR and non-ACR (ADC) reporting and collaborate on a reference design and implementation.  I believe the current action on this sits with me to elaborate requirements to sufficient detail in order to support a meaningful technical discussion. Can we target this for next Wednesday?
 

As a PPS – Alan, I don’t know whether it was you or Sam that mentioned APIs. I know some of your competitors have APIs on top of their platforms to support controlled and robust access to [near] real-time data. If this is on your roadmap and Steve isn’t already aware a discussion might be warranted.
 
Simon
 
From: Moss, Simon - INV 
Sent: 09 March 2022 14:54
To: Ritchie, Mike <Mike.Ritchie@blackrock.com>; Harker, Steve <steve.harker@aegonam.com>
Cc: Lee, Alan <alan.c.lee@blackrock.com>
Subject: RE: ADC / ACR - Technical Discussion [EXTERNAL]
 
Afternoon Mike, 
Not sure of which meeting today you are referring to. I have nothing in my diary. Which is fine as I am rammed supporting US Dual testing. As a result I will not be able to input further in to the below activity until next week.
 
On the decision tree piece – Paul Huizinger (reports to Steve) is on point on this. He is getting the same question from multiple directions and is due to have something out in a few days.
 
Simon
 
From: Ritchie, Mike <Mike.Ritchie@blackrock.com> 
Sent: 09 March 2022 14:49
To: Moss, Simon - INV <smoss3@aegonam.com>; Harker, Steve <steve.harker@aegonam.com>
Cc: Lee, Alan <alan.c.lee@blackrock.com>
Subject: RE: ADC / ACR - Technical Discussion [EXTERNAL]
 
Good afternoon gents
 
Checking if we missed the “Decision Tree” ahead of today’s meeting.  For the call today, it would be useful to understand the options in the decision tree and some examples that fall into the categories where the Aladdin suite is not meeting your expectations.  As we discussed last time, we will then be able to specifically target where to focus our collective efforts (e.g. should we be building out ACR more aggressively to mitigate the need for users to have to go into ADC).
 
Let’s review this on the call today if possible.
 
Thanks
Mike
 
 
From: Moss, Simon - INV <smoss3@aegonam.com> 
Sent: 03 March 2022 21:49
To: Harker, Steve <steve.harker@aegonam.com>; Payne, Angel <apayne@aegonam.com>; Ritchie, Mike <Mike.Ritchie@blackrock.com>; Lee, Alan <alan.c.lee@blackrock.com>; Tubiello, Sam <sam.tubiello@blackrock.com>; Connolly, Stephen <stephen.connolly@blackrock.com>; Gary Logan <glogan@uk.ey.com>; Gururaja, Anitha <AGururaja@aegonam.com>
Subject: RE: ADC / ACR - Technical Discussion
 
External Email: Use caution with links and attachments
Brief write-up to limited audience from our earlier session. Please feedback any comments\omissions. 
 
Exec Summary
It was recognised that discussion should focus on challenges to Milestone 1 and Milestone 2-3 rather than strategic platform roadmap.
Follow-up required for strategic concerns.
 
Milestone 1
1.	We need to understand scope of the remaining internal report development still outstanding for M1. (action :Angel 2022-03-04)
2.	It was not considered viable to attempt to deliver reporting artefacts from ACR in the time remaining.
3.	Next steps: 
a.	Resource plan for closing skills gap required for remaining work if querying from ADC required and considered a remaining AAM gap.
b.	Refine and collectively agree "definition of done" that must include consideration of DQ Assurance.
c.	Detailed plan based on size\complexity of remaining work (consider confirmation of business need, target state confirmation, better Requirements)
•	SM Note : Steve has separately agreed that in the short-term a user run query out of Snowflake would be acceptable for "extract" use cases. This would avoid the need for Power BI dev (but not SQL).
•	SM Note : The "Extract" deliverables in ACR were introduced as part of user training provided today by BRS. Is it worth exploring if this provides any easy wins?
 
Milestone 2
1.	Agreed that we should look at a delivered US report and explore how this might be done in a way that addresses concerns raised and shared by both AAM and BRS. 
a.	Define Reference Design and Reference Implementation.
b.	Qualify\quantify potential debt against strategic implementation.
2.	AAM to share Decision Tree for target state reporting. (action :Simon 2022-03-04)
 
Proposed workshops
Ref	Description	When 	Objective	Inputs	AAM Contributors	BRS Contributors
1	Milestone 1 Internal Reporting backlog review and planning	ASAP	Joint view on how best to deliver remaining extract \ reporting components.	Backlog (inc good description of business need)	Anitha Gururaja
Angel Payne
Steve Harker (delegate)	TBC
2	Milestone 2 reference implementation review	w\c 2022-03-07	Define reference design and implementation for known report.
 	Candidate report	Jenn Eisenhart
Steve Harker (delegate)
Simon Moss	TBC
3	Strategic roadmap review	April 2022	Review of BRS Data Platform roadmap and playback of M1 and M2  design closeout.	 	Nicole Sandig
Steve Harker
Angel Payne
Gary Logan
Anitha Gururaja
Simon Moss	TBC
 
 
 
-----Original Appointment-----
From: Harker, Steve <steve.harker@aegonam.com> 
Sent: 01 March 2022 09:20
To: Harker, Steve; Tavernier, Sebastien; Malik, Sanjeev; Payne, Angel; Moss, Simon - INV; Ritchie, Mike; alan.c.lee@blackrock.com; Tubiello, Sam; david.woodhead@blackrock.com; lindsey.pedrotty@blackrock.com; Daniel.Gourvitch@blackrock.com; daniel.kallas@blackrock.com; Paul.Gallant@blackrock.com; Love, Marcia; Brothers, Eric; Lam, Talent; Elbaz, Ben; Licata, Brian; Connolly, Stephen
Cc: Gary Logan; Sandig, Nicole; Gururaja, Anitha; paul.conroy@blackrock.com
Subject: ADC / ACR - Technical Discussion
When: 03 March 2022 17:00-18:00 (UTC+00:00) Dublin, Edinburgh, Lisbon, London.
Where: Microsoft Teams Meeting
 
Placeholder for meeting on Thursday. Proposed agenda as follows:
 
Introductions
Aladdin target vision for ADC / ACR unification
•	[BRS] present end state vision and convergence with ADC as the single unified date store
•	[BRS] present major milestones and approach to convergence
•	[BRS] propose ongoing partnership interaction model with AAM 
 
Review general observations of challenges identified
•	[JOINT] Discuss examples from Phase 1 reporting using AAM presentation as baseline
•	[AAM] Highlight new Phase 2 use cases, both known and anticipated
•	[JOINT] Agree approach to efficiently govern phase 2 process 
 
What is going to prevent us from going live with Phase 2?
•	[AAM] Present critical and high dependencies and concerns required for phase 2 go live
•	[JOINT] Agree follow-up actions and materials for meeting with CTO and COO following week
 
Kind regards
Steve
________________________________________________________________________________ 
Microsoft Teams meeting 
Join on your computer or mobile app 
Click here to join the meeting 
Join with a video conferencing device 
453426348@teamsconnect.aegon.com 
Video Conference ID: 123 887 981 0 
Alternate VTC instructions 
**Never use Teams Meeting Chat to discuss any PII or Sensitive Aegon/Transamerica information** 
Learn More | Meeting options 
________________________________________________________________________________ 
 
CONFIDENTIALITY: This message and accompanying documents are intended only for use by the individual or entity to which they are addressed and may contain information that is privileged, confidential, or exempt from disclosure under applicable law. If the reader of this document is not the intended recipient, you are hereby notified you are strictly prohibited from reading, disseminating, distributing, or copying this communication. If you have received this document in error, please notify sender immediately and destroy the original transmission. 

Archiving Notice: Recipients should be aware that all emails exchanged with sender are automatically archived and may be accessed at any time by duly authorized persons and may be produced to other parties, including public authorities, in compliance with applicable laws. 

Information about our data privacy and collection practices is available on our websites for Aegon Asset Management NA and Equitable AgriFinance.
' 
 
This message may contain information that is confidential or privileged. If you are not the intended recipient, please advise the sender immediately and delete this message. See http://www.blackrock.com/corporate/compliance/email-disclaimers for further information.  Please refer to http://www.blackrock.com/corporate/compliance/privacy-policy for more information about BlackRock’s Privacy Policy.

BlackRock Advisors (UK) Limited and BlackRock Investment Management (UK) Limited are authorised and regulated by the Financial Conduct Authority. Registered in England No. 796793 and No. 2020394 respectively. BlackRock Life Limited is authorised by the Prudential Regulation Authority and regulated by the Financial Conduct Authority and the Prudential Regulation Authority. Registered in England No. 2223202. Registered Offices: 12 Throgmorton Avenue, London EC2N 2DL. BlackRock International Limited is authorised and regulated by the Financial Conduct Authority and is a registered investment adviser with the Securities and Exchange Commission (SEC). Registered in Scotland No. SC160821. Registered Office: Exchange Place One, 1 Semple Street, Edinburgh EH3 8BL.

For a list of BlackRock's office addresses worldwide, see http://www.blackrock.com/corporate/about-us/contacts-locations.

© 2022 BlackRock, Inc. All rights reserved.
________________________________________
Please note: This message originated outside your organization. Please use caution when opening links or attachments.
Associate of BlackRock Investments, LLC (“BRIL”) and/or BlackRock Execution Services, both members FINRA/SIPC. The iShares Funds and BlackRock Mutual Funds are distributed by BRIL. For current prospectuses for iShares products, go to www.ishares.com/prospectus. For current prospectuses for BlackRock Mutual Fund products, go to https://www.blackrock.com/us/individual/resources/regulatory-documents/mutual-funds.

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
    # remove space after comma
    nodename = nodename.replace(", ", ",")
    query = "match (n:{})-[:has_alias]-(a:alias) where a.name = '{}' return n.name as name".format(nodetype, nodename)
    logger.debug('nodetype: {}, nodename: {}'.format(nodetype,nodename))
    logger.debug('result: {}'.format(graph.run(query).data()[0]['name']))

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
    get entiaties and entity typing from text
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

print('found known entities')
[print(x) for x in x]
print(60*'-')
print('found unknown entities')
[print(y) for y in y]
