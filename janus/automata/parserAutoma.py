import pydot
from janus.automata.automa import Automa

def get_file(path):
    try:
        with open(path, 'r') as file:
            lines = file.readlines()
            file.close()
        return lines
    except IOError:
        print('[ERROR]: Not able to open the file from the path {}'.format(path))

def get_graph_from_dot(path):
    try:
        dot_graph = pydot.graph_from_dot_file(path)
        return dot_graph[0]
    except IOError:
        print('[ERROR]: Not able to import the dot file')

def get_final_label(label):

    s1 = label.replace(" ", "")
    s2 = s1.replace('"','')

    if s2 == '':
        return ['X']
    elif len(s2) < 2:
        return [s2]
        #return _split_dont_care(list(s2))
    else:
        s3 = s2.replace(",","")
        s4 = s3.split('\\n') # now s4 should be a list like ['01', '0X', '00']

        leng_elem = len(s4[0])#length of elements in s4
        temp = ''
        inter_label = []
        for i in range(leng_elem):
            for elem in s4:
                temp += elem[i]
            inter_label.append(temp)
            temp = ''

        return inter_label

def parse_dot(path, symbols):

    graph = get_graph_from_dot(path)

    #taking integer nodes
    nodes = [] ## list of integer nodes as string (in the example: 3,1,2)
    for node in graph.get_nodes():
        if node.get_name().isdigit():
            nodes.append(node.get_name())
        else: continue

    # assign set of states
    states = set(nodes)

    # getting the initial state as a string
    initial_state = sorted(nodes, key=int)[0]

    # let's get the accepting states
    lines = get_file(path)
    accepting_states = set() #set containing all accepting states of the automaton
    for line in lines[7:]:
        if line.strip() != 'node [shape = circle];':
            temp = line.replace(";\n", "")
            accepting_states.add(temp.strip())
        else:
            break

    # let's get sources nodes
    sources = []
    for elem in graph.get_edges():
        if elem.get_source().isdigit():
            sources.append(elem.get_source())
        else: continue

    # let's get transitions
    i = 0
    transitions = dict()
    for source in sources:
        label = graph.get_edges()[i].get_label()
        final_label = get_final_label(label)
        destination = graph.get_edges()[i].get_destination()
        #print('[LOOP #'+str(i)+'] source: '+str(source)+', destination: '+str(destination)+', label: '+str(final_label))
        i += 1
        for lab in final_label:
            if source in transitions:
                transitions[source][lab] = destination
            else:
                transitions[source] = dict({lab: destination})

    #istantiation of automaton
    automaton = Automa(
        symbols=symbols,
        alphabet={'0', '1', 'X'},
        states=states,
        initial_state=initial_state,
        accepting_states=accepting_states,
        transitions=transitions
    )
    return automaton