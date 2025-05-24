


# Towards Reliable Proof Generation with LLMs: <br> A Neuro-Symbolic Approach
This repository contains the code for the paper: https://arxiv.org/abs/2505.14479. </br>
**Authors: Oren Sultan, Eitan Stern, Dafna Shahaf, The Hebrew University of Jerusalem, Israel**. </br>



## 🚀 Setup

The code is implemented in **Python 3.10**.

To get started:

### 1. Create and activate the conda environment

```bash
conda env create -f environment.yml
conda activate FormalGeo_env  
```

Make sure to install required packages:
pip install formalgeo
pip install pandas
pip install openai
pip install matplotlib
Make sure to install the z3 library for the verifier:
pip install z3-solver

## 📁 Important Folders and Files

### `src/`


### `formalgeo7k_v1/`

This directory contains the FormalGeo7K dataset:

- `formalgeo7k_v1/gdl/theorem_GDL.json`  
  The **Geometry Definition Language (GDL)** theorem dictionary used across the dataset.

- `formalgeo7k_v1/problems/`  
  A collection of **problem JSON files**, each representing an individual problem in the FormalGeo7K dataset.

### `results/`

This directory contains:

- **Evaluation Data**  
  Subfolders grouped by difficulty level (`level_1` to `level_5`), each containing problems and their corresponding proof outputs evaluated in our experiments.

- **Figures Included in the Paper**
  - `correct_proofs_ablation.png` – *Figure 3*: Ablation study on correct proofs  
  - `retries_and_runs.png` – *Figure 4*: Effect of retries and multiple runs  
  - `tier_error_distribution.png` – *Figure 5*: Distribution of errors across difficulty tiers  
  - `analogy_stability.png` – *Figure 9*: Stability analysis of the analogy-based method



## Cite
 @article{sultan2025towards,
  title={Towards Reliable Proof Generation with LLMs: A Neuro-Symbolic Approach},
  author={Sultan, Oren and Stern, Eitan and Shahaf, Dafna},
  journal={arXiv preprint arXiv:2505.14479},
  year={2025}
}



## Contact
For inquiries, please send an email to oren.sultan@mail.huji.ac.il.

