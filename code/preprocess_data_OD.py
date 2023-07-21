#!/usr/bin/env python3
#
import sys, os, pdb
import json
import shutil, errno
from tqdm import tqdm
import pandas as pd
from constant import *


class PreProcessData(object):
    """docstring for PreProcessData"""
    def __init__(self):
        super(PreProcessData, self).__init__()
        self.data_dir = "/path/to/where/the/raw/dataset/is"
        self.save_dir = "/path/to/store/the/processed/dataset/" # e.g. ./data/processed/Open-Domain


    def _load_json(self, path=None):
        if path is None or not os.path.exists(path):
            raise IOError('File does not exist: %s' % path)
            # return None
        with open(path) as df:
            data = json.loads(df.read())
        return data

    
    def _load_txt(self, path=None, split_tok="\n", encoding="utf-8"):
        if path is None or not os.path.exists(path):
            raise IOError('File does not exist: %s' % path)
        with open(path, 'r', encoding=encoding) as df:
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
            ORI_DIAL_ID: ori_dial_id,
            DIAL_IDX: int(dial_idx),
            ORI_DIAL_INFO: {},
            LOG: [],
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



    def places(self):
        """
        no train/val/test split"""
        data_name = "PLACES3.5"
        mode = "train"
        data = self._load_jsonl(os.path.join(self.data_dir, data_name, "data.jsonl"))
        new_data, file_idx, dial_idx = {}, 1, 1
        for dial in (data):
            new_dial = self.init_dial(dial_idx=dial_idx)
            new_dial_id = f"{data_name}--{mode}--{dial_idx}"
            for key in dial:
                if key == "conversation": continue
                new_dial[ORI_DIAL_INFO][key] = dial[key]
            dial_hist, multiparty = [], False
            for turn_idx, utt in enumerate(dial["conversation"]):
                if utt.startswith("Alice:"):
                    new_turn = self.init_turn(turn_id=turn_idx//2+1)
                    new_turn[DIAL_HIST] = " ".join(dial_hist)
                    new_turn[USR_UTT] = utt.split("Alice:")[-1].strip()
                    dial_hist.append(f"<{SPEAKER1.upper()}> " + new_turn[USR_UTT])
                elif utt.startswith("Bob:"):
                    new_turn[SYS_UTT] = utt.split("Bob:")[-1].strip()
                    dial_hist.append(f"<{SPEAKER2.upper()}> " + new_turn[SYS_UTT])
                    new_dial[LOG].append(new_turn)
                elif utt.startswith("Emilie:"):
                    multiparty = True
                    break
                else:
                    if len(utt.split(":")[0].split()) == 1:
                        # might have a third speaker
                        raise ValueError("Unknown Speaker ... ")
                    else:
                        if not turn_idx: continue
                        if new_turn[SYS_UTT]:
                            new_turn[SYS_UTT] += " " + utt
                        else:
                            new_turn[USR_UTT] += " " + utt
                        dial_hist[-1] += " " + utt
            if multiparty: continue
            new_data[new_dial_id] = new_dial
            if (dial_idx) % 10000 == 0:
                self.save_dial(new_data, data_name=data_name, file_idx=file_idx, mode=mode)
                new_data = {} # reset
                file_idx += 1
            dial_idx += 1
        if new_data: self.save_dial(new_data, data_name=data_name, file_idx=file_idx, mode=mode)
        print(f"finishing processing {new_dial[DIAL_IDX]} dialogs for {mode} set ...")
        self.save_original_examples(data[:5], data_name)
        self.save_converted_examples(data_name)
        print("*"*10, f"finishing processing dataset {data_name}", "*"*10)


    def chitchat(self):
        """
        no train/val/test split"""
        data_name = "chitchat-dataset"
        mode = "train"
        data = self._load_json(os.path.join(self.data_dir, data_name, "chitchat_dataset/dataset.json"))
        new_data, file_idx, dial_idx = {}, 1, 1
        for dial_id, dial in data.items():
            new_dial = self.init_dial(dial_idx=dial_idx)
            new_dial_id = f"{data_name}--{mode}--{dial_idx}"
            new_dial[ORI_DIAL_ID] = dial_id
            for key in dial:
                if key == "messages": continue
                new_dial[ORI_DIAL_INFO][key] = dial[key]
            dial_hist, speakers = [], []
            for turn in dial["messages"]:
                if turn[0]["sender"] not in speakers:
                    speakers.append(turn[0]["sender"])
            if len(speakers) < 2: continue
            # if len(speakers) != 2:
            #     print("This is a multi-party dialog")
            #     continue
            for turn_idx, turn in enumerate(dial["messages"]):
                if turn[0]["sender"] == speakers[0]:
                    new_turn = self.init_turn(turn_id=turn_idx//2+1)
                    new_turn[DIAL_HIST] = " ".join(dial_hist)
                    new_turn[USR_UTT] = " ".join([row["text"] for row in turn])
                    new_turn[ORI_USR_ANN]["sender"] = turn[0]["sender"]
                    new_turn[ORI_USR_ANN]["timestamp"] = [row["timestamp"] for row in turn]
                    dial_hist.append(f"<{SPEAKER1.upper()}> " + new_turn[USR_UTT])

                elif turn[0]["sender"] == speakers[1]:
                    new_turn[SYS_UTT] = " ".join([row["text"] for row in turn])
                    new_turn[ORI_SYS_ANN]["sender"] = turn[0]["sender"]
                    new_turn[ORI_SYS_ANN]["timestamp"] = [row["timestamp"] for row in turn]
                    dial_hist.append(f"<{SPEAKER2.upper()}> " + new_turn[SYS_UTT])
                    new_dial[LOG].append(new_turn)
                    
            new_data[new_dial_id] = new_dial
            if (dial_idx) % 10000 == 0:
                self.save_dial(new_data, data_name=data_name, file_idx=file_idx, mode=mode)
                new_data = {} # reset
                file_idx += 1
            dial_idx += 1
        if new_data: self.save_dial(new_data, data_name=data_name, file_idx=file_idx, mode=mode)
        print(f"finishing processing {new_dial[DIAL_IDX]} dialogs for {mode} set ...")
        self.save_original_examples({k:data[k] for k in list(data.keys())[:5]}, data_name)
        self.save_converted_examples(data_name)
        print("*"*10, f"finishing processing dataset {data_name}", "*"*10)
        

    def prosocial(self):
        data_name = "Prosocial"
        from datasets import load_dataset
        for mode in ["train", "val", "test"]:
            new_data, file_idx = {}, 1
            real_name = "validation" if mode == "val" else mode
            data = load_dataset("allenai/prosocial-dialog", split=real_name)
            data_df = data.to_pandas()
            for row_id in (range(len(data_df))):
                if data_df["response_id"][row_id] == 0:
                    new_dial = self.init_dial(dial_idx=data_df["dialogue_id"][row_id]+1)
                    dial_hist = []

                new_turn = self.init_turn(turn_id=data_df["response_id"][row_id]+1)
                new_turn[DIAL_HIST] = " ".join(dial_hist)
                new_turn[USR_UTT] = data_df["context"][row_id]
                new_turn[SYS_UTT] = data_df["response"][row_id]
                dial_hist.append(f"<{SPEAKER1.upper()}> " + new_turn[USR_UTT])
                dial_hist.append(f"<{SPEAKER2.upper()}> " + new_turn[SYS_UTT])

                for key in data_df.keys():
                    if key in ["context", "response"]: continue
                    # numpy.ndarray cannot be written into json
                    if type(data_df[key][row_id]) == str:
                        new_turn[ORI_USR_ANN][key] = data_df[key][row_id]
                    else:
                        new_turn[ORI_USR_ANN][key] = data_df[key][row_id].tolist()

                new_dial[LOG].append(new_turn)
                if data_df["episode_done"][row_id]:
                    new_dial_id = f"{data_name}--{mode}--{new_dial[DIAL_IDX]}"
                    new_data[new_dial_id] = new_dial
                    if new_dial[DIAL_IDX] % 10000 == 0:
                        self.save_dial(new_data, data_name=data_name, file_idx=file_idx, mode=mode)
                        new_data = {} # reset
                        file_idx += 1
            if new_data: self.save_dial(new_data, data_name=data_name, file_idx=file_idx, mode=mode)
            print(f"finishing processing {new_dial[DIAL_IDX]} dialogs for {mode} set ...")
        self.save_original_examples(data[:5], data_name)
        self.save_converted_examples(data_name)
        print("*"*10, f"finishing processing dataset {data_name}", "*"*10)


    def hhrlhf(self):
        """
        only use the chosen pair"""
        from datasets import load_dataset
        data_name = "HH-RLHF"
        for mode in ["train", "test"]:
            data = load_dataset("Anthropic/hh-rlhf", split=mode)
            data_df = data.to_pandas()
            new_data, file_idx = {}, 1
            for i in (range(len(data_df))):
                new_dial = self.init_dial(dial_idx=i+1)
                new_dial_id = f"{data_name}--{mode}--{i+1}"
                dial_hist = []
                utts = data_df["chosen"][i].replace("Assistant:", "Human:").split("Human:")
                for turn_idx, utt in enumerate(utts[1:]):
                    utt = utt.replace("\n\n", " ").strip()
                    if turn_idx % 2 == 0:
                        new_turn = self.init_turn(turn_id=turn_idx//2+1)
                        new_turn[DIAL_HIST] = " ".join(dial_hist)
                        new_turn[USR_UTT] = utt
                        dial_hist.append(f"<{SPEAKER1.upper()}> " + new_turn[USR_UTT])
                    else:
                        new_turn[SYS_UTT] = utt
                        dial_hist.append(f"<{SPEAKER2.upper()}> " + new_turn[SYS_UTT])
                        new_dial[LOG].append(new_turn)
                    
                new_data[new_dial_id] = new_dial
                if new_dial[DIAL_IDX] % 10000 == 0:
                    self.save_dial(new_data, data_name=data_name, file_idx=file_idx, mode=mode)
                    new_data = {} # reset
                    file_idx += 1
            if new_data: self.save_dial(new_data, data_name=data_name, file_idx=file_idx, mode=mode)
            print(f"finishing processing {new_dial[DIAL_IDX]} dialogs for {mode} set ...")
        self.save_original_examples(data[:5], data_name)
        self.save_converted_examples(data_name)
        print("*"*10, f"finishing processing dataset {data_name}", "*"*10)


    def empathetic(self):
        """
        consecutive turns from the same speaker happens"""
        data_name = "Empathetic"
        from datasets import load_dataset
        for mode in ["train", "val", "test"]:
            real_name = "validation" if mode == "val" else mode
            data = load_dataset("empathetic_dialogues", split=real_name)
            data_df = data.to_pandas()
            new_data, file_idx, dial_idx, speakers = {}, 1, 1, []
            for row_id in (range(len(data_df))):
                utt = data_df["utterance"][row_id].replace("_comma_", ",").strip()
                if data_df["utterance_idx"][row_id] == 1:
                    new_dial = self.init_dial(dial_idx)
                    new_dial[ORI_DIAL_ID] = data_df["conv_id"][row_id]
                    new_dial[ORI_DIAL_INFO]["context"] = data_df["context"][row_id]
                    new_dial[ORI_DIAL_INFO]["selfeval"] = data_df["selfeval"][row_id]
                    dial_hist = []

                    # process the first turn
                    new_turn = self.init_turn(turn_id=1)
                    new_turn[USR_UTT] = data_df["prompt"][row_id].strip()
                    new_turn[SYS_UTT] = utt
                    new_turn[ORI_USR_ANN]["tags"] = ""
                    new_turn[ORI_USR_ANN]["speaker_idx"] = int(data_df["speaker_idx"][row_id+1])
                    new_turn[ORI_SYS_ANN]["tags"] = data_df["tags"][row_id]
                    new_turn[ORI_SYS_ANN]["speaker_idx"] = int(data_df["speaker_idx"][row_id])

                    dial_hist.append(f"<{SPEAKER1.upper()}> " + new_turn[USR_UTT])
                    dial_hist.append(f"<{SPEAKER2.upper()}> " + new_turn[SYS_UTT])
                    # speakers.append(data_df["speaker_idx"][row_id])
                    # in the first turn, the first speaker's utt is in the prompt and 
                    # utterance contains the utt from the second speaker
                    second_speaker_id = data_df["speaker_idx"][row_id]
                    new_dial[LOG].append(new_turn)
                    new_turn = self.init_turn(turn_id=(int(data_df["utterance_idx"][row_id])+1)//2+1)
                    new_turn[DIAL_HIST] = " ".join(dial_hist)
                
                elif data_df["speaker_idx"][row_id] == second_speaker_id:
                    if not new_turn[USR_UTT]: # in this case, consecutive turns from system side happens, we add utt directly to new_dial[LOG][-1]
                        new_dial[LOG][-1][SYS_UTT] += " " + utt
                        dial_hist[-1] += " " + utt
                        new_turn[DIAL_HIST] = " ".join(dial_hist)
                    else:
                        new_turn[SYS_UTT] = utt
                        new_turn[ORI_SYS_ANN]["tags"] = data_df["tags"][row_id]
                        new_turn[ORI_SYS_ANN]["speaker_idx"] = int(data_df["speaker_idx"][row_id])
                        dial_hist.append(f"<{SPEAKER2.upper()}> " + new_turn[SYS_UTT])
                        new_dial[LOG].append(new_turn)
                        new_turn = self.init_turn(turn_id=(int(data_df["utterance_idx"][row_id])+1)//2+1)
                        new_turn[DIAL_HIST] = " ".join(dial_hist)

                else:
                    if not new_turn[USR_UTT]:
                        new_turn[USR_UTT] = utt
                        new_turn[ORI_USR_ANN]["tags"] = data_df["tags"][row_id]
                        new_turn[ORI_USR_ANN]["speaker_idx"] = int(data_df["speaker_idx"][row_id])
                        dial_hist.append(f"<{SPEAKER1.upper()}> " + new_turn[USR_UTT])
                    else: # in this case, consecutive turns from user side happens, we add utt directly to new_turn
                        new_turn[USR_UTT] += " " + utt
                        dial_hist[-1] += " " + utt

                if row_id == len(data_df)-1 or data_df["utterance_idx"][row_id+1] == 1:
                    # append the rest dialog in case ends with user side
                    if new_turn[USR_UTT]:
                        new_dial[LOG].append(new_turn)

                    new_dial_id = f"{data_name}--{mode}--{dial_idx}"
                    new_data[new_dial_id] = new_dial
                    
                    if dial_idx % 10000 == 0:
                        self.save_dial(new_data, data_name=data_name, file_idx=file_idx, mode=mode)
                        new_data = {} # reset
                        file_idx += 1
                    dial_idx += 1
            if new_data: self.save_dial(new_data, data_name=data_name, file_idx=file_idx, mode=mode)
            print(f"finishing processing {dial_idx-1} dialogs for {mode} set ...")
        self.save_original_examples(data[:5], data_name)
        self.save_converted_examples(data_name)
        print("*"*10, f"finishing processing dataset {data_name}", "*"*10)


    def convai2(self):
        """
        incomplete dialog included, we remove dialog with equal or less than one turn"""
        from datasets import load_dataset
        data_name = "ConvAI2"
        mode = "train"
        data = load_dataset("conv_ai_2", split=mode)
        data_df = data.to_pandas()
        new_data, file_idx, dial_idx = {}, 1, 1
        for i in (range(len(data_df))):
            new_dial = self.init_dial(dial_idx=dial_idx)
            new_dial_id = f"{data_name}--{mode}--{dial_idx}"
            new_dial[ORI_DIAL_ID] = data_df["dialog_id"][i]
            new_dial[ORI_DIAL_INFO]["id"] = data_df["id"][i]
            new_dial[ORI_DIAL_INFO]["bot_profile"] = ["".join(persona) for persona in data_df["bot_profile"][i]]
            new_dial[ORI_DIAL_INFO]["user_profile"] = ["".join(persona) for persona in data_df["user_profile"][i]]
            new_dial[ORI_DIAL_INFO]["eval_score"] = int(data_df["eval_score"][i])
            new_dial[ORI_DIAL_INFO]["profile_match"] = int(data_df["profile_match"][i])
            if len(data_df["dialog"][i]) <= 2: continue
            if "Text is not given." in " ".join([turn["text"] for turn in data_df["dialog"][i]]): continue
            dial_hist = []
            for turn_idx, turn in enumerate(data_df["dialog"][i]):
                if turn_idx % 2 == 0:
                    new_turn = self.init_turn(turn_id=turn_idx//2+1)
                    new_turn[DIAL_HIST] = " ".join(dial_hist)
                    new_turn[USR_UTT] = turn["text"]
                    new_turn[ORI_USR_ANN]["id"] = turn["id"]
                    new_turn[ORI_USR_ANN]["sender"] = turn["sender"]
                    new_turn[ORI_USR_ANN]["sender_class"] = turn["sender_class"]

                    dial_hist.append(f"<{SPEAKER1.upper()}> " + new_turn[USR_UTT])
                else:
                    new_turn[SYS_UTT] = turn["text"]
                    new_turn[ORI_SYS_ANN]["id"] = turn["id"]
                    new_turn[ORI_SYS_ANN]["sender"] = turn["sender"]
                    new_turn[ORI_SYS_ANN]["sender_class"] = turn["sender_class"]
                    dial_hist.append(f"<{SPEAKER2.upper()}> " + new_turn[SYS_UTT])
                    new_dial[LOG].append(new_turn)
            if not new_turn[SYS_UTT]:
                new_dial[LOG].append(new_turn)
            new_data[new_dial_id] = new_dial
            if new_dial[DIAL_IDX] % 10000 == 0:
                self.save_dial(new_data, data_name=data_name, file_idx=file_idx, mode=mode)
                new_data = {} # reset
                file_idx += 1
            dial_idx += 1
        print(f"finishing processing {dial_idx-1} dialogs for {mode} set ...")
        if new_data: self.save_dial(new_data, data_name=data_name, file_idx=file_idx, mode=mode)
        self.save_original_examples(data[:5], data_name)
        self.save_converted_examples(data_name)
        print("*"*10, f"finishing processing dataset {data_name}", "*"*10)


    def antiscam(self):
        """
        0: attacker
        1: agent
        0 always starts conversation 
        1 always ends conversation
        """
        data_name = "AntiScam"
        data = self._load_txt(os.path.join(self.data_dir, data_name, "data/AntiScam_all.txt"), encoding='latin-1')
        new_data, file_idx, dial_idx, turn_idx, dial_hist = {}, 1, 1, 1, []
        mode = "train"
        new_dial = self.init_dial(dial_idx=dial_idx)
        new_turn = self.init_turn(turn_id=turn_idx)
        for row in (data):
            speaker, utt = row.split("\t")
            if speaker == "0":
                if new_turn[SYS_UTT]: # start a new turn
                    # wrap up the previous turn
                    new_dial[LOG].append(new_turn)
                    turn_idx += 1
                    dial_hist.append(f"<{SPEAKER1.upper()}> " + new_turn[USR_UTT])
                    dial_hist.append(f"<{SPEAKER2.upper()}> " + new_turn[SYS_UTT])
                    # start a new turn
                    new_turn = self.init_turn(turn_id=turn_idx)
                    new_turn[DIAL_HIST] = " ".join(dial_hist)
                    new_turn[USR_UTT] = utt.strip('\"')
                else: # multiple utt from '0'
                    new_turn[USR_UTT] += " " + utt.strip('\"')
                    new_turn[USR_UTT] = new_turn[USR_UTT].strip()
            elif speaker == "1":
                new_turn[SYS_UTT] += " " + utt.strip('"')
                new_turn[SYS_UTT] = new_turn[SYS_UTT].strip()
            elif not speaker: # finish a dialog
                if new_turn[SYS_UTT]: # wrap up the previous turn
                    new_dial[LOG].append(new_turn)
                new_dial_id = f"{data_name}--{mode}--{dial_idx}"
                new_data[new_dial_id] = new_dial
                if dial_idx % 10000 == 0:
                    self.save_dial(new_data, data_name=data_name, file_idx=file_idx, mode=mode)
                    new_data = {} # reset
                    file_idx += 1
                dial_idx += 1
                turn_idx = 1
                dial_hist = []
                new_dial = self.init_dial(dial_idx=dial_idx)
                new_turn = self.init_turn(turn_id=turn_idx)
            else:
                raise ValueError("Unknown speaker ... ")
        if new_turn[SYS_UTT]:
            new_dial[LOG].append(new_turn)
        new_dial_id = f"{data_name}--{mode}--{dial_idx}"
        new_data[new_dial_id] = new_dial
        print(f"finishing processing {dial_idx} dialogs for {mode} set ...")
        self.save_dial(new_data, data_name=data_name, file_idx=file_idx, mode=mode)

        if new_data: self.save_dial(new_data, data_name=data_name, file_idx=file_idx, mode=mode)
        self.save_original_examples(data[:150], data_name)
        self.save_converted_examples(data_name)
        print("*"*10, f"finishing processing dataset {data_name}", "*"*10)




    def run_all(self):
        # self.places()
        # self.chitchat()
        # self.prosocial()
        # self.hhrlhf()
        # self.empathetic()
        # self.convai2()
        self.antiscam()


    def copy_example(self):
        source_dir = self.save_dir
        for target_dir in [ "/home/qkun/projs/TOD-Project/Datasets/Open-Domain_PROCESSED/", "/home/qkun/projs/DialogStudio-Release/open-domain-dialogues/"]:
            # target_dir = "/home/qkun/projs/TOD-Project/Datasets/Open-Domain_PROCESSED/"
            # target_dir2 = "/home/qkun/projs/DialogStudio-Release/open-domain-dialogues/"
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