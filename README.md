# AI-Based Honeypot Attack Detection System

## Overview

This project combines honeypot technology and machine learning to detect cyber attacks.

## Technologies

- Python
- Cowrie Honeypot
- Dionaea Honeypot
- Scikit-Learn
- Pandas
- Linux

## Workflow

1. Deploy honeypots
2. Capture attacker activity
3. Extract features from logs
4. Generate dataset
5. Train Random Forest model
6. Predict attack type

## Features Used

- Total Attempts
- Unique Usernames
- Failed Attempts
- Success Attempts
- Average Time Gap
- Command Count
- Session Duration

## Project Architecture

Attacker
↓
Cowrie / Dionaea
↓
JSON Logs
↓
Feature Extraction
↓
CSV Dataset
↓
Random Forest Model
↓
Attack Classification


## Results

- Classification of Brute Force and Interactive Attacks
- Average Cross Validation Accuracy: 71.67%
