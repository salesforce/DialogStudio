# What is CoSQL?

CoSQL is a corpus for building cross-domain Conversational text-to-SQL systems. It is the dialogue version of the Spider and SParC tasks. CoSQL consists of 30k+ turns plus 10k+ annotated SQL queries, obtained from a Wizard-of-Oz collection of 3k dialogues querying 200 complex databases spanning 138 domains. Each dialogue simulates a real-world DB query scenario with a crowd worker as a user exploring the database and a SQL expert retrieving answers with SQL, clarifying ambiguous questions, or otherwise informing of unanswerable questions.

# CoSQL includes three tasks:
- SQL-grounded dialogue state tracking to map user utterances into SQL queries if possible given the interaction history
- natural language response generation based on an executed SQL and its results for user verification
- user dialogue act prediction to detect and resolve ambiguous and unanswerable questions

# Citation:
```commandline
@article{yu2019cosql,
  title={Cosql: A conversational text-to-sql challenge towards cross-domain natural language interfaces to databases},
  author={Yu, Tao and Zhang, Rui and Er, He Yang and Li, Suyi and Xue, Eric and Pang, Bo and Lin, Xi Victoria and Tan, Yi Chern and Shi, Tianze and Li, Zihan and others},
  journal={arXiv preprint arXiv:1909.05378},
  year={2019}
}
```

