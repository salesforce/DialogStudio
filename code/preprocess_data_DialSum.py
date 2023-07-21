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
        self.save_dir = "/path/to/store/the/processed/dataset/" # e.g. ./data/processed/Dialogue-Summarization


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
            ORI_DIAL_ID: ori_dial_id,
            DIAL_IDX: dial_idx,
            ORI_DIAL_INFO: {},
            LOG: [],
            PROMPT: [],
        }
        return dial


    def init_turn(self, turn_id=0, dial_hist=[]):
        turn = {
            TURN_ID: turn_id,
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
            if filename.startswith("."): continue # ignore hidden files
            if filename.startswith("__"): continue # ignore hidden files
            if filename in exp_list: continue
            if filename.endswith(".py"): continue
            source_path = os.path.join(source_dir, filename)
            target_path = os.path.join(target_dir, filename)
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


    def _import_system_file(self, filename="", module_name=""):
        import importlib, sys
        spec = importlib.util.spec_from_file_location(module_name, filename)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module


    def tweetsum(self):
        """
        real data store in kaggle, need to download and preprocess first
        """
        data_name = "TweetSumm"
        # prepare data
        Modules = self._import_system_file(os.path.join(self.data_dir, data_name, "tweet_sum_processor.py"), "TweetSumProcessor")
        processor = Modules.TweetSumProcessor(os.path.join(self.data_dir, data_name, "archive/twcs/twcs.csv"))
        exp_list = ["tweet_sum_data_files", "archive", "tweet_sum_processor.py"]
        for mode in ["train", "val", "test"]:
            real_name = f"final_{mode}_tweetsum.jsonl" if mode != "val" else "final_valid_tweetsum.jsonl"
            path = os.path.join(self.data_dir, data_name, "tweet_sum_data_files", real_name)

            # split = self._load_jsonl(path)
            new_data = {}
            file_idx = 1
            original_data_sample = []

            with open(path) as f:
                dialog_with_summaries = processor.get_dialog_with_summaries(f.readlines())
                for dial_idx, dialog_with_summary in tqdm(enumerate(dialog_with_summaries)):
                    new_dial_id = f"{data_name}--{mode}--{dial_idx+1}"

                    json_format = dialog_with_summary.get_json()
                    dial = json.loads(json_format)
                    if mode == "train" and dial_idx < 5:
                        original_data_sample.append(dial)

                    new_dial = self.init_dial(dial_idx=dial_idx+1, ori_dial_id=dial["dialog"]["dialog_id"]) # idx starts from 1
                    new_dial[ORI_DIAL_INFO] = {
                        "summaries" : dial["summaries"]
                    }
                    turn_id, dial_hist = 1, []
                    new_turn = self.init_turn(turn_id=turn_id)
                    for idx, turn in enumerate(dial["dialog"]["turns"]):
                        utt = " ".join(turn["sentences"])
                        if turn["is_agent"]:
                            new_turn[SYS_UTT] += f" {utt}"
                            new_turn[SYS_UTT] = new_turn[SYS_UTT].strip()
                            if idx == len(dial["dialog"]["turns"]) - 1 or \
                                not dial["dialog"]["turns"][idx+1]["is_agent"]:

                                new_dial[LOG].append(new_turn)
                                turn_id += 1
                                if new_turn[USR_UTT]:
                                    dial_hist.append("<USER> " + new_turn[USR_UTT])
                                dial_hist.append("<SYSTEM> " + new_turn[SYS_UTT])
                                new_turn = self.init_turn(turn_id=turn_id)
                                new_turn[DIAL_HIST] = " ".join(dial_hist)
                        else:
                            new_turn[USR_UTT] += f" {utt}"
                            new_turn[USR_UTT] = new_turn[USR_UTT].strip()

                    new_data[new_dial_id] = new_dial
                    if (dial_idx+1) % 1000 == 0 or dial_idx+1 == len(dialog_with_summaries):
                        self.save_dial(new_data, data_name=data_name, file_idx=file_idx, mode=mode)
                        new_data = {} # reset
                        file_idx += 1
        
            if mode == "train": self.save_original_examples(original_data_sample, data_name)
        self.save_converted_examples(data_name)
        self.copy_related_files(data_name, exp_list)
        print("*"*10, f"finishing processing dataset {data_name}", "*"*10)


    def samsum(self):
        """
        1. achieved from HF datasets "samsum"
        2. no sys/user, but two human being, assuming the first utterance comes from user, ignore residual
        """
        data_name = "SAMSum"
        # prepare data
        from datasets import load_dataset
        data = load_dataset("samsum")
        for mode in ["train", "val", "test"]:
            real_name = mode if mode != "val" else "validation"
            new_data, file_idx = {}, 1

            for dial_idx, dial in tqdm(enumerate(data[real_name])):
                new_dial_id = f"{data_name}--{mode}--{dial_idx+1}"
                new_dial = self.init_dial(dial_idx=dial_idx+1, ori_dial_id=dial["id"]) # idx starts from 1
                new_dial[ORI_DIAL_INFO] = {
                    "summary" : dial["summary"]
                }
                dial_hist = []
                sep = "\r\n" if "\r\n" in dial["dialogue"] else "\n"
                for turn_idx, turn in enumerate(dial["dialogue"].split(sep)):
                    speaker, utt = turn.split(": ")[0], ": ".join(turn.split(": ")[1:])
                    if turn_idx % 2 == 0:
                        new_turn = self.init_turn(turn_id=turn_idx//2+1)
                        new_turn[DIAL_HIST] = " ".join(dial_hist)
                        new_turn[USR_UTT] = utt.strip().replace("  ", " ")
                        new_turn[ORI_USR_ANN]['speaker'] = speaker
                    else:
                        new_turn[SYS_UTT] = utt.strip().replace("  ", " ")
                        new_turn[ORI_SYS_ANN]['speaker'] = speaker
                        dial_hist.append("<USER> " + new_turn[USR_UTT])
                        dial_hist.append("<SYSTEM> " + new_turn[SYS_UTT])
                        new_dial[LOG].append(new_turn)

                new_data[new_dial_id] = new_dial
                if (dial_idx+1) % 1000 == 0 or dial_idx+1 == len(data[real_name]):
                    self.save_dial(new_data, data_name=data_name, file_idx=file_idx, mode=mode)
                    new_data = {} # reset
                    file_idx += 1
        
        self.save_original_examples(data["train"][:5], data_name)
        self.save_converted_examples(data_name)
        print("*"*10, f"finishing processing dataset {data_name}", "*"*10)


    def dialogsum(self):
        """
        1. we use the data from github: https://github.com/cylnlp/dialogsum/tree/main/DialogSum_Data 
            but, it is also available from HF datasets "knkarthick/dialogsum"
        2. no sys/user, but two human being, assuming the first utterance comes from user, ignore residual
        """
        data_name = "DialogSum"

        for mode in ["train", "val", "test"]:
            real_name = mode if mode != "val" else "dev"
            path = os.path.join(self.data_dir, data_name, f"DialogSum_Data/dialogsum.{real_name}.jsonl")
            data = self._load_jsonl(path)
            new_data, file_idx = {}, 1

            for dial_idx, dial in tqdm(enumerate(data)):
                new_dial_id = f"{data_name}--{mode}--{dial_idx+1}"
                new_dial = self.init_dial(dial_idx=dial_idx+1, ori_dial_id=dial["fname"]) # idx starts from 1
                for key in dial:
                    if key in ["fname", "dialogue"]: continue
                    new_dial[ORI_DIAL_INFO][key] = dial[key]

                dial_hist = []
                turns = dial["dialogue"].replace("PErson","Person").split("#Person")[1:]
                for turn_idx, turn in enumerate(turns):
                    speaker, utt = turn.split("#:")
                    speaker = "Person" + speaker
                    utt = utt.replace("\n","").strip()

                    if turn_idx % 2 == 0:
                        new_turn = self.init_turn(turn_id=turn_idx//2+1)
                        new_turn[DIAL_HIST] = " ".join(dial_hist)
                        new_turn[USR_UTT] = utt.strip()
                        new_turn[ORI_USR_ANN]['speaker'] = speaker.replace("#","")
                    else:
                        new_turn[SYS_UTT] = utt.strip()
                        new_turn[ORI_SYS_ANN]['speaker'] = speaker.replace("#","")
                        dial_hist.append("<USER> " + new_turn[USR_UTT])
                        dial_hist.append("<SYSTEM> " + new_turn[SYS_UTT])
                        new_dial[LOG].append(new_turn)

                new_data[new_dial_id] = new_dial
                if (dial_idx+1) % 1000 == 0 or dial_idx+1 == len(data):
                    self.save_dial(new_data, data_name=data_name, file_idx=file_idx, mode=mode)
                    new_data = {} # reset
                    file_idx += 1
        
            if mode == "train": self.save_original_examples(data[:5], data_name)
        self.save_converted_examples(data_name)
        self.copy_related_files(data_name, ['Baseline'])
        print("*"*10, f"finishing processing dataset {data_name}", "*"*10)


    def ami(self):
        """
        download processed data from https://drive.google.com/drive/folders/1BbmaZnzG9WrqOO-D3h211NOJePotqwQJ
        the data is separated into 6 files based on annotation
        here we extract the dialog context based on file "dialogueActs"
        no train/val/test split, consider all as train
        no readme file needs to be copied
        we use ABCD instead of USR_UTT/SYS_UTT

        1. each dialog contains more than 2 speaker? yes A,B,C,D
        2. speaking in any order? yes A->B->C->D
        """
        data_name = "AMI"
        mode = "train"
        data_dir = os.path.join(self.data_dir, data_name, "dialogueActs")
        new_data, dial_idx = {}, 1

        for filename in os.listdir(data_dir):
            dial = self._load_json(os.path.join(data_dir, filename))
            new_dial = self.init_dial(dial_idx=dial_idx) # idx starts from 1
            # # # save dialog log
            new_dial[ORI_DIAL_INFO]["dialog history"] = []
            for turn in dial:
                new_dial[ORI_DIAL_INFO]["dialog history"].append(turn["speaker"] + " : " + turn["text"])

            # # # save abstractive summary
            if os.path.exists(os.path.join(self.data_dir, data_name, "abstractive", filename)):
                abs_sum = self._load_json(os.path.join(self.data_dir, data_name, "abstractive", filename))
                new_dial[ORI_DIAL_INFO]["abstractive summary"] = abs_sum
            # # # save extractive summary
            if os.path.exists(os.path.join(self.data_dir, data_name, "extractive", filename)):
                ext_sum = self._load_json(os.path.join(self.data_dir, data_name, "extractive", filename))
                new_dial[ORI_DIAL_INFO]["extractive summary"] = []
                for ext_turn in ext_sum:
                    new_dial[ORI_DIAL_INFO]["extractive summary"].append(ext_turn["speaker"] + " : " + ext_turn["text"])

            new_dial_id = f"{data_name}--{mode}--{dial_idx}"
            new_dial[ORI_DIAL_ID] = filename
            new_data[new_dial_id] = new_dial
            dial_idx += 1
            if dial_idx == 2:
                self.save_original_examples(dial, data_name)

        self.save_dial(new_data, data_name=data_name, file_idx=1, mode=mode)
        self.save_converted_examples(data_name)
        print("*"*10, f"finishing processing dataset {data_name}", "*"*10)

        
    def icsi(self):
        """
        similar as AMI
        speak can last to A->J
        """
        data_name = "ICSI"
        mode = "train"
        data_dir = os.path.join(self.data_dir, data_name, "dialogueActs")
        new_data, dial_idx = {}, 1

        for filename in os.listdir(data_dir):
            dial = self._load_json(os.path.join(data_dir, filename))
            new_dial = self.init_dial(dial_idx=dial_idx) # idx starts from 1
            # # # save dialog log
            new_dial[ORI_DIAL_INFO]["dialog history"] = []
            for turn in dial:
                new_dial[ORI_DIAL_INFO]["dialog history"].append(turn["speaker"] + " : " + turn["text"])

            # # # save abstractive summary
            if os.path.exists(os.path.join(self.data_dir, data_name, "abstractive", filename)):
                abs_sum = self._load_json(os.path.join(self.data_dir, data_name, "abstractive", filename))
                new_dial[ORI_DIAL_INFO]["abstractive summary"] = abs_sum
            # # # save extractive summary
            if os.path.exists(os.path.join(self.data_dir, data_name, "extractive", filename)):
                ext_sum = self._load_json(os.path.join(self.data_dir, data_name, "extractive", filename))
                new_dial[ORI_DIAL_INFO]["extractive summary"] = []
                for ext_turn in ext_sum:
                    new_dial[ORI_DIAL_INFO]["extractive summary"].append(ext_turn["speaker"] + " : " + ext_turn["text"])

            new_dial_id = f"{data_name}--{mode}--{dial_idx}"
            new_dial[ORI_DIAL_ID] = filename
            new_data[new_dial_id] = new_dial
            dial_idx += 1
            if dial_idx == 2:
                self.save_original_examples(dial, data_name)

        self.save_dial(new_data, data_name=data_name, file_idx=1, mode=mode)
        self.save_converted_examples(data_name)
        print("*"*10, f"finishing processing dataset {data_name}", "*"*10)


    def qmsum(self):
        data_name = "QMSum"
        for mode in ["train", "val", "test"]:
            path = os.path.join(self.data_dir, data_name, f"data/ALL/{mode}")
            data = self._load_dir_json(path)
            new_data, file_idx = {}, 1
            for dial_idx, dial in tqdm(enumerate(data)):
                new_dial_id = f"{data_name}--{mode}--{dial_idx+1}"
                new_dial = self.init_dial(dial_idx=dial_idx+1)
                for key_ in dial:
                    if key_ == "meeting_transcripts": continue
                    new_dial[ORI_DIAL_INFO][key_] = dial[key_]
                
                new_dial[ORI_DIAL_INFO]["dialog history"] = []
                for turn in dial["meeting_transcripts"]:
                    new_dial[ORI_DIAL_INFO]["dialog history"].append(turn["speaker"] + " : " + turn["content"])

                new_data[new_dial_id] = new_dial
                if (dial_idx+1) % 1000 == 0 or dial_idx+1 == len(data):
                    self.save_dial(new_data, data_name=data_name, file_idx=file_idx, mode=mode)
                    new_data = {} # reset
                    file_idx += 1
        
            if mode == "train": self.save_original_examples(data[:5], data_name)
        self.save_converted_examples(data_name)
        self.copy_related_files(data_name, ['Baseline'])
        print("*"*10, f"finishing processing dataset {data_name}", "*"*10)


    def mediasum(self):
        data_name = "MediaSum"
        split_id = self._load_json(os.path.join(self.data_dir, data_name, "data/train_val_test_split.json"))
        data = self._load_json(os.path.join(self.data_dir, data_name, "data/news_dialogue.json"))

        split_id2mode, new_data, file_idx, dial_idx = {}, {}, {}, {}
        for mode in ["train", "val", "test"]:
            for dial_id in split_id[mode]:
                split_id2mode[dial_id] = mode
            new_data[mode], file_idx[mode], dial_idx[mode] = {}, 1, 1

        for dial in tqdm(data):
            new_dial = self.init_dial() # idx starts from 1
            new_dial[ORI_DIAL_ID] = dial['id']
            for key_ in dial:
                if key_ in ["id", "utt", "speaker"]: continue
                new_dial[ORI_DIAL_INFO][key_] = dial[key_]
            dialog_log = []
            for idx in range(len(dial["utt"])):
                dialog_log.append(dial["speaker"][idx] + " : " + dial["utt"][idx])
            new_dial[ORI_DIAL_INFO]["dialog history"] = dialog_log

            mode = split_id2mode.get(dial["id"], "train")
            new_dial_id = f"{data_name}--{mode}--{dial_idx[mode]}"
            new_dial[DIAL_IDX] = dial_idx[mode]
            new_data[mode][new_dial_id] = new_dial
            dial_idx[mode] += 1

            if len(new_data[mode]) == 1000:
                self.save_dial(new_data[mode], data_name=data_name, file_idx=file_idx[mode], mode=mode)
                new_data[mode] = {} # reset
                file_idx[mode] += 1

        # if there are some unsaved dialogs left, save it now
        for mode in ["train", "val", "test"]:
            if new_data[mode]:
                self.save_dial(new_data[mode], data_name=data_name, file_idx=file_idx[mode], mode=mode)

        self.save_original_examples(data[:5], data_name)
        self.save_converted_examples(data_name)
        self.copy_related_files(data_name, ["data"])
        print("*"*10, f"finishing processing dataset {data_name}", "*"*10)


    def crd3(self):
        """
        For this dataset, we choose present only chunk_size=2 offset=0
        some file are missing for chunk size = 2
        """
        data_name = "CRD3"
        exp_list = []
        for filename in os.listdir(os.path.join(self.data_dir, data_name)):
            if filename == "readme.txt": continue
            if filename == "LICENSE": continue
            exp_list.append(filename)
        for mode in ["train", "val", "test"]:
            new_data, file_idx, dial_idx = {}, 1, 1
            for file_name in self._load_txt(os.path.join(self.data_dir, data_name, f"data/aligned data/{mode}_files")):
                file_path = os.path.join(self.data_dir, data_name, f"data/aligned data/c=2/{file_name}_2_0.json")
                if not os.path.exists(file_path): continue
                data = self._load_json(file_path)

                new_dial_id = f"{data_name}--{mode}--{dial_idx}"
                new_dial = self.init_dial(dial_idx=dial_idx)
                new_dial[ORI_DIAL_ID] = file_name
                new_dial[ORI_DIAL_INFO] = data
                new_data[new_dial_id] = new_dial
                dial_idx += 1

                if (dial_idx) % 1000 == 0:
                    self.save_dial(new_data, data_name=data_name, file_idx=file_idx, mode=mode)
                    new_data = {} # reset
                    file_idx += 1
            if new_data: self.save_dial(new_data, data_name=data_name, file_idx=file_idx, mode=mode)
            if mode == "train": self.save_original_examples([new_dial[ORI_DIAL_INFO]], data_name)
        self.save_converted_examples(data_name)
        self.copy_related_files(data_name, exp_list)
        print("*"*10, f"finishing processing dataset {data_name}", "*"*10)


    def ectsum(self):
        data_name = "ECTSum"
        for mode in ["train", "val", "test"]:
            new_data, file_idx, dial_idx = {}, 1, 1
            data_dir = os.path.join(self.data_dir, data_name, "data/final", mode)
            for file_name in os.listdir(os.path.join(data_dir, "ects")):
                if not file_name.endswith("txt"): pdb.set_trace()
                ect_data = self._load_txt(os.path.join(data_dir, "ects", file_name))
                sum_data = self._load_txt(os.path.join(data_dir, "gt_summaries", file_name))

                new_dial_id = f"{data_name}--{mode}--{dial_idx}"
                new_dial = self.init_dial(dial_idx=dial_idx)
                new_dial[ORI_DIAL_INFO]["file_name"] = file_name
                new_dial[ORI_DIAL_INFO]["ect"] = ect_data
                new_dial[ORI_DIAL_INFO]["summary"] = sum_data
                new_data[new_dial_id] = new_dial
                dial_idx += 1

                if (dial_idx) % 1000 == 0:
                    self.save_dial(new_data, data_name=data_name, file_idx=file_idx, mode=mode)
                    new_data = {} # reset
                    file_idx += 1
            if new_data: self.save_dial(new_data, data_name=data_name, file_idx=file_idx, mode=mode)
            if mode == "train": self.save_original_examples([new_dial[ORI_DIAL_INFO]], data_name)
        self.save_converted_examples(data_name)
        self.copy_related_files(data_name, ['codes', 'data'])
        print("*"*10, f"finishing processing dataset {data_name}", "*"*10)


    def run_all(self):
        # self.todsum()
        # self.tweetsum()
        # self.samsum()
        # self.dialogsum()
        # self.ami()
        # self.icsi()
        # self.qmsum()
        self.mediasum()
        # self.crd3()
        # self.ectsum()
        pass


    def copy_example(self):
        source_dir = self.save_dir
        target_dir = "/home/qkun/projs/TOD-Project/Datasets/Dialogue-Summarization_PROCESSED/"
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