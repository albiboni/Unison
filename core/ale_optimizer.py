"""
Created by Alejandro Daniel Noel
"""
from core.plant_graph.machine import Machine
from core.plant_graph.time_schedule import create_time_schedule


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


def separate_number(name):
    parts = name.rsplit(' ', maxsplit=1)
    if len(parts) == 1:
        return name, 0
    elif parts[1].isdigit():
        return parts[0], int(parts[1])
    else:
        return name, 0


def optimize_topology(output_machine: Machine, target_output_rate):
    while maximize_output(output_machine) < target_output_rate:
        schedule = create_time_schedule(output_machine)
        for machine in schedule:
            name, number = separate_number(machine[0])
            if machine[3] > 99.0:
                next_num = max([separate_number(m[0])[1] for m in schedule if separate_number(m[0])[0] == name]) + 1
                the_machine = output_machine.search_machine_by_name(machine[0])
                new_machine = Machine(name=name + " " + str(next_num),
                                      batch_size=the_machine.batch_size,
                                      batch_time=the_machine.batch_time,
                                      min_batch_time=the_machine.min_batch_time,
                                      max_batch_time=the_machine.max_batch_time,
                                      output_product=the_machine.output_product,
                                      suppliers=the_machine.suppliers,
                                      delays=the_machine.delays)
                for downstream_machine in the_machine.next_machines:
                    downstream_machine.add_supplier(new_machine, downstream_machine.delay_for_supplier(the_machine))
                break
    return output_machine.set_supplier_rates(target_output_rate)

