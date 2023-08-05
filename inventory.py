import helpers
import csv


class Inventory:
    def __init__(self, S, s, I, days_constraint):
        self.S = S
        self.s = s
        self.I = I
        self.z = 0
        self.time = 0
        self.previous_time = 0
        self.previous_I = 0
        self.week = 1
        self.next_delivery_time = None
        self.next_demand_time = None
        self.next_demand_amount = None
        self.output_file = open('output.csv', 'w', newline='')
        self.output = csv.writer(self.output_file)
        self.output.writerow(['time', 'I'])
        self.Ap = 0
        self.An = 0
        self.order_cost = 0
        self.days_constraint = days_constraint
        self.weeks_with_shortage = []

    def get_time(self):
        return self.time

    def weeks_with_shortage_count(self):
        return len(self.weeks_with_shortage)

    def demand(self, d):
        self.previous_I = self.I
        self.I -= d
        if self.I < 0 and self.week not in self.weeks_with_shortage and self.time < self.days_constraint:
            self.weeks_with_shortage.append(self.week)

    def request(self):
        self.next_delivery_time = self.time + helpers.randomLeadTime()
        self.z = self.S - self.I

    def delivery(self, z):
        self.previous_I = self.I
        self.I += z
        self.order_cost += 15 + 2 * z

    def next_demand(self, time, amount):
        self.next_demand_time = self.time + time
        self.next_demand_amount = amount

    def trigger_next_event(self):
        self.output.writerow([self.time, self.I])
        if self.next_delivery_time and self.next_delivery_time < self.next_demand_time:
            self.previous_time = self.time
            self.time = self.next_delivery_time
            self.delivery(self.z)
            self.next_delivery_time = None
            self.z = None
            delta_t = min(self.days_constraint, self.time) - self.previous_time
            if self.previous_I < 0:
                self.An -= self.previous_I * delta_t
            else:
                self.Ap += self.previous_I * delta_t
            self.trigger_next_event()
        else:
            self.previous_time = self.time
            if self.I < self.s and self.time <= self.week * 7 <= self.next_demand_time:
                # self.previous_time = self.time
                self.time = self.week * 7
                self.request()
            self.week = int(self.time / 7) + 1
            self.time = self.next_demand_time
            self.demand(self.next_demand_amount)
            delta_t = min(self.days_constraint, self.time) - self.previous_time
            if self.previous_I < 0:
                self.An -= self.previous_I * delta_t
            else:
                self.Ap += self.previous_I * delta_t

    def average_annual_inventory_cost(self):
        return self.Ap * 52 / 70 / self.week

    def average_annual_shortage_cost(self):
        return self.An * 520 / 7 / self.week

    def average_annual_order_cost(self):
        return self.order_cost * 52 / self.week

    def average_total_cost(self):
        return (self.average_annual_inventory_cost() +
                self.average_annual_shortage_cost() +
                self.average_annual_order_cost())
