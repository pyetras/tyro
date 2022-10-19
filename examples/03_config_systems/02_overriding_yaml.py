"""Overriding YAML Configs

If you have a library of existing YAML files that you want to use, `tyro` can be used to
override values in them.

Usage:
`python ./02_overriding_yaml.py --help`
`python ./02_overriding_yaml.py --training.checkpoint-steps 300 1000 9000`
"""

import yaml

import tyro

# Our YAML configuration. Note that this could also be loaded from a file!
# Environment variables are an easy way to select between different YAML files.
default_yaml = r"""
exp_name: test
optimizer:
    learning_rate: 0.0001
    type: adam
training:
    batch_size: 32
    num_steps: 10000
    checkpoint_steps:
    - 500
    - 1000
    - 1500
""".strip()

if __name__ == "__main__":
    # Convert out YAML config into a nested dictionary.
    default_config = yaml.safe_load(default_yaml)

    # Override fields in the dictionary.
    overridden_config = tyro.cli(dict, default=default_config)

    # Print the overridden config.
    overridden_yaml = yaml.safe_dump(overridden_config)
    print(overridden_yaml)
