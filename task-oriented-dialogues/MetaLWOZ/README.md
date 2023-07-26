A Dataset of Multi-Domain Dialogs for the Fast Adaptation of Conversation Models

# Intro
Meta-Learning Wizard-of-Oz (MetaLWOz) is a dataset designed to help develop models capable of predicting user responses in unseen domains. It can improve dialog systems, such as those used in voice assistants, to help users accomplish tasks such as booking a flight. This dataset is particularly suited for meta-learning dialog models or fine-tuning models with transfer-learning approaches. This dataset aims to reduce the amount of data required to train domain-specific dialog systems and it is one of the first datasets designed with meta-learning dialog models in mind.

The problem that MetaLWOz is designed to solve is that neural dialog systems must learn from very large datasets in order to output grammatically correct sentences. This makes it extremely hard to scale the system to new domains that feature limited in-domain data. Moving from booking a table at a restaurant to buying a plane ticket requires knowing very different user queries, for example.

The role of the user in dialogs is growing as a research focus. While a dialog system trained on a large corpus from a source such as Twitter or Reddit may output grammatically correct sentences and stay generally on-topic, it will likely fail to predict the utterances of customers interacting with a goal-oriented bot, such as a travel assistant.

Conversely, a system trained solely on a small dataset of domain-specific dialogs will fail to produce coherent responses or will overfit on the training dialogs.

## A new dataset for training adaptable task-oriented dialog systems
This large dataset was created by crowdsourcing 37,884 goal-oriented dialogs, covering 227 tasks in 47 domains. Domains include bus schedules, apartment search, alarm setting, banking, and event reservation. Each dialog was grounded in a scenario with roles, pairing a person acting as the bot and a person acting as the user. (This is the Wizard of Oz reference—using people behind the curtain who act as the machine). Each pair were given a domain and a task, and instructed to converse for 10 turns to satisfy the user’s queries. For example, if a user asked if a bus stop was operational, the bot would respond that the bus stop had been moved two blocks north, which starts a conversation that addresses the user’s actual need.

The goal was to automate the user utterances so domain-specific dialog systems are easier to train, requiring less domain-specific data. Combined with large general conversational corpora or smaller goal-oriented datasets like MultiWOz, this dataset can be especially useful for training, fine-tuning, and evaluating dialog systems.

The [MetaLWOz dataset](https://www.microsoft.com/en-us/research/project/metalwoz/) is initially being used as the baseline for the DSTC8 dialog competition. Please cite the work if you use the dataset!
