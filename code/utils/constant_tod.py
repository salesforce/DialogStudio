"""
 Copyright (c) 2023, salesforce.com, inc.
 All rights reserved.
 SPDX-License-Identifier: Apache License 2.0
 For full license text, see the LICENSE file in the repo root or https://www.apache.org/licenses/LICENSE-2.0
"""


#!/usr/bin/env python3
#

# key used for direct usage
SPEAKER1 = "user"
SPEAKER2 = "system"
ORI_DIAL_ID = "original dialog id"
DIAL_IDX = "dialog index"
ORI_DIAL_INFO = "original dialog info"
TURN_ID = "turn id"
USR_UTT = f"{SPEAKER1} utterance"
SYS_UTT = f"{SPEAKER2} response"
DIAL_HIST = "dialog history"
ORI_USR_ANN = f"original {SPEAKER1} side information"
ORI_SYS_ANN = f"original {SPEAKER2} side information"
LOG = "log"

# # # output for different task
# domain prediction
DOM = "domain"
# intent prediction, including dialog act prediction if intent missing
INTENT = "intent"
INTENT_SPLIT = " , "
# dst
DST = "dst"
DST_ACC = "dst accumulated"
DST_SPLIT = " , "

# # # used for external knowledge
EK = "external knowledge"
EK_DST = "dst knowledge"
EK_INTENT = "intent knowledge"
# non-flat external knowledge dictionary
EK_ORI = "external knowledge non-flat"
TOD_EK = "metadata"
TOD_LENGTH = 10
# DOM_EK = "domains"
INTENT_EK = "intents"
DST_EK = "slots and values"
DST_LENGTH = 10

# # # prompt for each dialog
PROMPT = "prompt"
PROMPT_DST = "prompt for dst task"
PROMPT_INTENT = "prompt for intent prediction"

MULTIWOZ_DOMAINS = ["taxi", "police", "hospital", "hotel","attraction","train","restaurant"]

