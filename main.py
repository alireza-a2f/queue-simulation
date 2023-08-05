from inventory import Inventory
import helpers

if __name__ == '__main__':
    S = 175
    s = 25
    I = 40
    weeks = 2
    inv = Inventory(S, s, I, 7 * weeks)

    while inv.get_time() <= weeks * 7:
        inv.next_demand(helpers.randomDemandTime(), helpers.randomDemandAmount())
        inv.trigger_next_event()

    print("Average annual inventory cost:", inv.average_annual_inventory_cost())
    print("Average annual shortage cost:", inv.average_annual_shortage_cost())
    print("Average annual order cost:", inv.average_annual_order_cost())
    print("Average annual total cost:", inv.average_total_cost())
    print("Percentage of weeks with shortage:", inv.weeks_with_shortage_count() / weeks * 100)
