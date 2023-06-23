# MediaSum
This large-scale media interview dataset contains 463.6K transcripts with abstractive summaries, collected from interview transcripts and overview / topic descriptions from NPR and CNN.

<ins>Please restrict your usage of this dataset to research purpose only</ins>. And please cite our paper:

**<a href="https://arxiv.org/abs/2103.06410">MediaSum: A Large-scale Media Interview Dataset for Dialogue Summarization</a>**

_Chenguang Zhu*, Yang Liu*, Jie Mei and Michael Zeng (*: Equal contribution)_

_North American Chapter of the Association for Computational Linguistics (**NAACL**), Mexico City, Mexico, 2021._

• Sample data:
```
{
  "id": "NPR-11",
  "program": "Day to Day",
  "date": "2008-06-10",
  "url": "https://www.npr.org/templates/story/story.php?storyId=91356794",
  "title": "Researchers Find Discriminating Plants",
  "summary": "The \"sea rocket\" shows preferential treatment to plants that are its kin. Evolutionary plant ecologist Susan Dudley of McMaster University in Ontario discusses her discovery.",
  "utt": [
    "This is Day to Day.  I'm Madeleine Brand.",
    "And I'm Alex Cohen.",
    "Coming up, the question of who wrote a famous religious poem turns into a very unchristian battle.",
    "First, remember the 1970s?  People talked to their houseplants, played them classical music. They were convinced plants were sensuous beings and there was that 1979 movie, \"The Secret Life of Plants.\"",
    "Only a few daring individuals, from the scientific establishment, have come forward with offers to replicate his experiments, or test his results. The great majority are content simply to condemn his efforts without taking the trouble to investigate their validity.",
    ...
    "OK. Thank you.",
    "That's Susan Dudley. She's an associate professor of biology at McMaster University in Hamilt on Ontario. She discovered that there is a social life of plants."
  ],
  "speaker": [
    "MADELEINE BRAND, host",
    "ALEX COHEN, host",
    "ALEX COHEN, host",
    "MADELEINE BRAND, host",
    "Unidentified Male",    
    ..."
    Professor SUSAN DUDLEY (Biology, McMaster University)",
    "MADELEINE BRAND, host"
  ]
}
```

• Data split:
<p align="left">
  <img src="https://github.com/zcgzcgzcg1/MediaSum/blob/main/figures/data_split.png" width="350" alt="data_split">
</p>


• Comparison with previous dialogue summarization datasets:
<p align="left">
  <img src="https://github.com/zcgzcgzcg1/MediaSum/blob/main/figures/data_comparison.png" width="650" alt="data_split">
</p>

• Data distribution:
<p align="left">
  <img src="https://github.com/zcgzcgzcg1/MediaSum/blob/main/figures/data_distribution.png" width="650" alt="data_split">
</p>

## Ethics:
We have used only the publicly available transcripts data from the media sources and adhere to their only-for-research-purpose guideline.

As media and guests may have biased views, the transcripts and summaries will likely contain them. The content of the transcripts and summaries only reflect the views of the media and guests, and should be viewed with discretion. 


## Citation
If you are using MediaSum in your work, please cite using the following Bibtex entry:

```
@article{zhu2021mediasum,
  title={MediaSum: A Large-scale Media Interview Dataset for Dialogue Summarization},
  author={Zhu, Chenguang and Liu, Yang and Mei, Jie and Zeng, Michael},
  journal={arXiv preprint arXiv:2103.06410},
  year={2021}
}
```

