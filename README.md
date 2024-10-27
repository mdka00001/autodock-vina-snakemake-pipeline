# AutoDock Vina Snakemake Pipeline

This repository contains a Snakemake pipeline to automate molecular docking using AutoDock Vina on a batch of receptors and ligands in a concurrent environment. The pipeline uses the [FlipbookApp](https://github.com/MolecularFlipbook/FlipbookApp) for visualizations and analysis.

## Table of Contents
- [Installation](#installation)
- [Pipeline Setup](#pipeline-setup)
- [Usage](#usage)
- [Project Structure](#project-structure)

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/your-repo.git
    cd your-repo
    ```

2. **Clone the FlipbookApp**:
    Within the repository directory, clone the [FlipbookApp](https://github.com/MolecularFlipbook/FlipbookApp) repository:
    ```bash
    git clone https://github.com/MolecularFlipbook/FlipbookApp
    ```

3. **Install AutoDock Vina**:
    Make sure AutoDock Vina is installed. For Ubuntu, you can install it with:
    ```bash
    sudo apt install vina
    ```

4. **Install Open Babel**:
    Open Babel (obabel) is required to handle molecular file conversions:
    ```bash
    sudo apt install obabel
    ```

## Pipeline Setup

1. **Directory Structure**:
    Create the necessary directories to store receptor and ligand files:
    ```bash
    mkdir -p data/proteins
    mkdir -p data/ligands
    ```

2. **Add Receptors and Ligands**:
    - Place receptor files (proteins) in the `data/proteins` directory.
    - Place ligand files in the `data/ligands` directory.

## Usage

To run the pipeline, simply execute the `Snakefile.py` with Snakemake:
```bash
snakemake -s Snakefile.py


your-repo/
├── data/
│   ├── proteins/          # Directory for receptor files
│   └── ligands/           # Directory for ligand files
├── FlipbookApp/           # Clone of the FlipbookApp repository
├── Snakefile.py           # Snakemake pipeline script
└── README.md              # Project documentation


