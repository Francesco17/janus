from janus.io.InputHandler import InputHandler
from janus.formulas.separatedFormula import SeparatedFormula
from janus.formulas.formula import Formula
from janus.automata.sepautset import SeparatedAutomataSet
import argparse, copy

args_parser = argparse.ArgumentParser(description='Janus algorithm computes the interestingness degree of an RCon over'+
                                                  ' a trace taken by an event log L')
args_parser.add_argument('<event-log>', help='Path to the event log -- MANDATORY')
args_parser.add_argument('<activator>', type=str, help='Activator -- MANDATORY')
# args_parser.add_argument('<formula>', type=str, help='Formula to be checked -- MANDATORY')

params = vars(args_parser.parse_args())

input_log = InputHandler(params['<event-log>'])
trace = input_log.event_log
print('[TRACE]: ' + str(trace))
activator = params['<activator>']
print('[ACTIVATOR]: ' + activator)

# formula = params['<formula>']

sepFormula1 = SeparatedFormula(('Yb', 'T', 'T'))
sepFormula2 = SeparatedFormula(('T', 'T', 'Ec'))

constraint = Formula([sepFormula1, sepFormula2]) # set manually the constraint
print('[SEPARATED FORMULAS]: ' + str(constraint))

sepautset = SeparatedAutomataSet(constraint).automa_set

# JANUS ALGORITHM SKETCH
O = []
for event in trace:
    for pastAut in sepautset:
        pastAut[0].make_transition(event)
        # if pastAut[0].symbol == 'b':
        #     print('[PAST AUT ' + str(pastAut[0].symbol) + ' ]: ' + str(pastAut[0].current_state))
    if event == activator:
        #J = set()
        J = {}
        for past, now, future in sepautset:
            if past.is_accepting() and now.accepts(event):
                #print('[PAST ' + str(past.symbol) + ' IN ACCEPTING]: state == ' + str(past.current_state))
                #J.add((future.initial_state, future))
                temp = copy.deepcopy(future)
                J[temp] = future.initial_state
        #print('Janus is: ' + str(J))
        O.append(J)
        #print('O bag is: ' + str(O))
    #print('[OBAG EVENT ' + event + '] ' + str(O))
    for j in O:
        for aut, st in j.items():
            aut.make_transition(event)
            #print('aut {0}, state after transition {1}: {2}'.format(aut.symbol, event, aut.current_state))
            j[aut] = aut.current_state

if O:
    count = 0
    for janus in O:
        for automa, state in janus.items():
            if state in automa.accepting_states:
                count += 1
            else:
                continue
    print('[ACTIVATED]: ' + str(len(O)))
    print('[FULFILLED]: ' + str(count))
    print(count/len(O))
else:
    print(0)