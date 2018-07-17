import pickle
from networkx import draw, Graph, draw_networkx, MultiGraph
#from networkx.drawing.nx_pydot import graphviz_layout
from pylab import show
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Network(object):

    def __init__(self, name, network_dict={}):
        """ initializes a network object """
        self.name = name
        self.__network_dict = network_dict
        connections = {}
        for member in self.__network_dict:
            for partner in self.__network_dict[member]:
                    connections[partner] = [member]
        for key in connections:
            if key in self.__network_dict:
                self.__network_dict[key] += connections[key]
            else:
                self.__network_dict[key] = connections[key]
        

    def members(self):
        """ returns the members of a network """
        return list(self.__network_dict.keys())


    def connections(self):
        """ returns the sonnections of a network """
        return self.__generate_connections()


    def add_member(self, member):
        """ If the memeber "member" is not in 
            self.__network_dict, a key "member" with an empty
            list as a value is added to the dictionary. 
            Otherwise nothing has to be done. 
        """
        if member not in self.__network_dict:
            self.__network_dict[member] = []


    def add_connection(self, connection):
        """ assumes that connection is of type set, tuple or list; 
            between two members can be multiple connections! 
        """
        connection = set(connection)
        (member1, member2) = tuple(connection)
        if member1 in self.__network_dict:
            self.__network_dict[member1].append(member2)
        else:
            self.__network_dict[member1] = [member2]
        if member2 in self.__network_dict:
            self.__network_dict[member2].append(member1)
        else:
            self.__network_dict[member2] = [member1]
     
    def delete_connection(self,connection):
        """ assumes that connection is of type set, tuple or list;  
        """ 
        connection = set(connection)
        (member1, member2) = tuple(connection)
        if member1 in self.__network_dict:
            if member2 in self.__network_dict[member1]:
                self.__network_dict[member1].remove(member2)
        else:
            print('Verbindung existiert nicht')
        if member2 in self.__network_dict:
            if member1 in self.__network_dict[member2]:
                self.__network_dict[member2].remove(member1)
        else:
            print('Verbindung existiert nicht')

    def delete_member(self, member):
        if member in self.__network_dict:
            partner = self.__network_dict[member]
            del self.__network_dict[member]
        for i in partner:
            if member in self.__network_dict[i]:
                self.__network_dict[i].remove(member)

    def rename_member(self, member, new_member):
        if new_member in self.__network_dict:
            print('Person existiert bereits!')
        if member in self.__network_dict:
            partner = self.__network_dict[member]
            del self.__network_dict[member]
            self.__network_dict[new_member] = partner
        for i in partner:
            if member in self.__network_dict[i]:
                self.__network_dict[i].remove(member)
                self.__network_dict[i].append(new_member)
                
                
    def __generate_connections(self):
        """ A static method generating the connections of the 
            network "network". Connections are represented as sets 
            with one (a loop back to the member) or two 
            members 
        """
        connections = []
        for member in self.__network_dict:
            for partner in self.__network_dict[member]:
                if {partner, member} not in connections:
                    connections.append({member, partner})
        return connections


    def __str__(self):
        res = "members: "
        for k in self.__network_dict:
            res += str(k) + " "
        res += "\nconnections: "
        for connection in self.__generate_connections():
            res += str(connection) + " "
        return res


    def find_path(self, start_member, end_member, path=[]):
        """ find a path from start_member to end_member 
            in network """
        network = self.__network_dict
        path = path + [start_member]
        if start_member == end_member:
            return path
        if start_member not in network:
            return None
        for member in network[start_member]:
            if member not in path:
                extended_path = self.find_path(member, 
                                               end_member, 
                                               path)
                if extended_path: 
                    return extended_path
        return None


    def find_all_paths(self, start_member, end_member, path=[]):
        """ find all paths from start_member to 
            end_member in network """
        network = self.__network_dict 
        path = path + [start_member]
        if start_member == end_member:
            return [path]
        if start_member not in network:
            return []
        paths = []
        for member in network[start_member]:
            if member not in path:
                extended_paths = self.find_all_paths(member, 
                                                     end_member, 
                                                     path)
                for p in extended_paths: 
                    paths.append(p)
        return paths


    def is_connected(self, 
                     members_encountered = set(), 
                     start_member=None):
        """ determines if the network is connected """
        gdict = self.__network_dict        
        members = gdict.keys() 
        if not start_member:
            # chosse a member from network as a starting point
            start_member = members[0]
        members_encountered.add(start_member)
        if len(members_encountered) != len(members):
            for member in gdict[start_member]:
                if member not in members_encountered:
                    if self.is_connected(members_encountered, member):
                        return True
        else:
            return True
        return False


    def member_degree(self, member):
        """ The degree of a member is the number of connections connecting
            it, i.e. the number of adjacent members. Loops are counted 
            double, i.e. every occurence of member in the list 
            of adjacent members. """ 
        adj_members =  self.__network_dict[member]
        degree = len(adj_members) + adj_members.count(member)
        return degree


    def degree_sequence(self):
        """ calculates the degree sequence """
        seq = []
        for member in self.__network_dict:
            seq.append(self.member_degree(member))
        seq.sort(reverse=True)
        return tuple(seq)


    @staticmethod
    def is_degree_sequence(sequence):
        """ Method returns True, if the sequence "sequence" is a 
            degree sequence, i.e. a non-increasing sequence. 
            Otherwise False is returned.
        """
        # check if the sequence sequence is non-increasing:
        return all( x>=y for x, y in zip(sequence, sequence[1:]))


    def delta(self):
        """ the minimum degree of the members """
        min = 100000000
        for member in self.__network_dict:
            member_degree = self.member_degree(member)
            if member_degree < min:
                min = member_degree
        return min

        
    def Delta(self):
        """ the maximum degree of the members """
        max = 0
        for member in self.__network_dict:
            member_degree = self.member_degree(member)
            if member_degree > max:
                max = member_degree
        return max


    def density(self):
        """ method to calculate the density of a network """
        g = self.__network_dict
        V = len(g.keys())
        E = len(self.connections())
        return 2.0 * E / (V *(V - 1))


    def diameter(self):
        """ calculates the diameter of the network """
        
        v = self.members() 
        pairs = [ (v[i],v[j]) for i in range(len(v)) for j in range(i+1, len(v)-1)]
        smallest_paths = []
        for (s,e) in pairs:
            paths = self.find_all_paths(s,e)
            smallest = sorted(paths, key=len)[0]
            smallest_paths.append(smallest)

        smallest_paths.sort(key=len)

        # longest path is at the end of list, 
        # i.e. diameter corresponds to the length of this path
        diameter = len(smallest_paths[-1])
        return diameter


    @staticmethod
    def erdoes_gallai(dsequence):
        """ Checks if the condition of the Erdoes-Gallai inequality 
            is fullfilled 
        """
        if sum(dsequence) % 2:
            # sum of sequence is odd
            return False
        if Network.is_degree_sequence(dsequence):
            for k in range(1,len(dsequence) + 1):
                left = sum(dsequence[:k])
                right =  k * (k-1) + sum([min(x,k) for x in dsequence[k:]])
                if left > right:
                    return False
        else:
            # sequence is increasing
            return False
        return True


    def save(self, fname):
        with open(fname, 'wb') as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)


    def draw_network(self):
        ''' draws the network using networks and matplotlib'''
        fig = plt.figure(figsize=(12,12))
        ax = fig.add_subplot(111)
        #ax.patch.set_facecolor('black')
        g = Graph()
        g.add_edges_from(self.__generate_connections())
        #draw_networkx(g, pos=graphviz_layout(g), with_labels=True, node_size=1000, node_color='black', font_size=16, linewidths=0, font_family='monospace', edge_color='white', font_color='white')        
        draw_networkx(g, with_labels=True, node_size=1000, node_color='black', font_size=16, linewidths=0, font_family='monospace', edge_color='white', font_color='white')        
        ax.patch.set_facecolor('black')
        #plt.tight_layout()
        plt.savefig("chart.png", format='PNG')
        show()

        
def load_network(fname):
    '''loads network saved in given filename'''
    with open(fname, 'rb') as f:
        return pickle.load(f)
        
def load_from_txt(fname, name):
    network = Network(name)
    with open(fname, 'rb') as f:
        for line in f:
            line = str(line)
            line = line.strip('b')
            line = line.strip("'")
            line = line.strip('\\n')
            line = line.strip('\\r')
            line = line.strip('\n')
            line = line.strip('\r')
            member = line.split(':')[0]
            network.add_member(member)
            for partner in str(line).split(':')[1].split(','):
                network.add_connection([member,partner])
                
    print(network)
    return network
        

def create_HGW_network():
    '''creates test network'''
    g = { "Jule" : ["Tine"],
          "Malle" : ["Sarah", "Lisa", "Trace", "Hanna", "Tine"],
          "Caro" : ["Denise", "Maria", "Julia", "Katja"],
          "Denise" : ["Caro", "Lenny"],
          "Sarah": ["Malle", "Trace"],
          "Lisa" : ["Denise", "Malle", "Tine", "Hanna2", "Henny", "Julia2"]
        }
    network = Network('HGW', g)
    #print("Members of network:")
    #print(network.members())

    #print("Connections of network:")
    #print(network.connections())
    return network
