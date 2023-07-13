class Permutations():
    @staticmethod
    def new_dict_without_key(input_dict, key):
        if isinstance(input_dict, dict):
            return {k: Permutations.new_dict_without_key(v, key) for k, v in input_dict.items() if k != key}
        elif isinstance(input_dict, list):
            return [Permutations.new_dict_without_key(element, key) for element in input_dict]
        else:
            return input_dict

    @staticmethod
    def new_dict_with_null_key(input_dict, key):
        if isinstance(input_dict, dict):
            return {k: Permutations.new_dict_with_null_key(v, key) if k != key else None for k, v in input_dict.items()}
        elif isinstance(input_dict, list):
            return [Permutations.new_dict_with_null_key(element, key) for element in input_dict]
        else:
            return input_dict

    @staticmethod
    def new_dict_with_new_value(input_dict, key, new_value):
        if isinstance(input_dict, dict):
            return {
                k: Permutations.new_dict_with_new_value(v, key, new_value) if k != key
                else new_value for k, v in input_dict.items()
            }
        elif isinstance(input_dict, list):
            return [Permutations.new_dict_with_new_value(element, key, new_value) for element in input_dict]
        else:
            return input_dict
