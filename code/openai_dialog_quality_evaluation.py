"""
 Copyright (c) 2023, salesforce.com, inc.
 All rights reserved.
 SPDX-License-Identifier: Apache License 2.0
 For full license text, see the LICENSE file in the repo root or https://www.apache.org/licenses/LICENSE-2.0
"""


import os
os.environ["OPENAI_API_KEY"] = ""


from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
import json
from utils import open_json, save_json, open_jsonl
from collections import defaultdict

class EvaluateDialogs(object):
    """ Evaluate Dialogs based on OpenAI. To run this:
        pip install openai
        pip install langchain
    """
    def __init__(self):
        self.data_dir = "/Users/jianguozhang/TOD-Family/TOD-Studio/open-source/"
        self.excluded_datasets = ['MetaLWOZ', "MuDoCo", "SalesBot", "HDSA-Dialog", "MULTIWOZ2_2"]  # "SGD"

        self.quality_agent_prompt = PromptTemplate(
            input_variables=["dialog"],
            template="""
            Hi AI, I plan to train a language model for response generation. Please analyze the following dialogue and evaluate it based on the criteria provided. Assign a score from 1 (poor) to 5 (excellent) for each category. We're looking for a critical assessment, and higher scores should only be given to truly exceptional examples. The criteria for evaluation are: Understanding, Relevance, Completeness, Correctness, and Coherence.
        
            After your assessment, provide an overall score for the dialogue along with a concise summary  of your evaluation. The overall score should also be on a scale of 1 (poor) to 5 (excellent) and should represent a holistic assessment of the dialogue.
            
            Please present your evaluation and comment into the following format:
            
            {{
              "Understanding": _,
              "Relevance": _,
              "Completeness": _,
              "Correctness": _,
              "Coherence": _,
              "Overall": {{"score": _, "comment": _}}
            }}
            
            Please replace each underscore (_) with the appropriate score. For the 'Overall' field, provide the score and a concise comment. Regarding to the comment, it should not only summarize the dialogue's quality but also highlight any issues or shortcomings you may have identified in the dialogue.
            
            Below is the dialog:
            
            {dialog}  
            
            Evaluate the dialog now.
            """
        )

        self.quality_chain = LLMChain(llm=ChatOpenAI(temperature=0.2, model_name="gpt-3.5-turbo"), prompt=self.quality_agent_prompt)

    def run_openai_evaluation(self, dialog):
        res = self.quality_chain.run(dialog=dialog)
        try:
            res = json.loads(res)
        except:
            res = str(res)
        return res

    def tod(self):
        """
        Evaluate TOD dialogues
        :return:
        """
        folder_name = "Task-Oriented-Dialogues--OpenAI"
        folder_path = os.path.join(self.data_dir, folder_name)
        dataset_names = os.listdir(folder_path)
        print(dataset_names)
        print()
        for dataset_name in dataset_names:
            if not os.path.isdir(os.path.join(folder_path, dataset_name)):
                continue

            data = open_json(os.path.join(folder_path, dataset_name, "train.json"))
            f_writer = open(os.path.join(folder_path, dataset_name, "train_quality_scores.json"), "w")
            print("Start processing: {} #total dialogs: {}".format(dataset_name, len(data)))

            for index, item in enumerate(data):

                output = defaultdict(dict)
                output["source"] = item["source"]
                output["quality score"] = self.run_openai_evaluation(item["dialog"])

                json.dump(output, f_writer)
                f_writer.write("\n")  # Add a new line for readability
                if index % 10 == 0 or index + 1 == len(data):
                    f_writer.flush()  # Flush the buffer to update the file immediately

    def run(self):
        self.tod()

process = EvaluateDialogs()
# Run evaluations for dialogs
process.run()
