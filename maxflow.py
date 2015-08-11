from __future__ import division

import csv
import math
import getopt
import sys

class FordFulkerson:
    def __init__(self):
        self.adjacency_list = {}
        self.back_adjacency_list = {}
        self.flow = {}
        self.capacity = {}

    def add_vertex(self, vertex):
        if vertex in self.adjacency_list:
            return

        self.adjacency_list[vertex] = set()
        self.back_adjacency_list[vertex] = set()

    def get_adj_vertexes(self, v):
        return self.adjacency_list[v]

    def get_back_adj_vertexes(self, v):
        return self.back_adjacency_list[v]

    def add_edge(self, u, v, w=0):
        uv = u + v
        if uv in self.capacity:
            return
        vu = v + u
        self.capacity[uv] = w
        self.capacity[vu] = 0
        self.adjacency_list[u].add(v)
        self.back_adjacency_list[v].add(u)
        self.flow[uv] = 0
        self.flow[vu] = 0

    def bfs(self, source, sink):
        queue = [source]
        paths = {source: []}
        while queue:
            u = queue.pop(0)
            for v in self.get_adj_vertexes(u):
                uv = u + v
                residual = self.capacity[uv] - self.flow[uv]
                if residual > 0 and v not in paths:
                    paths[v] = paths[u] + [(u, v, residual)]
                    if v == sink:
                        return paths[v]
                    queue.append(v)
        return None

    def max_flow(self, source, sink):
        path = self.bfs(source, sink)
        while path is not None:
            mflow = min(res for u, v, res in path)
            for u, v, res in path:
                uv = u + v
                vu = v + u
                self.flow[uv] += mflow
                self.flow[vu] -= mflow
            path = self.bfs(source, sink)
        return sum(self.flow[source+v] for v in self.get_adj_vertexes(source))

    # Update the constraints between Source (S) and all the clients
    def update_SC_constraints(self, percent):
        adj_vert = self.get_adj_vertexes('S')

        total_sum = 0.0

        for v in adj_vert:
            constraint = math.ceil(len(self.adjacency_list[v]) * (percent/100))
            self.capacity['S'+v] = constraint
            total_sum = total_sum + constraint

        return total_sum

    # Update the contraints between the products and the sink (T)
    def update_PT_constraints(self, percent):
        adj_vert = self.get_back_adj_vertexes('T')

        total_sum = 0.0

        for v in adj_vert:
            constraint = math.floor(len(self.back_adjacency_list[v]) * (percent/100))
            self.capacity[v+'T'] = constraint
            total_sum = total_sum + constraint

        return total_sum

    def is_feasible_circulation(self, total_sum, max_flow_result):
        return max_flow_result == total_sum

    def load_data(self, filename):
        self.add_vertex('S')
        self.add_vertex('T')

        with open(filename, 'r') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',')
            for row in csvreader:
                customer = 'C'+row[0]
                product = 'P'+row[1]
                self.add_vertex(customer)
                self.add_vertex(product)
                self.add_edge('S', customer, 0)
                self.add_edge(customer, product, 1)
                self.add_edge(product, 'T', 9999999)


def usage():
    print 'python maxflow.py -d [dataset] -c [customer%] '\
          '-p [product% range(begin-end)] -s [step]'


def main(argv):
    try:
        opts, args = getopt.getopt(argv,
                                   'd:c:p:s:h',
                                   ['dataset=', 'customers=',
                                    'products=', 'step=', 'help'])
    except getopt.GetoptError:
        usage()
        sys.exit(1)

    dataset_path = None
    customers_percent = None

    products_percent_start = None
    products_percent_end = None
    products_percent_step = None

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-d", "--dataset"):
            dataset_path = arg
        elif opt in ("-c", "--customers"):
            try:
                customers_percent = int(arg)
            except ValueError:
                usage()
                sys.exit(2)
        elif opt in ("-p", "--products"):
            try:
                prod_percents = arg.split("-")
                products_percent_start = int(prod_percents[0])
                products_percent_end = int(prod_percents[1])
                if (products_percent_end <= products_percent_start):
                    raise ValueError('End range should be greater than the start')
            except ValueError:
                usage()
                sys.exit(3)
        elif opt in ("-s", "--step"):
            try:
                products_percent_step = int(arg)
            except ValueError:
                usage()
                sys.exit(4)

    if dataset_path is None:
        usage()
        sys.exit(5)

    ek = FordFulkerson()

    ek.load_data(dataset_path)

    total_ci_sum = ek.update_SC_constraints(customers_percent)

    start = products_percent_step
    end = products_percent_end + products_percent_step
    step = products_percent_step

    print 'Please wait... It can take several minutes :)'
    print ''

    for cur_prod_percent in xrange(start, end, step):
        total_pj_sum = ek.update_PT_constraints(cur_prod_percent)

        print '---------------------------------------------------------------'
        print 'Running feasible circulation for values:'
        print 'C\'I: 40%% | P\'J: %d%%' % cur_prod_percent
        print ''

        max_flow_result = ek.max_flow('S', 'T')

        print 'MAX FLOW: %d' % max_flow_result
        print 'TOTAL CIs SUM: %d' % total_ci_sum
        print 'TOTAL PJs SUM: %d' % total_pj_sum
        print 'Is it feasible? %r' % ek.is_feasible_circulation(total_pj_sum,
                                                                max_flow_result)
        print '---------------------------------------------------------------'
        print ''

        sys.stdout.flush()

if __name__ == "__main__":
    main(sys.argv[1:])
