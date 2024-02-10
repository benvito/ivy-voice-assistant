import re

from utils.utils import WordNum, Time
from errors.errors import *
from config.config import ADD_EACH, CONCAT, PICK_FIRST_MATCH, PICK_LAST_MATCH, PICK_LAST_IN_FIRST_MATCH, PICK_FIRST_IN_FIRST_MATCH, PICK_FIRST_IN_LAST_MATCH, PICK_LAST_IN_LAST_MATCH, CMD_ARGS, REGEX_ON, PREFIX, ARGS_SEP, POSTFIX

class ArgumentConstructor:
    """
    ARGUMENT CONSTRUCTOR CLASS

    CONCAT ARGUMENTS BY DIFFERENT METHODS
    """
    @staticmethod
    def all_list_to_str(lst : list) -> list:
        r"""
        CONVERT ALL LIST ELEMENTS TO STR
        EXAMPLE:
        >>> lst = [1, 2, 3]
        >>> all_list_to_str(lst)
        ['1', '2', '3']
        """
        return list(map(str, lst))

    @staticmethod
    def unpack_matches(re_arguments : list) -> str:
        r"""
        UNPACK MATCHES FROM RE ARGUMENTS
        EXAMPLE:
        >>> re_arguments = ['монетка', 'монетку', 'монетки']
        result = 'монетка монетку монетки'

        >>> re_arguments = [('2', 'часа'), ('5', 'минут')]
        result = '2 часа 5 минут'
        """
        result = ''
        if ArgumentsProcessor.is_multi_group_match(re_arguments):
            for match in re_arguments:
                for m in match:
                    result += m + ' '
        else:
            for match in re_arguments:
                result += match
        return result

    @staticmethod
    def concat_arguments(cmd_arguments : list, re_arguments : list, prefix : str, postfix : str) -> str:
        r"""
        CONCAT ARGUMENTS FROM RE ARGUMENTS TO CMD ARGUMENTS
        EXAMPLE:
        >>> cmd_arguments = ['1', '2']
        >>> re_arguments = [('3', '4'), ('5', '6')]
        cmd_arguments = ['1', '2', '3', '4', '5', '6']

        >>> cmd_arguments = ['1', '2']
        >>> re_arguments = ['3', '4']
        cmd_arguments = ['1', '2', '3', '4']
        """
        cmd_arguments.append(prefix + ArgumentConstructor.unpack_matches(re_arguments) + postfix)
        return cmd_arguments

    @staticmethod
    def re_arg_to_list(re_arguments : list) -> list:
        r"""
        CONVERT RE ARGUMENTS TO LIST
        EXAMPLE:
        >>> re_arguments = [('3', '4'), ('5', '6')]
        result = ['3', '4', '5', '6']

        >>> re_arguments = ['3', '4']
        result = ['3', '4']
        """
        result = []
        if ArgumentsProcessor.is_multi_group_match(re_arguments):
            for match in re_arguments:
                for m in match:
                    result.append(m)
        else:
            for match in re_arguments:
                result.append(match)
        return result

    @staticmethod
    def add_each_re_arg(cmd_arguments : list, re_arguments : list, prefix : str, postfix : str) -> list:
        r"""
        ADD EACH RE ARGUMENT TO CMD ARGUMENTS
        EXAMPLE:
        >>> cmd_arguments = ['1', '2']
        >>> re_arguments = [('3', '4'), ('5', '6')]
        cmd_arguments = ['1', '2', '3', '4', '5', '6']

        >>> cmd_arguments = ['1', '2']
        >>> re_arguments = ['3', '4']
        cmd_arguments = ['1', '2', '3', '4']
        """
        if ArgumentsProcessor.is_multi_group_match(re_arguments):
            re_arguments = ArgumentConstructor.re_arg_to_list(re_arguments)
        for i in range(len(re_arguments)):
            cmd_arguments.append(prefix + re_arguments[i] + postfix)
        
        return cmd_arguments

    @staticmethod
    def format_each_match_concat(re_arguments : list) -> list:
        r"""
        FORMAT EACH MATCH FROM RE ARGUMENTS AND CONCAT THEY
        EXAMPLE:
        >>> re_arguments = [('3', '4'), ('5', '6')]
        result = ['34', '56']

        >>> re_arguments = ['3', '4']
        result = ['3', '4']
        """
        new_re_arg = []
        if ArgumentsProcessor.is_multi_group_match(re_arguments):
            for i in range(len(re_arguments)):
                arg = ''
                for j in range(len(re_arguments[i])):
                    arg += re_arguments[i][j]
                new_re_arg.append(arg)
        else:
            new_re_arg = re_arguments
        
        return new_re_arg

    @staticmethod
    def add_each_match(cmd_arguments : list, re_arguments : list, prefix : str, postfix : str) -> list:
        r"""
        ADD EACH MATCH FROM RE ARGUMENTS TO CMD ARGUMENTS
        EXAMPLE:
        >>> cmd_arguments = ['1', '2']
        >>> re_arguments = [('3', '4'), ('5', '6')]
        cmd_arguments = ['1', '2', '34', '56']

        >>> cmd_arguments = ['1', '2']
        >>> re_arguments = ['3', '4']
        cmd_arguments = ['1', '2', '3', '4']
        """
        new_re_arg = ArgumentConstructor.format_each_match_concat(re_arguments)
        
        for i in range(len(new_re_arg)):
            cmd_arguments.append(prefix + new_re_arg[i] + postfix)

        return cmd_arguments

    @staticmethod
    def pick_first_match_arg(cmd_arguments : list, re_arguments : list, prefix : str, postfix : str) -> list:
        r"""
        PICK FIRST MATCH FROM RE ARGUMENTS
        EXAMPLE:
        >>> cmd_arguments = ['1', '2']
        >>> re_arguments = [('3', '4'), ('5', '6')]
        cmd_arguments = ['1', '2', '34']

        >>> cmd_arguments = ['1', '2']
        >>> re_arguments = ['3', '4']

        cmd_arguments = ['1', '2', '3']
        """
        re_arguments = ArgumentConstructor.format_each_match_concat(re_arguments)
        cmd_arguments.append(prefix + re_arguments[0] + postfix)
        return cmd_arguments
    
    @staticmethod
    def pick_last_match_arg(cmd_arguments : list, re_arguments : list, prefix : str, postfix : str) -> list:
        r"""
        PICK FIRST MATCH FROM RE ARGUMENTS
        EXAMPLE:
        >>> cmd_arguments = ['1', '2']
        >>> re_arguments = [('3', '4'), ('5', '6')]
        cmd_arguments = ['1', '2', '56']

        >>> cmd_arguments = ['1', '2']
        >>> re_arguments = ['3', '4']

        cmd_arguments = ['1', '2', '4']
        """
        re_arguments = ArgumentConstructor.format_each_match_concat(re_arguments)
        cmd_arguments.append(prefix + re_arguments[-1] + postfix)
        return cmd_arguments
    
    @staticmethod
    def pick_last_in_first_match_arg(cmd_arguments : list, re_arguments : list, prefix : str, postfix : str) -> list:
        r"""
        PICK FIRST MATCH FROM RE ARGUMENTS
        EXAMPLE:
        >>> cmd_arguments = ['1', '2']
        >>> re_arguments = [('3', '4'), ('5', '6')]
        cmd_arguments = ['1', '2', '4']

        >>> cmd_arguments = ['1', '2']
        >>> re_arguments = ['3', '4']

        cmd_arguments = ['1', '2', '4']
        """
        print(re_arguments)
        if ArgumentsProcessor.is_multi_group_match(re_arguments):
            cmd_arguments.append(prefix + re_arguments[0][-1] + postfix)
        else:
            cmd_arguments.append(prefix + re_arguments[-1] + postfix)
        return cmd_arguments
    
    @staticmethod
    def pick_first_in_first_match_arg(cmd_arguments : list, re_arguments : list, prefix : str, postfix : str) -> list:
        r"""
        PICK FIRST IN FIRST MATCH FROM RE ARGUMENTS
        EXAMPLE:
        >>> cmd_arguments = ['1', '2']
        >>> re_arguments = [('3', '4'), ('5', '6')]
        cmd_arguments = ['1', '2', '3']

        >>> cmd_arguments = ['1', '2']
        >>> re_arguments = ['3', '4']

        cmd_arguments = ['1', '2', '3']
        """
        print(re_arguments)
        if ArgumentsProcessor.is_multi_group_match(re_arguments):
            cmd_arguments.append(prefix + re_arguments[0][0] + postfix)
        else:
            cmd_arguments.append(prefix + re_arguments[0] + postfix)
        return cmd_arguments
    
    @staticmethod
    def pick_last_in_last_match_arg(cmd_arguments : list, re_arguments : list, prefix : str, postfix : str) -> list:
        r"""
        PICK LAST IN LAST MATCH FROM RE ARGUMENTS
        EXAMPLE:
        >>> cmd_arguments = ['1', '2']
        >>> re_arguments = [('3', '4'), ('5', '6')]
        cmd_arguments = ['1', '2', '5']

        >>> cmd_arguments = ['1', '2']
        >>> re_arguments = ['3', '4']

        cmd_arguments = ['1', '2', '3']
        """
        print(re_arguments)
        if ArgumentsProcessor.is_multi_group_match(re_arguments):
            cmd_arguments.append(prefix + re_arguments[-1][-1] + postfix)
        else:
            cmd_arguments.append(prefix + re_arguments[-1] + postfix)
        return cmd_arguments

    @staticmethod
    def pick_first_in_last_match_arg(cmd_arguments : list, re_arguments : list, prefix : str, postfix : str) -> list:
        r"""
        PICK FIRST IN LAST MATCH FROM RE ARGUMENTS
        EXAMPLE:
        >>> cmd_arguments = ['1', '2']
        >>> re_arguments = [('3', '4'), ('5', '6')]
        cmd_arguments = ['1', '2', '5']

        >>> cmd_arguments = ['1', '2']
        >>> re_arguments = ['3', '4']

        cmd_arguments = ['1', '2', '3']
        """
        print(re_arguments)
        if ArgumentsProcessor.is_multi_group_match(re_arguments):
            cmd_arguments.append(prefix + re_arguments[-1][0] + postfix)
        else:
            cmd_arguments.append(prefix + re_arguments[0] + postfix)
        return cmd_arguments

