# 📊 Complete Guide: Generate Synthetic Training Data

**Last Updated:** November 8, 2025
**Estimated Time:** 2-4 hours
**Status:** Ready to Execute

---

## 📋 Quick Overview

```
Backend API (FastAPI)
    ↓ (generates Kundali for random birth data)
Synthetic Data Generator
    ↓ (calls API 10,000 times)
training_data.csv (10,000 records × 215 columns)
    ↓ (validate quality)
Data Validator
    ↓
validation_report.json (quality metrics)
```

---

## ✅ PRE-EXECUTION CHECKLIST

Before starting, verify:

- [ ] Python 3.8+ installed: `python --version`
- [ ] Required libraries installed: `pip install requests pandas numpy`
- [ ] Backend API code exists in `server/` directory
- [ ] `synthetic_data_generator.py` exists in `server/ml/`
- [ ] `data_validator.py` exists in `server/ml/`
- [ ] `monitor_generation.py` exists in `server/ml/` (for real-time tracking)
- [ ] At least 500 MB free disk space
- [ ] Git repository initialized (to track changes)

---

## 🚀 EXECUTION PLAN

### STEP 1: Open Terminal #1 - START BACKEND API

```bash
# Navigate to project root
cd C:\Users\ACER\Desktop\FInalProject

# Start FastAPI server
python -m uvicorn server.main:app --reload --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

✅ **LEAVE THIS TERMINAL OPEN!**

---

### STEP 2: Test Backend is Running

In a **new terminal**, test the API:

```bash
# Windows
curl http://localhost:8000/health

# Or use PowerShell
Invoke-WebRequest http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "success": true,
  "data": {
    "status": "healthy",
    "ephemeris": "initialized",
    "database": "connected"
  }
}
```

✅ If you see this, backend is ready!

---

### STEP 3: Open Terminal #2 - MONITOR GENERATION (Optional but Recommended)

In another terminal:

```bash
cd C:\Users\ACER\Desktop\FInalProject\server\ml

# Start the real-time monitor
# It will watch for training_data.csv and show progress
python monitor_generation.py --target 10000 --interval 5
```

**Expected Output:**
```
================================================================================
 SYNTHETIC DATA GENERATION MONITOR
================================================================================

⏳ Waiting for file to be created...
```

✅ **LEAVE THIS TERMINAL OPEN!** (It will update every 5 seconds)

---

### STEP 4: Open Terminal #3 - RUN THE GENERATOR

In another **new terminal**:

```bash
cd C:\Users\ACER\Desktop\FInalProject

# Run the synthetic data generator
python -m server.ml.synthetic_data_generator
```

**What happens:**
1. Generator creates random birth parameters
2. Calls backend API for Kundali generation
3. Extracts 200+ features from response
4. Generates 8 target labels
5. Saves to `training_data.csv`

**Expected Progress Output:**
```
2025-11-08 10:30:15,123 - root - INFO - Starting generation of 10000 synthetic records...
2025-11-08 10:30:20,456 - root - INFO - Generated 100/10000 records
2025-11-08 10:30:25,789 - root - INFO - Generated 200/10000 records
2025-11-08 10:30:30,123 - root - INFO - Generated 300/10000 records
...
```

**Monitor Terminal (#2) will show:**
```
📊 PROGRESS
   [████████████████████░░░░░░░░░░░░░░░░░░░░░░] 35.5% (3,550/10,000 records)

⏱️  TIMING
   Elapsed: 0h 28m 45s
   ETA: 0h 52m 30s
   Completion: ~11:23:15

🚀 SPEED
   2.06 records/second
   123 records/minute

📁 FILE INFO
   Rows: 3,550
   Columns: 215
   Size: 18.45 MB
```

⏱️ **Estimated Time:** 30 minutes to 2 hours (depending on system speed)

---

## 🎯 What Gets Generated

### Dataset Structure
```
training_data.csv
├── id (1-10000)
├── birth_date (YYYY-MM-DD)
├── birth_time (HH:MM)
├── location (city name)
├── is_synthetic (True)
├── FEATURES (200+):
│   ├── Planet positions (sun_degree, moon_degree, ...)
│   ├── House placements (sun_house, moon_house, ...)
│   ├── Planetary strengths (sun_strength, mars_strength, ...)
│   ├── Yoga indicators (raj_yoga_present, parivartana_yoga_present, ...)
│   ├── Dasha information (current_dasha_remaining_years)
│   └── Divisional charts (d1_d9_alignment, chart_quality_score)
└── TARGETS (8):
    ├── career_potential (0-100)
    ├── wealth_potential (0-100)
    ├── marriage_happiness (0-100)
    ├── children_prospects (0-100)
    ├── health_status (0-100)
    ├── spiritual_inclination (0-100)
    ├── chart_strength (0-100)
    └── life_ease_score (0-100)
```

---

## ✓ AFTER GENERATION COMPLETES

### Step 5: Validate Data Quality

```bash
cd C:\Users\ACER\Desktop\FInalProject\server\ml

# Run validator
python data_validator.py
```

**Expected Output:**
```
============================================================
DATA VALIDATION REPORT
============================================================

Dataset Size: 10000 records
Features: 215

✓ Quality Score: 92.35%
✓ Status: PASS

