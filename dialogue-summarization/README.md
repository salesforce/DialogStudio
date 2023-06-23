### Dialogue Summarizations

General formats:

```js
{
    "dataset_name--train/val/test--dialog_id": {
        "original dialog id": str,
        "dialog index": int,
        "original dialog info": {
            "summary": str,
        },
        "log": [
            {
                "turn id": int,
                "user utterance": str,
                "system response": str,
                "dialog history": str,
                "original user side information": dict,
                "original system side information": dict,
            },
         	...
        ],
        "prompt": [
            "This is a conversation between two speakers. Given the dialogue context, please generate a summarization about the dialogue.",
            ...
        ]
    },
```

Notice that we cannot form a turn with utterances from only two sides for those datasets consisting of multi-party dialogs (e.g. AMI, ICSI). Therefore, we dump the dialog context and summary in the "original dialog info" and leave the "log" blank.
