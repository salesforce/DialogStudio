# The ATIS (Airline Travel Information System) Dataset
本仓库包含了 Python pickle 格式和 Rasa NLU JSON 格式（[https://rasa.com/docs/nlu/dataformat/#json-format](https://rasa.com/docs/nlu/dataformat/#json-format)）的 ATIS Dataset(数据集)，并提供了读取脚本和示例代码。

## 数据样本
### 原始格式
```text
   0:         flight: BOS i want to fly from boston at 838 am and arrive in denver at 1110 in the morning EOS
                              BOS                                        O
                                i                                        O
                             want                                        O
                               to                                        O
                              fly                                        O
                             from                                        O
                           boston                      B-fromloc.city_name
                               at                                        O
                              838                       B-depart_time.time
                               am                       I-depart_time.time
                              and                                        O
                           arrive                                        O
                               in                                        O
                           denver                        B-toloc.city_name
                               at                                        O
                             1110                       B-arrive_time.time
                               in                                        O
                              the                                        O
                          morning              B-arrive_time.period_of_day
                              EOS                                        O
```

### Rasa NLU Json 格式
```json
{
    "rasa_nlu_data": {
        "common_examples": [
            {
                "text": "i would like to find a flight from charlotte to las vegas that makes a stop in st. louis",
                "intent": "flight",
                "entities": [
                    {
                        "start": 35,
                        "end": 44,
                        "value": "charlotte",
                        "entity": "fromloc.city_name"
                    },
                    {
                        "start": 48,
                        "end": 57,
                        "value": "las vegas",
                        "entity": "toloc.city_name"
                    },
                    {
                        "start": 79,
                        "end": 88,
                        "value": "st. louis",
                        "entity": "stoploc.city_name"
                    }
                ]
            },
            ...
        ]
    }
}
```

## 数据统计
| 样本数 | 词汇数 | 实体数 | 意图数 |
| --- | --- | --- | --- |
| 4978(训练集)+893(测试集) | 943 | 129 | 26 |

## 示例代码
[summary_data.py](summary_data.py) 中包含了读取原始数据的代码，用户可以参考该代码，实现从原始文件读取数据。

## 下载

| 数据格式 | 训练集 | 测试集 |
| --- | --- | --- |
| Python 3 Pickle 格式 | [atis.train.pkl](data/raw_data/ms-cntk-atis/atis.train.pkl) | [atis.test.pkl](data/raw_data/ms-cntk-atis/atis.test.pkl) |
| Rasa NLU JSON 格式 | [train.json](data/standard_format/rasa/train.json) | [test.json](data/standard_format/rasa/test.json) |



## Credit
* 本项目的原始数据集来自 [ATIS DataSet by siddhadev](https://www.kaggle.com/siddhadev/atis-dataset)，部分代码亦来自此处。
    * NOTE: `ATIS DataSet by siddhadev` 数据集则来自于 [MicroSoft CNTK Examples](https://github.com/Microsoft/CNTK/tree/master/Examples/LanguageUnderstanding/ATIS/Data)

## 同类项目
* https://github.com/mesnilgr/is13 也提供了 ATIS 数据集，但该数据集只有实体数据没有意图数据。