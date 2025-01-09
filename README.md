# Investor-Founder Matchmaking with Excel

This repository provides a Python script, **`matchmaker_excel.py`**, for scheduling investor-founder meetings based on three matching criteria:

1. **Investment Type** (e.g., Angel, Pre-Seed, Seed, Series A, Series B)  
2. **Business Type** (e.g., B2B, B2C, CPG, Enterprise)  
3. **Sector** (e.g., AI, FinTech, Cybersecurity, etc.)

Matches occur only if an investor and a founder share at least one “Yes” in **each** category.

---

## Requirements & Constraints

1. **Event Duration**: 8:00 AM – 12:00 PM  
2. **Session Timing & Structure**  
   - **10 time slots**, each lasting 20 minutes  
   - 5-minute break between each 20-minute session (implicit in the slot start times)  
   - **20 concurrent investor-founder pairings** per time slot  

3. **Matching Logic**  
   - A founder and an investor must align on at least one “Yes” in **each** of the three categories (Investment, Biz Type, Sector).  
   - **No repeated pairs**: Once an investor meets a founder, they cannot meet again in a later slot.  
   - **Investor rules**:  
     - One founder meeting per slot (so up to 10 total meetings if they attend all slots).  
     - They cannot meet the same founder more than once.  
   - **Founder rules**:  
     - Must meet at least one investor during the event (if a valid match is possible).  
     - They can meet multiple investors, but not more than one investor in the same slot.

4. **Output Format**  
   - The script writes results into **`Schedule.xlsx`**.  
   - Each time slot has a row in `Schedule.xlsx`, with up to 20 pairings split across columns labeled “Table 1 - Company,” “Table 1 - Investor,” “Table 2 - Company,” “Table 2 - Investor,” and so on.  

---

## Files

1. **`matchmaker_excel.py`**  
   - Main script that reads investor/founder data, applies matching logic, schedules meetings in 10 slots (20 pairs per slot), and writes the results to `Schedule.xlsx`.

2. **`Company Data.xlsx`**  
   - Excel sheet of founder data. Each row describes a company’s name and whether it has “Yes/No” for each Investment Type, Biz Type, and Sector.

3. **`Investor Data.xlsx`**  
   - Excel sheet of investor data. Each row details the “Investment Firm” name and “Yes/No” columns for each category.

4. **`Schedule.xlsx`**  
   - An Excel template with rows for the session start times (8:00 AM, 8:25 AM, 8:50 AM, etc.) and blank columns for table pairings that will be filled by the script.

---

## Installation & Usage

1. **Install Python 3** (if not already installed).

2. **Install Dependencies**:
   ```bash
   pip install pandas networkx openpyxl
File Placement:

Place Company Data.xlsx, Investor Data.xlsx, and Schedule.xlsx in the same directory as matchmaker_excel.py.
If you want to store them in a different folder, update the file paths in matchmaker_excel.py accordingly.
Run the script:

bash
Copy code
python matchmaker_excel.py
The script will process the data, find all valid investor-founder pairs, assign them into 10 slots with up to 20 pairs each, and fill Schedule.xlsx.
Check Schedule.xlsx:

Each time slot row (starting from row 2) will have up to 20 pairings.
Columns labeled “Table 1 - Company,” “Table 1 - Investor,” “Table 2 - Company,” “Table 2 - Investor,” etc., will be populated with the matched company and investor names.
Script Capabilities
Reads two Excel files (Company Data.xlsx and Investor Data.xlsx) and identifies all pairs that align on Investment Type, Biz Type, Sector.
Greedy Bipartite Matching per slot:
Ensures an investor only meets one founder per slot.
Ensures no repeated pairs across slots.
Truncates each slot to a maximum of 20 simultaneous meetings.
Writes the scheduled matches into Schedule.xlsx under the respective time slot rows and table columns.
Adapting the Script
Time Slots

If you need different times, edit the time_slots list in schedule_slots().
For example, if you want 8:00-8:20, 8:25-8:45, etc., adjust that array.
Meetings Per Slot (Default = 20)

If you want fewer or more parallel meetings, update matched_this_slot[:20] in schedule_slots() to the desired number.
“Yes/No” Column Names

Adjust the lists INVESTMENT_TYPE_COLS, BIZ_TYPE_COLS, SECTOR_COLS if your Excel columns differ (e.g., renaming “Sector: Cybersecurity” or adding new categories).
Ensuring Every Founder is Matched

The script attempts to match as many valid pairs as possible. However, if you have more founders than total pairing slots, some may remain unmatched.
For guaranteed coverage, consider adding a coverage step or using a constraint solver (Google OR-Tools).
Constraint Solvers

If you need strict coverage, fairness distribution, or advanced conflict resolution (e.g., last-minute cancellations), a specialized solver can better handle those advanced constraints.
Known Limitations
Greedy Matching: The script runs a bipartite matching each slot, which is often sufficient but not always “perfectly fair.” Some founders or investors with many possible matches might appear more frequently.
Coverage: Founders who have limited “Yes” overlap may still miss out if high-demand matches fill the 20 slots quickly.
Excel Layout Assumptions: The script assumes Schedule.xlsx has time slots in column A (rows 2 through 11 for the 10 slots) and at least 40 columns (for up to 20 pairs).
Support
For questions or customizations:

Open an issue in this GitHub repository.
Or contact the maintainers directly.
Enjoy using the Investor-Founder Matchmaking solution!