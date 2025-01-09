#!/usr/bin/env python3
import pandas as pd
import networkx as nx
from networkx.algorithms import bipartite

def load_data(investors_file, founders_file):
    investors_df = pd.read_csv(investors_file)
    founders_df = pd.read_csv(founders_file)
    return investors_df, founders_df

def find_valid_pairs(investors_df, founders_df):
    valid_pairs = []
    investment_types = ["angel", "venture", "private_equity"]
    business_types = ["startup", "sme", "scale_up"]
    sectors = ["technology", "healthcare", "finance"]
    for _, inv_row in investors_df.iterrows():
        investor_name = inv_row["investor_name"]
        for _, fdr_row in founders_df.iterrows():
            founder_name = fdr_row["founder_name"]
            inv_invest_type_match = any(inv_row[it] == "Yes" and fdr_row[it] == "Yes" for it in investment_types)
            inv_business_type_match = any(inv_row[bt] == "Yes" and fdr_row[bt] == "Yes" for bt in business_types)
            inv_sector_match = any(inv_row[s] == "Yes" and fdr_row[s] == "Yes" for s in sectors)
            if inv_invest_type_match and inv_business_type_match and inv_sector_match:
                valid_pairs.append((investor_name, founder_name))
    return valid_pairs

def schedule_slots(valid_pairs, investors_df, founders_df):
    num_slots = 10
    schedule = [[] for _ in range(num_slots)]
    used_pairs = set()
    investors = list(investors_df["investor_name"].unique())
    founders = list(founders_df["founder_name"].unique())
    for slot_idx in range(num_slots):
        graph = nx.Graph()
        graph.add_nodes_from(investors, bipartite=0)
        graph.add_nodes_from(founders, bipartite=1)
        for inv, fdr in valid_pairs:
            if (inv, fdr) not in used_pairs:
                graph.add_edge(inv, fdr)
        matching_dict = bipartite.matching.maximum_matching(graph, top_nodes=set(investors))
        matched_this_slot = []
        matched_investors = set()
        matched_founders = set()
        for inv in investors:
            if inv in matching_dict:
                fdr = matching_dict[inv]
                if fdr not in matched_founders and inv not in matched_investors:
                    matched_this_slot.append((inv, fdr))
                    matched_investors.add(inv)
                    matched_founders.add(fdr)
        matched_this_slot = matched_this_slot[:20]
        schedule[slot_idx] = matched_this_slot
        for pair in matched_this_slot:
            used_pairs.add(pair)
    return schedule

def ensure_founders_coverage(schedule, valid_pairs, founders_df):
    founders = list(founders_df["founder_name"].unique())
    found_founders = set()
    for slot_pairs in schedule:
        for _, fdr in slot_pairs:
            found_founders.add(fdr)
    unmatched_founders = [f for f in founders if f not in found_founders]
    if not unmatched_founders:
        return
    used_pairs = set()
    for slot_pairs in schedule:
        used_pairs.update(slot_pairs)
    from collections import defaultdict
    fdr_to_inv = defaultdict(list)
    for inv, fdr in valid_pairs:
        fdr_to_inv[fdr].append(inv)
    for unmatched_f in unmatched_founders:
        possible_investors = fdr_to_inv[unmatched_f]
        for slot_idx, slot_pairs in enumerate(schedule):
            if len(slot_pairs) >= 20:
                continue
            slot_investors = {p[0] for p in slot_pairs}
            for inv in possible_investors:
                if (inv, unmatched_f) in used_pairs:
                    continue
                if inv in slot_investors:
                    continue
                schedule[slot_idx].append((inv, unmatched_f))
                used_pairs.add((inv, unmatched_f))
                break
            if any(x[1] == unmatched_f for x in schedule[slot_idx]):
                break

def get_time_slot_labels():
    return [
        "8:00 AM – 8:20 AM",
        "8:25 AM – 8:45 AM",
        "8:50 AM – 9:10 AM",
        "9:15 AM – 9:35 AM",
        "9:40 AM – 10:00 AM",
        "10:05 AM – 10:25 AM",
        "10:30 AM – 10:50 AM",
        "10:55 AM – 11:15 AM",
        "11:20 AM – 11:40 AM",
        "11:45 AM – 12:05 PM"
    ]

def print_schedule(schedule):
    time_slots = get_time_slot_labels()
    print()
    print("Final Event Schedule")
    print("====================")
    header = ["Pairing #"] + time_slots
    print(",".join(header))
    max_pairs = 20
    for pairing_index in range(max_pairs):
        row = [f"Pairing {pairing_index+1}"]
        for slot_idx in range(len(time_slots)):
            if pairing_index < len(schedule[slot_idx]):
                inv, fdr = schedule[slot_idx][pairing_index]
                row.append(f"{inv} / {fdr}")
            else:
                row.append("")
        print(",".join(row))

def main():
    investors_file = "data/investors.csv"
    founders_file = "data/founders.csv"
    investors_df, founders_df = load_data(investors_file, founders_file)
    valid_pairs = find_valid_pairs(investors_df, founders_df)
    print(f"Total valid Investor-Founder pairings found: {len(valid_pairs)}")
    schedule = schedule_slots(valid_pairs, investors_df, founders_df)
    ensure_founders_coverage(schedule, valid_pairs, founders_df)
    print_schedule(schedule)

if __name__ == "__main__":
    main()
