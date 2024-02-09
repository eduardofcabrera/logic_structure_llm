from random import randint, choice
from typing import List, Any, Tuple, Dict


class SampleGenerator:
    def __init__(self, sample_json_format: Dict):
        self.sample_json_format = sample_json_format
        self.variables = [
            variable for variable in sample_json_format["variables"].keys()
        ]

    def _generate_int_variable(
        self, lower_bound: int, upper_bound: int, delimiter: int, **kwargs
    ) -> Tuple[int, int]:
        variable = delimiter
        while variable == delimiter:
            variable = randint(lower_bound, upper_bound)
        if variable > delimiter:
            return variable, 1
        return variable, 0

    def _generate_binary_option_variable(
        self, options: Tuple[Any, Any], **kwargs
    ) -> Tuple[Any, int]:
        _id = randint(0, 1)
        return options[_id], _id

    def _generate_binary_group_variable(
        self, groups: Tuple[List[Any], List[Any]], **kwargs
    ) -> int:
        group_id = randint(0, 1)
        group = groups[group_id]
        return choice(group), group_id

    def _get_category_from_int_variable(
        self, delimiter: int, variable_value: int, **kwargs
    ) -> int:
        if variable_value > delimiter:
            return 1
        return 0

    def _get_category_from_binary_option_variable(
        self,
        options: Tuple[Any, Any],
        variable_value: Any,
        **kwargs,
    ) -> int:
        return options.index(variable_value)

    def _get_category_from_binary_group_variable(
        self, groups: Tuple[List[Any], List[Any]], variable_value: Any, **kwargs
    ) -> int:
        if variable_value in groups[0]:
            return 0
        return 1

    def _generate_variable(self, variable_config: Dict) -> Tuple[Any, int]:
        if variable_config["type"] == "int_variable":
            return self._generate_int_variable(**variable_config)
        elif variable_config["type"] == "binary_option_variable":
            return self._generate_binary_option_variable(**variable_config)
        elif variable_config["type"] == "binary_group_variable":
            return self._generate_binary_group_variable(**variable_config)
        return 0, 0

    def generate_sample(self):
        sample_json_format = self.sample_json_format
        variables = self.variables

        sample = {}
        for variable in variables:
            sample[variable] = self._generate_variable(
                sample_json_format["variables"][variable]
            )

        return sample

    def _get_category_from_variable(
        self, variable_config: Dict, variable_value: Any
    ) -> int:
        if variable_config["type"] == "int_variable":
            return self._get_category_from_int_variable(
                variable_value=variable_value, **variable_config
            )
        elif variable_config["type"] == "binary_option_variable":
            return self._get_category_from_binary_option_variable(
                variable_value=variable_value, **variable_config
            )
        elif variable_config["type"] == "binary_group_variable":
            return self._get_category_from_binary_group_variable(
                variable_value=variable_value, **variable_config
            )
        return 0

    def get_true_choice_from_sampe(self, sample: Dict) -> Tuple:

        choice = tuple(
            [
                self._get_category_from_variable(
                    variable_config=self.sample_json_format["variables"][variable_name],
                    variable_value=variable_value,
                )
                for variable_name, variable_value in sample.items()
            ]
        )
        return choice
