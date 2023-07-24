### Knowledge Grounded Dialogues

Below is a general format for knowledge-grounded dialogues:
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


Acknowledgement: Under this folder, a portion of the datasets has been further refined based on the work done by [UnifiedSKG](https://github.com/HKUNLP/UnifiedSKG). We extend our profound appreciation for their valuable work. If you use their work, please also give them due citation. Thank you!

