"""
Created by Alejandro Daniel Noel
"""


def create_time_schedule(output_machine):
    # [process_name, duration, end_time, dependencies, performance_percent]
    rows = output_machine.get_scheduling(end_time=0.0, output_units_required=1.0)

    # Find starting time
    min_time = 0.0
    for row in rows:
        if row[1] < min_time:
            min_time = row[1]

    # Offset all times so that the entire process starts at 0
    for row in rows:
        row[1] += abs(min_time)
        row[2] += abs(min_time)

    return sorted(rows, key=lambda row: row[2])
