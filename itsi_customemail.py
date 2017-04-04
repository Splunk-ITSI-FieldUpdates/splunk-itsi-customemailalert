# Copyright (C) 2005-2016 Splunk Inc. All Rights Reserved.

"""
Ping is an example of an action that can be taken programmatically on one or
more Notable Events in ITSI.

It is implemented as a Splunk Modular Alert Action.

Chunk of the logic lies in the method `execute()` where we work on one event
at a time.

Using this as an example, you could implement other actions like telnet,
work on external ticket and then update your ITSI Event worklog, update status,
severity, owner etc...
"""

import sys
import json
import platform
import subprocess
import emaillib

from splunk.clilib.bundle_paths import make_splunkhome_path

sys.path.append(make_splunkhome_path(['etc', 'apps', 'SA-ITOA', 'lib']))

from ITOA.fix_appserver_import import FixAppserverImports
from ITOA.setup_logging import setup_logging
from itsi.event_management.sdk.eventing import Event
from itsi.event_management.sdk.custom_event_action_base import CustomEventActionBase

class Email(CustomEventActionBase):
    def execute(self):
     
        self.logger.debug('Received settings from splunkd=`%s`',json.dumps(self.settings))
        self.logger.info('Executed action. Processed events count=`%s`.', count)
  
if __name__ == "__main__":
    logger = setup_logging("itsi_event_management.log", "itsi.event_action.customemail")
    logger.info("Starting Email Creation")
    if len(sys.argv) > 1 and sys.argv[1] == '--execute':
        input_params = sys.stdin.read()
        logger.info(input_params)
        payload = json.loads(input_params)
        logger.info(payload)
        event_id = payload['result']['event_id']
        session_key = payload['session_key'] 
        logger.info("Session Key:"+session_key+" event id:"+event_id)
        kpiid = payload['result']['all_service_kpi_ids']
        logger.info("KPI IDs:"+kpiid)
        ylist=kpiid.split(":")
        logger.info("Individual IDs:"+str(ylist))
        maddress = emaillib.getaddress()
        logger.info(maddress)
        serverstatus=[]
        #logger.info("Step1")
        for kpi in ylist:
            interimlist = emaillib.getEntities(kpi)
            logger.info (str(interimlist)+" for KPI:"+str(kpi))
            serverstatus.append(interimlist)
            #logger.info("Step2")
        logger.info (serverstatus)
        #logger.info("Step3")
        emaillib.send_email('myusername','mypassword','myrecipient@gmail.com','KPI is not Healthy - list of impacted entities attached','Please see list of impacted servers',serverstatus)


