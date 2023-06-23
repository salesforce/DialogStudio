# STAR: A Schema-Guided Dialog Dataset for Transfer Learning

This dataset and how it came to be, along with some baseline models, are described [in this paper](https://arxiv.org/abs/2010.11853).

## Data Format

Each JSON file in the `dialogues` directory contains one dialogue in the following format:

| Key                        | Value                                                                             |
|----------------------------|-----------------------------------------------------------------------------------|
| "AnonymizedUserWorkerID"   | String that is unique for each worker but unrelated to the worker's AMT Worker ID |
| "AnonymizedWizardWorkerID" | String that is unique for each worker but unrelated to the worker's AMT Worker ID |
| "BatchID"                  | We collected dialogues in batches, identified by this ID                          |
| "CompletionLevel"          | Can be "Complete", "EarlyDisconnectDuringDialogue", or "DisconnectDuringDialogue" |
| "DialogueID"               | Unique ID of this dialogue                                                        |
| "Events"                   | List of events representing the dialogue                                          |
| "FORMAT-VERSION"           |                                                                                   |
| "Scenario"                 | Dictionary containing information about the scenario of this dialogue             |
| "UserQuestionnaire"        | List of question/answer pairs for questions given to the user                     |
| "WizardQuestionnaire"      | List of question/answer pairs for questions given to the wizard                   |


## Citation

Please use the following bibtex entry if you are using STAR for your research:
```

@article{mosig2020star,
  	   author = {Johannes E. M. Mosig and Shikib Mehri and Thomas Kober},
        title = "{STAR: A Schema-Guided Dialog Dataset for Transfer Learning}",
      journal = {arXiv e-prints},
     keywords = {Computer Science - Computation and Language},
         year = 2020,
        month = oct,
          eid = {arXiv:2010.11853},
archivePrefix = {arXiv},
       eprint = {2010.11853},
 primaryClass = {cs.CL},
}
```