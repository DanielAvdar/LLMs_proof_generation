


# Towards Reliable Proof Generation with LLMs: <br> A Neuro-Symbolic Approach
This repository contains the code for the paper: https://arxiv.org/abs/2505.14479. </br>
**Authors: Oren Sultan, Eitan Stern, Dafna Shahaf, The Hebrew University of Jerusalem, Israel**. </br>



## 🚀 Setup

The code is implemented in **Python 3.10**.

To get started:

### Create and activate the conda environment

```bash
conda env create -f environment.yml
conda activate FormalGeo_env  
```

### Install testing dependencies

To run the tests, you'll need to install pytest:

```bash
pip install pytest
```


## 📁 Important Folders and Files

### `src/`

- `formalgeo/create_problems_proofs_similarity_dataset.py`
  The creation of the abstracted dataset (Section 3.1)
- `formalgeo/similar_proofs_model.py`
  The regressor model training (Section 3.2). Run with argument --run-model-pred 1 to run the model.
- `formalgeo/similar_proofs_retrieval.py`
  Retrieve analogies for our analogy-based method, or random problems for the base model baseline (see Section 4). This code is used in LLM_analogy_based_solver.py. 
- `formalgeo/LLM_analogy_based_solver.py`
  Run the LLM solver, default base model is o1 (set in argument "model"). (whether with analogy-based / base model settings, should be set in "variant" argument). You should set your key for OpenAI model. You should set the problem you want to solve in chosen_problems_by_level. The output proof file and log will be generate in /results folder
- `formalgeo/geometric_verifier.py`
  Our SMT verifier based on z3 library (see Section 3.4)
  

- `formalgeo/prompt/geometry_similar_problems_prompt.txt`
  The prompt given to the LLM solver (see Figure 6)
- `formalgeo/verifier/verifier.py`
  Our code for the verifier to support tier 1 errors, based on FormalGeo codebase (see Section 3.4)

- `formalgeo/experiments/exp_new.py`
  Our code to run the plots for the results of the experiments (see Section 5)


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

## ⚠️ Important Notes

You should **manually overwrite** the following files in your conda environment:

- Replace `~/miniforge3/envs/FormalGeo_env/lib/python3.10/site-packages/formalgeo/solver/interactive.py`  
  with `src/formalgeo/solver/interactive.py`

- Replace `~/miniforge3/envs/FormalGeo_env/lib/python3.10/site-packages/formalgeo/tools/output.py`  
  with `src/formalgeo/tools/output.py`

This ensures that the solver and output behavior matches the modified logic described in the paper and used in our experiments.







## Cite
 @article{sultan2025towards,
  title={Towards Reliable Proof Generation with LLMs: A Neuro-Symbolic Approach},
  author={Sultan, Oren and Stern, Eitan and Shahaf, Dafna},
  journal={arXiv preprint arXiv:2505.14479},
  year={2025}
}



## 🧪 Running Tests

To run the test suite:

```bash
# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Run tests for a specific module
pytest tests/formalgeo/tools/

# Generate test coverage report
pytest --cov=src
```

## Contact
For inquiries, please send an email to oren.sultan@mail.huji.ac.il.

