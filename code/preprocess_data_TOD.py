#!/usr/bin/env python3
#
import random
import sys, os, pdb
import json, math
import shutil, errno
from tqdm import tqdm
import pandas as pd
from collections import defaultdict
from utils.domain_mapping import generate_prompt
from utils.constant import *

random.seed(42)

class PreProcessData(object):
    """docstring for PreProcessData"""
    def __init__(self):
        super(PreProcessData, self).__init__()
        self.data_dir = "/path/to/where/the/raw/dataset/is"
        self.save_dir = "/path/to/store/the/processed/dataset/" # e.g. ./data/processed/Task-Oriented


    def _load_json(self, path=None):
        if path is None or not os.path.exists(path):
            raise IOError('File does not exist: %s' % path)
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


    def _load_dir_json(self, dir_path=None):
        if dir_path is None or not os.path.exists(dir_path): return None
        total_data = [] # assume data is a list of dialogs
        for filename in sorted(os.listdir(dir_path)):
            if filename in ["schema.json"]: continue
            if not filename.endswith(".json"): continue
            file_path = os.path.join(dir_path, filename)
            data = self._load_json(path=file_path)
            if type(data) == list:
                for item in data:
                    item["filename"] = filename.split(".json")[0]
                total_data.extend(data)
            else: # assume is a dict
                data["filename"] = filename.split(".json")[0]
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
            data["filename"] = filename.split(".tsv")[0]
            total_data = pd.concat([total_data, data], ignore_index=True)
        return total_data


    def _save_json(self, data, path):
        with open(path, "w") as tf:
            json.dump(data, tf, indent=4)


    def init_dial(self, dial_idx=0):
        dial = {
            ORI_DIAL_ID: "",
            DIAL_IDX: dial_idx,
            ORI_DIAL_INFO: {},
            LOG: [],
            EK_ORI: {
                TOD_EK:{},
                DST_EK:{},
                INTENT_EK:{},
            },
            EK: "",
            EK_DST: "",
            EK_INTENT: "",
            PROMPT: [],
        }
        return dial


    def init_turn(self, turn_id=1, dial_hist=[]):
        turn = {
            TURN_ID: turn_id,
            USR_UTT: "",
            SYS_UTT: "",
            DIAL_HIST: " ".join(dial_hist),
            ORI_USR_ANN: {},
            ORI_SYS_ANN: {},
            DST: "",
            DST_ACC: "",
        }
        return turn


    def save_dial(self, data, data_name="", file_idx=0, mode="train"):
        save_name = f"dialogues_{file_idx}.json"
        folder_path = os.path.join(self.save_dir, data_name, mode)
        if not os.path.exists(folder_path): os.makedirs(folder_path)
        path = os.path.join(folder_path, save_name)
        self._save_json(data, path)

        # pdb.set_trace()


    def copy_general(self, src, dst):
        try:
            shutil.copytree(src, dst, dirs_exist_ok=True)
        except OSError as exc: # python >2.5
            if exc.errno in (errno.ENOTDIR, errno.EINVAL):
                shutil.copy(src, dst)
            else: raise


    def copy_related_files(self, data_name, exp_list=[], extra_dir=""):
        source_dir = os.path.join(self.data_dir, data_name, extra_dir)
        target_dir = os.path.join(self.save_dir, data_name)
        for filename in os.listdir(source_dir):
            source_path = os.path.join(source_dir, filename)
            target_path = os.path.join(target_dir, filename)
            if filename in exp_list: continue
            self.copy_general(source_path, target_path)


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
    
    
    def filter_cand(self, cand_list, constraints):
        """
        pop up cands that satisfy constraints
        cand_list = [
            {
                attribute1: ...,
                attribute2: ...,
                ...
            }, 
            ...
        ]
        constraints = [
            {
                attribute1: ...,
                attributei: ...,
            }
        ]
        constraints[i].keys() is a subset of cand_list[k].keys()
        """
        satisfy_results = []
        for cand in cand_list:
            for constraint in constraints:
                flag = 1 # flag for marking whether constraint is satisfied
                for key_ in constraint:
                    # if key_ == "category" and (key_ not in cand or key_ not in constraint):
                    #     pdb.set_trace()
                    if key_ not in cand: continue
                    if cand[key_] != constraint[key_]:
                        flag = 0
                        break
                if flag:
                    satisfy_results.append(cand)
                    break
        for cand in satisfy_results:
            cand_list.remove(cand)
        return satisfy_results, cand_list


    def kvret(self):
        """
        system or user side might have consecutive turns"""
        data_name, exp_list = "KVRET", []
        # slot type belonging to each doamin
        dom_slot = {
            "schedule": {_key:[] for _key in ["event","time","data","party","room","agenda"]},
            "weather": {_key:[] for _key in ["location","weekly_time","temperature","weather_attribute"]},
            "navigate": {_key:[] for _key in ["traffic_info","poi_type","poi","distance"]},
        }
        schema = self._load_json(os.path.join(self.data_dir, data_name, "kvret_entities.json"))
        for slot in schema:
            for domain in dom_slot:
                if slot in dom_slot[domain]:
                    dom_slot[domain][slot] = schema[slot]
        for mode in ["train", "val", "test"]:
            real_name = f"kvret_{mode}_public.json" if mode != "val" else "kvret_dev_public.json"
            path = os.path.join(self.data_dir, data_name, real_name)
            exp_list.append(real_name)

            data = self._load_json(path)
            new_data = {}
            file_idx = 1

            for dial_idx, dial in enumerate(data):
                domain = dial["scenario"]["task"]["intent"]
                new_dial_id = f"{data_name}--{mode}--{dial_idx+1}"
                new_dial = self.init_dial(dial_idx=dial_idx+1) # idx starts from 1
                new_dial[ORI_DIAL_ID] = dial["scenario"]['uuid']
                new_dial[ORI_DIAL_INFO] = {
                    "scenario" : dial["scenario"]
                }
                dial_hist, result_list, dst_dict = [], [], {}
                usr_utts, sys_utts, turn_id = [], [], 2
                new_turn = self.init_turn()
                for idx, turn in enumerate(dial["dialogue"]):
                    utt = turn["data"]["utterance"]
                    if turn["turn"] == "driver":
                        if idx and  dial["dialogue"][idx - 1]["turn"] == "assistant":
                            # wrap previous turn
                            new_turn[USR_UTT] = " ".join(usr_utts)
                            new_turn[SYS_UTT] = sys_utts[-1] if sys_utts else " ".join(sys_utts)
                            new_dial[LOG].append(new_turn)
                            dial_hist.append(f"<USER> {new_turn[USR_UTT]}")
                            dial_hist.append(f"<SYSTEM> {new_turn[SYS_UTT]}")

                            # new turn start from user
                            new_turn = self.init_turn(turn_id=turn_id)
                            turn_id += 1
                            usr_utts, sys_utts = [], []
                            new_turn[DIAL_HIST] = " ".join(dial_hist)
                        # # include user utterance into dialog history
                        # dial_hist.append(f"<USER> {utt}")

                        if utt in usr_utts: continue
                        usr_utts.append(utt)
                        # other annotation for user side
                        for key in turn["data"]:
                            if key == "utterance": continue
                            new_turn[ORI_USR_ANN][key] = turn["data"][key]

                    if turn["turn"] == "assistant":
                        # new_turn[SYS_UTT] = utt
                        if utt in sys_utts: continue
                        sys_utts.append(utt)
                        # include system response into dialog history
                        # dial_hist.append(f"<SYSTEM> {utt}")
                        # other annotation for system side
                        for key in turn["data"]:
                            if key == "utterance": continue
                            new_turn[ORI_SYS_ANN][key] = turn["data"][key]
                        #  adding dst output
                        # if "slots" not in turn["data"]: continue # checked
                        new_turn[DST] = ", ".join([f"{domain} {slot} {value}" for slot, value in turn["data"]["slots"].items()])
                        # adding accumulated dst output
                        if domain not in dst_dict: dst_dict[domain] = {}
                        dst_dict[domain].update(turn["data"]["slots"])
                        new_turn[DST_ACC] = self.dst_dict_to_str(dst_dict)
                        if "slots" in turn and "poi" in turn["slots"]:
                            result_list.append(turn["slots"]["poi"])
                        elif "slots" in turn and "event" in turn["slots"]:
                            result_list.append(turn["slots"]["event"])
                        
                if usr_utts or sys_utts:
                    new_turn[USR_UTT] = " ".join(usr_utts)
                    new_turn[SYS_UTT] = sys_utts[-1] if sys_utts else " ".join(sys_utts)
                    new_dial[LOG].append(new_turn)
                    
                
                # adding metadata for TOD task
                new_dial[EK_ORI][TOD_EK][domain] = []
                if dial["scenario"]["kb"]["items"] is not None:
                    cand_list = dial["scenario"]["kb"]["items"]
                    for result in dial["scenario"]["kb"]["items"]:
                        if "poi" in result and result["poi"] in result_list:
                            new_dial[EK_ORI][TOD_EK][domain].append(result)
                            cand_list.remove(result)
                        elif "event" in result and result["event"] in result_list:
                            new_dial[EK_ORI][TOD_EK][domain].append(result)
                            cand_list.remove(result)
                    if len(dial["scenario"]["kb"]["items"]) < TOD_LENGTH:
                        new_dial[EK_ORI][TOD_EK][domain].extend(cand_list)
                    else:
                        new_dial[EK_ORI][TOD_EK][domain].extend(random.choices(cand_list, k=(TOD_LENGTH-len(result_list))))
                # adding ek for DST task
                new_dial[EK_ORI][DST_EK] = dom_slot[domain]
                # turn the external knowledge into a flat string
                new_dial[EK] = self.dict_to_str(new_dial[EK_ORI][TOD_EK])
                new_dial[EK_DST] = self.dict_to_str(new_dial[EK_ORI][DST_EK])
                new_dial[EK_INTENT] = self.dict_to_str(new_dial[EK_ORI][INTENT_EK])
                # adding prompt for each dialog
                domains = [domain]
                new_dial[PROMPT] = generate_prompt(data_name, domains)
                # finish and wrap the current dialog
                new_data[new_dial_id] = new_dial
                if (dial_idx+1) % 1000 == 0 or dial_idx+1 == len(data):
                    self.save_dial(new_data, data_name=data_name, file_idx=file_idx, mode=mode)
                    new_data = {} # reset
                    file_idx += 1
    
            if mode == "train": self.save_original_examples(data[:5], data_name)
            print(f"finishing processing {len(data)} dialogs for {mode} set ...")
        self.save_converted_examples(data_name)
        self.copy_related_files(data_name, exp_list)
        print("*"*10, f"finishing processing dataset {data_name}", "*"*10)


    def woz(self):
        # dialog ends on the user side
        # first system response recorded in the second turn
        data_name, exp_list = "WOZ2_0", []
        otgy = self._load_json(os.path.join(self.save_dir, data_name, "otgy.json"))
        del otgy["request"]

        for mode in ["train", "val", "test"]:
            real_name = f"{mode}_en.json" if mode != "val" else "valid_en.json"
            path = os.path.join(self.data_dir, data_name, real_name)
            exp_list.append(real_name)

            data = self._load_json(path)
            new_data = {}
            file_idx = 1

            for dial_idx, dial in enumerate(data):
                new_dial_id = f"{data_name}--{mode}--{dial_idx+1}"
                new_dial = self.init_dial(dial_idx=dial_idx+1) # idx starts from 1
                new_dial[ORI_DIAL_ID] = dial['dialogue_idx']
                dial_hist, dst_dict = [], {}
                new_turn = self.init_turn(turn_id=1)
                for idx, turn in enumerate(dial["dialogue"]):
                    usr_utt, sys_utt = turn["transcript"], turn["system_transcript"]

                    if sys_utt:
                        new_turn[ORI_SYS_ANN]["system_acts"] = turn["system_acts"]
                        new_turn[SYS_UTT] = sys_utt
                        dial_hist.append(f"<SYSTEM> {sys_utt}")
                        new_dial[LOG].append(new_turn)
                        # reset new turn for next
                        new_turn = self.init_turn(turn_id=idx+1)
                        new_turn[DIAL_HIST] = " ".join(dial_hist)
                    
                    # dst output
                    # if "turn_label" not in turn: pdb.set_trace() # checked
                    slot_list = []
                    for slot in turn["turn_label"]:
                        if slot[0] == "request": continue
                        slot_type = "_".join(slot[0].split())
                        slot_list.append(f"restaurant {slot_type} {slot[1]}")
                    new_turn[DST] = ", ".join(slot_list)
                    # accumulate dst output
                    dst_dict = self.update_with_slot_list(dst_dict, slot_list)
                    new_turn[DST_ACC] = self.dst_dict_to_str(dst_dict)


                    new_turn[USR_UTT] = usr_utt
                    dial_hist.append(f"<USER> {usr_utt}")
                    for key in turn:
                        if key.startswith("system"): continue
                        new_turn[ORI_USR_ANN][key] = turn[key]
                # append the last turn with no system response
                new_dial[LOG].append(new_turn)

                # adding ek for DST task
                new_dial[EK_ORI][DST_EK] = {"restaurant" : otgy}
                for slot in new_dial[EK_ORI][DST_EK]["restaurant"]:
                    if len(new_dial[EK_ORI][DST_EK]["restaurant"][slot]) > 2*DST_LENGTH:
                        new_dial[EK_ORI][DST_EK]["restaurant"][slot] = random.choices(otgy[slot], k=DST_LENGTH)
                # turn the external knowledge into a flat string
                new_dial[EK] = self.dict_to_str(new_dial[EK_ORI][TOD_EK])
                new_dial[EK_DST] = self.dict_to_str(new_dial[EK_ORI][DST_EK])
                new_dial[EK_INTENT] = self.dict_to_str(new_dial[EK_ORI][INTENT_EK])
                # adding prompt for each dialog
                domains = ["restaurant"]
                new_dial[PROMPT] = generate_prompt(data_name, domains)
                # finish and wrap the current dialog

                new_data[new_dial_id] = new_dial
                if (dial_idx+1) % 1000 == 0 or dial_idx+1 == len(data):
                    self.save_dial(new_data, data_name=data_name, file_idx=file_idx, mode=mode)
                    new_data = {} # reset
                    file_idx += 1

            if mode == "train": self.save_original_examples(data[:5], data_name)
            print(f"finishing processing {dial_idx} dialogs for {mode} set ...")
        self.save_converted_examples(data_name)
        self.copy_related_files(data_name, exp_list)
        print("*"*10, f"finishing processing dataset {data_name}", "*"*10)


    def sgd(self):
        data_name, exp_list = "SGD", []
        for mode in ["train", "val", "test"]:
            real_name = mode if mode != "val" else "dev"
            dir_path = os.path.join(self.data_dir, data_name, real_name)
            exp_list.append(real_name)

            data = self._load_dir_json(dir_path)
            schema = self._load_json(os.path.join(self.data_dir, data_name, real_name, "schema.json"))
            new_data = {}
            file_idx = 1

            for dial_idx, dial in (enumerate(data)):
                new_dial_id = f"{data_name}--{mode}--{dial_idx+1}"
                new_dial = self.init_dial(dial_idx=dial_idx+1) # idx starts from 1
                new_dial[ORI_DIAL_ID] = dial['dialogue_id']
                new_dial[ORI_DIAL_INFO]["services"] = dial["services"]

                dial_hist, result_list, cand_list = [], {}, {}
                for idx, turn in enumerate(dial["turns"]):
                    utt = turn["utterance"]
                    if turn["speaker"] == "USER":
                        # new turn start from user
                        new_turn = self.init_turn(turn_id=idx//2+1)
                        new_turn[USR_UTT] = utt
                        new_turn[DIAL_HIST] = " ".join(dial_hist)
                        # include user utterance into dialog history
                        dial_hist.append(f"<USER> {utt}")
                        # other annotation for user side
                        new_turn[ORI_USR_ANN]["frames"] = turn["frames"]
                        # add dst output
                        slot_list = []
                        for frame in turn["frames"]:
                            if not frame["slots"]: continue
                            for slot in frame["slots"]:
                                slot_list.append(frame["service"] +" "+ slot["slot"] +" "+ turn["utterance"][slot["start"]: slot["exclusive_end"]])
                        new_turn[DST] = DST_SPLIT.join(slot_list)
                        # add accu dst output
                        slot_list = []
                        for frame in turn["frames"]:
                            if not frame["state"]: continue
                            for slot_type, slot_values in frame["state"]["slot_values"].items():
                                slot_list.append(frame["service"]+" "+slot_type+" "+slot_values[0])
                        new_turn[DST_ACC] = DST_SPLIT.join(slot_list)
                        # dialog ends at user side
                        if idx == len(dial["turns"]) - 1:
                            new_dial[LOG].append(new_turn)

                    if turn["speaker"] == "SYSTEM":
                        new_turn[SYS_UTT] = utt
                        # include system response into dialog history
                        dial_hist.append(f"<SYSTEM> {utt}")
                        # other annotation for system side
                        new_turn[ORI_SYS_ANN]["frames"] = turn["frames"]
                        # turn must end at assistant side
                        new_dial[LOG].append(new_turn)

                        for frame in turn["frames"]:
                            if "service_results" in frame:
                                domain = frame["service"]
                                # # # accumulate db results
                                if domain not in cand_list:
                                    cand_list[domain] = []
                                cand_list[domain].extend(frame["service_results"])
                                # # # accumulate offered results
                                if domain not in result_list:
                                    result_list[domain] = []
                                result_list[domain].append(frame["service_call"]["parameters"])
                # adding EK for TOD
                for domain in cand_list:
                    new_dial[EK_ORI][TOD_EK][domain] = []
                    satisfied_cand, unsatisfied_cand = self.filter_cand(cand_list[domain], result_list[domain])
                    if len(satisfied_cand)+len(unsatisfied_cand) < TOD_LENGTH:
                        new_dial[EK_ORI][TOD_EK][domain] = satisfied_cand + unsatisfied_cand
                    else:
                        new_dial[EK_ORI][TOD_EK][domain] = satisfied_cand
                        new_dial[EK_ORI][TOD_EK][domain].extend(random.choices(unsatisfied_cand, k=(TOD_LENGTH-len(satisfied_cand))))
                # adding EK for DST
                for domain in dial["services"]:
                    new_dial[EK_ORI][DST_EK][domain] = {}
                    for service in schema:
                        if service["service_name"] != domain: continue
                        for slot in service["slots"]:
                            if not slot["possible_values"]: continue
                            new_dial[EK_ORI][DST_EK][domain][slot["name"]] = slot["possible_values"]
                # adding EK for Intent
                for domain in dial["services"]:
                    new_dial[EK_ORI][INTENT_EK][domain] = []
                    for service in schema:
                        if service["service_name"] != domain: continue
                        for intent in service["intents"]:
                            new_dial[EK_ORI][INTENT_EK][domain].append(intent["name"])
                # turn the external knowledge into a flat string
                new_dial[EK] = self.dict_to_str(new_dial[EK_ORI][TOD_EK])
                new_dial[EK_DST] = self.dict_to_str(new_dial[EK_ORI][DST_EK])
                new_dial[EK_INTENT] = self.dict_to_str(new_dial[EK_ORI][INTENT_EK])
                # adding prompt for each dialog
                domains = [domain.lower().split("_")[0] for domain in dial["services"]]
                new_dial[PROMPT] = generate_prompt(data_name, domains)
                # finish and wrap the current dialog
                new_data[new_dial_id] = new_dial
                if (dial_idx+1) % 1000 == 0 or dial_idx+1 == len(data):
                    self.save_dial(new_data, data_name=data_name, file_idx=file_idx, mode=mode)
                    new_data = {} # reset
                    file_idx += 1
    
            if mode == "train": self.save_original_examples(data[:5], data_name)
            print(f"finishing processing {dial_idx+1} dialogs for {mode} set ...")
        self.save_converted_examples(data_name)
        self.copy_related_files(data_name, exp_list)
        for mode in ["train", "dev", "test"]:
            source_path = os.path.join(self.data_dir, data_name, mode, "schema.json")
            target_dir = os.path.join(self.save_dir, data_name, mode)
            shutil.copy(source_path, target_dir)
        print("*"*10, f"finishing processing dataset {data_name}", "*"*10)


    def bitod(self):
        data_name, exp_list = "BiTOD", []
        otgy = self._load_json(os.path.join(self.save_dir, data_name, "otgy.json"))
        for mode in ["train", "val", "test"]:
            real_name = f"{mode}_en.json" if mode != "val" else "valid_en.json"
            path = os.path.join(self.data_dir, data_name, real_name)
            exp_list.append(real_name)

            data = self._load_json(path)
            new_data, file_idx, dial_idx = {}, 1, 1

            for dial_id in data:
                new_dial_id = f"{data_name}--{mode}--{dial_idx}"
                new_dial = self.init_dial(dial_idx=dial_idx) # idx starts from 1
                new_dial[ORI_DIAL_ID] = dial_id
                new_dial[ORI_DIAL_INFO]["Scenario"] = data[dial_id]["Scenario"]
                domains = []
                for intent in data[dial_id]["Scenario"]["User_Goal"]:
                    domains.append(intent.split("_")[0])
                domains = list(set(domains))
                dial_hist, idx = [], 0
                dst_dict = {}
                for turn in data[dial_id]["Events"]:
                    if "Text" not in turn: continue
                    utt = turn["Text"]
                    if turn["Agent"] == "User":
                        idx += 1
                        # new turn start from user
                        new_turn = self.init_turn(turn_id=idx)
                        new_turn[USR_UTT] = utt
                        new_turn[DIAL_HIST] = " ".join(dial_hist)
                        # include user utterance into dialog history
                        dial_hist.append(f"<USER> {utt}")
                        # adding dst output
                        # if "active_intent" not in turn: pdb.set_trace() #checked
                        domain = turn["active_intent"].split("_")[0]
                        if domain == "chat": 
                            new_turn[DST] = ""
                        else:
                            slot_list = []
                            for act in turn["Actions"]:
                                if act["act"] != "inform": continue
                                slot_type = act["slot"]
                                slot_values = act["value"]
                                slot_list.append(f"{domain} {slot_type} {slot_values[0]}")
                            new_turn[DST] = ", ".join(slot_list)

                            # accumulate dst output
                            dst_dict = self.update_with_slot_list(dst_dict, slot_list)
                        new_turn[DST_ACC] = self.dst_dict_to_str(dst_dict)
                        # adding intent prediction output
                        new_turn[INTENT] = turn["active_intent"]
                        # other annotation for user side
                        for key in turn:
                            if key == "Text": continue
                            new_turn[ORI_USR_ANN][key] = turn[key]

                    if turn["Agent"] == "Wizard":
                        new_turn[SYS_UTT] = utt
                        # include system response into dialog history
                        dial_hist.append(f"<SYSTEM> {utt}")
                        # other annotation for system side
                        for key in turn:
                            if key == "Text": continue
                            new_turn[ORI_SYS_ANN][key] = turn[key]
                        # turn must end at assistant side
                        new_dial[LOG].append(new_turn)
                # adding EK for Intent Prediction
                new_dial[EK_ORI][INTENT_EK] = {}
                for domain in domains:
                    if domain not in otgy:
                        pdb.set_trace()
                    if "intents" not in otgy[domain]:
                        pdb.set_trace()
                    new_dial[EK_ORI][INTENT_EK][domain] = otgy[domain]["intents"]
                # adding EK for DST task
                new_dial[EK_ORI][DST_EK] = {}
                for domain in domains:
                    new_dial[EK_ORI][DST_EK][domain] = otgy[domain]["slots"]
                    for slot in new_dial[EK_ORI][DST_EK][domain]:
                        if len(new_dial[EK_ORI][DST_EK][domain][slot]) > 2*DST_LENGTH:
                            new_dial[EK_ORI][DST_EK][domain][slot] = random.choices(otgy[domain]["slots"][slot], k=DST_LENGTH)
                # turn the external knowledge into a flat string
                new_dial[EK] = self.dict_to_str(new_dial[EK_ORI][TOD_EK])
                new_dial[EK_DST] = self.dict_to_str(new_dial[EK_ORI][DST_EK])
                new_dial[EK_INTENT] = self.dict_to_str(new_dial[EK_ORI][INTENT_EK])
                # adding prompt for each dialog
                new_dial[PROMPT] = generate_prompt(data_name, domains)
                # finish and wrap the current dialog
                new_data[new_dial_id] = new_dial
                if (dial_idx) % 1000 == 0 or dial_idx == len(data):
                    self.save_dial(new_data, data_name=data_name, file_idx=file_idx, mode=mode)
                    new_data = {} # reset
                    file_idx += 1
                dial_idx += 1
    
            if mode == "train": self.save_original_examples([data[key] for key in list(data.keys())[:5]], data_name)

            print(f"finishing processing {dial_idx} dialogs for {mode} set ...")
        self.save_converted_examples(data_name)
        self.copy_related_files(data_name, exp_list)
        print("*"*10, f"finishing processing dataset {data_name}", "*"*10)


    def metalwoz(self):
        """
        system side starts first
        """
        data_name, exp_list = "MetaLWOZ", []
        for mode in ["train", "test"]:
            if mode == "train":
                real_name = "dialogues"
                exp_list.append(real_name)
            else:
                real_name = "MetalWOZ-Test-v1/dstc8_metalwoz_heldout/dialogues"
                exp_list.append("MetalWOZ-Test-v1")
            dir_path = os.path.join(self.data_dir, data_name, real_name)

            data = self._load_dir_txt(dir_path)
            new_data = {}
            file_idx = 1
            for dial_idx, dial_str in enumerate(data):
                dial = json.loads(dial_str)
                new_dial_id = f"{data_name}--{mode}--{dial_idx+1}"
                new_dial = self.init_dial(dial_idx=dial_idx+1) # idx starts from 1
                new_dial[ORI_DIAL_ID] = dial['id']
                for key in dial:
                    if key in ["turns"]: continue
                    new_dial[ORI_DIAL_INFO][key] = dial[key]

                dial_hist, new_turn = [], self.init_turn(turn_id=1)
                for idx, utt in enumerate(dial["turns"]):
                    if not idx: continue
                    if idx % 2 == 0:
                        # the first turn start from system
                        new_turn[SYS_UTT] = utt
                        # turn must end at assistant side
                        new_dial[LOG].append(new_turn)
                        # include system response into dialog history
                        dial_hist.append(f"<SYSTEM> {utt}")
                    else:
                        # a new turn (except the first) start from user
                        new_turn = self.init_turn(turn_id=(idx+1)//2)
                        new_turn[USR_UTT] = utt
                        new_turn[DIAL_HIST] = " ".join(dial_hist)
                        # include user utterance into dialog history
                        dial_hist.append(f"<USER> {utt}")
                        # dialog ends at user side
                        if idx == len(dial["turns"]) - 1:
                            new_dial[LOG].append(new_turn)

                # adding prompt for each dialog
                domains = [dial["domain"].lower()]
                new_dial[PROMPT] = generate_prompt(data_name, domains)
                # finish and wrap the current dialog
                new_data[new_dial_id] = new_dial
                if (dial_idx+1) % 1000 == 0 or dial_idx == len(data)-1:
                    self.save_dial(new_data, data_name=data_name, file_idx=file_idx, mode=mode)
                    new_data = {} # reset
                    file_idx += 1

            if mode == "train": self.save_original_examples(data[:5], data_name)

            print(f"finishing processing {dial_idx} dialogs for {mode} set ...")
        self.save_converted_examples(data_name)
        self.copy_related_files(data_name, exp_list)
        print("*"*10, f"finishing processing dataset {data_name}", "*"*10)


    def star(self):
        """
        1. No train/val/test split is availble
        2. Agents in this dataset includes "User", "UserGuide", "Wizard" and "KnowledgeBase"
        """
        data_name, exp_list = "STAR", []
        for mode in ["train"]:
            dir_path = os.path.join(self.data_dir, data_name, "dialogues")
            exp_list.append("dialogues")
            data = self._load_dir_json(dir_path)
            data.sort(key=lambda x:x["DialogueID"])
            new_data = {}
            file_idx = 1

            for dial_idx, dial in enumerate(data):
                new_dial_id = f"{data_name}--{mode}--{dial_idx+1}"
                new_dial = self.init_dial(dial_idx=dial_idx+1) # idx starts from 1
                new_dial[ORI_DIAL_ID] = dial['DialogueID']
                for key in dial:
                    if key == "Events": continue
                    new_dial[ORI_DIAL_INFO][key] = dial[key]

                dial_hist, turn_id = [], 1
                for idx, turn in enumerate(dial["Events"]):
                    # ignore "userguide" and "knowledgebase"
                    if turn["Agent"] not in ["User", "Wizard"] or \
                        turn["Action"] not in ["utter", "pick_suggestion"]: continue
                    utt = turn["Text"]
                    if turn["Agent"] == "User":
                        # new turn start from user
                        new_turn = self.init_turn(turn_id=turn_id)
                        new_turn[USR_UTT] = utt
                        new_turn[DIAL_HIST] = " ".join(dial_hist)
                        # include user utterance into dialog history
                        dial_hist.append(f"<USER> {utt}")
                        # other annotation for user side
                        for key in turn:
                            if key == "Text": continue
                            new_turn[ORI_USR_ANN][key] = turn[key]
                        # dialog ends at user side
                        if idx == len(dial["Events"]) - 1:
                            new_dial[LOG].append(new_turn)

                    if turn["Agent"] == "Wizard":
                        new_turn[SYS_UTT] = utt
                        # include system response into dialog history
                        dial_hist.append(f"<SYSTEM> {utt}")
                        # other annotation for system side
                        for key in turn:
                            if key == "Text": continue
                            new_turn[ORI_SYS_ANN][key] = turn[key]
                        # turn must end at assistant side
                        new_dial[LOG].append(new_turn)
                        turn_id += 1

                # adding prompt for each dialog
                domains = dial["Scenario"]["Domains"]
                if domains == [None]:
                    domains = [dial["Scenario"]["WizardCapabilities"][0]["Task"]]
                new_dial[PROMPT] = generate_prompt(data_name, domains)
                # finish and wrap the current dialog
                new_data[new_dial_id] = new_dial
                if (dial_idx+1) % 1000 == 0 or dial_idx+1 == len(data):
                    self.save_dial(new_data, data_name=data_name, file_idx=file_idx, mode=mode)
                    new_data = {} # reset
                    file_idx += 1
    
            if mode == "train": self.save_original_examples(data[:5], data_name)

        print(f"finishing processing {dial_idx} dialogs for {mode} set ...")
        self.save_converted_examples(data_name)
        self.copy_related_files(data_name, exp_list)
        print("*"*10, f"finishing processing dataset {data_name}", "*"*10)


    def taskmaster1(self):
        data_name = "Taskmaster1"
        path = os.path.join(self.data_dir, data_name, "self-dialogs.json")
        data = self._load_json(path)
        # data.extend(self._load_json(os.path.join(self.data_dir, data_name, "woz-dialogs.json")))
        exp_list = ["self-dialogs.json"]
        split_id, new_data, file_idx, finish_flag, dial_idx = {}, {}, {}, {}, {}
        otgy = self._load_json(os.path.join(self.save_dir, data_name, "otgy.json"))
        for mode in ["train", "val", "test"]:
            real_name = f"{mode}.csv" if mode != "val" else "dev.csv"
            idx_path = os.path.join(self.data_dir, data_name, "train-dev-test", real_name)
            split_id[mode] = self._load_txt(idx_path, split_tok=",\n")
            new_data[mode], file_idx[mode], finish_flag[mode], dial_idx[mode] = {}, 1, 0, 1

        for dial in data:
            new_dial = self.init_dial() # idx starts from 1
            new_dial[ORI_DIAL_ID] = dial['conversation_id']
            new_dial[ORI_DIAL_INFO]["instruction_id"] = dial["instruction_id"]
            dial_hist, dst_dict = [], {}
            domain = dial["instruction_id"].split("-")[0]
            usr_utts, sys_utts, turn_id = [], [], 2
            new_turn = self.init_turn()
            for idx, turn in enumerate(dial["utterances"]):
                utt = turn["text"]
                if turn["speaker"] == "USER": # user side
                    if idx and dial["utterances"][idx-1]["speaker"] == "ASSISTANT":
                        # wrap up the previous turn
                        new_turn[USR_UTT] = " ".join(usr_utts)
                        new_turn[SYS_UTT] = " ".join(sys_utts)
                        if usr_utts and sys_utts:
                            new_dial[LOG].append(new_turn)
                            dial_hist.append(f"<USER> {new_turn[USR_UTT]}")
                            dial_hist.append(f"<SYSTEM> {new_turn[SYS_UTT]}")
                            # initialize a new turn
                            new_turn = self.init_turn(turn_id=turn_id)
                            new_turn[DIAL_HIST] = " ".join(dial_hist)
                            turn_id += 1
                            usr_utts, sys_utts = [], []
                    usr_utts.append(utt)
                    # dial_hist.append(f"<USER> {utt}")
                    new_turn[ORI_USR_ANN]['speaker'] = turn["speaker"]
                    slot_list = []
                    if "segments" in turn:
                        new_turn[ORI_USR_ANN]['speaker'] = turn["segments"]
                        # add output for dst task (only accumulated dst provided)
                        for segment in turn["segments"]:
                            slot_value = segment["text"].replace(",","")
                            if len(segment["annotations"][0]["name"].split(".")) == 2:
                                slot_type = segment["annotations"][0]["name"].split(".")[1]
                            else:
                                slot1, dom = segment["annotations"][0]["name"].split(".")[1], segment["annotations"][0]["name"].split(".")[2]
                                if dom == domain:
                                    slot_type = slot1
                                else:
                                    slot_type = f"{dom}_{slot1}"
                            slot_list.append(f"{domain} {slot_type} {slot_value}")
                    new_turn[DST] = ", ".join(slot_list)
                    # accumulate dst output
                    dst_dict = self.update_with_slot_list(dst_dict, slot_list)
                    new_turn[DST_ACC] = self.dst_dict_to_str(dst_dict)

                else: # system side
                    if idx == 0 : continue
                    sys_utts.append(utt)
                    # new_turn[SYS_UTT] = utt
                    # dial_hist.append(f"<SYSTEM> {utt}")
                    new_turn[ORI_SYS_ANN]['speaker'] = turn["speaker"]
                    new_turn[ORI_SYS_ANN]['segments'] = []
                    if "segments" in turn:
                        new_turn[ORI_SYS_ANN]['segments'] = turn["segments"]
                    new_turn[EK] = self.dict_to_str(new_turn[ORI_SYS_ANN]["segments"])
                    new_turn[EK_ORI] = new_turn[ORI_SYS_ANN]["segments"]
                if idx+1 == len(dial["utterances"]) and usr_utts and sys_utts:
                    new_turn[USR_UTT] = " ".join(usr_utts)
                    new_turn[SYS_UTT] = " ".join(sys_utts)
                    new_dial[LOG].append(new_turn)
                    turn_id += 1
                    usr_utts, sys_utts = [], []
            # adding EK for DST task
            new_dial[EK_ORI][DST_EK] = {domain: otgy["slots"][domain]}
            for slot in new_dial[EK_ORI][DST_EK][domain]:
                if len(new_dial[EK_ORI][DST_EK][domain][slot]) > DST_LENGTH:
                    new_dial[EK_ORI][DST_EK][domain][slot] = random.choices(otgy["slots"][domain][slot], k=DST_LENGTH//2)
            
            # turn the external knowledge into a flat string
            new_dial[EK] = self.dict_to_str(new_dial[EK_ORI][TOD_EK])
            new_dial[EK_DST] = self.dict_to_str(new_dial[EK_ORI][DST_EK])
            new_dial[EK_INTENT] = self.dict_to_str(new_dial[EK_ORI][INTENT_EK])
            # adding prompt for each dialog
            domains = [domain]
            new_dial[PROMPT] = generate_prompt(data_name, domains)
            # finish and wrap the current dialog

            mode = "train"
            for mode_option in ["val", "test"]:
                if dial["conversation_id"] in split_id[mode_option]:
                    mode = mode_option
            new_dial_id = f"{data_name}--{mode}--{dial_idx[mode]}"
            new_dial[DIAL_IDX] = dial_idx[mode]
            dial_idx[mode] += 1
            new_data[mode][new_dial_id] = new_dial
            if not new_dial[LOG]:
                pdb.set_trace()
            if len(new_data[mode]) == 1000:
                self.save_dial(new_data[mode], data_name=data_name, file_idx=file_idx[mode], mode=mode)
                new_data[mode] = {} # reset
                file_idx[mode] += 1
                finish_flag[mode] = 1
            else:
                finish_flag[mode] = 0

        # if there are some unsaved dialogs left, save it now
        for mode in ["train", "val", "test"]:
            if not finish_flag[mode]:
                self.save_dial(new_data[mode], data_name=data_name, file_idx=file_idx[mode], mode=mode)
            print(f"finishing processing {dial_idx[mode]} dialogs for {mode} set ...")

        self.save_original_examples(data[:5], data_name)
        self.save_converted_examples(data_name)
        self.copy_related_files(data_name, exp_list)
        print("*"*10, f"finishing processing dataset {data_name}", "*"*10)


    def taskmaster2(self):
        """
        user/system side utterances are separated into sentences
        """
        data_name = "Taskmaster2"
        dir_path, exp_list = os.path.join(self.data_dir, data_name, "data"), ["data"]
        data = self._load_dir_json(dir_path)
        new_data, file_idx, mode = {}, 1, "train"
        otgy = self._load_json(os.path.join(self.save_dir, data_name, "otgy.json"))

        for dial_idx, dial in enumerate(data):
            new_dial_id = f"{data_name}--{mode}--{dial_idx+1}"
            new_dial = self.init_dial(dial_idx=dial_idx+1) # idx starts from 1
            new_dial[ORI_DIAL_ID] = dial['conversation_id']
            # if new_dial[ORI_DIAL_ID] == "dlg-bcc6972e-13e0-4c70-b703-8197ebfb388b":
            #     pdb.set_trace()
            new_dial[ORI_DIAL_INFO]["instruction_id"] = dial["instruction_id"]

            domain = dial["instruction_id"].split("-")[0]
            dial_hist, turn_id, usr_utt_list, sys_utt_list, dst_dict = [], 1, [], [], {}
            for idx, turn in enumerate(dial["utterances"]):
                if turn["speaker"] == "USER":
                    # finish previous turn
                    if sys_utt_list:
                        new_turn[SYS_UTT] = " ".join(sys_utt_list)
                        dial_hist.append("<SYSTEM> " + new_turn[SYS_UTT])
                        new_turn[EK_ORI] = new_turn[ORI_SYS_ANN]['segments'] if 'segments' in new_turn[ORI_SYS_ANN] else []
                        new_turn[EK] = self.dict_to_str(new_turn[EK_ORI])
                        new_dial[LOG].append(new_turn)
                        turn_id += 1
                        sys_utt_list = []
                    if not usr_utt_list:
                        # initialize a new turn for the following
                        new_turn = self.init_turn(turn_id=turn_id)
                        new_turn[DIAL_HIST] = " ".join(dial_hist)

                    usr_utt_list.append(turn["text"])
                    new_turn[ORI_USR_ANN]['speaker'] = turn["speaker"]
                    slot_list = []
                    if "segments" in turn:
                        if "segments" not in new_turn[ORI_USR_ANN]:
                            new_turn[ORI_USR_ANN]['segments'] = []
                        new_turn[ORI_USR_ANN]['segments'].extend(turn["segments"])
                        # add output for dst task (only accumulated dst provided)
                        for segment in turn["segments"]:
                            slot_value = segment["text"].replace(",","")
                            if len(segment["annotations"][0]["name"].split(".")) == 2:
                                slot_type = segment["annotations"][0]["name"].split(".")[1]
                            else:
                                slot1, dom = segment["annotations"][0]["name"].split(".")[1], segment["annotations"][0]["name"].split(".")[2]
                                if dom == domain:
                                    slot_type = slot1
                                else:
                                    slot_type = f"{dom}_{slot1}"
                            slot_list.append(f"{domain} {slot_type} {slot_value}")
                    new_turn[DST] = ", ".join(slot_list)
                    # accumulate dst output
                    dst_dict = self.update_with_slot_list(dst_dict, slot_list)
                    new_turn[DST_ACC] = self.dst_dict_to_str(dst_dict)

                if turn["speaker"] == "ASSISTANT": # system side
                    # process previous user side utt
                    if usr_utt_list: # process only for the first system side turn
                        new_turn[USR_UTT] = " ".join(usr_utt_list)
                        dial_hist.append("<USER> " + new_turn[USR_UTT])
                        usr_utt_list = []
                    if not dial_hist: # skip for the first turn
                        continue

                    # record system side info
                    sys_utt_list.append(turn["text"])
                    new_turn[ORI_SYS_ANN]["speaker"] = turn["speaker"]
                    if "segments" not in new_turn[ORI_SYS_ANN]:
                        new_turn[ORI_SYS_ANN]['segments'] = []
                    if "segments" in turn:
                        new_turn[ORI_SYS_ANN]['segments'].extend(turn["segments"])

            if usr_utt_list:
                new_turn[USR_UTT] = " ".join(usr_utt_list)
            if sys_utt_list:
                new_turn[SYS_UTT] = " ".join(sys_utt_list)
                new_turn[EK_ORI] = new_turn[ORI_SYS_ANN]["segments"]
                new_turn[EK] = self.dict_to_str(new_turn[EK_ORI])
                new_dial[LOG].append(new_turn)

            # adding EK for DST task
            new_dial[EK_ORI][DST_EK] = {domain: otgy["slots"][domain]}
            for slot in new_dial[EK_ORI][DST_EK][domain]:
                if len(new_dial[EK_ORI][DST_EK][domain][slot]) > DST_LENGTH:
                    new_dial[EK_ORI][DST_EK][domain][slot] = random.choices(otgy["slots"][domain][slot], k=DST_LENGTH//2)

            # turn the external knowledge into a flat string
            new_dial[EK] = self.dict_to_str(new_dial[EK_ORI][TOD_EK])
            new_dial[EK_DST] = self.dict_to_str(new_dial[EK_ORI][DST_EK])
            new_dial[EK_INTENT] = self.dict_to_str(new_dial[EK_ORI][INTENT_EK])
            # adding prompt for each dialog
            domains = [dial["filename"]]
            new_dial[PROMPT] = generate_prompt(data_name, domains)
            # finish and wrap the current dialog
            new_data[new_dial_id] = new_dial

            if (dial_idx+1) % 1000 == 0 or dial_idx+1 == len(data):
                self.save_dial(new_data, data_name=data_name, file_idx=file_idx, mode=mode)
                new_data = {} # reset
                file_idx += 1

        print(f"finishing processing {dial_idx} dialogs for {mode} set ...")
        self.save_original_examples(data[:5], data_name)
        self.save_converted_examples(data_name)
        self.copy_related_files(data_name, exp_list)
        print("*"*10, f"finishing processing dataset {data_name}", "*"*10)


    def taskmaster3(self):
        """
        for set split
         # some id exist in more than one set
         # some id does not exist in any set
         # almost all val dialog exists in train split set
         # therefore we set up val and test set first, and dump all left to train
         # Since val and test only have 3 / 1 unique dialog
         # we set test val with a size of 2000
         # and consider the rest dialogs as train data"""
        data_name = "Taskmaster3"
        dir_path = os.path.join(self.data_dir, data_name, "data")
        data = self._load_dir_json(dir_path)
        exp_list = ["data", "splits"]
        split_id, new_data, file_idx, finish_flag, dial_idx = {}, {}, {}, {}, {}
        otgy = self._load_json(os.path.join(self.data_dir, data_name, "otgy.json"))

        for mode in ["train", "val", "test"]:
            real_name = mode if mode != "val" else "dev"
            split_dir = os.path.join(self.data_dir, data_name, "splits", real_name)
            split_file = self._load_dir_txt(dir_path=split_dir, file_type="tsv")
            split_id[mode] = []
            for line in split_file:
                split_id[mode].append(line.split()[-1])
            new_data[mode], file_idx[mode], finish_flag[mode], dial_idx[mode] = {}, 1, 0, 1

        for dial in tqdm(data):
            new_dial = self.init_dial() # idx starts from 1
            new_dial[ORI_DIAL_ID] = dial['conversation_id']
            domain = "movie"
            for key in ["vertical", "scenario", "instructions"]:
                new_dial[ORI_DIAL_INFO][key] = dial[key]
            dial_hist, dst_dict = [], {}
            usr_utts, sys_utts, turn_id = [], [], 2
            new_turn = self.init_turn()
            for idx, turn in enumerate(dial["utterances"]):
                utt = turn["text"]
                if turn["speaker"] == "user":
                    if idx and  dial["utterances"][idx-1]["speaker"] == "assistant":
                        # wrap up the previous turn
                        new_turn[USR_UTT] = " ".join(usr_utts)
                        new_turn[SYS_UTT] = " ".join(sys_utts)
                        if usr_utts and sys_utts:
                            new_dial[LOG].append(new_turn)
                            dial_hist.append(f"<USER> {new_turn[USR_UTT]}")
                            dial_hist.append(f"<SYSTEM> {new_turn[SYS_UTT]}")
                            # initialize a new turn
                            new_turn = self.init_turn(turn_id=turn_id)
                            new_turn[DIAL_HIST] = " ".join(dial_hist)
                            turn_id += 1
                            usr_utts, sys_utts = [], []
                    usr_utts.append(utt)
                    for key in turn:
                        if key in ["text", "speaker", "index"]: continue
                        new_turn[ORI_USR_ANN][key] = turn[key]
                    # dial_hist.append(f"<USER> {utt}")

                    slot_list = []
                    if "segments" in turn:
                        # add output for dst task (only accumulated dst provided)
                        for segment in turn["segments"]:
                            slot_value = segment["text"].replace(",","") # remove ",", because we use "," to separate slot triplet
                            if len(segment["annotations"][0]["name"].split(".")) == 1:
                                slot_type = segment["annotations"][0]["name"]
                            else:
                                slot1, dom = segment["annotations"][0]["name"].split(".")[0], segment["annotations"][0]["name"].split(".")[1]
                                if dom == domain:
                                    slot_type = slot1
                                else:
                                    slot_type = f"{dom}_{slot1}"
                            slot_list.append(f"{domain} {slot_type} {slot_value}")
                    new_turn[DST] = ", ".join(slot_list)
                    # accumulate dst output
                    dst_dict = self.update_with_slot_list(dst_dict, slot_list)
                    new_turn[DST_ACC] = self.dst_dict_to_str(dst_dict)

                else: # system side
                    if idx == 0 : continue
                    sys_utts.append(utt)
                    # new_turn[SYS_UTT] = utt
                    # dial_hist.append(f"<SYSTEM> {utt}")
                    new_turn[ORI_SYS_ANN]["segments"] = []
                    if "segments" in turn:
                        new_turn[ORI_SYS_ANN]["segments"] = turn["segments"]
                    new_turn[EK] = self.dict_to_str(new_turn[ORI_SYS_ANN]["segments"])
                    new_turn[EK_ORI] = new_turn[ORI_SYS_ANN]["segments"]

                if idx+1 == len(dial["utterances"]) and usr_utts and sys_utts:
                    new_turn[USR_UTT] = " ".join(usr_utts)
                    new_turn[SYS_UTT] = " ".join(sys_utts)
                    new_dial[LOG].append(new_turn)
                    turn_id += 1
                    usr_utts, sys_utts = [], []

            # adding EK for DST task
            new_dial[EK_ORI][DST_EK] = {domain: otgy["slots"][domain]}
            for slot in new_dial[EK_ORI][DST_EK][domain]:
                if len(new_dial[EK_ORI][DST_EK][domain][slot]) > DST_LENGTH:
                    new_dial[EK_ORI][DST_EK][domain][slot] = random.choices(otgy["slots"][domain][slot], k=DST_LENGTH//2)
            
            # turn the external knowledge into a flat string
            new_dial[EK] = self.dict_to_str(new_dial[EK_ORI][TOD_EK])
            new_dial[EK_DST] = self.dict_to_str(new_dial[EK_ORI][DST_EK])
            new_dial[EK_INTENT] = self.dict_to_str(new_dial[EK_ORI][INTENT_EK])
            # adding prompt for each dialog
            domains = ["movie"]
            new_dial[PROMPT] = generate_prompt(data_name, domains)
            # finish and wrap the current dialog

            if dial["conversation_id"] in split_id["val"] and \
                dial["conversation_id"] not in split_id["train"]:
                mode = "val"
            elif dial["conversation_id"] in split_id["test"] and \
                dial["conversation_id"] not in split_id["train"]:
                mode = "test"
            elif dial["conversation_id"] in split_id["val"] and dial_idx["val"] < 2000:
                mode = "val"
            elif dial["conversation_id"] in split_id["test"] and dial_idx["test"] < 2000:
                mode = "test"
            else:
                mode = "train"
            new_dial_id = f"{data_name}--{mode}--{dial_idx[mode]}"
            new_dial[DIAL_IDX] = dial_idx[mode]
            dial_idx[mode] += 1
            new_data[mode][new_dial_id] = new_dial
            if len(new_data[mode]) == 1000:
                self.save_dial(new_data[mode], data_name=data_name, file_idx=file_idx[mode], mode=mode)
                new_data[mode] = {} # reset
                file_idx[mode] += 1
                finish_flag[mode] = 1
            else:
                finish_flag[mode] = 0
                

        # if there are some unsaved dialogs left, save it now
        for mode in ["train", "val", "test"]:
            if not finish_flag[mode]:
                self.save_dial(new_data[mode], data_name=data_name, file_idx=file_idx[mode], mode=mode)

            print(f"finishing processing {dial_idx[mode]} dialogs for {mode} set ...")
        self.save_original_examples(data[:5], data_name)
        self.save_converted_examples(data_name)
        self.copy_related_files(data_name, exp_list)
        print("*"*10, f"finishing processing dataset {data_name}", "*"*10)


    def simjoint(self):
        """
        original turn format leads by system side
        """
        for data_name in ["SimJointMovie", "SimJointRestaurant"]:
            exp_list = []
            otgy = self._load_json(os.path.join(self.save_dir, data_name, "otgy.json"))
            domain = "movie" if data_name == "SimJointMovie" else "restaurant"
            for mode in ["train", "val", "test"]:
                real_name = f"{mode}.json" if mode != "val" else "dev.json"
                path = os.path.join(self.data_dir, data_name, real_name)
                exp_list.append(real_name)

                data = self._load_json(path)
                new_data = {}
                file_idx = 1

                for dial_idx, dial in enumerate(data):
                    new_dial_id = f"{data_name}--{mode}--{dial_idx+1}"
                    new_dial = self.init_dial(dial_idx=dial_idx+1) # idx starts from 1
                    new_dial[ORI_DIAL_ID] = dial["dialogue_id"]
                    dial_hist, dst_dict = [], {}
                    for idx, turn in enumerate(dial["turns"]):
                        if "system_utterance" in turn:
                            new_turn[SYS_UTT] = turn["system_utterance"]["text"]
                            for key in ["system_acts", "system_utterance"]:
                                new_turn[ORI_SYS_ANN][key] = turn[key]
                            dial_hist.append("<SYSTEM> " + new_turn[SYS_UTT])
                            new_dial[LOG].append(new_turn)

                        if "user_utterance" in turn:
                            new_turn = self.init_turn(turn_id=idx+1)
                            new_turn[USR_UTT] = turn["user_utterance"]["text"]
                            new_turn[DIAL_HIST] = " ".join(dial_hist)
                            for key in ["dialogue_state", "user_acts", "user_intents", "user_utterance"]:
                                if key in turn:
                                    new_turn[ORI_USR_ANN][key] = turn[key]
                            # adding dst output
                            slot_list = []
                            for slot in turn["user_utterance"]["slots"]:
                                slot_type = slot["slot"]
                                slot_value = " ".join(turn["user_utterance"]["tokens"][slot["start"]:slot["exclusive_end"]])
                                slot_list.append(f"{domain} {slot_type} {slot_value}")
                            new_turn[DST] = ", ".join(slot_list)
                            # accumulate dst output
                            dst_dict = self.update_with_slot_list(dst_dict, slot_list)
                            new_turn[DST_ACC] = self.dst_dict_to_str(dst_dict)
                            # adding intent prediction output
                            # if len(turn["user_acts"]) > 1: pdb.set_trace() # checked: yes
                            intent_list = [intent["type"] for intent in turn["user_acts"]]
                            new_turn[INTENT] = ", ".join(intent_list)
                            dial_hist.append("<USER> " + new_turn[USR_UTT])
                    if not new_turn[SYS_UTT]:
                        new_dial[LOG].append(new_turn)

                    # adding EK for Intent Prediction
                    new_dial[EK_ORI][INTENT_EK] = {domain:otgy["intents"]}
                    # adding EK for DST task
                    new_dial[EK_ORI][DST_EK] = {domain: otgy["slots"]}
                    for slot in new_dial[EK_ORI][DST_EK][domain]:
                        if len(new_dial[EK_ORI][DST_EK][domain][slot]) > 2*DST_LENGTH:
                            new_dial[EK_ORI][DST_EK][domain][slot] = random.choices(otgy["slots"][slot], k=DST_LENGTH)
                    # turn the external knowledge into a flat string
                    new_dial[EK] = self.dict_to_str(new_dial[EK_ORI][TOD_EK])
                    new_dial[EK_DST] = self.dict_to_str(new_dial[EK_ORI][DST_EK])
                    new_dial[EK_INTENT] = self.dict_to_str(new_dial[EK_ORI][INTENT_EK])
                    # adding prompt for each dialog
                    domains = [domain]
                    new_dial[PROMPT] = generate_prompt(data_name, domains)
                    # finish and wrap the current dialog
                    new_data[new_dial_id] = new_dial
                    if (dial_idx+1) % 1000 == 0 or dial_idx+1 == len(data):
                        self.save_dial(new_data, data_name=data_name, file_idx=file_idx, mode=mode)
                        new_data = {} # reset
                        file_idx += 1
        
                if mode == "train": self.save_original_examples(data[:5], data_name)

                print(f"finishing processing {len(data)} dialogs for {mode} set ...")
            self.save_converted_examples(data_name)
            self.copy_related_files(data_name, exp_list)
            print("*"*10, f"finishing processing dataset {data_name}", "*"*10)


    def simjointgen(self):
        """
        original turn format leads by system side
        but our format should end by system side
        """
        data_name = "SimJointGEN"
        exp_list = ["data"]
        otgy = self._load_json(os.path.join(self.data_dir, data_name, "data/db.json"))
        domain = "movie"
        for mode in ["train", "val", "test"]:
            real_name = f"{mode}.json" if mode != "val" else "dev.json"
            path = os.path.join(self.data_dir, data_name, "data", real_name)

            data = self._load_json(path)
            new_data = {}
            file_idx = 1

            for dial_idx, dial in tqdm(enumerate(data)):
                new_dial_id = f"{data_name}--{mode}--{dial_idx+1}"
                new_dial = self.init_dial(dial_idx=dial_idx+1) # idx starts from 1
                new_dial[ORI_DIAL_ID] = dial["dialogue_id"]
                dial_hist, prev_slot_list = [], []

                # init the first turn, which would contain only system utt
                new_turn = self.init_turn(turn_id=1)
                for idx, turn in enumerate(dial["turns"]):
                    if "system_utterance" in turn: # turn ends at system side
                        new_turn[SYS_UTT] = turn["system_utterance"]
                        new_turn[ORI_SYS_ANN]["system_acts"] = turn["system_acts"]
                        dial_hist.append("<SYSTEM> " + new_turn[SYS_UTT])
                        dial_hist.append("<USER> " + new_turn[USR_UTT])
                        new_dial[LOG].append(new_turn)

                    if "user_utterance" in turn: # turn starts at user side
                        new_turn = self.init_turn(turn_id=idx+2)
                        new_turn[USR_UTT] = turn["user_utterance"]
                        new_turn[DIAL_HIST] = " ".join(dial_hist)
                        for key in ["dialogue_state", "database_state"]:
                            if key in turn:
                                new_turn[ORI_USR_ANN][key] = turn[key]
                        # add output for accumulated dst task (only accumulated dst provided)
                        slot_list = []
                        for slot_type, slot_value in turn["dialogue_state"].items():
                            slot_list.append(f"{domain} {slot_type} {slot_value}")
                        new_turn[DST_ACC] = ", ".join(slot_list)
                        # add output for current turn dst task
                        current_slot_list = []
                        for slot_type, slot_value in turn["dialogue_state"].items():
                            slot = f"{domain} {slot_type} {slot_value}"
                            if slot in prev_slot_list: continue
                            current_slot_list.append(slot)
                        new_turn[DST] = ", ".join(current_slot_list)
                        prev_slot_list = current_slot_list

                if not new_turn[SYS_UTT]:
                    new_dial[LOG].append(new_turn)

                # adding EK for DST task
                new_dial[EK_ORI][DST_EK] = {domain: otgy}
                for slot in new_dial[EK_ORI][DST_EK][domain]:
                    if len(new_dial[EK_ORI][DST_EK][domain][slot]) > 2*DST_LENGTH:
                        new_dial[EK_ORI][DST_EK][domain][slot] = random.choices(otgy[slot], k=DST_LENGTH)
                # turn the external knowledge into a flat string
                new_dial[EK] = self.dict_to_str(new_dial[EK_ORI][TOD_EK])
                new_dial[EK_DST] = self.dict_to_str(new_dial[EK_ORI][DST_EK])
                new_dial[EK_INTENT] = self.dict_to_str(new_dial[EK_ORI][INTENT_EK])
                # adding prompt for each dialog
                domains = ["movie"]
                new_dial[PROMPT] = generate_prompt(data_name, domains)
                # finish and wrap the current dialog
                new_data[new_dial_id] = new_dial
                if (dial_idx+1) % 1000 == 0 or dial_idx+1 == len(data):
                    self.save_dial(new_data, data_name=data_name, file_idx=file_idx, mode=mode)
                    new_data = {} # reset
                    file_idx += 1
    
            if mode == "train": self.save_original_examples(data[:5], data_name)

            print(f"finishing processing {len(data)} dialogs for {mode} set ...")
        self.save_converted_examples(data_name)
        self.copy_related_files(data_name, exp_list)
        self.copy_general(os.path.join(self.data_dir, data_name, "data", "db.json"), os.path.join(self.save_dir, data_name, "db.json"))
        print("*"*10, f"finishing processing dataset {data_name}", "*"*10)


    def muldogo(self):
        """
        raw data in ./data/unannotated/${domain}.tsv in format of:
            conversationId,turnNumber,utteranceId,utterance,authorRole
            acs-31971762-f14e-4d55-b909-0370f6e4db19-1,0,acs-2571cf40-4e39-46b6-940c-7b8cce559bae,HI GOOD MORNING,customer
        split and annotation in ./data/paper_splits/splits_annotated_at_turn_level/${domain}/[train/dev/test].tsv in format of:
            conversationId  turnNumber  utteranceId utterance   slot-labels intent
            31971762-f14e-4d55-b909-0370f6e4db19    0   <CONV>31971762-f14e-4d55-b909-0370f6e4db19<TURN>0   hi good morning O O O   openinggreeting

        1. conversationId in raw has prefix (acs-) and suffix (-1/-2)
        2. user/system turn can be consecutive
        3. not all data have been annotated
        4. split in sentence level is different from that in turn level. use turn level split for now
        """
        data_name = "MulDoGO"
        dir_dial = os.path.join(self.data_dir, data_name, "data/unannotated")
        dir_split = os.path.join(self.data_dir, data_name, "data/paper_splits/splits_annotated_at_turn_level")
        data = self._load_dir_tsv(dir_dial, sep=",")
        split_annotation, new_data, file_idx, finish_flag, dial_idx = {}, {}, {}, {}, {}
        exp_list = ["data"]

        for mode in ["train", "val", "test"]:
            real_name = mode if mode != "val" else "dev"
            split_annotation[mode] = None
            for domain in sorted(os.listdir(dir_split)):
                split_file = self._load_csv(os.path.join(dir_split, domain, f"{real_name}.tsv"))
                split_file["domain"] = domain
                split_annotation[mode] = pd.concat([split_annotation[mode], split_file], ignore_index=True)
            new_data[mode], file_idx[mode], finish_flag[mode], dial_idx[mode] = {}, 1, 0, 1

        new_dial = None
        for idx, turn in tqdm(data.iterrows()):
            if turn.conversationId.endswith("2"): continue # repeated conversation
            dial_id = turn.conversationId[:-2]
            if dial_id.startswith("acs-"): dial_id = dial_id[4:]
            # init a new dial for the current and following turns
            if new_dial is None:
                annotate_flag = 0
                for mode in ["val", "test", "train"]:
                    if dial_id in split_annotation[mode]['conversationId'].values:
                        annotate_flag = 1
                        index = split_annotation[mode][split_annotation[mode]['conversationId']==dial_id].index[0]
                        domain_ = split_annotation[mode]["domain"][index]
                        # pdb.set_trace()
                        break
                new_dial_id = f"{data_name}--{mode}--{dial_idx[mode]}"
                new_dial = self.init_dial(dial_idx=dial_idx[mode])
                new_dial[ORI_DIAL_ID] = dial_id
                new_dial[ORI_DIAL_INFO]["domain"] = domain_
                turn_id, dial_hist = 1, []
                new_turn = self.init_turn(turn_id=turn_id)

            # continue extending the current dial
            if turn.authorRole == "customer":
                # adding utterances 
                new_turn[USR_UTT] += f" {turn.utterance}"
                new_turn[USR_UTT] = new_turn[USR_UTT].strip()
                # adding annotation for turn level
                if annotate_flag:
                    utt_id = f"<CONV>{dial_id}<TURN>{turn.turnNumber}"
                    row = split_annotation[mode][split_annotation[mode]["utteranceId"]==utt_id]
                    # pdb.set_trace()
                    new_turn[ORI_USR_ANN]["slot-labels"] = row["slot-labels"].tolist()
                    new_turn[ORI_USR_ANN]["intent"] = row["intent"].values.tolist()

            elif turn.authorRole == "agent":
                # no annotation on system side
                new_turn[SYS_UTT] += f" {turn.utterance}"
                new_turn[SYS_UTT] = new_turn[SYS_UTT].strip()

                # wrap up turn
                if idx == len(data)-1 or data.authorRole[idx+1] != "agent":
                    new_dial[LOG].append(new_turn)
                    turn_id += 1
                    dial_hist.append("<USER> " + new_turn[USR_UTT])
                    dial_hist.append("<SYSTEM> " + new_turn[SYS_UTT])
                    new_turn = self.init_turn(turn_id=turn_id)
                    new_turn[DIAL_HIST] = " ".join(dial_hist)

            # wrap up dial (add new dial to new data)
            if idx == len(data)-1 or dial_id not in data.conversationId[idx+1]:
                # adding prompt for each dialog
                domains = [turn["filename"]]
                new_dial[PROMPT] = generate_prompt(data_name, domains)
                # finish and wrap the current dialog
                if new_dial[LOG]:
                    new_data[mode][new_dial_id] = new_dial
                    dial_idx[mode] += 1
                new_dial = None

                if len(new_data[mode]) == 1000:
                    self.save_dial(new_data[mode], data_name=data_name, file_idx=file_idx[mode], mode=mode)
                    new_data[mode] = {} # reset
                    file_idx[mode] += 1
                    finish_flag[mode] = 1
                else:
                    finish_flag[mode] = 0

        # if there are some unsaved dialogs left, save it now
        for mode in ["train", "val", "test"]:
            if not finish_flag[mode]:
                self.save_dial(new_data[mode], data_name=data_name, file_idx=file_idx[mode], mode=mode)
            print(f"finishing processing {dial_idx[mode]} dialogs for {mode} set ...")
        
        self.save_original_examples(data[:6].to_string(index=False).split('\n'), data_name)
        self.save_converted_examples(data_name)
        self.copy_related_files(data_name, exp_list)
        print("*"*10, f"finishing processing dataset {data_name}", "*"*10)


    def casino(self):
        """
        1. operation like "Submit-Deal","Accept-Deal" and "Reject-Deal" inlcuded in the "chat-log"
        we move them to dialog-level annotation: new_dial[ORI_DIAL_INFO]["result"] = [turn1, turn2, ...]
        2. no user/system but mturk_agent_1/2, and either might start the dialog. Therefore, we consider
        whoever starts the dialog as user.
        3. no consecutive turn from the same side
        4. xxx-Deal can happens during the dialog
        """
        data_name = "CaSiNo"
        exp_list = ["data"]
        dir_data = os.path.join(self.data_dir, data_name, "data/split")
        for mode in ["train", "val", "test"]:
            real_name = mode if mode != "val" else "valid"
            data = self._load_json(os.path.join(dir_data, f"casino_{real_name}.json"))
            new_data, file_idx = {}, 1
            for dial_idx, dial in tqdm(enumerate(data)):
                new_dial_id = f"{data_name}--{mode}--{dial_idx+1}"
                new_dial = self.init_dial(dial_idx=dial_idx+1) # idx starts from 1
                new_dial[ORI_DIAL_ID] = dial["dialogue_id"]
                new_dial[ORI_DIAL_INFO]["participant_info"] = dial["participant_info"]
                new_dial[ORI_DIAL_INFO]["annotations"] = dial["annotations"]
                new_dial[ORI_DIAL_INFO]["results"] = []
                dial_hist = []
                speaker_user = dial["chat_logs"][0]["id"]
                new_turn = self.init_turn()
                usr_utts, sys_utts, turn_id = [], [], 2

                for idx, turn in enumerate(dial["chat_logs"]):
                    # skip those negotiation decision turns
                    if turn["text"].endswith("-Deal"):
                        new_dial[ORI_DIAL_INFO]["results"].append(turn)
                        continue
                    if turn["id"] == speaker_user:
                        if sys_utts:
                            new_turn[USR_UTT] = " ".join(usr_utts)
                            new_turn[SYS_UTT] = " ".join(sys_utts)
                            new_dial[LOG].append(new_turn)
                            dial_hist.append("<USER> " + new_turn[USR_UTT])
                            dial_hist.append("<SYSTEM> " + new_turn[SYS_UTT])
                            new_turn = self.init_turn(turn_id=turn_id)
                            new_turn[DIAL_HIST] = " ".join(dial_hist)
                            turn_id += 1
                            usr_utts, sys_utts = [], []

                        # if not usr_utts:
                        #     new_turn = self.init_turn(turn_id=turn_id, dial_hist=dial_hist)
                        usr_utts.append(turn["text"])
                        # new_turn[USR_UTT] = turn["text"]
                        new_turn[ORI_USR_ANN] = turn["task_data"]
                        new_turn[ORI_USR_ANN]["speakere"] = turn["id"]
                    else:
                        sys_utts.append(turn["text"])
                        new_turn[ORI_SYS_ANN] = turn["task_data"]
                        new_turn[ORI_SYS_ANN]["speaker"] = turn["id"]

                if usr_utts or sys_utts:
                    new_turn[USR_UTT] = " ".join(usr_utts)
                    new_turn[SYS_UTT] = " ".join(sys_utts)
                    new_dial[LOG].append(new_turn)
                    usr_utts, sys_utts = [], []

                # adding prompt for each dialog
                domains = ["negotiate"]
                new_dial[PROMPT] = generate_prompt(data_name, domains)
                # finish and wrap the current dialog
                new_data[new_dial_id] = new_dial
                if (dial_idx+1) % 1000 == 0 or dial_idx+1 == len(data):
                    self.save_dial(new_data, data_name=data_name, file_idx=file_idx, mode=mode)
                    new_data = {} # reset
                    file_idx += 1
    
            if mode == "train": self.save_original_examples(data[:5], data_name)
            print(f"finishing processing {dial_idx} dialogs for {mode} set ...")
        self.save_converted_examples(data_name)
        self.copy_related_files(data_name, exp_list)
        print("*"*10, f"finishing processing dataset {data_name}", "*"*10)


    def airdialogue(self):
        """
        both user and system can end a dialog. we ignore the last utt if user ends a dialog.
        system side can start a dialog, ignore it
        """
        data_name = "AirDialogue"
        exp_list = ["airdialogue"]
        dir_path = os.path.join(self.data_dir, data_name, "airdialogue")
        for mode in ["val", "train"]:
            real_name = mode if mode != "val" else "dev"
            data = self._load_txt(os.path.join(dir_path, f"{real_name}_data.json"))
            database = self._load_txt(os.path.join(dir_path, f"{real_name}_kb.json"))
            new_data, file_idx = {}, 1

            for dial_idx, dial in tqdm(enumerate(data)):
                dial = json.loads(dial)
                new_dial_id = f"{data_name}--{mode}--{dial_idx+1}"
                new_dial = self.init_dial(dial_idx=dial_idx+1) # idx starts from 1
                for key in dial:
                    if key == "dialogue": continue
                    new_dial[ORI_DIAL_INFO][key] = dial[key]
                dial_hist, turn_id = [], 1
                for idx, turn in enumerate(dial["dialogue"]):
                    speaker, utt = turn.split(": ")[0], ": ".join(turn.split(": ")[1:])
                    if idx == 0 and speaker == "agent": continue
                    if speaker == "customer":
                        new_turn = self.init_turn(turn_id=turn_id, dial_hist=dial_hist)
                        new_turn[USR_UTT] = utt
                    elif speaker == "agent":
                        new_turn[SYS_UTT] = utt
                        new_dial[LOG].append(new_turn)
                        dial_hist.append("<USER> " + new_turn[USR_UTT])
                        dial_hist.append("<SYSTEM> " + new_turn[SYS_UTT])
                        turn_id += 1
                        
                target_fligt_num_list, cands = new_dial[ORI_DIAL_INFO]["action"]["flight"], []
                ek = json.loads(database[dial_idx])
                for flight in ek["kb"]:
                    if flight["flight_number"] in target_fligt_num_list:
                        cands.append(flight)
                while len(cands) < TOD_LENGTH:
                    cand = random.choice(ek["kb"])
                    if cand not in cands:
                        cands.append(cand)
                new_dial[EK_ORI][TOD_EK]["flight"] = cands
                # turn the external knowledge into a flat string
                new_dial[EK] = self.dict_to_str(new_dial[EK_ORI][TOD_EK])
                new_dial[EK_DST] = self.dict_to_str(new_dial[EK_ORI][DST_EK])
                new_dial[EK_INTENT] = self.dict_to_str(new_dial[EK_ORI][INTENT_EK])
                # adding prompt for each dialog
                domains = ["flight"]
                new_dial[PROMPT] = generate_prompt(data_name, domains)
                # finish and wrap the current dialog
                new_data[new_dial_id] = new_dial
                if (dial_idx+1) % 1000 == 0 or dial_idx+1 == len(data):
                    self.save_dial(new_data, data_name=data_name, file_idx=file_idx, mode=mode)
                    new_data = {} # reset
                    file_idx += 1
    
            if mode == "train": self.save_original_examples(data[:5], data_name)

            print(f"finishing processing {dial_idx} dialogs for {mode} set ...")
        self.save_converted_examples(data_name)
        self.copy_related_files(data_name, exp_list)
        self.copy_general(os.path.join(self.data_dir, data_name, "airdialogue", "train_kb.json"), os.path.join(self.save_dir, data_name, "train_kb.json"))
        self.copy_general(os.path.join(self.data_dir, data_name, "airdialogue", "dev_kb.json"), os.path.join(self.save_dir, data_name, "val_kb.json"))
        print("*"*10, f"finishing processing dataset {data_name}", "*"*10)


    def msdc(self):
        """
        1. raw data is not standardized with error:
        pandas.errors.ParserError: Error tokenizing data. C error: Expected 10 fields in line 23317, saw 11
        therefore process as txt file

        2. agent might have consecutive utt at the end of dialog
        """
        data_name = "MS-DC"
        mode, new_data, file_idx, new_dial, dial_idx = "train", {}, 1, None, 1
        otgy = self._load_json(os.path.join(self.save_dir, data_name, "otgy.json"))

        for filename in os.listdir(os.path.join(self.data_dir, data_name)):
            domain = filename.split("_")[0]
            data = self._load_txt(os.path.join(self.data_dir, data_name, filename))[1:]

            for idx, row in tqdm(enumerate(data)):
                [dial_id, turn_id, timestamp, speaker, utt], act = row.strip().split("\t")[:5], row.strip().split("\t")[5:]
                if new_dial is None:
                    # init dialog
                    new_dial_id = f"{data_name}--{mode}--{dial_idx}"
                    new_dial = self.init_dial(dial_idx=dial_idx)
                    new_dial[ORI_DIAL_ID] = dial_id
                    new_dial[ORI_DIAL_INFO]["domain"] = domain
                    dst_dict = {}
                    # init turn
                    turn_idx, prev_speaker, dial_hist = 1, None, []
                    new_turn = self.init_turn(turn_id=turn_idx)
                    new_turn[ORI_USR_ANN]["act"] = []
                    new_turn[ORI_SYS_ANN]["act"] = []

                # continue extending the current dial
                if speaker == "user":
                    # adding utterances 
                    new_turn[USR_UTT] += f" {utt}"
                    new_turn[USR_UTT] = new_turn[USR_UTT].strip()
                    new_turn[ORI_USR_ANN]["act"].extend(act)

                elif speaker == "agent":
                    # no annotation on system side
                    new_turn[SYS_UTT] += f" {utt}"
                    new_turn[SYS_UTT] = new_turn[SYS_UTT].strip()
                    new_turn[ORI_SYS_ANN]["act"].extend(act)

                    # wrap up turn
                    if idx == len(data)-1 or data[idx+1].split("\t")[3] != "agent":
                        # adding output for dst task
                        slot_list = []
                        for act in new_turn[ORI_USR_ANN]["act"]:
                            if act.split("(")[0] not in ["inform", "request"]: continue
                            slots = act.split("(")[1][:-1].replace("?",";").replace("==","=").replace(",",";c").replace("||",";")
                            if slots.startswith("mc_list"): continue
                            for slot in slots.split(";"):
                                if slot == "pickup_location_city=West Roxburystate=MA":
                                    slot_list.append(f"{domain} pickup_location_city West Roxbury")
                                    slot_list.append(f"{domain} state MA")
                                    continue
                                if slot == "date=Apr 2ndstarttime=1pm":
                                    slot_list.append(f"{domain} date Apr 2nd")
                                    slot_list.append(f"{domain} starttime 1pm")
                                    continue
                                if slot == "numberofpeople=2date=tomorrow night":
                                    slot_list.append(f"{domain} numberofpeople 2")
                                    slot_list.append(f"{domain} date tomorrow night")
                                    continue
                                if slot == "city=Washington DCtheater=a regular":
                                    slot_list.append(f"{domain} city Washington DC")
                                    slot_list.append(f"{domain} theater a regular")
                                    continue
                                if "=" in slot:
                                    slot_type = slot.split("=")[0].strip()
                                    slot_value = "=".join(slot.split("=")[1:])
                                    slot_value = slot_value.replace("\\","").replace("{{","{").strip()
                                    if not slot_value: continue
                                    if slot_type in ["result","closing","greeting"]: continue
                                    if slot_type in ["cstate", "ccity", "cdate", "cnumberofpeople", "cstarttime", "cpickup_location_city"]: slot_type = slot_type[1:]
                                    slot_list.append(f"{domain} {slot_type} {slot_value}")
                        new_turn[DST] = ", ".join(slot_list)
                        # accumulate dst output
                        dst_dict = self.update_with_slot_list(dst_dict, slot_list)
                        new_turn[DST_ACC] = self.dst_dict_to_str(dst_dict)
                        # adding output for intents task
                        new_turn[INTENT] = ", ".join([act.split("(")[0] for act in new_turn[ORI_USR_ANN]["act"]])
                        new_dial[LOG].append(new_turn)
                        turn_idx += 1
                        dial_hist.append("<USER> " + new_turn[USR_UTT])
                        dial_hist.append("<SYSTEM> " + new_turn[SYS_UTT])
                        new_turn = self.init_turn(turn_id=turn_idx)
                        new_turn[DIAL_HIST] = " ".join(dial_hist)
                        new_turn[ORI_USR_ANN]["act"] = []
                        new_turn[ORI_SYS_ANN]["act"] = []

                # wrap up dial (add new dial to new data)
                if idx == len(data)-1 or dial_id != data[idx+1].split("\t")[0]:
                    # adding EK for DST task
                    new_dial[EK_ORI][DST_EK] = {domain: otgy["slots"][domain]}
                    for slot in new_dial[EK_ORI][DST_EK][domain]:
                        if len(new_dial[EK_ORI][DST_EK][domain][slot]) > 2*DST_LENGTH:
                            new_dial[EK_ORI][DST_EK][domain][slot] = random.choices(otgy["slots"][domain][slot], k=DST_LENGTH)
                    # adding EK for Intent task
                    new_dial[EK_ORI][INTENT_EK] = {domain: otgy["intents"][domain]}
                    # turn the external knowledge into a flat string
                    new_dial[EK] = self.dict_to_str(new_dial[EK_ORI][TOD_EK])
                    new_dial[EK_DST] = self.dict_to_str(new_dial[EK_ORI][DST_EK])
                    new_dial[EK_INTENT] = self.dict_to_str(new_dial[EK_ORI][INTENT_EK])

                    # adding prompt for each dialog
                    domains = [domain]
                    new_dial[PROMPT] = generate_prompt(data_name, domains)
                    # finish and wrap the current dialog
                    new_data[new_dial_id] = new_dial
                    new_dial = None
                    dial_idx += 1

                    if (dial_idx-1) % 1000 == 0 or dial_idx == len(data):
                        self.save_dial(new_data, data_name=data_name, file_idx=file_idx, mode=mode)
                        new_data = {} # reset
                        file_idx += 1

        print(f"finishing processing {dial_idx} dialogs for {mode} set ...")
        self.save_original_examples(data[:50], data_name)
        self.save_converted_examples(data_name)
        print("*"*10, f"finishing processing dataset {data_name}", "*"*10)


    def abcd(self):
        """
        1. consecutive turns exist, with repeated annotation
        2. conversation starts from agent. Therefore, no user utt is included in the first turn
           "dialog history": "<USER>  <SYSTEM> Hello. How can i help you today?",
        """
        data_name = "ABCD"
        data = self._load_json(os.path.join(self.data_dir, data_name, "data/abcd_v1.1.json"))
        new_data, file_idx, exp_list = {}, {}, ["abcd_v1.1.json"]
        otgy = self._load_json(os.path.join(self.save_dir, data_name, "otgy.json"))

        for real_name, split_data in data.items():
            mode = real_name if real_name != "dev" else "val"
            new_data[mode] = {}
            file_idx[mode] = 1

            for dial_idx, dial in tqdm(enumerate(split_data)):
                # init dialog
                new_dial_id = f"{data_name}--{mode}--{dial_idx+1}"
                new_dial = self.init_dial(dial_idx=dial_idx+1)
                new_dial[ORI_DIAL_ID] = dial["convo_id"]
                new_dial[ORI_DIAL_INFO] = dial["scenario"]
                # init the first turn
                turn_idx, prev_speaker, dial_hist = 1, None, []
                new_turn = self.init_turn(turn_id=turn_idx)
                new_turn[ORI_USR_ANN]["delexed"], new_turn[ORI_SYS_ANN]["delexed"] = [], []
                domain = dial["scenario"]["flow"]
                dst_dict = {}
                for idx, [speaker, utt] in enumerate(dial["original"]):
                    # continue extending the current dial
                    if speaker == "customer":
                        # adding utterances 
                        new_turn[USR_UTT] += f" {utt}"
                        new_turn[USR_UTT] = new_turn[USR_UTT].strip()
                        new_turn[ORI_USR_ANN]["delexed"].append(dial["delexed"][idx])
                        slot_list = []
                        if "<" in dial["delexed"][idx]["text"]:
                            slot_val_list = self.compare_delex(utt, dial["delexed"][idx]["text"])
                            for [slot_value, slot_type] in slot_val_list:
                                if not slot_type.startswith("<") and not slot_type.endswith(">"): continue
                                slot_type = slot_type.split(">")[0].split("<")[-1]
                                slot_list.append(f"{domain} {slot_type} {slot_value}")
                        new_turn[DST] = ", ".join(slot_list)
                        # accumulate dst output
                        dst_dict = self.update_with_slot_list(dst_dict, slot_list)
                        new_turn[DST_ACC] = self.dst_dict_to_str(dst_dict)


                    if speaker == "agent":
                        # no annotation on system side
                        new_turn[SYS_UTT] += f" {utt}"
                        new_turn[SYS_UTT] = new_turn[SYS_UTT].strip()
                        new_turn[ORI_SYS_ANN]["delexed"].append(dial["delexed"][idx])

                        # wrap up turn
                        if idx == len(dial["original"])-1 or dial["original"][idx+1][0] != "agent":
                            new_dial[LOG].append(new_turn)
                            turn_idx += 1
                            if new_turn[USR_UTT]:
                                dial_hist.append("<USER> " + new_turn[USR_UTT])
                            dial_hist.append("<SYSTEM> " + new_turn[SYS_UTT])
                            new_turn = self.init_turn(turn_id=turn_idx)
                            new_turn[DIAL_HIST] = " ".join(dial_hist)
                            new_turn[ORI_USR_ANN]["delexed"], new_turn[ORI_SYS_ANN]["delexed"] = [], []

                # adding EK for DST task
                new_dial[EK_ORI][DST_EK] = {domain: otgy["slots"][domain]}
                for slot in new_dial[EK_ORI][DST_EK][domain]:
                    if len(new_dial[EK_ORI][DST_EK][domain][slot]) > 2*DST_LENGTH:
                        new_dial[EK_ORI][DST_EK][domain][slot] = random.choices(otgy["slots"][domain][slot], k=DST_LENGTH)
                # turn the external knowledge into a flat string
                new_dial[EK] = self.dict_to_str(new_dial[EK_ORI][TOD_EK])
                new_dial[EK_DST] = self.dict_to_str(new_dial[EK_ORI][DST_EK])
                new_dial[EK_INTENT] = self.dict_to_str(new_dial[EK_ORI][INTENT_EK])
                # adding prompt for each dialog
                domains = [dial["scenario"]["flow"]]
                new_dial[PROMPT] = generate_prompt(data_name, domains)
                # finish and wrap the current dialog
                new_data[mode][new_dial_id] = new_dial
                if (dial_idx+1) % 1000 == 0 or dial_idx+1 == len(split_data):
                    self.save_dial(new_data[mode], data_name=data_name, file_idx=file_idx[mode], mode=mode)
                    new_data[mode] = {} # reset
                    file_idx[mode] += 1
    
            if mode == "train": self.save_original_examples(split_data[:5], data_name)
            print(f"finishing processing {dial_idx} dialogs for {mode} set ...")
        self.save_converted_examples(data_name)
        self.copy_related_files(data_name, exp_list, "data")
        print("*"*10, f"finishing processing dataset {data_name}", "*"*10)


    def salesbot(self):
        """
        chitchat+top, no user/system 
        no ek
        """
        data_name = "SalesBot"
        data = self._load_dir_json(os.path.join(self.data_dir, data_name, "data/dialogues"))
        mode, new_data, file_idx, exp_list = "train", {}, 1, ["data"]
        for dial_idx, dial in tqdm(enumerate(data)):
            # init dialog
            new_dial_id = f"{data_name}--{mode}--{dial_idx+1}"
            new_dial = self.init_dial(dial_idx=dial_idx+1)
            new_dial[ORI_DIAL_ID] = dial["id"]
            new_dial[ORI_DIAL_INFO]["intent"] = dial["intent"]
            new_dial[ORI_DIAL_INFO]["transition_candidates"] = dial["transition_candidates"]
            dial_hist = []
            for turn_idx, utt in enumerate(dial["dialog"]):
                if turn_idx%2==0:
                    new_turn = self.init_turn(turn_id=turn_idx//2+1)
                    finish_turn_flag = 0
                    new_turn[DIAL_HIST] = " ".join(dial_hist)
                    new_turn[USR_UTT] = utt
                else:
                    new_turn[SYS_UTT] = utt
                    new_dial[LOG].append(new_turn)
                    finish_turn_flag = 1
                    dial_hist.append("<USER> " + new_turn[USR_UTT])
                    dial_hist.append("<SYSTEM> " + new_turn[SYS_UTT])

            if not finish_turn_flag:
                new_dial[LOG].append(new_turn)
            # adding prompt for each dialog
            domains = dial["intent"]["type"]
            new_dial[PROMPT] = generate_prompt(data_name, domains)
            new_data[new_dial_id] = new_dial
            if (dial_idx+1) % 1000 == 0 or dial_idx+1 == len(data):
                self.save_dial(new_data, data_name=data_name, file_idx=file_idx, mode=mode)
                new_data = {} # reset
                file_idx += 1
    
        print(f"finishing processing {dial_idx} dialogs for {mode} set ...")
        self.save_original_examples(data[:5], data_name)
        self.save_converted_examples(data_name)
        self.copy_related_files(data_name, exp_list, "data")
        print("*"*10, f"finishing processing dataset {data_name}", "*"*10)


    def craigslist(self):
        """
        1. dialog acts of the last two turns could be "offer" and "accept/reject" ("message" for usual cases)
        since outcome has already been included in dial["outcome"], therefore we skip all turns withour action "message"
        2. no consecutive turns
        3. no user/system. we consider the agent who starts the conversation as user (seller/buyer might exchange over dialogs)
        4. action space: ["accept", "reject", "quit", "message", "offer"]
        """

        data_name = "CraigslistBargains"
        exp_list = []
        for mode in ["train", "val", "test"]:
            data = self._load_json(os.path.join(self.data_dir, data_name, f"{mode}.json"))
            new_data, file_idx = {}, 1
            exp_list.append(f"{mode}.json")
            dial_idx = 1

            for dial in (data):
                # init dialog
                new_dial = self.init_dial(dial_idx=dial_idx)
                new_dial[ORI_DIAL_ID] = dial["uuid"]
                for key in dial:
                    if key in ["uuid", "events"]: continue
                    new_dial[ORI_DIAL_INFO][key] = dial[key]
                dial_hist, turn_id = [], 1
                for idx, turn in enumerate(dial["events"]):
                    if turn["action"] != "message": continue
                    turn["data"] = turn["data"].replace("\\","")
                    turn_id += 1
                    if turn_id%2==0:
                        new_turn = self.init_turn(turn_id=turn_id//2)
                        finish_turn_flag = 0
                        new_turn[DIAL_HIST] = " ".join(dial_hist)
                        new_turn[USR_UTT] = turn["data"]
                        for key in turn:
                            if key == "data": continue
                            new_turn[ORI_USR_ANN][key] = turn[key]
                    else:
                        new_turn[SYS_UTT] = turn["data"]
                        for key in turn:
                            if key == "data": continue
                            new_turn[ORI_USR_ANN][key] = turn[key]
                        new_dial[LOG].append(new_turn)
                        finish_turn_flag = 1
                        dial_hist.append("<USER> " + new_turn[USR_UTT])
                        dial_hist.append("<SYSTEM> " + new_turn[SYS_UTT])
                    if not finish_turn_flag and idx+1 == len(dial["events"]):
                        new_dial[LOG].append(new_turn)

                # adding prompt for each dialog
                domains = ["bargain"]
                new_dial[PROMPT] = generate_prompt(data_name, domains)
                if new_dial[LOG]:
                    new_dial[DIAL_IDX] = dial_idx
                    new_dial_id = f"{data_name}--{mode}--{dial_idx}"
                    new_data[new_dial_id] = new_dial
                    dial_idx += 1
                if (dial_idx-1) % 1000 == 0 or dial_idx == len(data):
                    self.save_dial(new_data, data_name=data_name, file_idx=file_idx, mode=mode)
                    new_data = {} # reset
                    file_idx += 1
        
            if mode == "train": self.save_original_examples(data[:5], data_name)

            print(f"finishing processing {dial_idx} dialogs for {mode} set ...")
        self.save_converted_examples(data_name)
        self.copy_related_files(data_name, exp_list)
        print("*"*10, f"finishing processing dataset {data_name}", "*"*10)


    def frames(self):
        data_name = "FRAMES"
        otgy = self._load_json(os.path.join(self.save_dir, data_name, "otgy.json"))
        exp_list = []
        for mode in ['train', 'test']:
            data = self._load_json(os.path.join(self.data_dir, data_name, f"{mode}_dials.json"))
            new_data, file_idx = {}, 1
            for dial_idx, dial in tqdm(enumerate(data["dialogues"])):
                new_dial_id = f"{data_name}--{mode}--{dial_idx+1}"
                new_dial = self.init_dial(dial_idx=dial_idx+1)
                new_dial[ORI_DIAL_ID] = dial["dialogue_id"]
                new_dial[ORI_DIAL_INFO]["scenario"] = dial["scenario"]
                domain = dial["scenario"]["task"]

                utterances = dial["utterances"]
                # There are formats such as <USR>,...,<USR>,...<SYS>,...<SYS>,...<USR>
                user_uttr = ""
                sys_uttr = ""
                dialog_history = ""
                user_da_label = "" # dialog acts
                sys_da_label = ""
                sys_slots_values = {}
                uttr_index = 0
                turn_index = 1
                mentioned_slots = {
                    "dst_city": set(),
                    "or_city": set(),
                }
                dst_dict = {}
                while uttr_index < len(utterances):
                    while uttr_index < len(utterances) and utterances[uttr_index]["speaker"] == "USR":
                        user_uttr += " " + utterances[uttr_index]["text"]
                        user_uttr = user_uttr.strip()

                        # Keep the latest
                        user_da_label = utterances[uttr_index]["da_label"]

                        uttr_index += 1

                    while uttr_index < len(utterances) and utterances[uttr_index]["speaker"] == "SYS":
                        sys_uttr += " " + utterances[uttr_index]["text"]
                        sys_uttr = sys_uttr.strip()

                        # Keep the latest
                        sys_da_label = utterances[uttr_index]["da_label"]
                        sys_slots_values = utterances[uttr_index]["slots"]

                        uttr_index += 1

                    # converted "null", i.e., no dialog act labels, to ""
                    if sys_da_label == "null":
                        sys_da_label = ""

                    turn_log = {}
                    turn_log["turn id"] = turn_index
                    turn_log["user utterance"] = user_uttr
                    turn_log["system response"] = sys_uttr
                    turn_log["dialog history"] = dialog_history
                    turn_log["original user side information"] = {}
                    turn_log["original system side information"] = {}

                    turn_log["original user side information"]["da_label"] = user_da_label
                    turn_log["original system side information"]["da_label"] = sys_da_label
                    turn_log["original system side information"]["slots"] = sys_slots_values
                    # adding output for intent task
                    turn_log[INTENT] = user_da_label
                    # adding output for dst task
                    slot_list = []
                    for slot_type, slot_value in sys_slots_values.items():
                        slot_list.append(f"{domain} {slot_type} {slot_value}")
                    turn_log[DST] = DST_SPLIT.join(slot_list)
                    # accumulate dst output
                    dst_dict = self.update_with_slot_list(dst_dict, slot_list)
                    turn_log[DST_ACC] = self.dst_dict_to_str(dst_dict)
                    new_dial['log'].append(turn_log)

                    dialog_history += " <USER> " + user_uttr + " <SYSTEM> " + sys_uttr
                    dialog_history = dialog_history.strip()

                    user_uttr = ""
                    sys_uttr = ""
                    user_da_label = ""
                    sys_da_label = ""
                    sys_slots_values = {}

                    turn_index += 1
                    if "dst_city" in sys_slots_values:
                        mentioned_slots["dst_city"].add(sys_slots_values["dst_city"])
                    if "or_city" in sys_slots_values:
                        mentioned_slots["or_city"].add(sys_slots_values["or_city"])

                # adding EK for TOD task
                if len(dial["scenario"]["items"]) <= TOD_LENGTH:
                    new_dial[EK_ORI][TOD_EK]["travel"] = dial["scenario"]["items"]
                else:
                    # select the dialog-mentioned item first and then random select the rest
                    cands = []
                    for item in dial["scenario"]["items"]:
                        if item["trip"]["or_city"] in mentioned_slots["or_city"] and \
                            item["hotel"]["dst_city"] in mentioned_slots["dst_city"]:
                            cands.append(item)
                    while len(cands) < TOD_LENGTH:
                        cand = random.choice(dial["scenario"]["items"])
                        if cand not in cands:
                            cands.append(cand)
                    new_dial[EK_ORI][TOD_EK]["travel"] = cands
                # adding EK for DST task
                new_dial[EK_ORI][DST_EK] = {domain: otgy["slots"][domain]}
                for slot in new_dial[EK_ORI][DST_EK][domain]:
                    if len(new_dial[EK_ORI][DST_EK][domain][slot]) > 2*DST_LENGTH:
                        new_dial[EK_ORI][DST_EK][domain][slot] = random.choices(otgy["slots"][domain][slot], k=DST_LENGTH)
                # adding EK for Intent task
                new_dial[EK_ORI][INTENT_EK] = {domain: otgy["intents"][domain]}
                # turn the external knowledge into a flat string
                new_dial[EK] = self.dict_to_str(new_dial[EK_ORI][TOD_EK])
                new_dial[EK_DST] = self.dict_to_str(new_dial[EK_ORI][DST_EK])
                new_dial[EK_INTENT] = self.dict_to_str(new_dial[EK_ORI][INTENT_EK])
                # adding prompt for each dialog
                domains = ["trip"]
                new_dial[PROMPT] = generate_prompt(data_name, domains)

                new_data[new_dial_id] = new_dial

                if (dial_idx+1) % 1000 == 0 or dial_idx+1 == len(data["dialogues"]):
                    self.save_dial(new_data, data_name=data_name, file_idx=file_idx, mode=mode)
                    new_data = {} # reset
                    file_idx += 1
        
            if mode == "train": self.save_original_examples(data["dialogues"][:5], data_name)
            print(f"finishing processing {dial_idx} dialogs for {mode} set ...")
        self.save_converted_examples(data_name)
        self.copy_related_files(data_name, exp_list)
        print("*"*10, f"finishing processing dataset {data_name}", "*"*10)


    def dstc2(self):
        data_name = "DSTC2-Clean"
        otgy = self._load_json(os.path.join(self.data_dir, data_name, "ontology_en.json"))
        del otgy["informable"]["request"]
        exp_list = []
        domain = "restaurant"
        for mode in ["train", "test", "val"]:
            real_name = f"{mode}_en.json" if mode!="val" else "valid_en.json"
            new_data, file_idx = {}, 1
            f_text = self._load_json(os.path.join(self.data_dir, data_name, real_name))
            for index, text in enumerate(f_text):
                dialog = self.init_dial(dial_idx=index+1)
                # dialog = defaultdict(list)
                dialog[ORI_DIAL_ID] = ""
                dialog[DIAL_IDX] = index + 1
                dialog[ORI_DIAL_INFO] = defaultdict(list)
                dialog_history = ""
                turn_index = 1
                new_dial_id = f"{data_name}--{mode}--{index+1}"

                messages = text['dialogue']
                for uttr_index, utterance in enumerate(messages):
                    if uttr_index == 0:
                        sys_uttr = utterance["system_transcript"]

                        turn_log = self.save_info_to_dict(turn_index, "", sys_uttr, dialog_history)
                        turn_log[ORI_SYS_ANN]["system_acts"] = utterance["system_acts"]

                        dialog['log'].append(turn_log)

                        dialog_history = "<SYS> " + sys_uttr
                        user_uttr = utterance["transcript"]
                        user_turn_label = utterance["turn_label"]
                        user_asr = utterance["asr"]

                    else:
                        sys_uttr = utterance["system_transcript"]

                        turn_log = self.save_info_to_dict(turn_index, user_uttr, sys_uttr, dialog_history)

                        turn_log[ORI_USR_ANN]["turn_label"] = user_turn_label
                        turn_log[ORI_USR_ANN]["asr"] = user_asr
                        turn_log[ORI_SYS_ANN]["system_acts"] = utterance["system_acts"]

                        # adding output for dst task
                        # if user_turn_label:
                        slot_list = []
                        for [slot_type, slot_value] in user_turn_label:
                            slot_list.append(f"{domain} {slot_type} {slot_value}")
                        turn_log[DST] = ", ".join(slot_list)

                        dialog['log'].append(turn_log)

                        dialog_history += " <USER> " + user_uttr + " <SYSTEM> " + sys_uttr
                        user_uttr = utterance["transcript"]
                        user_turn_label = utterance["turn_label"]
                        user_asr = utterance["asr"]

                    if uttr_index + 1 == len(messages):
                        turn_log = self.save_info_to_dict(turn_index + 1, user_uttr, "", dialog_history)

                        turn_log[ORI_USR_ANN]["turn_label"] = user_turn_label
                        turn_log[ORI_USR_ANN]["asr"] = user_asr
                        turn_log[ORI_SYS_ANN]["system_acts"] = utterance["system_acts"]

                        # adding output for dst task
                        # if user_turn_label:
                        slot_list = []
                        for [slot_type, slot_value] in user_turn_label:
                            slot_list.append(f"{domain} {slot_type} {slot_value}")
                        turn_log[DST] = ", ".join(slot_list)
                        dialog['log'].append(turn_log)

                    turn_index += 1

                # adding EK for DST task
                dialog[EK_ORI][DST_EK] = {domain: otgy["informable"]}
                for slot in dialog[EK_ORI][DST_EK][domain]:
                    if len(dialog[EK_ORI][DST_EK][domain][slot]) > 2*DST_LENGTH:
                        dialog[EK_ORI][DST_EK][domain][slot] = random.choices(otgy["informable"][slot], k=DST_LENGTH)

                # turn the external knowledge into a flat string
                dialog[EK] = self.dict_to_str(dialog[EK_ORI][TOD_EK])
                dialog[EK_DST] = self.dict_to_str(dialog[EK_ORI][DST_EK])
                dialog[EK_INTENT] = self.dict_to_str(dialog[EK_ORI][INTENT_EK])

                # adding prompt for each dialog
                domains = ["restaurant"]
                dialog[PROMPT] = generate_prompt(data_name, domains)

                new_data[new_dial_id] = dialog
                # Save every 1000 dialogs to a file
                if (index + 1) % 1000 == 0 or (index + 1) == len(f_text):
                    self.save_dial(new_data, data_name=data_name, file_idx=file_idx, mode=mode)
                    new_data = {} # reset
                    file_idx += 1
        
            if mode == "train": self.save_original_examples(f_text[:5], data_name)
            print(f"finishing processing {index} dialogs for {mode} set ...")
        self.save_converted_examples(data_name)
        self.copy_related_files(data_name, exp_list)
        print("*"*10, f"finishing processing dataset {data_name}", "*"*10)


    def multiwoz_hdsa(self):
        data_name, exp_list = "HDSA-Dialog", []
        for mode in ["train", "val", "test"]:
            dir_path = os.path.join(self.data_dir, data_name, f"data/{mode}.json")
            data = self._load_json(dir_path)
            new_data = {}
            file_idx = 1

            for dial_idx, dial in tqdm(enumerate(data)):
                new_dial_id = f"{data_name}--{mode}--{dial_idx+1}"
                new_dial = self.init_dial(dial_idx=dial_idx+1) # idx starts from 1
                new_dial[ORI_DIAL_ID] = dial["file"]

                dial_hist, result_list, cand_list = [], {}, {}
                for idx, turn in enumerate(dial["info"]):
                    new_turn = self.init_turn(turn_id=idx+1)
                    new_turn[USR_UTT] = turn["user"]
                    new_turn[SYS_UTT] = turn["sys"]
                    new_turn[DIAL_HIST] = " ".join(dial_hist)
                    # include user utterance into dialog history
                    dial_hist.append(f"<USER> {new_turn[USR_UTT]}")
                    dial_hist.append(f"<SYSTEM> {new_turn[SYS_UTT]}")
                    for key_ in turn.keys():
                        if key_ in ["user", "sys"]: continue
                        elif key_ in ["sys_orig", "source", "KB", "act"]:
                            new_turn[ORI_SYS_ANN][key_] = turn[key_]
                        else:
                            new_turn[ORI_USR_ANN][key_] = turn[key_]
                    new_dial[LOG].append(new_turn)

                # finish and wrap the current dialog
                new_data[new_dial_id] = new_dial
                if (dial_idx+1) % 1000 == 0 or dial_idx+1 == len(data):
                    self.save_dial(new_data, data_name=data_name, file_idx=file_idx, mode=mode)
                    new_data = {} # reset
                    file_idx += 1
    
            if mode == "train": self.save_original_examples(data[:5], data_name)
            print(f"finishing processing {dial_idx} dialogs for {mode} set ...")
        self.save_converted_examples(data_name)
        # self.copy_related_files(data_name, exp_list)
        print("*"*10, f"finishing processing dataset {data_name}", "*"*10)


    def multiwoz22(self):
        data_name, exp_list = "MULTIWOZ2_2", []
        for mode in ["train", "val", "test"]:
            real_name = mode if mode != "val" else "dev"
            data = self._load_dir_json(os.path.join(self.data_dir, data_name, real_name))
            data_21 = self._load_json(os.path.join(self.data_dir, "MULTIWOZ2_1", f"{mode}_dials.json"))
            otgy = self.multiwoz_dst_otgy()
            intents = self._load_json(os.path.join(self.data_dir, "MultiWOZ_2.1", "intents.json" ))
            exp_list.append(real_name)
            new_data = {}
            file_idx = 1
            turn_num = 0
            for dial_idx, dial in tqdm(enumerate(data)):
                new_dial_id = f"{data_name}--{mode}--{dial_idx+1}"
                new_dial = self.init_dial(dial_idx=dial_idx+1) # idx starts from 1
                new_dial[ORI_DIAL_ID] = dial['dialogue_id']
                new_dial[ORI_DIAL_INFO]["services"] = dial["services"]

                dial_hist, prev_dst_set = [], set()
                for idx, turn in enumerate(dial["turns"]):
                    utt = turn["utterance"]
                    if turn["speaker"] == "USER":
                        # new turn start from user
                        new_turn = self.init_turn(turn_id=idx//2+1)
                        new_turn[USR_UTT] = utt
                        new_turn[DIAL_HIST] = " ".join(dial_hist)
                        # include user utterance into dialog history
                        dial_hist.append(f"<USER> {utt}")
                        # other annotation for user side
                        new_turn[ORI_USR_ANN]["frames"] = turn["frames"]
                        # add dst output
                        slot_list = []
                        # # only for the current turn and non-categorical slots
                        # for frame in turn["frames"]:
                        #     if not frame["slots"]: continue
                        #     for slot in frame["slots"]:
                        #         dom, slot_type = slot["slot"].split("-")
                        #         value = slot["value"] if type(slot["value"]) == str else slot["value"][0]
                        #         slot_list.append(f"{dom} {slot_type} {value}")
                        # used for accumulated slots
                        for frame in turn["frames"]:
                            if not frame["state"]["slot_values"]: continue
                            for slot, value in frame["state"]["slot_values"].items():
                                dom, slot_type = slot.split("-")
                                value = value[0] if type(value) == list else value
                                slot_list.append(f"{dom} {slot_type} {value}")
                        new_turn[DST_ACC] = DST_SPLIT.join(slot_list)
                        # compute the non-accumulated slots
                        new_turn[DST] = DST_SPLIT.join(list(set(slot_list).difference(prev_dst_set)))
                        prev_dst_set = set(slot_list)
                        # add intent output
                        intent_list = []
                        for frame in turn["frames"]:
                            if frame["state"]["active_intent"] != "NONE":
                                intent_list.append(frame["state"]["active_intent"])
                        new_turn[INTENT] = ", ".join(intent_list)

                        # dialog ends at user side
                        if idx == len(dial["turns"]) - 1:
                            new_dial[LOG].append(new_turn)

                    if turn["speaker"] == "SYSTEM":
                        new_turn[SYS_UTT] = utt
                        # include system response into dialog history
                        dial_hist.append(f"<SYSTEM> {utt}")
                        # turn must end at assistant side
                        new_dial[LOG].append(new_turn)
                        turn_num += 1
                goal = data_21[dial["dialogue_id"]]["goal"]
                # get active domains
                domains = []
                for dom in MULTIWOZ_DOMAINS:
                    if goal[dom]: domains.append(dom)
                # adding EK for TOD
                for dom in ["restaurant", "hotel", "attraction", "train"]:
                    if not goal[dom]: continue
                    constraint = [goal[dom]["info"]]
                    db = self._load_json(os.path.join(self.data_dir, data_name, f"db/{dom}_db.json"))

                    new_dial[EK_ORI][TOD_EK][dom] = []
                    satisfied_cand, unsatisfied_cand = self.filter_cand(db, constraint)
                    if len(satisfied_cand)+len(unsatisfied_cand) < TOD_LENGTH:
                        new_dial[EK_ORI][TOD_EK][dom] = satisfied_cand + unsatisfied_cand
                    else:
                        new_dial[EK_ORI][TOD_EK][dom] = satisfied_cand
                        new_dial[EK_ORI][TOD_EK][dom].extend(random.choices(unsatisfied_cand, k=(TOD_LENGTH-len(satisfied_cand))))
                # adding EK for DST
                for dom in domains:
                    if dom not in otgy: continue
                    if dom not in new_dial[EK_ORI][DST_EK]: new_dial[EK_ORI][DST_EK][dom] = {}
                    for slot_type in otgy[dom]:
                        new_dial[EK_ORI][DST_EK][dom][slot_type] = random.choices(otgy[dom][slot_type], k=DST_LENGTH)
                # adding EK for Intent
                for dom in domains+["booking", "general"]:
                    if dom not in intents: continue
                    new_dial[EK_ORI][INTENT_EK][dom] = intents[dom]
                # turn the external knowledge into a flat string
                new_dial[EK] = self.dict_to_str(new_dial[EK_ORI][TOD_EK])
                new_dial[EK_DST] = self.dict_to_str(new_dial[EK_ORI][DST_EK])
                new_dial[EK_INTENT] = self.dict_to_str(new_dial[EK_ORI][INTENT_EK])
                # adding prompt for each dialog
                domains = dial["services"] # some dial["services"] are not annotated
                new_dial[PROMPT] = generate_prompt(data_name, domains)
                # finish and wrap the current dialog
                new_data[new_dial_id] = new_dial
                if (dial_idx+1) % 1000 == 0 or dial_idx+1 == len(data):
                    self.save_dial(new_data, data_name=data_name, file_idx=file_idx, mode=mode)
                    new_data = {} # reset
                    file_idx += 1
            
            print(f"Processing {mode} data with {dial_idx} dialogs i.e. {turn_num} turns ... " )
            if mode == "train": self.save_original_examples(data[:5], data_name)
        self.save_converted_examples(data_name)
        self.copy_related_files(data_name, exp_list)
        print("*"*10, f"finishing processing dataset {data_name}", "*"*10)


    def mudoco(self):
        def save_info_to_dict(turn_index, user_uttr, sys_uttr, dialog_history):
            turn_log = defaultdict(list)
            turn_log["turn id"] = turn_index
            turn_log["user utterance"] = user_uttr
            turn_log["system response"] = sys_uttr

            turn_log["dialog history"] = dialog_history
            turn_log["original user side information"] = defaultdict(list)
            turn_log["original system side information"] = defaultdict(list)
            return turn_log

        data_name = "MuDoCo"
        exp_list = []
        # combine dialog from each domain
        data = defaultdict(list)
        domains = ["calling", "messaging", "music", "news", "reminders", "weather"]
        for domain in domains:
            domain_data = self._load_json(os.path.join(self.data_dir, data_name, f"mudoco_{domain}.json"))
            exp_list.append(f"mudoco_{domain}.json")
            for dial_id in domain_data["dialogs"]:
                domain_data["dialogs"][dial_id]["domain"] = domain
            data.update(domain_data["dialogs"])
        # split dialogs into train/val/test set
        f_text = defaultdict(list)
        for dialog_id in data:
            mode = data[dialog_id]["split"]
            if mode == "eval":
                mode = "val"
            f_text[mode].append([dialog_id, data[dialog_id]])

        for mode in ["train", "val", "test"]:
            # out_folder_path = os.path.join(folder_path + '_PROCESSED', out_dataset_name, attribute)
            data = defaultdict(list)
            file_idx = 1
            for dial_idx, (dialog_id, text) in enumerate(f_text[mode]):
                dialog = self.init_dial()
                dialog[ORI_DIAL_ID] = dialog_id
                dialog[DIAL_IDX] = dial_idx + 1
                dialog[ORI_DIAL_INFO] = {
                    "split": text["split"],
                    "domain": text["domain"],
                }

                dialog_history = ""
                turn_index = 1
                for uttr_index, utterance in enumerate(text["turns"]):
                    if uttr_index %2 == 0:
                        user_uttr = utterance["utterance"]
                        user_name_entities = utterance["named_entities"]
                        user_references = utterance["references"]
                        user_links = utterance["links"]
                    elif uttr_index %2 == 1:
                        sys_uttr = utterance["utterance"]
                        sys_name_entities = utterance["named_entities"]
                        sys_references = utterance["references"]
                        sys_links = utterance["links"]

                        new_turn = self.init_turn(turn_id=turn_index, dial_hist=[dialog_history])
                        new_turn[USR_UTT] = user_uttr
                        new_turn[SYS_UTT] = sys_uttr
                        # turn_log = save_info_to_dict(turn_index, user_uttr, sys_uttr, dialog_history)

                        new_turn[ORI_USR_ANN]["name_entities"] = user_name_entities
                        new_turn[ORI_USR_ANN]["references"] = user_references
                        new_turn[ORI_USR_ANN]["links"] = user_links
                        new_turn[ORI_SYS_ANN]["name_entities"] = sys_name_entities
                        new_turn[ORI_SYS_ANN]["references"] = sys_references
                        new_turn[ORI_SYS_ANN]["links"] = sys_links
                        dialog['log'].append(new_turn)
                        dialog_history += " <USR> " + user_uttr + " <SYS> " + sys_uttr
                        turn_index += 1

                    if uttr_index %2 == 0 and (uttr_index + 1) == len(text):
                        new_turn = self.init_turn(turn_id=turn_index, dial_hist=[dialog_history])
                        new_turn[USR_UTT] = user_uttr
                        new_turn[SYS_UTT] = ""
                        # turn_log = save_info_to_dict(turn_index, user_uttr, "", dialog_history)

                        new_turn[ORI_USR_ANN]["name_entities"] = user_name_entities
                        new_turn[ORI_USR_ANN]["references"] = user_references
                        new_turn[ORI_USR_ANN]["links"] = user_links

                        dialog['log'].append(new_turn)

                dial_id = f"{data_name}--{mode}--{dial_idx+1}"
                data[dial_id] = dialog

                if (dial_idx+1) % 1000 == 0 or dial_idx+1 == len(f_text[mode]):
                    self.save_dial(data, data_name=data_name, file_idx=file_idx, mode=mode)
                    data = defaultdict(list) # reset
                    file_idx += 1
        
            if mode == "train": self.save_original_examples(data["dialogues"][:5], data_name)
            print(f"finishing processing {dial_idx} dialogs for {mode} set ...")
        self.save_converted_examples(data_name)
        self.copy_related_files(data_name, exp_list)
        print("*"*10, f"finishing processing dataset {data_name}", "*"*10)


    def ketod(self):
        """
        This dataset is build based on SGD, focusing on enrich system response with knowledge
        therefore, we igore the DST and INTENT task, since the annotation would be exactly same as SGD
        we replace utt with utt_enrich if it exists, otherwise keep the same
        we add turn-level ek for enriched knowledge
        the entity query usually expose the ground-truth item
        so it might not be necessary to add noisy items"""
        data_name = "KETOD"
        exp_list = []
        for mode in ["train", "val", "test"]:
            real_name = "dev" if mode == "val" else mode
            data = self._load_json(os.path.join(self.data_dir, data_name, f"{real_name}.json"))
            new_data, file_idx = {}, 1
            for dial_idx, dial in (enumerate(data)):
                new_dial_id = f"{data_name}--{mode}--{dial_idx+1}"
                new_dial = self.init_dial(dial_idx=dial_idx+1) # idx starts from 1
                new_dial[ORI_DIAL_ID] = dial['dialogue_id']
                # new_dial[ORI_DIAL_INFO]["services"] = dial["services"]
                domains = []

                dial_hist, result_list, cand_list = [], {}, {}
                for idx, turn in enumerate(dial["turns"]):
                    utt = turn["utterance"]
                    if turn["speaker"] == "USER":
                        # new turn start from user
                        new_turn = self.init_turn(turn_id=idx//2+1)
                        new_turn[EK_ORI] = {TOD_EK:{}}
                        new_turn[EK] = ""
                        new_turn[USR_UTT] = utt
                        new_turn[DIAL_HIST] = " ".join(dial_hist)
                        # include user utterance into dialog history
                        dial_hist.append(f"<USER> {utt}")
                        # other annotation for user side
                        new_turn[ORI_USR_ANN]["frames"] = turn["frames"]
                        new_turn[ORI_USR_ANN]["enrich"] = turn["frames"]
                        # dialog ends at user side
                        if idx == len(dial["turns"]) - 1:
                            new_dial[LOG].append(new_turn)
                        for frame in turn["frames"]:
                            if frame["service"] not in domains: domains.append(frame["service"])

                    if turn["speaker"] == "SYSTEM":
                        if turn["enrich"]:
                            new_turn[SYS_UTT] = turn["enriched_utter"]
                            new_turn[ORI_SYS_ANN]["original_utt"] = utt
                            new_turn[ORI_SYS_ANN]["entity_query"] = turn["entity_query"]
                            new_turn[ORI_SYS_ANN]["kg_snippets"] = turn["kg_snippets"]
                            new_turn[ORI_SYS_ANN]["kg_snippets_text"] = turn["kg_snippets_text"]
                            new_turn[EK_ORI][TOD_EK]["entity_query"] = turn["entity_query"]
                            new_turn[EK_ORI][TOD_EK]["kg_snippets_text"] = turn["kg_snippets_text"]
                            new_turn[EK] = self.dict_to_str(new_turn[EK_ORI][TOD_EK])
                        else:
                            new_turn[SYS_UTT] = utt
                        # include system response into dialog history
                        dial_hist.append(f"<SYSTEM> {utt}")
                        # other annotation for system side
                        new_turn[ORI_SYS_ANN]["frames"] = turn["frames"]
                        # turn must end at assistant side
                        new_dial[LOG].append(new_turn)

                        for frame in turn["frames"]:
                            if "service_results" in frame:
                                domain = frame["service"]
                                # # # accumulate db results
                                if domain not in cand_list:
                                    cand_list[domain] = []
                                cand_list[domain].extend(frame["service_results"])
                                # # # accumulate offered results
                                if domain not in result_list:
                                    result_list[domain] = []
                                result_list[domain].append(frame["service_call"]["parameters"])
                # adding EK for TOD
                for domain in cand_list:
                    new_dial[EK_ORI][TOD_EK][domain] = []
                    satisfied_cand, unsatisfied_cand = self.filter_cand(cand_list[domain], result_list[domain])
                    if len(satisfied_cand)+len(unsatisfied_cand) < TOD_LENGTH:
                        new_dial[EK_ORI][TOD_EK][domain] = satisfied_cand + unsatisfied_cand
                    else:
                        new_dial[EK_ORI][TOD_EK][domain] = satisfied_cand
                        new_dial[EK_ORI][TOD_EK][domain].extend(random.choices(unsatisfied_cand, k=(TOD_LENGTH-len(satisfied_cand))))
                # turn the external knowledge into a flat string
                new_dial[EK] = self.dict_to_str(new_dial[EK_ORI][TOD_EK])
                # adding prompt for each dialog
                domains = [domain.lower().split("_")[0] for domain in domains]
                new_dial[PROMPT] = generate_prompt("SGD", domains)
                # finish and wrap the current dialog
                new_data[new_dial_id] = new_dial
                if (dial_idx+1) % 1000 == 0 or dial_idx+1 == len(data):
                    self.save_dial(new_data, data_name=data_name, file_idx=file_idx, mode=mode)
                    new_data = {} # reset
                    file_idx += 1
            
            print(f"Processing {mode} data with {dial_idx} dialogs ... " )
            if mode == "train": self.save_original_examples(data[:5], data_name)
        self.save_converted_examples(data_name)
        self.copy_related_files(data_name, exp_list)
        print("*"*10, f"finishing processing dataset {data_name}", "*"*10)


    def task2dial(self):
        data_name = "Task2Dial"
        mode = "train"
        from datasets import load_dataset
        data = load_dataset("cstrathe435/Task2Dial")
        for dial in data:
            pdb.set_trace()
            pass


    def gecor(self):
        """
        constructed based on CamRest676
        [{"dial":[{}, ...]},...]
        also, since annotation are the same as camrest676
        we do not care about the DST or INTENT tasks"""
        data_name = "GECOR"
        exp_list = []
        for filename in os.listdir(os.path.join(self.data_dir, data_name)):
            if filename in ["LICENSE", "readme.txt"]: continue
            exp_list.append(filename)

        data = self._load_json(os.path.join(self.data_dir, data_name, "CamRest676_for_coreference_and_ellipsis_resolution/CamRest676_annotated.json"))
        schema = self._load_json(os.path.join(self.data_dir, data_name, "CamRest676_for_coreference_and_ellipsis_resolution/CamRestOTGY.json"))
        db = self._load_json(os.path.join(self.data_dir, data_name, "CamRest676_for_coreference_and_ellipsis_resolution/CamRestDB.json"))
        mode = "train"
        new_data, file_idx = {}, 1
        for dial_idx, dial in tqdm(enumerate(data)):
            new_dial_id = f"{data_name}--{mode}--{dial_idx+1}"
            new_dial = self.init_dial(dial_idx=dial_idx+1) # idx starts from 1
            new_dial[ORI_DIAL_ID] = dial['dialogue_id']
            new_dial[ORI_DIAL_INFO]["finished"] = dial['finished']
            new_dial[ORI_DIAL_INFO]["goal"] = dial['goal']
            dial_hist = []
            for turn in dial["dial"]:
                new_turn = self.init_turn(turn_id=turn["turn"])
                new_turn[USR_UTT] = turn["usr"]["transcript"]
                new_turn[SYS_UTT] = turn["sys"]["sent"]
                new_turn[DIAL_HIST] = " ".join(dial_hist)
                for key_ in turn["usr"]:
                    if key_ == "transcript": continue
                    new_turn[ORI_USR_ANN][key_] = turn["usr"][key_]
                new_turn[ORI_SYS_ANN]["DA"] = turn["sys"]["DA"]
                dial_hist.append(f"<USER> {new_turn[USR_UTT]}")
                dial_hist.append(f"<SYSTEM> {new_turn[SYS_UTT]}")
                new_dial[LOG].append(new_turn)

            # adding EK for TOD
            constraint = [{cons[0]:cons[1] for cons in dial['goal']["constraints"]}]
            new_dial[EK_ORI][TOD_EK] = []
            satisfied_cand, unsatisfied_cand = self.filter_cand(db, constraint)
            if len(satisfied_cand)+len(unsatisfied_cand) < TOD_LENGTH:
                new_dial[EK_ORI][TOD_EK] = satisfied_cand + unsatisfied_cand
            else:
                new_dial[EK_ORI][TOD_EK] = satisfied_cand
                new_dial[EK_ORI][TOD_EK].extend(random.choices(unsatisfied_cand, k=(TOD_LENGTH-len(satisfied_cand))))

            # turn the external knowledge into a flat string
            new_dial[EK] = self.dict_to_str(new_dial[EK_ORI][TOD_EK])
            # adding prompt for each dialog, since camrest676 is only about restaurant, we use...
            domains = ["restaurant"]
            new_dial[PROMPT] = generate_prompt("MULTIWOZ2_2", domains)
            # finish and wrap the current dialog
            new_data[new_dial_id] = new_dial
            if (dial_idx+1) % 1000 == 0 or dial_idx+1 == len(data):
                self.save_dial(new_data, data_name=data_name, file_idx=file_idx, mode=mode)
                new_data = {} # reset
                file_idx += 1
            
        print(f"Processing {mode} data with {dial_idx+1} dialogs ... " )
        if mode == "train": self.save_original_examples(data[:5], data_name)
        self.save_converted_examples(data_name)
        self.copy_related_files(data_name, exp_list)
        print("*"*10, f"finishing processing dataset {data_name}", "*"*10)


    def disamb(self):
        """
        a variant of multiwoz22, though in format of multiwoz21"""
        data_name = "Disambiguation"
        exp_list = []
        for filename in os.listdir(os.path.join(self.data_dir, data_name)):
            if not filename.startswith("data_aug"):continue
            exp_list.append(filename)
        otgy = self.multiwoz_dst_otgy()
        intents = self._load_json(os.path.join(self.data_dir, "MultiWOZ_2.1", "intents.json" ))
        for mode in ["train", "val", "test"]:
            data = self._load_json(os.path.join(self.data_dir, data_name, f"data_aug_{mode}.json"))
            new_data, dial_idx, file_idx = {}, 1, 1
            for dial_id, dial in tqdm(data.items()):
            
                new_dial_id = f"{data_name}--{mode}--{dial_idx}"
                new_dial = self.init_dial(dial_idx=dial_idx) # idx starts from 1, set this when checking its source
                new_dial[ORI_DIAL_ID] = dial_id
                new_dial[ORI_DIAL_INFO]["goal"] = dial['goal']
                dial_hist = []
                #     """
                #     note: these five dialogs do not contain any annotation
                #     for user side, including span_info or dialog acts
                #     therefore, we exclude these five dialogs since slot-->ek-->utt
                #     """
                if dial_id in ["pmul4707.json", "pmul2245.json", "pmul4776.json", "pmul3872.json", "pmul4859.json"]: continue
                for turn_num in range(math.ceil(len(dial["log"]) / 2)):
                    # # # turn number
                    usr_turn = dial["log"][turn_num*2]
                    sys_turn = dial["log"][turn_num*2+1]

                    new_turn = self.init_turn(turn_id=turn_num+1)
                    new_turn[USR_UTT] = usr_turn["text"]
                    new_turn[SYS_UTT] = sys_turn["text"]
                    new_turn[DIAL_HIST] = " ".join(dial_hist)
                    dial_hist.append(f"<USER> {new_turn[USR_UTT]}")
                    dial_hist.append(f"<SYSTEM> {new_turn[SYS_UTT]}")
                    for key_ in ["metadata", "dialog_act", "span_info"]:
                        # other annotation for user side
                        if key_ in usr_turn:
                            new_turn[ORI_USR_ANN][key_] = usr_turn[key_]
                        # other annotation for system side
                        if key_ in sys_turn:
                            new_turn[ORI_SYS_ANN][key_] = sys_turn[key_]
                    
                    # used for accumulated slots, extracted based on "metadata", only in system side (turn_num * 2 + 1)
                    slot_list_acc = []
                    for dom, slot in sys_turn["metadata"].items():
                        for slot_type, slot_val in slot["book"].items():
                            if not slot_val or slot_type == "booked" or slot_val == "not mentioned": continue
                            slot_list_acc.append(f"{dom} {slot_type} {slot_val[0]}")
                        for slot_type, slot_val in slot["semi"].items():
                            if not slot_val or slot_val == "not mentioned": continue
                            slot_list_acc.append(f"{dom} {slot_type} {slot_val[0]}")
                    new_turn[DST_ACC] = DST_SPLIT.join(slot_list_acc).lower()
                    # compute the non-accumulated slots
                    slot_list = []
                    for act in usr_turn["dialog_act"]:
                        if not act.endswith("inform"): continue
                        for slot_type, slot_val in usr_turn["dialog_act"][act]:
                            dom = act.split("-")[0]
                            slot_type = slot_type
                            slot_list.append(f"{dom} {slot_type} {slot_val}")
                    new_turn[DST] = DST_SPLIT.join(slot_list).lower()
                    # add intent output
                    new_turn[INTENT] = ", ".join(list(usr_turn["dialog_act"].keys())).lower()
                    new_dial[LOG].append(new_turn)

                # get active domains
                domains = []
                for dom in MULTIWOZ_DOMAINS:
                    if dial["goal"][dom]: domains.append(dom)
                # adding EK for TOD
                goal = dial['goal']
                for dom in ["restaurant", "hotel", "attraction", "train"]:
                    if not goal[dom]: continue
                    constraint = [goal[dom]["info"]]
                    db = self._load_json(os.path.join(self.data_dir, "MultiWOZ_2.1", f"{dom}_db.json"))

                    new_dial[EK_ORI][TOD_EK][dom] = []
                    satisfied_cand, unsatisfied_cand = self.filter_cand(db, constraint)
                    if len(satisfied_cand)+len(unsatisfied_cand) < TOD_LENGTH:
                        new_dial[EK_ORI][TOD_EK][dom] = satisfied_cand + unsatisfied_cand
                    else:
                        new_dial[EK_ORI][TOD_EK][dom] = satisfied_cand
                        new_dial[EK_ORI][TOD_EK][dom].extend(random.choices(unsatisfied_cand, k=(TOD_LENGTH-len(satisfied_cand))))
                # adding EK for DST
                for dom in domains:
                    if dom not in otgy: continue
                    if dom not in new_dial[EK_ORI][DST_EK]: new_dial[EK_ORI][DST_EK][dom] = {}
                    for slot_type in otgy[dom]:
                        new_dial[EK_ORI][DST_EK][dom][slot_type] = random.choices(otgy[dom][slot_type], k=DST_LENGTH)
                # adding EK for Intent
                for dom in domains+["booking", "general"]:
                    if dom not in intents: continue
                    new_dial[EK_ORI][INTENT_EK][dom] = intents[dom]
                # turn the external knowledge into a flat string
                new_dial[EK] = self.dict_to_str(new_dial[EK_ORI][TOD_EK])
                new_dial[EK_DST] = self.dict_to_str(new_dial[EK_ORI][DST_EK])
                new_dial[EK_INTENT] = self.dict_to_str(new_dial[EK_ORI][INTENT_EK])

                # turn the external knowledge into a flat string
                new_dial[EK] = self.dict_to_str(new_dial[EK_ORI][TOD_EK])
                # adding prompt for each dialog, since camrest676 is only about restaurant, we use...
                domains = []
                for dom in MULTIWOZ_DOMAINS:
                    if dial["goal"][dom]: domains.append(dom)
                new_dial[PROMPT] = generate_prompt("MULTIWOZ2_2", domains)
                # finish and wrap the current dialog
                new_data[new_dial_id] = new_dial
                if (dial_idx) % 1000 == 0:
                    self.save_dial(new_data, data_name=data_name, file_idx=file_idx, mode=mode)
                    new_data = {} # reset
                    file_idx += 1
                dial_idx += 1
            
            if len(new_data) > 0: self.save_dial(new_data, data_name=data_name, file_idx=file_idx, mode=mode)
            print(f"Processing {mode} data with {dial_idx-1} dialogs ... " )
            if mode=="train":self.save_original_examples({k:data[k] for k in list(data.keys())[:5]}, data_name)
        self.save_converted_examples(data_name)
        self.copy_related_files(data_name, exp_list)
        print("*"*10, f"finishing processing dataset {data_name}", "*"*10)


    def multiwoz21(self):
        data_name, exp_list = "MultiWOZ_2.1", ["data.json"]
        MULTIWOZ_DOMAINS = ["taxi", "police", "hospital", "hotel","attraction","train","restaurant"]
        data = self._load_json(os.path.join(self.data_dir, data_name, "data.json"))
        val_list = self._load_txt(os.path.join(self.data_dir, data_name, "valListFile.txt"))
        test_list = self._load_txt(os.path.join(self.data_dir, data_name, "testListFile.txt"))
        otgy = self.multiwoz_dst_otgy()
        intents = self._load_json(os.path.join(self.data_dir, "MultiWOZ_2.1", "intents.json" ))
        new_data = {"train":{}, "val":{}, "test":{}}
        dial_idx = {"train":1, "val":1, "test":1}
        file_idx = {"train":1, "val":1, "test":1}
        for dial_id, dial in tqdm(data.items()):
            if dial_id in test_list:
                mode = "test"
            elif dial_id in val_list:
                mode = "val"
            else:
                mode = "train"
            
            new_dial_id = f"{data_name}--{mode}--{dial_idx[mode]}"
            new_dial = self.init_dial(dial_idx=dial_idx[mode]) # idx starts from 1, set this when checking its source
            new_dial[ORI_DIAL_ID] = dial_id
            new_dial[ORI_DIAL_INFO]["goal"] = dial['goal']
            dial_hist = []
            #     """
            #     note: these five dialogs do not contain any annotation
            #     for user side, including span_info or dialog acts
            #     therefore, we exclude these five dialogs since slot-->ek-->utt
            #     """
            if dial_id in ["PMUL4707.json", "PMUL2245.json", "PMUL4776.json", 
                            "PMUL3872.json", "PMUL4859.json"]:
                continue
            for turn_num in range(math.ceil(len(dial["log"]) / 2)):
                # # # turn number
                usr_turn = dial["log"][turn_num*2]
                sys_turn = dial["log"][turn_num*2+1]

                new_turn = self.init_turn(turn_id=turn_num+1)
                new_turn[USR_UTT] = usr_turn["text"]
                new_turn[SYS_UTT] = sys_turn["text"]
                new_turn[DIAL_HIST] = " ".join(dial_hist)
                dial_hist.append(f"<USER> {new_turn[USR_UTT]}")
                dial_hist.append(f"<SYSTEM> {new_turn[SYS_UTT]}")
                for key_ in ["metadata", "dialog_act", "span_info"]:
                    # other annotation for user side
                    if key_ in usr_turn:
                        new_turn[ORI_USR_ANN][key_] = usr_turn[key_]
                    # other annotation for system side
                    if key_ in sys_turn:
                        new_turn[ORI_SYS_ANN][key_] = sys_turn[key_]
                
                # used for accumulated slots, extracted based on "metadata", only in system side (turn_num * 2 + 1)
                slot_list_acc = []
                for dom, slot in sys_turn["metadata"].items():
                    for slot_type, slot_val in slot["book"].items():
                        if not slot_val or slot_type == "booked" or slot_val == "not mentioned": continue
                        slot_list_acc.append(f"{dom} {slot_type} {slot_val}")
                    
                    for slot_type, slot_val in slot["semi"].items():
                        if not slot_val or slot_val == "not mentioned": continue
                        slot_list_acc.append(f"{dom} {slot_type} {slot_val}")
                new_turn[DST_ACC] = DST_SPLIT.join(slot_list_acc).lower()
                # compute the non-accumulated slots
                slot_list = []
                for act in usr_turn["dialog_act"]:
                    if not act.endswith("Inform"): continue
                    for slot_type, slot_val in usr_turn["dialog_act"][act]:
                        dom = act.split("-")[0]
                        slot_type = slot_type
                        slot_list.append(f"{dom} {slot_type} {slot_val}")
                new_turn[DST] = DST_SPLIT.join(slot_list).lower()
                # add intent output
                new_turn[INTENT] = ", ".join(list(usr_turn["dialog_act"].keys())).lower()

                new_dial[LOG].append(new_turn)

            # get active domains
            domains = []
            for dom in MULTIWOZ_DOMAINS:
                if dial["goal"][dom]: domains.append(dom)
            # adding EK for TOD
            for dom in ["restaurant", "hotel", "attraction", "train"]:
                if not dial["goal"][dom]: continue
                constraint = [dial['goal'][dom]["info"]]
                db = self._load_json(os.path.join(self.data_dir, data_name, f"{dom}_db.json"))
                new_dial[EK_ORI][TOD_EK][dom] = []
                satisfied_cand, unsatisfied_cand = self.filter_cand(db, constraint)
                if len(satisfied_cand)+len(unsatisfied_cand) < TOD_LENGTH:
                    new_dial[EK_ORI][TOD_EK][dom] = satisfied_cand + unsatisfied_cand
                else:
                    new_dial[EK_ORI][TOD_EK][dom] = satisfied_cand
                    new_dial[EK_ORI][TOD_EK][dom].extend(random.choices(unsatisfied_cand, k=(TOD_LENGTH-len(satisfied_cand))))
            # adding EK for DST
            for dom in domains:
                if dom not in otgy: continue
                if dom not in new_dial[EK_ORI][DST_EK]: new_dial[EK_ORI][DST_EK][dom] = {}
                for slot_type in otgy[dom]:
                    new_dial[EK_ORI][DST_EK][dom][slot_type] = random.choices(otgy[dom][slot_type], k=DST_LENGTH)
            # adding EK for Intent
            for dom in domains+["booking", "general"]:
                if dom not in intents: continue
                new_dial[EK_ORI][INTENT_EK][dom] = intents[dom]
            # turn the external knowledge into a flat string
            new_dial[EK] = self.dict_to_str(new_dial[EK_ORI][TOD_EK])
            new_dial[EK_DST] = self.dict_to_str(new_dial[EK_ORI][DST_EK])
            new_dial[EK_INTENT] = self.dict_to_str(new_dial[EK_ORI][INTENT_EK])
            # adding prompt for each dialog, since camrest676 is only about restaurant, we use...
            new_dial[PROMPT] = generate_prompt("MULTIWOZ2_2", domains)
            # finish and wrap the current dialog
            new_data[mode][new_dial_id] = new_dial
            if (dial_idx[mode]) % 1000 == 0:
                # pdb.set_trace()
                self.save_dial(new_data[mode], data_name=data_name, file_idx=file_idx[mode], mode=mode)
                new_data[mode] = {} # reset
                file_idx[mode] += 1
            if file_idx[mode]>100: pdb.set_trace()
            dial_idx[mode] += 1
        for mode in ["train", "test", "val"]:
            if len(new_data[mode]) > 0: self.save_dial(new_data[mode], data_name=data_name, file_idx=file_idx[mode], mode=mode)
            print(f"Processing {mode} data with {dial_idx[mode]-1} dialogs ... " )
        self.save_original_examples({k:data[k] for k in list(data.keys())[:5]}, data_name)
        self.save_converted_examples(data_name)
        self.copy_related_files(data_name, exp_list)
        print("*"*10, f"finishing processing dataset {data_name}", "*"*10)

    def multiwoz21_trade(self):
        pass


    def run_all(self):
        # self.kvret() # 800 tod+dst
        # self.woz()    # dst
        # self.sgd()    # 16k tod+dst+intent
        # self.bitod()
        # self.metalwoz()
        # self.star()
        # self.taskmaster1()  # 643 dst only
        # self.taskmaster2()  # 981 dst only
        self.taskmaster3()  # 1167 dst only
        # self.simjoint()     # dst
        # self.simjointgen()  # dst
        # self.muldogo()
        # self.casino()
        # self.airdialogue() # 1595
        # self.msdc()         # 759 dst+intent
        # self.abcd()         # 8034 dst
        # self.salesbot()
        # self.craigslist()
        # self.frames()   # 2000 tod+dst+intent
        # self.dstc2()
        # self.multiwoz_hdsa()
        # self.multiwoz22()
        # self.mudoco()
        # self.ketod()
        # self.task2dial()
        # self.gecor()
        # self.disamb()
        # self.multiwoz21()
        pass

    def multiwoz_dst_otgy(self):
        """
        transfer the ontology file in multiwoz from format:
        {domain-semi/book-slot_type:[slot_value, ...],}
        into
        {domain:{slot_type:[slot_value, ...],}"""
        otgy_ori = self._load_json(os.path.join(self.data_dir, "MultiWOZ_2.1/ontology.json"))
        otgy = {}
        for dom_slot in otgy_ori:
            dom, _, slot_type = dom_slot.split("-")
            if dom not in otgy: otgy[dom] = {}
            otgy[dom][slot_type] = otgy_ori[dom_slot]
        return otgy

    def save_info_to_dict(self, turn_index, user_uttr, sys_uttr, dialog_history):
        turn_log = self.init_turn(turn_id=turn_index, dial_hist=dialog_history)
        turn_log[TURN_ID] = turn_index
        turn_log[USR_UTT] = user_uttr
        turn_log[SYS_UTT] = sys_uttr
        turn_log[DIAL_HIST] = dialog_history
        return turn_log


    def compare_delex(self, utt_ori, utt_delex):
        """
        original: Yes my order id is 4870952797
        delexicalized: yes my order id is <order_id>
        assuming delexicalized token is only of length 1
        """
        utt_ori = utt_ori.lower().replace(",", " , ").replace(". ", " . ").replace(":", " : ").replace("  ", " ").replace(" | ", " and ").split()
        utt_delex = utt_delex.replace(",", " , ").replace(". ", " . ").replace(":", " : ").replace("  ", " ").replace(" | ", " and ").split()
        utt_ori = [slot_value.strip(",.$?\"\\()") for slot_value in utt_ori]
        utt_delex = [slot_type.strip(",.$?\"\\0()") for slot_type in utt_delex]
        pointer_ori_start, pointer_ori_end, pointer_delex = 0, 0, 0
        result = []
        while pointer_ori_start < len(utt_ori):
            if utt_ori[pointer_ori_start] == utt_delex[pointer_delex]: # not slot, continue
                pointer_ori_start += 1
                pointer_delex += 1
            elif pointer_delex == len(utt_delex) - 1: # the last token
                result.append([" ".join(utt_ori[pointer_ori_start:]), utt_delex[pointer_delex]])
                break
            else:
                for pointer_delex_end in range(pointer_delex+1,len(utt_delex)):
                    if not (utt_delex[pointer_delex_end].startswith("<") or utt_delex[pointer_delex_end].endswith(">")):
                        break
                flag = 0
                for pointer_ori_end in range(pointer_ori_start+1, len(utt_ori)):
                    if utt_ori[pointer_ori_end] == utt_delex[pointer_delex_end]:
                        result.extend(self.match(utt_ori[pointer_ori_start:pointer_ori_end], utt_delex[pointer_delex:pointer_delex_end]))
                        pointer_ori_start = pointer_ori_end + 1
                        pointer_delex += 2
                        flag = 1
                        break
                if not flag:
                    result.extend(self.match(utt_ori[pointer_ori_start:], utt_delex[pointer_delex:]))
                    break
        return result


    def match(self, list_ori, list_delex):
        if len(list_delex) == 0:
            return []
        elif len(list_delex) == 1: # only one slot
            return [[" ".join(list_ori), " ".join(list_delex)]]
        elif len(list_ori) == len(list_delex): # slot has only length 1
            return [[list_ori[i], list_delex[i]] for i in range(len(list_delex))]
        elif len(list_ori) < len(list_delex): # something wrong with annotation
            return []
        else: # multiple, length-variant slots
            if "<email>" in list_delex:
                i_delex = list_delex.index("<email>")
                for i_ori, value in enumerate(list_ori):
                    if "@" in value:
                        break
                result = self.match(list_ori[:i_ori], list_delex[:i_delex])
                result.append([value, "<email>"])
                # pdb.set_trace()
                if i_ori < len(list_ori) - 1:
                    result.extend(self.match(list_ori[i_ori+1:], list_delex[i_delex+1:]))
                return result
            elif list_delex[0] in ["<amount>", "<username>", "<zip_code>", "<order_id>"]:
                result = [[list_ori[0], list_delex[0]]]
                result.extend(self.match(list_ori[1:], list_delex[1:]))
                return result
            elif list_delex[-1] in ["<amount>", "<username>", "<zip_code>", "<order_id>"]:
                result = [[list_ori[-1], list_delex[-1]]]
                result.extend(self.match(list_ori[:-1], list_delex[:-1]))
                return result
            else:
                # return [[" ".join(list_ori), " ".join(list_delex)]]
                return []


    def copy_example(self):
        source_dir = self.save_dir
        target_dir = "/home/qkun/projs/TOD-Project/Datasets/Task-Oriented_PROCESSED/"
        file_list = ["converted_examples.json", "original_examples.json", "readme.txt", "LICENSE"]
        for dir_name in sorted(os.listdir(source_dir)):
            if os.path.isfile(os.path.join(source_dir, dir_name)): continue
            if not os.path.exists(os.path.join(target_dir, dir_name)): os.makedirs(os.path.join(target_dir, dir_name))
            for filename in file_list:
                source_path = os.path.join(source_dir, dir_name, filename)
                target_path = os.path.join(target_dir, dir_name, filename)
                if not os.path.exists(source_path): continue
                shutil.copy(source_path, target_path)


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


    def dst_dict_to_str(self, dst_dict):
        """
        use a dict to store updated dst state, and now conver it into string for generation
        """
        slot_list = []
        for domain in dst_dict:
            for slot, value in dst_dict[domain].items():
                slot_list.append(f"{domain} {slot} {value.strip()}")
        return ", ".join(slot_list)


    def update_with_slot_list(self, dst_dict, slot_list):
        """
        assuming using a dict to store updated dst state, now update the dict with slot_list
        """
        for slot in slot_list:
            if len(slot.split()) < 2:
                pdb.set_trace()
            domain, slot_type, slot_value = slot.split()[0], slot.split()[1], " ".join(slot.split()[2:])
            if domain not in dst_dict:
                dst_dict[domain] = {}
            dst_dict[domain][slot_type] = slot_value
        return dst_dict


    def examine(self):
        for data_name in sorted(os.listdir(self.save_dir)):
            if data_name in ["AirDialogue"]: continue
            print(f"Loading {data_name} ...")
            if os.path.isfile(os.path.join(self.save_dir, data_name)): continue
            for filename in os.listdir(os.path.join(self.save_dir, data_name, "train")):
                if not filename.startswith("dialog"): continue
                idx = 1
                data = self._load_json(os.path.join(self.save_dir, data_name, "train", filename))
                for dial_id, dial in data.items():
                    if not dial_id.endswith(str(idx)) and idx != 1000:
                        print(data_name, filename, dial_id, idx)
                        pdb.set_trace()
                    idx += 1
                    # for idx, turn in enumerate(dial[LOG]):
                    #     if idx + 1 != turn[TURN_ID]:
                    #         print(data_name, dial_id)


def main():
    preprocess = PreProcessData()
    preprocess.run_all()
    preprocess.copy_example()
    # preprocess.examine()

if __name__ == '__main__':
    main()