# MultiModalQA: Complex Question Answering over Text, Tables and Images

MultiModalQA is a challenging question answering dataset that requires joint reasoning over text, tables and images, consisting of 29,918 examples. This repository contains the MultiModalQA dataset, format description, and link to the images file.

For more details check out our ICLR21 paper ["MultiModalQA: Complex Question Answering over Text, Tables and Images"](https://openreview.net/pdf?id=ee6W5UgQLa),
and [website](https://allenai.github.io/multimodalqa/).  


### Changelog

- `23/04/2021` Initial release. 



# MultiModalQA Dataset Format

In the [dataset](https://github.com/allenai/multimodalqa/tree/master/dataset) folder you will find the following file question and contexts files:
1) `MultiModalQA_train/dev/test.jsonl.gz` - contains questions and answers, for train, dev and test set respectively
2) `tables.jsonl.gz` - contains the tables contexts
3) `texts.jsonl.gz` - contains the texts contexts
4) `images.jsonl.gz` - contains the metadata of the images, the images themselves can be downloaded from [images.zip](https://multimodalqa-images.s3-us-west-2.amazonaws.com/final_dataset_images/final_dataset_images.zip) 

# QA Files Format

Each line of the examples files (e.g. `MultiModalQA_train/dev.jsonl.gz`) contains one question, alongside its answers, metadata (described below, the all related context documents will be found there) and supporting context ids (the exact context ids that contain the answers and intermediate answers)

```json
{
  "qid": "5454c14ad01e722c2619b66778daa98b",
  "question": "who owns the rights to little shop of horrors?",
  "answers": ["answer1", "answer2"],
  "metadata": {},
  "supporting_context": [{
      "doc_id": "46ae2a8e7928ed5a8e5f9c59323e5e49",
      "doc_part": "table"
    },
    {
      "doc_id": "d57e56eff064047af5a6ef074a570956",
      "doc_part": "image"
    }]
}
```

`MultiModalQA_test.jsonl.gz` contains is of similar format, but does not contain `answers` 
nor `supporting_context`.

## A Single Answer

Each answer in the `answers` field contains an answer string that may be of type string or yesno, each answer points to the text, table or image context documents where it can be found (see context files for matching ids):

```json
{
  "answer": "some string here",
  "type": "string/yesno",
  "modality": "text/image/table",
  "text_instances": [{
          "doc_id": "b95b35eabfc80a0f1a8fd8455cd6d109",
          "part": "text",
          "start_byte": 345,
          "text": "AnswerText"
        }],
  "table_indices": [[5, 2]],
  "image_instances": [{
              "doc_id": "d57e56eff064047af5a6ef074a570956",
              "doc_part": "image"
            }]
}
```

## A Single Question Metadata

The metadata of each question contains its type, modalities required to solve it, the wikipedia entities that appear in the question and in the answers, the machine generated question (the question before human rephrasing), as well as an annotation field containing the rephrasing accuracy and confidence (between 0 and 1), and a list of texts docs ids and image docs ids and table id that are part of the full context for
this question (some context docs contain the answer and some are distractors).
We include a list of intermediate answers, these are the answers of the sub-questions composing the multi-modal question, providing supervision for multi-step training.  

```json
{
    "type": "Compose(TableQ,ImageListQ)",
    "modalities": [
      "image",
      "table"
    ],
    "wiki_entities_in_question": [
      {
        "text": "Domenico Dolce",
        "wiki_title": "Domenico Dolce",
        "url": "https://en.wikipedia.org/wiki/Domenico_Dolce"
      }
    ],
    "wiki_entities_in_answers": [],
    "pseudo_language_question": "In [Members] of [LGBT billionaires] what was the [Net worth USDbn](s) when the [Name] {is completely bald and wears thick glasses?}",
    "rephrasing_meta": {
      "accuracy": 1.0,
      "edit_distance": 0.502092050209205,
      "confidence": 0.7807520791930855
    },
    "image_doc_ids": [
      "89c1b7c3c061cc80bb98d99cbbec50dd",
      "0f3858e2186b2030b77c759fc727e20b"
    ],
    "text_doc_ids": [
      "498369348c988d866b5fac0add45bac5",
      "57686242cf542e30cbad13037017b478"
    ],
    "intermediate_answers": ["single_answer_format(1)", "single_answer_format(2)"], 
    "table_id": "46ae2a8e7928ed5a8e5f9c59323e5e49"
  }
```

# A Single Table Format

Each line of `tables.jsonl.gz` represents a single table. `table_rows` is a list of rows, and each row contains is a list of cells. Each cell is provided with its text string and wikipedia entities. `header` provides for each column in the table: its name alongside parsing metadata computed such as NERs and item types. 

```json
{
  "title": "Dutch Ruppersberger",
  "url": "https://en.wikipedia.org/wiki/Dutch_Ruppersberger",
  "id": "dcd7cb8f23737c6f38519c3770a6606f",
  "table": {
    "table_rows": [
      [
        {
          "text": "Baltimore County Executive",
          "links": [
            {
              "text": "Baltimore County Executive",
              "wiki_title": "Baltimore County Executive",
              "url": "https://en.wikipedia.org/wiki/Baltimore_County_Executive"
            }
          ]
        },
      ]
    ],
    "table_name": "Electoral history",
    "header": [
      {
        "column_name": "Year",
        "metadata": {
          "parsed_values": [
            1994.0,
            1998.0
          ],
          "type": "float",
          "num_of_links": 9,
          "ner_appearances_map": {
            "DATE": 10,
            "CARDINAL": 1
          },
          "is_key_column": true,
          "entities_column": true
        }
      }
    ]
  }
}
```

# A Single Image Metadata Format

Each line in `images.jsonl.gz` holds metadata for each image. The `path` provided points to the image file  in the provided images directory.

```json
{
  "title": "Taipei",
  "url": "https://en.wikipedia.org/wiki/Taipei",
  "id": "632ea110be92836441adfb3167edf8ff",
  "path": "Taipei.jpg"
}
```

# A Single Text Metadata Format
Each line in `texts.jsonl.gz` represents a single text paragraph. 

```json
{
  "title": "The Legend of Korra (video game)",
  "url": "https://en.wikipedia.org/wiki/The_Legend_of_Korra_(video_game)",
  "id": "16c61fe756817f0b35df9717fae1000e",
  "text": "Over three years after its release, the game was removed from sale on all digital storefronts on December 21, 2017."
}
```
