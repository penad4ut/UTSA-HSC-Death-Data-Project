# UTSA-HSC-Death-Data-Project  
Multi-Source Mortality Integration and Obituary Evidence Extraction System

## Overview
The UTSA-HSC-Death-Data-Project is a mortality integration platform was designed and engineered under the leadership of Dr. Mahanaz Syed, whose team developed innovative methods to consolidate, validate, and reconcile death information from multiple institutional and external sources. The system incorporates LLM-based obituary extraction, identity linkage algorithms, and multi-source reconciliation workflows to produce accurate, research-ready mortality records for clinical studies and outcomes analysis.

Foundational institutional needs for improved mortality ascertainment emerged within CTSA- and P30-supported NIH research programs at UT San Antonio Health Science Center (UTSA-HSC). This platform represents a purpose-built, significantly expanded system designed by Dr. Syed to address persistent gaps in survival measurement and follow-up completeness across oncology, registry, and real-world evidence studies.

## Key Features
- **Multi-source integration**  
  - Institutional EHR death indicators  
  - State-level data (On Availability)  
  - Social Security Death Master File (SSADMF)  
  - National Death Index (NDI) matching outputs  
  - Public obituary sources  

- **LLM-based obituary extraction**  
  - Extracts name, date of birth, date of death, places, and identifiers  
  - Converts unstructured obituary narratives into structured evidence  
  - Produces fields suitable for linkage and quality checks  

- **Identity linkage workflows**  
  - Deterministic and probabilistic matching  
  - Configurable thresholds  
  - Handles partial information and multi-field uncertainty  

- **Reconciliation engine**  
  - Prioritizes highest-quality source  
  - Produces a unified “best-available” mortality record  
  - Flags discrepancies for human review  
  - Generates audit trails  

- **Research-ready outputs**  
  - Structured JSON  
  - CSV/Parquet options  
  - Optional FHIR® DeathRecord / Observation mappings

## Data Privacy Notice
This repository contains only non-PHI source code and synthetic or illustrative example files. No protected health information (PHI), identifiable patient data, or confidential institutional information is stored or distributed through this repository.
