# Investor-Founder Matchmaking with Excel

This repository provides a Python script, **`matchmaker_excel.py`**, for scheduling investor-founder meetings based on three matching criteria:

1. **Investment Type** (e.g., Angel, Pre-Seed, Seed, Series A, Series B)  
2. **Business Type** (e.g., B2B, B2C, CPG, Enterprise)  
3. **Sector** (e.g., AI, FinTech, Cybersecurity, etc.)

A match occurs only if an investor and a founder share **at least one "Yes"** in **each** category.

---

## Requirements & Constraints

### 1. Event Duration
- **8:00 AM – 12:00 PM**

### 2. Session Timing & Structure
- **10 time slots**, each lasting 20 minutes
- **5-minute break** between each 20-minute session
- **20 concurrent investor-founder pairings** per time slot

### 3. Matching Logic
- Matches require alignment on at least one "Yes" in **each** of the three categories (Investment, Business Type, Sector).
- **No repeated pairs**: Once an investor meets a founder, they cannot meet again.

#### Investor Rules:
- Can meet one founder per slot (up to 10 total meetings).
- Cannot meet the same founder more than once.

#### Founder Rules:
- Must meet at least one investor during the event (if a valid match exists).
- Can meet multiple investors, but not more than one in the same slot.

### 4. Output Format
- The script writes results to **`Schedule.xlsx`**.
- Each time slot has a **row** in `Schedule.xlsx`, with **up to 20 pairings** split across columns labeled:
  - "Table 1 - Company," "Table 1 - Investor"
  - "Table 2 - Company," "Table 2 - Investor," etc.

---

## Files

1. **`matchmaker_excel.py`**
   - Main script. Reads investor and founder data, applies matching logic, schedules meetings, and writes results to `Schedule.xlsx`.

2. **`Company Data.xlsx`**
   - Contains founder/startup information. Each row includes a "Startup Name" and "Yes/No" under each category (Investment, Business Type, Sector).

3. **`Investor Data.xlsx`**
   - Contains investor information. Each row includes "Investment Firm" and "Yes/No" under each category (Investment, Business Type, Sector).

4. **`Schedule.xlsx`**
   - Excel template with rows for session start times (e.g., 8:00 AM, 8:25 AM, etc.) and blank table columns to be filled by the script.

---

## Installation & Usage

### 1. Install Python 3
Ensure Python 3 is installed on your system.

### 2. Install Dependencies
Run the following command to install required libraries:
```bash
pip install pandas networkx openpyxl
```

### 3. File Placement
Place `Company Data.xlsx`, `Investor Data.xlsx`, and `Schedule.xlsx` in the same directory as `matchmaker_excel.py`.
If you prefer a different folder structure, update the file paths in the script accordingly.

### 4. Run the Script
Execute the script with the following command:
```bash
python matchmaker_excel.py
```
The script will:
- Read investor and founder data.
- Identify all valid matches based on the three criteria.
- Assign matches to 10 time slots (up to 20 pairs per slot).
- Write the schedule to `Schedule.xlsx`.

### 5. Check the Output
Open `Schedule.xlsx` to view the results:
- Each time slot (starting from row 2) will list up to 20 pairings.
- Columns labeled "Table 1 - Company," "Table 1 - Investor," etc., will display matched company and investor names.

---

## Script Capabilities

- Reads `Company Data.xlsx` and `Investor Data.xlsx` to identify valid matches.
- Implements **Greedy Bipartite Matching** for each slot:
  - Ensures one founder per investor per slot.
  - Prevents duplicate investor-founder pairs across slots.
  - Limits each slot to 20 simultaneous meetings.
- Writes the scheduled matches to `Schedule.xlsx`.

---

## Adapting the Script

### Time Slots
To modify time slots (e.g., 8:00–8:20, 8:25–8:45), edit the `time_slots` list in the `schedule_slots()` function.

### Meetings per Slot
By default, the script limits each slot to 20 pairs. Update this by modifying the slicing `[:20]` in the code.

### Column Names
Adjust `INVESTMENT_TYPE_COLS`, `BIZ_TYPE_COLS`, and `SECTOR_COLS` if your Excel column headers differ (e.g., "Investment Type: Angel" instead of "Angel Investor").

### Ensuring Every Founder Is Matched
The script uses a greedy approach. If you want to guarantee that all founders are matched (and there are more founders than available spots), consider adding a coverage step or using a constraint solver like Google OR-Tools.

---

## Known Limitations

1. **Greedy Matching**
   - Matches are based on availability and fairness but might not always be "optimal" in complex scenarios.

2. **Coverage**
   - Founders with limited overlap in categories might remain unmatched if other high-demand pairs fill the slots.

3. **Excel Layout Assumptions**
   - The script assumes `Schedule.xlsx` contains time slots in column A (rows 2–11 for 10 slots) and has at least 40 columns for 20 pairings.

---

## Support
For questions or suggestions, open an issue in this repository or contact the maintainers directly.

Enjoy using the Investor-Founder Matchmaking solution!

