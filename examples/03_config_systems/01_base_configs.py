"""Base Configurations

We can integrate `tyro.cli()` into common configuration patterns: here, we select
one of multiple possible base configurations, create a subcommand for each one, and then
use the CLI to either override (existing) or fill in (missing) values.

Note that our interfaces don't prescribe any of the mechanics used for storing
base configurations. A Hydra-style YAML approach could just as easily
be used for the config library (although we generally prefer to avoid YAMLs; staying in
Python is convenient for autocompletion and type checking).

Usage:
`python ./10_base_configs.py --help`
`python ./10_base_configs.py small --help`
`python ./10_base_configs.py small --seed 94720`
`python ./10_base_configs.py big --help`
`python ./10_base_configs.py big --seed 94720`
"""

from dataclasses import dataclass
from typing import Callable, Literal, Tuple, Union

from torch import nn

import tyro


@dataclass(frozen=True)
class AdamOptimizer:
    learning_rate: float = 1e-3
    betas: Tuple[float, float] = (0.9, 0.999)


@dataclass(frozen=True)
class SgdOptimizer:
    learning_rate: float = 3e-4


@dataclass(frozen=True)
class ExperimentConfig:
    # Dataset to run experiment on.
    dataset: Literal["mnist", "imagenet-50"]

    # Optimizer parameters.
    optimizer: Union[AdamOptimizer, SgdOptimizer]

    # Model size.
    num_layers: int
    units: int

    # Batch size.
    batch_size: int

    # Total number of training steps.
    train_steps: int

    # Random seed. This is helpful for making sure that our experiments are all
    # reproducible!
    seed: int

    # Activation to use. Not specifiable via the commandline.
    activation: Callable[[], nn.Module]


# Note that we could also define this library using separate YAML files (similar to
# `config_path`/`config_name` in Hydra), but staying in Python enables seamless type
# checking + IDE support.
descriptions = {}
base_configs = {}

descriptions["small"] = "Train a smaller model."
base_configs["small"] = ExperimentConfig(
    dataset="mnist",
    optimizer=SgdOptimizer(),
    batch_size=2048,
    num_layers=4,
    units=64,
    train_steps=30_000,
    # The tyro.MISSING sentinel allows us to specify that the seed should have no
    # default, and needs to be populated from the CLI.
    seed=tyro.MISSING,
    activation=nn.ReLU,
)


descriptions["big"] = "Train a bigger model."
base_configs["big"] = ExperimentConfig(
    dataset="imagenet-50",
    optimizer=AdamOptimizer(),
    batch_size=32,
    num_layers=8,
    units=256,
    train_steps=100_000,
    seed=tyro.MISSING,
    activation=nn.GELU,
)


if __name__ == "__main__":
    config = tyro.cli(
        tyro.extras.subcommand_type_from_defaults(base_configs, descriptions),
    )
    # ^Note that this is equivalent to:
    #
    # config = tyro.cli(
    #     Union[
    #         Annotated[
    #             ExperimentConfig,
    #             tyro.conf.subcommand(
    #                 "small",
    #                 default=base_configs["small"],
    #                 description=descriptions["small"],
    #             ),
    #         ],
    #         Annotated[
    #             ExperimentConfig,
    #             tyro.conf.subcommand(
    #                 "big",
    #                 default=base_configs["big"],
    #                 description=descriptions["big"],
    #             ),
    #         ],
    #     ]
    # )
    print(config)