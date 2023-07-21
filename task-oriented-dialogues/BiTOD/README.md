# BiToD: A Bilingual Multi-Domain Dataset For Task-Oriented Dialogue Modeling

This repository includes the dataset and baselines of the paper:

**BiToD: A Bilingual Multi-Domain Dataset For Task-Oriented Dialogue Modeling** (Accepted in NeurIPS 2021 Track on Datasets and Benchmarks) [[PDF]](https://arxiv.org/pdf/2106.02787.pdf). 

**Authors**: [Zhaojiang Lin](https://zlinao.github.io), [Andrea Madotto](https://andreamad8.github.io), [Genta Indra Winata](https://gentawinata.com), Peng Xu, Feijun Jiang, Yuxiang Hu, Chen Shi, Pascale Fung


## Abstract:
Task-oriented dialogue (ToD) benchmarks provide an important avenue to measure progress and develop better conversational agents. However, existing datasets for end-to-end ToD modelling are limited to a single language, hindering the development of robust end-to-end ToD systems for multilingual countries and regions. Here we introduce BiToD, the first bilingual multi-domain dataset for end-to-end task-oriented dialogue modeling. BiToD contains over 7k multi-domain dialogues (144k utterances) with a large and realistic parallel knowledge base. It serves as an effective benchmark for evaluating bilingual ToD systems and cross-lingual transfer learning approaches. We provide state-of-the-art baselines under three evaluation settings (monolingual, bilingual and cross-lingual). The analysis of our baselines in different settings highlights 1) the effectiveness of training a bilingual ToD system comparing to two independent monolingual ToD systems, and 2) the potential of leveraging a bilingual knowledge base and cross-lingual transfer learning to improve the system performance in the low resource condition.

## Dataset
Training, validation and test data are avalible in `data` folder. We also provide the data split for cross-lingual few shot setting.
```
{
    dialogue_id:{
        "Scenario": {
            "WizardCapabilities": [
            ],
            "User_Goal": {
            }
        }
        "Events":{
            {
                "Agent": "User",
                "Actions": [
                    {
                        "act": "inform_intent",
                        "slot": "intent",
                        "relation": "equal_to",
                        "value": [
                        "restaurants_en_US_search"
                        ]
                    }
                ],
                "active_intent": "restaurants_en_US_search",
                "state": {
                "restaurants_en_US_search": {}
                },
                "Text": "Hi, I'd like to find a restaurant to eat",
            },
            {
                "Agent": "Wizard",
                "Actions": [
                    {
                        "act": "request",
                        "slot": "price_level",
                        "relation": "",
                        "value": []
                    }
                ],
                "Text": "Hi there. Would you like a cheap or expensive restaurant?",
                "PrimaryItem": null,
                "SecondaryItem": null,
            },
            ...
        }
    }
}
```
## Citation:
The bibtex is listed below:
<pre>
@article{lin2021bitod,
  title={BiToD: A Bilingual Multi-Domain Dataset For Task-Oriented Dialogue Modeling},
  author={Lin, Zhaojiang and Madotto, Andrea and Winata, Genta Indra and Xu, Peng and Jiang, Feijun and Hu, Yuxiang and Shi, Chen and Fung, Pascale},
  journal={arXiv preprint arXiv:2106.02787},
  year={2021}
}
</pre>