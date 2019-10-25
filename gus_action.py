from simple_salesforce import Salesforce

import os

GUS_ORG_ID = "00DT0000000DpvcMAC"

username = str(os.environ.get("USERNAME"))
password = str(os.environ.get("PASSWORD"))
sf = Salesforce(organizationId=GUS_ORG_ID, username=username, password=password)

GUS_ENTITY_WORK_ITEM = "ADM_Work__c"
GUD_FIELD_WORK_ID_AND_SUBJECT = "WorkId_and_Subject__c"
GUS_FIELD_STATUS = "Status__c"
GUS_FIELD_SPRINT = "Sprint__c"
SBD_11A_SPRINT = "a0lB0000001qmeYIAQ"


def update_status(work_id, new_status):
    if not work_id or len(work_id) == 0:
        return 400
    entity_id = sf.query(f"""
        SELECT Id
        FROM {GUS_ENTITY_WORK_ITEM}
        WHERE {GUD_FIELD_WORK_ID_AND_SUBJECT} LIKE '%{work_id}%'
        AND {GUS_FIELD_SPRINT} = '{SBD_11A_SPRINT}'
    """)["records"][0]["Id"]
    ret = sf.ADM_Work__c.update(entity_id, {GUS_FIELD_STATUS: new_status})
    return ret
