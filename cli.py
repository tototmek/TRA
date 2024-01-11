import argparse
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
    effect_params = construct_effect_params(args)
    return effect_params


def construct_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=PROGRAM_DESCRIPTION)
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


def construct_effect_params(args: argparse.Namespace) -> DelayEffectParams:
    args = args_to_dict(args)
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


def args_to_dict(args):
    return {
        attr: getattr(args, attr)
        for attr in dir(args)
        if not callable(getattr(args, attr)) and not attr.startswith("__")
    }