class ArgumentsProcessor:
    """
    ARGUMENT PROCESS CLASS

    ALL ABOUT TAKING ARGS FROM VOICE INPUT
    """
    @staticmethod
    def recognize_arguments(command: dict, command_class: str, voice_input: str) -> list:
        switch_arg_sep = {
                        ADD_EACH : ArgumentConstructor.add_each_re_arg,
                        CONCAT : ArgumentConstructor.concat_arguments,
                        PICK_FIRST_MATCH : ArgumentConstructor.pick_first_match_arg,
                        PICK_LAST_MATCH : ArgumentConstructor.pick_last_match_arg,
                        PICK_LAST_IN_FIRST_MATCH : ArgumentConstructor.pick_last_in_first_match_arg,
                        PICK_FIRST_IN_FIRST_MATCH : ArgumentConstructor.pick_first_in_first_match_arg,
                        PICK_FIRST_IN_LAST_MATCH : ArgumentConstructor.pick_first_in_last_match_arg,
                        PICK_LAST_IN_LAST_MATCH : ArgumentConstructor.pick_last_in_last_match_arg
                    }
        cmd_arguments = []
        for arg, params in command[CMD_ARGS].items():
            if params[REGEX_ON] == True:
                try:
                    re_arguments = ArgumentsProcessor.take_arg_from_string(voice_input, arg)
                except RegexArgumentError as e:
                    e.command_class = command_class
                    e.proccess_critical_error()
                    if command_class != 'random/number':
                        raise ArgumentError(command_class=command_class, argument=arg) from e  
                    else:
                        re_arguments = []
                except RegexPatternError as e:
                    e.command_class = command_class
                    e.proccess_critical_error()
                    raise ArgumentError(command_class=command_class, argument=arg) from e
                    
                arg = re_arguments

                if command_class == 'shutdown/timer':
                    cmd_arguments.append(params[PREFIX] + str(Time.convert_to_seconds(arg)) + params[POSTFIX])
                else:
                    cmd_arguments = switch_arg_sep[command[ARGS_SEP]](cmd_arguments, arg, params[PREFIX], params[POSTFIX])
                
            else:
                arg = params[PREFIX] + str(arg) + params[POSTFIX]
                cmd_arguments.append(arg)

        return cmd_arguments

    @staticmethod
    def concat_cmd_command_and_arguments(cmd_command : str, cmd_arguments : list) -> str:
        if cmd_arguments:
            return cmd_command + ' ' + ' '.join(cmd_arguments)
        return cmd_command
    
    @staticmethod
    def is_multi_group_match(match : list) -> bool:
        if len(match) > 0:
            return type(match[0]) == tuple
        return False

    @staticmethod
    def take_arg_from_string(voice_input : str, arg : str):
        nums_voice_input = WordNum.word_to_num_in_string(voice_input)
        regex = arg

        try:
            pattern = re.compile(regex)
        except TypeError:
            raise RegexPatternError(argument=arg)

        match = pattern.findall(nums_voice_input)

        if not match:
            raise RegexArgumentError(argument=arg)
        return match
