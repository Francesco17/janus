from ltlf2dfa.Translator import Translator
from ltlf2dfa.DotHandler import DotHandler
from janus.automata.parserAutoma import parse_dot
import os, re

class SeparatedAutomataSet:

    def __init__(self, separated_formulas_set):
        self.separated_formulas_set = separated_formulas_set
        self._automa_set = self.compute_automa()

    @property
    def automa_set(self):
        return self._automa_set

    def build_automaton(self, triple):
        automata_list = []
        for formula in triple:
            symbols = re.findall('(?<![a-z])(?!true|false)[_a-z0-9]+', str(formula))
            trans = Translator(formula)
            trans.formula_parser()
            trans.translate()
            trans.createMonafile(False)  # true for DECLARE assumptions
            trans.invoke_mona() # returns inter-automa.dot
            dot = DotHandler()
            dot.modify_dot()
            dot.output_dot() # returns automa.dot
            automata_list.append(parse_dot("automa.dot", symbols))
            os.remove("automa.mona")
            os.remove("automa.dot")
            symbols = []
        return automata_list

    def compute_automa(self):
        result = []
        for triple in self.separated_formulas_set:
            past, present, future = self.build_automaton(triple)
            result.append( (past, present, future) )
        return result