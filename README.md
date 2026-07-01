# Candidate Transformer

A configurable candidate data transformation pipeline that ingests candidate information from multiple sources, merges them into a canonical profile, tracks provenance and confidence, and generates different JSON outputs using runtime configuration.

---

## Features

- Multi-source candidate ingestion (Resume PDF + Recruiter CSV)
- Canonical candidate schema
- Identity resolution across sources
- Data normalization
  - Email
  - Phone (E.164)
  - Dates (YYYY-MM)
  - Country (ISO-3166 Alpha-2)
- Candidate merging
- Provenance tracking
- Confidence scoring
- Runtime configurable projection
- Output validation

---

## Project Structure

```text
candidate-transformer/
│
├── app.py
├── input/
├── output/
├── src/
├── requirements.txt
└── README.md
```

---

## Setup

Clone the repository.

```bash
git clone <repository-url>
cd candidate-transformer
```

Create a virtual environment.

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

---

## Running the Project

### Default Canonical Output

```bash
python app.py
```

### Verbose Execution

```bash
python app.py --verbose --pretty
```

### Recruiter Projection

```bash
python app.py \
    --config src/projection/sample_configs/recruiter.json
```

### Compact Projection

```bash
python app.py \
    --config src/projection/sample_configs/compact.json
```

---

## CLI Arguments

| Argument | Description |
|----------|-------------|
| `--resume` | Resume PDF input |
| `--csv` | Recruiter CSV input |
| `--config` | Runtime projection configuration |
| `--output` | Output JSON path |
| `--verbose` | Display pipeline execution |
| `--pretty` | Pretty-print JSON output |
| `--explain` | Display additional processing details |

---

## Sample Output

### Default Configuration

Produces the complete canonical candidate profile containing:

- Candidate ID
- Personal Information
- Contact Information
- Location
- Skills
- Experience
- Education
- Provenance
- Overall Confidence

### Recruiter Configuration

Produces a recruiter-friendly JSON containing only essential hiring fields.

### Compact Configuration

Produces a lightweight candidate profile with only the most important information.

---

## Validation

Every projected output is validated before being written.

Validation includes:

- Required fields
- Data types
- Email format
- Phone format (E.164)
- Date format (YYYY-MM)
- Country format (ISO-3166 Alpha-2)
- Skill schema
- Confidence range

---

## Tests

The project has been tested with:

- Resume + Recruiter CSV
- Default projection
- Recruiter projection
- Compact projection
- Missing field handling
- Runtime configuration validation

---

## Demo

A short demonstration video (~2 minutes) is included with the submission, showing:

- Running the pipeline
- Default output
- Custom projection output
- Brief explanation of the runtime projection design

---

## Design Highlights

- Modular architecture with independent processing stages
- Canonical internal schema separates ingestion from projection
- Runtime configurable projection without code changes
- Deterministic merging with provenance tracking
- Explainable confidence scoring