### Natural Language Understanding Dialogues

Below is a general format for Natural Language Understanding dialogues:
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
                "external knowledge": str,
            },
         	...
        ]
        // "prompt": list, # To be added
    },
    ...
}
```
Please refer to each dataset folder for more details.
