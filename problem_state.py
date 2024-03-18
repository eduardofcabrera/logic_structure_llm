import pddl.logic.base as pddl_logic
import pddl.logic.predicates as pddl_predicates
import pddl.logic.terms as pddl_terms
import pddl.action as pddl_action
import pddl.core as pddl_core

import pddl_prover

import random

from typing import *
from itertools import product
from copy import deepcopy


class ProblemState:
    def __init__(self, domain: pddl_core.Domain, problem: pddl_core.Problem, seed: int = 42):
        
        random.seed(seed)
        self.domain = domain
        self.problem = problem

        self.constant_mapping = self._get_constant_mapping()
        self.predicate_mapping = self._get_predicate_mapping()

        self.list_state_predicate_list = [list(problem.init)]
        self.actions_taken = []

    @property
    def actions(self) -> List[pddl_action.Action]:
        return list(self.domain.actions)

    @property
    def current_state_predicate_list(self) -> List[pddl_logic.Formula]:
        return self.list_state_predicate_list[-1]

    @property
    def goal(self) -> pddl_logic.Formula:
        return self.problem.goal

    def add_state_predicate_list(
        self, state_predicate_list: List[pddl_logic.Formula]
    ) -> None:
        self.list_state_predicate_list.append(state_predicate_list)

    def _get_constant_mapping(self) -> Dict[str, pddl_prover.Constant]:
        return {
            c.name: pddl_prover.Constant(c.name) for c in list(self.problem.objects)
        }

    def _get_predicate_mapping(self) -> Dict[str, pddl_prover.Predicate]:
        return {
            p.name: pddl_prover.Predicate(p.name, p.arity)
            for p in list(self.domain.predicates)
        }

    def _get_state_mapping(
        self, state_predicate_list: List[pddl_logic.Formula]
    ) -> Set[Tuple[str, Tuple[str]]]:
        return {
            (p_state.name, tuple(term.name for term in p_state.terms))
            for p_state in state_predicate_list
        }

    def _get_state_dict(
        self, state_predicate_list: List[pddl_logic.Formula]
    ) -> Tuple[Set[pddl_prover.Constant], Set[Tuple[str, Tuple[str]]]]:
        state_mapping = self._get_state_mapping(state_predicate_list)
        constants = {constant for constant in self.constant_mapping.values()}
        return (constants, state_mapping)

    def get_current_state_dict(
        self,
    ) -> Tuple[Set[pddl_prover.Constant], Set[Tuple[str, Tuple[str]]]]:
        return self._get_state_dict(self.current_state_predicate_list)

    def _precondition_to_predicate_called(
        self,
        precondition: pddl_logic.Formula,
        parameters_mapping: Dict[str, str],
    ) -> pddl_prover.Formula:

        if isinstance(precondition, (pddl_logic.And, pddl_logic.Or)):
            operands_list = []
            for operand in precondition.operands:
                if isinstance(operand, pddl_logic.Not):
                    operand = deepcopy(operand.argument)
                    predicate = self.predicate_mapping[operand.name]
                    predicate = pddl_prover.Not(predicate)
                else:
                    predicate = self.predicate_mapping[operand.name]
                predicate_args = (
                    self.constant_mapping[parameters_mapping[term.name]]
                    for term in operand.terms
                )
                operands_list.append(predicate(*(predicate_args)))
            if isinstance(precondition, pddl_logic.And):
                return pddl_prover.And(*operands_list)
            return pddl_prover.Or(*operands_list)

        elif isinstance(precondition, pddl_predicates.Predicate):
            predicate = self.predicate_mapping[precondition.name]
            predicate_args = (
                self.constant_mapping[parameters_mapping[term.name]]
                for term in precondition.terms
            )
            return predicate(*predicate_args)

    def _apply_action_effect(
        self, action: pddl_action.Action, parameters: Tuple[str]
    ) -> List[pddl_logic.Formula]:

        effect = action.effect
        operands = effect.operands

        new_state_predicate_list = self.current_state_predicate_list.copy()

        parameters_mapping = {
            param.name: parameters[i] for i, param in enumerate(action.parameters)
        }

        for operand in operands:
            is_not = False
            if isinstance(operand, pddl_logic.Not):
                is_not = True
                operand = deepcopy(operand.argument)
            terms = operand.terms
            operand_parameters = tuple(
                (pddl_terms.Constant(parameters_mapping[term.name]) for term in terms)
            )
            new_operand = deepcopy(operand)
            new_operand._terms = operand_parameters
            if is_not:
                new_state_predicate_list.remove(new_operand)
            else:
                new_state_predicate_list.append(new_operand)

        return new_state_predicate_list

    def is_action_possible(
        self, action: pddl_action.Action, parameters: Tuple[str]
    ) -> bool:

        parameters_mapping = {
            parameter.name: parameters[i]
            for i, parameter in enumerate(action.parameters)
        }
        precondition = action.precondition
        predicate_called = self._precondition_to_predicate_called(
            precondition, parameters_mapping
        )
        return predicate_called.evaluate(self.get_current_state_dict())

    def goal_reached(self) -> bool:
        goal_precondition = self.goal

        if isinstance(goal_precondition, (pddl_logic.And, pddl_logic.Or)):
            operands = goal_precondition.operands
        if isinstance(goal_precondition, (pddl_predicates.Predicate)):
            operands = [goal_precondition]

        parameters_mapping = {
            term.name: term.name for operand in operands for term in operand.terms
        }

        predicate_called = self._precondition_to_predicate_called(
            goal_precondition, parameters_mapping
        )

        return predicate_called.evaluate(self.get_current_state_dict())

    def get_all_possible_actions(self) -> List[Tuple[pddl_action.Action, Tuple[str]]]:
        actions = self.actions
        possible_actions = []

        for action in actions:
            n_parameters = len(action.parameters)
            parameters_choices = product(
                self.constant_mapping.keys(), repeat=n_parameters
            )
            for parameter_choice in parameters_choices:
                if self.is_action_possible(action, parameter_choice):
                    possible_actions.append((action, parameter_choice))

        return possible_actions
    
    def get_all_impossible_actions(self) -> List[Tuple[pddl_action.Action, Tuple[str]]]:
        actions = self.actions
        impossible_actions = []

        for action in actions:
            n_parameters = len(action.parameters)
            parameters_choices = product(
                self.constant_mapping.keys(), repeat=n_parameters
            )
            for parameter_choice in parameters_choices:
                if not self.is_action_possible(action, parameter_choice):
                    impossible_actions.append((action, parameter_choice))

        return impossible_actions

    def take_action(self, action: pddl_action.Action, parameters: Tuple[str]) -> bool:
        if not self.is_action_possible(action, parameters):
            return False

        new_state_predicate_list = self._apply_action_effect(action, parameters)
        self.add_state_predicate_list(new_state_predicate_list)
        self.actions_taken.append((action, parameters))

        return True
