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

For SODA, we design 6 prompts for each dialog and below shows the template:
```python
{
    "Imagine you are {speaker_system} and you are talking to {speaker_user}. Generate a coherent and appropriate response.",
    "In the role of {speaker_system}, engage with {speaker_user}. Formulate a response that is both consistent with the conversation and suitable to the context.",
    "As {speaker_system}, you are in a dialogue with {speaker_user}. Create a coherent and relevant reply that fits the ongoing discussion.",
    "Assuming the persona of {speaker_system}, you're conversing with {speaker_user}. Generate a logical and suitable response that aligns with the conversation.",
    "Imagine yourself as {speaker_system} engaging with {speaker_user}. Your task is to produce a coherent and fitting response to continue the conversation.",
    "Pretend to be {speaker_system} in a conversation with {speaker_user}. Construct a response that maintains the coherence of the dialogue and is appropriate for the context."
}
```
Where 'speaker_user' and 'speaker_system' represent the 'PersonX' name and the 'PersonY' name, respectively. 


