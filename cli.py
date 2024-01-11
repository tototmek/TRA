import argparse
import os
import yaml
from params import DelayEffectParams, FilterParams

PROGRAM_DESCRIPTION = "an audio delay effect"

ARG_DEFAULT_VALUES = {
    "time": 0.5,
    "dry": 0.6,
    "wet": 0.4,
    "feedback": 0.8,
    "filter-filterness": 0.8,
}

ARG_HELP = {
    "time": "Effect delay time.",
    "dry": "Dry gain.",
    "wet": "Wet gain.",
    "feedback": "Feedback gain.",
    "filter-filterness": "Some random filter param.",
}


def parse_args() -> DelayEffectParams:
    parser = construct_parser()
    args = parser.parse_args()
    if args.file is not None:
        args_dict = load_dict(args.file)
        print(f"Loaded configuration from '{args.file}'")
    else:
        args_dict = convert_to_dict(args)
    effect_params = construct_effect_params(args_dict)
    return effect_params


def construct_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=PROGRAM_DESCRIPTION)
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        help="Path to file containing configuration. If specified, other arguments are ignored.",
    )
    for field in get_field_names(DelayEffectParams):
        arg_name = format_as_arg(field)
        if arg_name == "filter":
            continue
        parser.add_argument(
            f"--{arg_name}",
            type=float,
            default=get_arg_default(arg_name),
            help=get_arg_help(arg_name),
        )
    for field in get_field_names(FilterParams):
        arg_name = "filter-" + format_as_arg(field)
        parser.add_argument(
            f"--{arg_name}",
            type=float,
            default=get_arg_default(arg_name),
            help=get_arg_help(arg_name),
        )
    return parser


def construct_effect_params(args: dict) -> DelayEffectParams:
    try:
        filter_params = FilterParams()
        for field in get_field_names(FilterParams):
            arg_name = "filter_" + field
            filter_params.__setattr__(field, args[arg_name])
        delay_effect_params = DelayEffectParams()
        for field in get_field_names(DelayEffectParams):
            arg_name = field
            if arg_name == "filter":
                continue
            delay_effect_params.__setattr__(field, args[arg_name])
        delay_effect_params.filter = filter_params
        return delay_effect_params
    except KeyError as e:
        print(f"Error: Parameter {e} not specified.")
        exit(0)


def get_field_names(class_type):
    return [field for field, _ in class_type.__annotations__.items()]


def format_as_arg(field_name):
    return field_name.replace("_", "-")


def get_arg_default(arg_name):
    if arg_name not in ARG_DEFAULT_VALUES:
        return 0.0
    else:
        return ARG_DEFAULT_VALUES[arg_name]


def get_arg_help(arg_name):
    if arg_name not in ARG_HELP:
        return f"The {arg_name} parameter. Default: {get_arg_default(arg_name)}"
    else:
        return ARG_HELP[arg_name] + f" Default: {get_arg_default(arg_name)}"


def load_dict(path: str):
    if not os.path.exists(path) or not os.path.isfile(path):
        print(f"Error: The file '{path}' does not exist.")
        exit(1)
    if not os.access(path, os.R_OK):
        print(f"Error: Cannot access '{path}': Permission denied.")
        exit(1)
    with open(path, "r") as file:
        try:
            data = yaml.safe_load(file)
            return data
        except yaml.YAMLError as e:
            print(f"Error: Couldn't load configuration from '{path}': {e}")
            exit(1)


def convert_to_dict(args: argparse.Namespace):
    return {
        attr: getattr(args, attr)
        for attr in dir(args)
        if not callable(getattr(args, attr)) and not attr.startswith("__")
    }
