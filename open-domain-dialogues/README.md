### Open-Domain Dialogues

Below is a general format for open domain dialogues:

```js
{
    "dataset_name--train/val/test--dialog_id": {
        "original dialog id": str,
        "dialog index": int,
        "original dialog info": dict,
        "log": [
            {
                "turn id": int,
                "user utterance": str,
                "system response": str,
                "dialog history": str,
                "original user1 side information": dict,
                "original user2 side information": dict,
            },
         	...
        ],
        "prompt": [
            "This is a conversation between two speakers talking about history. Given the dialog context, please generate a relevant response.",
            ...
        ]
    },
    ...
}
```

Chitchat dialogues generally do not involve extra annotations. Therefore the "original user1/2 side information" are usually left blank. Unlike task-oriented dialogues, chitchat does not necessarily end on the user2 side (system side in task-oriented dialogues). So, there are some dialogues contain only user1 utterance in the last turn.


