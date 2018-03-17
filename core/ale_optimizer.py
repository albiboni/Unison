"""
Created by Alejandro Daniel Noel
"""
from core.plant_graph.machine import Machine


def maximize_output(output_machine: Machine):
    increment = 1.0
    output_rate = 1.0

    while increment > 0.002:
        successful = output_machine.set_supplier_rates(output_rate)

        if successful:
            increment *= 2
            output_rate += increment
        else:
            output_rate -= increment
            increment *= 0.5
            output_rate += increment

    return output_rate
