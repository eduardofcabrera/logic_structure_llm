customer_json_format = {
    "variables": {
        "age": {
            "type": "int_variable",
            "lower_bound": 10,
            "upper_bound": 80,
            "delimiter": 45,
        },
        "height": {
            "type": "int_variable",
            "lower_bound": 130,
            "upper_bound": 210,
            "delimiter": 170,
        },
        "weight": {
            "type": "int_variable",
            "lower_bound": 20,
            "upper_bound": 100,
            "delimiter": 60,
        },
        "registration_time": {
            "type": "int_variable",
            "lower_bound": 0,
            "upper_bound": 24,
            "delimiter": 12,
        },
        "sex": {"type": "binary_option_variable", "options": ("male", "female")},
        "city": {
            "type": "binary_group_variable",
            "groups": (
                ["San Francisco", "Los Angeles", "San Diego"],
                ["New York", "Boston", "Washington"],
            ),
        },
    }
}