Check Results:
  • Duplicates: PASS
  • Feature Ranges: PASS
  • Missing Values: PASS
  • Target Distribution: PASS
  • Outliers: PASS

============================================================
```

**Success Criteria:**
- ✅ Quality Score > 85%
- ✅ Status = PASS
- ✅ All checks = PASS
- ✅ validation_report.json created

---

### Step 6: Quick Data Inspection

```bash
# Open Python terminal
python
```

Then in Python:

```python
import pandas as pd

# Load the data
df = pd.read_csv('training_data.csv')

# Basic info
print(f"Records: {len(df)}")
print(f"Columns: {len(df.columns)}")
print(f"\nFirst 5 rows:")
print(df.head())

# Check targets
targets = ['career_potential', 'wealth_potential', 'marriage_happiness',
           'children_prospects', 'health_status', 'spiritual_inclination',
           'chart_strength', 'life_ease_score']

print("\n=== TARGET STATISTICS ===")
for target in targets:
    print(f"{target}:")
    print(f"  Mean: {df[target].mean():.2f}")
    print(f"  Std:  {df[target].std():.2f}")
    print(f"  Min:  {df[target].min():.2f}")
    print(f"  Max:  {df[target].max():.2f}")

# Exit
exit()
```

---

## 🚨 TROUBLESHOOTING

### Issue 1: "Connection refused" error

```
ConnectionError: Failed to connect to API at http://localhost:8000
```

**Solution:**
- Check Terminal #1: Is the backend API running?
- Run: `python -m uvicorn server.main:app --reload --port 8000`
- Verify: `curl http://localhost:8000/health`

---

### Issue 2: "API request took too long" (Timeout)

```
TimeoutError: API request timeout after 30 seconds
```

**Solution (Option A):** Generate fewer records
```python
# Edit synthetic_data_generator.py line 445:
# Change: num_records=10000
# To:     num_records=1000
```

**Solution (Option B):** Increase timeout in generator
```python
# Edit synthetic_data_generator.py line 138:
# Change: timeout=30
# To:     timeout=60
```

---

### Issue 3: Out of memory error

```
MemoryError: Unable to allocate 2.50 GiB for an array
```

**Solution:**
- Generate in batches
- Check available RAM: `Get-ComputerInfo | Select-Object TotalPhysicalMemory`
- Close other applications
- Split into smaller CSV files

---

### Issue 4: "File already exists" error

```
FileExistsError: training_data.csv already exists
```

**Solution:**
```bash
# Rename old file
ren training_data.csv training_data_old.csv

# Or delete it
del training_data.csv

# Then re-run generator
python synthetic_data_generator.py
```

---

## 📊 EXPECTED FINAL RESULTS

After successful generation and validation:

```
Files Created:
├── training_data.csv           (50-100 MB, 10,000 rows)
├── validation_report.json      (Quality metrics)
└── Generated data summary

Key Metrics:
✓ Total Records: 10,000
✓ Total Features: 215 (200+ astrology features)
✓ Total Targets: 8 (life area predictions)
✓ Quality Score: > 85%
✓ Duplicates: 0 or <1%
✓ Missing Values: < 5%
✓ File Size: 50-100 MB
✓ Generation Time: 30 min - 2 hours
```

---

## 🎯 NEXT STEPS AFTER DATA GENERATION

Once you have `training_data.csv` with quality score > 85%:

### Phase 2: Train ML Models
```bash
cd server/ml
python train_models.py
```

This will:
- Split data (70/15/15)
- Train Neural Network
- Train XGBoost
- Evaluate performance
- Save models

### Phase 3: Deploy Prediction API
The `/ml/predict` endpoint will be ready to serve predictions

---

## 💾 FILE LOCATIONS

```
C:\Users\ACER\Desktop\FInalProject\
├── server/
│   ├── main.py (backend API)
│   ├── ml/
│   │   ├── synthetic_data_generator.py ✅ (RUN THIS)
│   │   ├── data_validator.py ✅ (THEN THIS)
│   │   ├── monitor_generation.py ✅ (OPTIONAL - TRACK PROGRESS)
│   │   ├── training_data.csv (OUTPUT - 10,000 records)
│   │   └── validation_report.json (OUTPUT - quality metrics)
│   └── routes/
│       └── kundali.py (generates Kundali)
└── ML_IMPLEMENTATION_GUIDE.md (reference)
```

---

## ✨ SUMMARY

```
Terminal 1: python -m uvicorn server.main:app --reload
Terminal 2: python monitor_generation.py  (optional)
Terminal 3: python -m server.ml.synthetic_data_generator
           ↓ (waits for completion)
           python data_validator.py
           ↓
Done! training_data.csv ready for ML training
```

---

## ⏱️ TIME ESTIMATE

| Phase | Duration | Status |
|-------|----------|--------|
| Backend startup | 10 sec | ✅ Quick |
| Data generation | 30 min - 2 hrs | ⏳ Variable |
| Data validation | 5 min | ✅ Quick |
| **Total** | **35 min - 2.5 hrs** | ✅ Ready |

---

## ✅ SUCCESS CRITERIA

You're done when:
- ✅ `training_data.csv` exists with 10,000 rows
- ✅ Quality score > 85%
- ✅ No "Connection refused" errors
- ✅ All 8 target variables present
- ✅ All 215 columns present

**Then you're ready for Phase 2: Train ML Models!**
