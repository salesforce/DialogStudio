"""
 Copyright (c) 2023, salesforce.com, inc.
 All rights reserved.
 SPDX-License-Identifier: Apache License 2.0
 For full license text, see the LICENSE file in the repo root or https://www.apache.org/licenses/LICENSE-2.0
"""

#!/usr/bin/env python3
#
import sys, os, pdb
import json
import shutil, errno
from tqdm import tqdm
import pandas as pd
from utils.constant import *


class PreProcessData(object):
    """docstring for PreProcessData"""
    def __init__(self):
        super(PreProcessData, self).__init__()
        self.data_dir = "/path/to/where/the/raw/dataset/is"
        self.save_dir = "/path/to/store/the/processed/dataset/" # e.g. ./data/processed/Knowledge-Grounded


    def _load_json(self, path=None):
        if path is None or not os.path.exists(path):
            raise IOError('File does not exist: %s' % path)
            # return None
        with open(path) as df:
            data = json.loads(df.read())
        return data

    
    def _load_txt(self, path=None, split_tok="\n"):
        if path is None or not os.path.exists(path):
            raise IOError('File does not exist: %s' % path)
        with open(path) as df:
            data = df.read().strip().split(split_tok)
        return data


    def _load_csv(self, path=None, sep="\t"):
        if path is None or not os.path.exists(path):
            raise IOError('File does not exist: %s' % path)
        with open(path) as df:
            data = pd.read_csv(df, sep=sep)
        return data


    def _load_jsonl(self, path=None):
        if path is None or not os.path.exists(path):
            raise IOError('File does not exist: %s' % path)
        data = []
        with open(path) as df:
            for line in df.readlines():
                data.append(json.loads(line))
        return data



    def _load_dir_json(self, dir_path=None):
        if dir_path is None or not os.path.exists(dir_path): return None
        total_data = [] # assume data is a list of dialogs
        for filename in sorted(os.listdir(dir_path)):
            if filename in ["schema.json"]: continue
            if not filename.endswith(".json"): continue
            file_path = os.path.join(dir_path, filename)
            data = self._load_json(path=file_path)
            if type(data) == list:
                total_data.extend(data)
            else:
                total_data.append(data)
        return total_data


    def _load_dir_txt(self, dir_path=None, file_type="txt"):
        if dir_path is None or not os.path.exists(dir_path): return None
        total_data = [] # assume data is a list of dialogs
        for filename in sorted(os.listdir(dir_path)):
            if not filename.endswith(file_type): continue
            file_path = os.path.join(dir_path, filename)
            data = self._load_txt(path=file_path)
            if type(data) == list:
                total_data.extend(data)
            else:
                total_data.append(data)
        return total_data


    def _load_dir_tsv(self, dir_path=None, sep="\t"):
        if dir_path is None or not os.path.exists(dir_path): return None
        total_data = None
        for filename in sorted(os.listdir(dir_path)):
            file_path = os.path.join(dir_path, filename)
            data = self._load_csv(path=file_path, sep=sep)
            total_data = pd.concat([total_data, data], ignore_index=True)
        return total_data


    def _save_json(self, data, path):
        with open(path, "w") as tf:
            json.dump(data, tf, indent=4)


    def init_dial(self, dial_idx=0, ori_dial_id=""):
        dial = {
            ORI_DIAL_ID: "",
            DIAL_IDX: dial_idx,
            ORI_DIAL_INFO: {},
            LOG: [],
            # EK_ORI: {
            #     TOD_EK:{},
            # },
            # EK: "",
            PROMPT: [],
        }
        return dial


    def init_turn(self, turn_id=0, dial_hist=[]):
        turn = {
            TURN_ID: int(turn_id),
            USR_UTT: "",
            SYS_UTT: "",
            DIAL_HIST: " ".join(dial_hist),
            ORI_USR_ANN: {},
            ORI_SYS_ANN: {},
            EK_ORI: {
                TOD_EK:{},
            },
            EK: "",
        }
        return turn


    def save_dial(self, data, data_name="", file_idx=0, mode="train"):
        save_name = f"dialogues_{file_idx}.json"
        folder_path = os.path.join(self.save_dir, data_name, mode)
        if not os.path.exists(folder_path): os.makedirs(folder_path)
        path = os.path.join(folder_path, save_name)
        self._save_json(data, path)


    def save_original_examples(self, examples, data_name):
        """
        save 5 original data points just for reference and check
        data would be a list of length 5, each entry is a dialog 
        in the form of dictionary
        """
        path = os.path.join(self.save_dir, data_name, "original_examples.json")
        self._save_json(examples, path)
        print("original examples saved")


    def save_converted_examples(self, data_name):
        """
        extract the first 5 examples from the train set of the 
        already processed data, just for reference and check
        """
        data = self._load_json(os.path.join(self.save_dir, data_name, "train/dialogues_1.json"))
        examples = {key: data[key] for key in list(data.keys())[:5]}
        self._save_json(examples, os.path.join(self.save_dir, data_name, "converted_examples.json"))
        print("converted examples saved")


    def dict_to_str(self, ek_ori):
        """
        turn non-flat external knowledge into string
        original format:
            "metadata":{
                domain: [
                    {
                        attr1: value1,
                        attr2: value2,
                        ...
                    },
                    ...
                ]
            }
        output format:
            ( metadata : ( domain : ( attr1 : value1 | attr2 : value2 | ... ) | ( ... ) | ... ))
        """
        ek = str(ek_ori).replace("'"," ").replace(", "," | ")
        ek = ek.replace("{","(").replace("}",")").replace("[","(").replace("]",")")
        ek = ek.replace("  ", " ")
        return ek


    def wow(self):
        """
        Speakers: Apprentice (always starts a turn), Wizard (ends a turn)
        turn-level EK only
        checked facts:

        """
        data_name = "wizard_of_wikipedia"
        for mode in ["train", "val", "test"]:
            if mode == "train": filename = "train.json"
            elif mode == "val": filename = "valid_topic_split.json"
            else:               filename = "test_topic_split.json"
            data = self._load_json(os.path.join(self.data_dir, data_name, filename))
            new_data, file_idx = {}, 1
            for dial_idx, dial in tqdm(enumerate(data)):
                new_dial = self.init_dial(dial_idx=dial_idx+1)
                new_dial_id = f"{data_name}--{mode}--{dial_idx+1}"
                new_dial[ORI_DIAL_INFO]["chosen_topic"] = dial["chosen_topic"]
                new_dial[ORI_DIAL_INFO]["persona"] = dial["persona"]
                new_dial[ORI_DIAL_INFO]["wizard_eval"] = dial["wizard_eval"]
                new_dial[ORI_DIAL_INFO]["chosen_topic_passage"] = dial["chosen_topic_passage"]
                turn_idx, dial_hist = 1, []
                new_turn = self.init_turn(turn_id=turn_idx)
                for turn in (dial["dialog"]):
                    if turn["speaker"].split("_")[-1] == "Apprentice":
                        new_turn = self.init_turn(turn_id=turn_idx)
                        new_turn[DIAL_HIST] = " ".join(dial_hist)
                        for key_ in turn:
                            if key_ == "text":
                                new_turn[USR_UTT] = turn["text"]
                            else:
                                new_turn[ORI_USR_ANN][key_] = turn[key_]

                        dial_hist.append(f"<{SPEAKER1.upper()}> " + new_turn[USR_UTT])
                    elif turn["speaker"].split("_")[-1] == "Wizard":
                        for key_ in turn:
                            if key_ == "text":
                                new_turn[SYS_UTT] = turn["text"]
                            else:
                                new_turn[ORI_SYS_ANN][key_] = turn[key_]
                        dial_hist.append(f"<{SPEAKER2.upper()}> " + new_turn[SYS_UTT])
                        if not turn["checked_passage"]:
                            turn["checked_passage"] = {"none": dial["chosen_topic"]}
                        if not turn["checked_sentence"]:
                            turn["checked_sentence"] = {"no_passages_used": "no_passages_used"}
                        if len(turn["checked_passage"]) == 2 and "no_passages_used" in turn["checked_passage"]: 
                            # for case  turn["checked_passage"] = {'chosen_topic_0_Aquarium': 'Aquarium', 'no_passages_used': 'no_passages_used'}
                            del turn["checked_passage"]["no_passages_used"]
                        # if len(turn["checked_passage"].values()) != 1 or len(turn["checked_sentence"].values()) != 1: pdb.set_trace()
                        title = list(turn["checked_passage"].values())[0]
                        sent = list(turn["checked_sentence"].values())[0]
                        new_turn[EK_ORI][TOD_EK][title] = sent
                        new_turn[EK] = self.dict_to_str(new_turn[EK_ORI][TOD_EK])
                        new_dial[LOG].append(new_turn)
                        turn_idx += 1
                    else:
                        print(turn["speaker"])
                        raise ValueError("Unknown speaker")

                if not new_turn[SYS_UTT]:
                    new_dial[LOG].append(new_turn)

                new_data[new_dial_id] = new_dial
                if new_dial[DIAL_IDX] % 10000 == 0:
                    self.save_dial(new_data, data_name=data_name, file_idx=file_idx, mode=mode)
                    new_data = {} # reset
                    file_idx += 1
            if new_data: self.save_dial(new_data, data_name=data_name, file_idx=file_idx, mode=mode)
            if mode == "train": self.save_original_examples(data[:5], data_name)
            print(f"finishing processing {dial_idx+1} dialogs for {mode} set ...")
        self.save_converted_examples(data_name)
        print("*"*10, f"finishing processing dataset {data_name}", "*"*10)
                

    def woi(self):
        """
        actions:
            Apprentice => Wizard
            Wizard => SearchAgent
            SearchAgent => Wizard
            Wizard => Apprentice
        """
        data_name = "wizard_of_internet"
        for mode in ["test", "train"]:
            data = self._load_jsonl(os.path.join(self.data_dir, data_name, f"{mode}.jsonl"))
            data = {k:v for dial in data for k,v in dial.items()}
            new_data, file_idx, dial_idx = {}, 1, 1
            for dial_id, dial in tqdm(data.items()):
                # new_dial = dial
                new_dial = self.init_dial(dial_idx=dial_idx)
                new_dial_id = f"{data_name}--{mode}--{dial_idx}"
                new_dial[ORI_DIAL_ID] = dial_id
                new_dial[ORI_DIAL_INFO]["apprentice_persona"] = dial["apprentice_persona"]
                new_dial[ORI_DIAL_INFO]["start_timestamp"] = dial["start_timestamp"]
                turn_idx, dial_hist = 1, []
                new_turn = self.init_turn(turn_id=turn_idx)
                for turn in dial["dialog_history"]:
                    if turn["action"] == "Apprentice => Wizard":
                        new_turn = self.init_turn(turn_id=turn_idx)
                        new_turn[DIAL_HIST] = " ".join(dial_hist)
                        new_turn[USR_UTT] = turn["text"]
                        new_turn[ORI_USR_ANN]["timestamp"] = turn["timestamp"]
                        dial_hist.append(f"<{SPEAKER1.upper()}> " + new_turn[USR_UTT])
                    elif turn["action"] == "Wizard => SearchAgent":
                        if "query" not in new_turn[ORI_SYS_ANN]:
                            new_turn[ORI_SYS_ANN]["query"] = []
                        new_turn[ORI_SYS_ANN]["query"].append({
                            "query": turn["text"],
                            "query_result": "",
                            "timestamp_query": turn["timestamp"],
                        })
                    elif turn["action"] == "SearchAgent => Wizard":
                        # checked, each query corresponds to one query result
                        # if new_turn[ORI_SYS_ANN]["query"][-1]["query_result"]: pdb.set_trace()
                        new_turn[ORI_SYS_ANN]["query"][-1]["query_result"] = turn["context"]
                    elif turn["action"] == "Wizard => Apprentice":
                        new_turn[SYS_UTT] = turn["text"]
                        for doc_id, doc in enumerate(turn["context"]["selected_contents"][1:]):
                            for sent_id, choose in enumerate(doc):
                                if choose:
                                    title = turn["context"]["contents"][doc_id]["title"]
                                    sent  = turn["context"]["contents"][doc_id]["content"][sent_id]
                                    if title not in new_turn[EK_ORI][TOD_EK]:
                                        new_turn[EK_ORI][TOD_EK][title] = []
                                    new_turn[EK_ORI][TOD_EK][title].append(sent)
                        new_turn[EK] = self.dict_to_str(new_turn[EK_ORI][TOD_EK])
                        new_turn[ORI_SYS_ANN]["context"] = turn["context"]
                        new_turn[ORI_SYS_ANN]["timestamp"] = turn["timestamp"]
                        dial_hist.append(f"<{SPEAKER2.upper()}> " + new_turn[SYS_UTT])
                        new_dial[LOG].append(new_turn)
                        turn_idx += 1
                    else:
                        # checked, no such turns
                        print(turn["action"])
                        raise ValueError("The fifth case")
                if not new_turn[SYS_UTT]:
                    new_dial[LOG].append(new_turn)
                
                # new_dial[EK_ORI][TOD_EK]["apprentice_persona"] = dial["apprentice_persona"]
                # new_dial[EK] = self.dict_to_str(new_dial[EK_ORI][TOD_EK])
                new_data[new_dial_id] = new_dial
                if dial_idx % 10000 == 0:
                    self.save_dial(new_data, data_name=data_name, file_idx=file_idx, mode=mode)
                    new_data = {} # reset
                    file_idx += 1
                dial_idx += 1
            if new_data: self.save_dial(new_data, data_name=data_name, file_idx=file_idx, mode=mode)
            if mode == "train": self.save_original_examples({k:data[k] for k in list(data.keys())[:5]}, data_name)
            print(f"finishing processing {dial_idx-1} dialogs for {mode} set ...")
        self.save_converted_examples(data_name)
        print("*"*10, f"finishing processing dataset {data_name}", "*"*10)

    def run_all(self):
        self.wow()
        self.woi()


    def copy_example(self):
        source_dir = self.save_dir
        for target_dir in [ "/home/qkun/projs/TOD-Project/Datasets/Knowledge-Grounded_PROCESSED/", "/home/qkun/projs/DialogStudio-Release/knowledge-grounded-dialogues/"]:
            # target_dir = "/home/qkun/projs/TOD-Project/Datasets/Knowledge-Grounded_PROCESSED/"
            file_list = ["converted_examples.json", "original_examples.json", "readme.txt", "LICENSE"]
            for dir_name in sorted(os.listdir(source_dir)):
                if os.path.isfile(os.path.join(source_dir, dir_name)): continue
                if not os.path.exists(os.path.join(target_dir, dir_name)): os.makedirs(os.path.join(target_dir, dir_name))
                for filename in file_list:
                    source_path = os.path.join(source_dir, dir_name, filename)
                    target_path = os.path.join(target_dir, dir_name, filename)
                    if not os.path.exists(source_path): continue
                    shutil.copy(source_path, target_path)


def main():
    preprocess = PreProcessData()
    preprocess.run_all()
    preprocess.copy_example()

if __name__ == '__main__':
    main()
