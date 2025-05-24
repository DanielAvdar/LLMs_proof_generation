


# Towards Reliable Proof Generation with LLMs: A Neuro-Symbolic Approach
This repository contains the code for the paper: https://arxiv.org/abs/2505.14479. </br>
**Authors: Oren Sultan, Eitan Stern, Dafna Shahaf, The Hebrew University of Jerusalem, Israel**. </br>



## Setup

[//]: # (The code is implemented in python 3.8.12. To run it, please install the requirements.txt file:)

[//]: # (```bash)

[//]: # (pip install -r minimalrequirements.txt)

[//]: # (```)

## Where to start?

[//]: # (Explore the **paper_experiments_results** folder for restoring the results in the experiment )

[//]: # (&#40;each folder contains a separate README file&#41;. <br/>)

[//]: # (Run **runner.py** for running our algorithm on a specific example of pairs of texts. <br/>)

[//]: # (Note that you don't need to run coreference and qa_srl, as the output files have already exist in the repo. )

[//]: # (&#40;You should run coreference and qa_srl only if you use a new input text files, )

[//]: # (by setting run_coref=False, run_qasrl=False in analogous_matching_algorithm function&#41;)

[//]: # ()
[//]: # (## Important folders)

[//]: # ()
[//]: # (**paper_experiments_results**:<br/>)

[//]: # (Contains the datasets, the labels of the annotators, as well as the data which generates the results in the figures )

[//]: # (and tables of the three experiments. Each inner folder contains a separate README file.<br/>)

[//]: # ()
[//]: # (**data:**<br/>)

[//]: # (Includes the following folders:<br/>)

[//]: # (**original_text_files** -- all the original texts files &#40;including the stories and paragraphs from ProPara&#41;.<br/>)

[//]: # (**coref_text_files** -- all the texts files after coreference &#40;including the stories and paragraphs from ProPara&#41;.<br/>)

[//]: # (**propara** -- data files relevant to ProPara dataset, output files of the ranking lists for the different models )

[//]: # (   &#40;see Section 4.1 in the paper&#41;, and some code files to read and print stats on ProPara and the methods.<br/>)

[//]: # (   )
[//]: # (**s2e-coref:**<br/>)

[//]: # (Contains the implementation code for the coreference model that we used &#40;see Section 3.1 in the paper&#41;.<br/>)

[//]: # ()
[//]: # (**qasrl-modeling**<br/>)

[//]: # (Contains the implementation code for the QA-SRL model that we used &#40;see Section 3.2 in the paper&#41;.<br/>)

[//]: # ()
[//]: # (## Important py. files)

[//]: # ()
[//]: # (## Algorithm's code files)

[//]: # (**runner.py** -- runner of our analogous matching algorithm on given pairs.<br/>)

[//]: # (**find_mappings.py** -- run FMQ method on a given pair of texts  &#40;called from outside to generate_mappings function&#41;.<br/>)

[//]: # (**find_mappings_verbs.py** -- run FMV method on a given pair of texts &#40;called from outside to generate_mappings function&#41;.\)

[//]: # (**sentence_bert.py** -- run SBERT on a given pair of texts.<br/>)

[//]: # (**coref.py** -- run our coreference implementation on input files.<br/>)

[//]: # (**qa-srl.py** -- run our QA-SRL implementation on texts files &#40;after coref&#41;.<br/>)

[//]: # ()
[//]: # (## Experiment's code files)

[//]: # (**run_propara_all_pairs_exp.py** -- run experiment 1 &#40;see Section 4.1 in the paper&#41;.<br/>)

[//]: # (**analogies_mining_exp_annotators_consistency.py** -- run annotators consistency confusion matrix )

[//]: # (&#40;see Section 4.1 in the paper&#41;.<br/>)

[//]: # (**run_mappings_evaluation_exp.py** -- run experiment 2 &#40;see Section 4.2 in the paper&#41;.<br/>)

[//]: # (**run_robustness_to_paraphrases_exp.py** -- run experiment 3 &#40;see Section 4.3 in the paper&#41;.<br/>)

## Cite
@article{sultan2025towards, <br/>
  @article{sultan2025towards,
  title={Towards Reliable Proof Generation with LLMs: A Neuro-Symbolic Approach},
  author={Sultan, Oren and Stern, Eitan and Shahaf, Dafna},
  journal={arXiv preprint arXiv:2505.14479},
  year={2025}
} <br/>
}



## Contact
For inquiries, please send an email to oren.sultan@mail.huji.ac.il.


Towards Reliable Proof Generation with LLMs: A Neuro-Symbolic Approach