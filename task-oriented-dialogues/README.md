### Task Oriented Dialogues

General formats:

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
                "original user side information": dict,
                "original system side information": dict,
                "dst": str,
                "dst accumulated": str
            },
         	...
        ],
        "external knowledge non-flat": {
            "metadata": dict,
            "slots and values": dict
            "intents": dict,
            ...
        },
        "external knowledge": str,
        "intent knowledge": str,
        "prompt": [
            "This is a bot helping users to get navigation. Given the dialog context and external database, please generate a relevant system response for the user.",
            ...
        ]
    },
```