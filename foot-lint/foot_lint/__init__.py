import click, rich
from ._types import *
from .linter import lint_main
import json

DEFAULT_OPTIONS: LintOptions = {
    "columnWidth": 8,
    "labelColumn": 0,
    "instructionColumn": 1,
    "operandColumn": 2,
    "commentSpace": 1,
    "lineLength": 80,
    "fileHeader": [
        "# Filename: {filename}",
        "# Author: {author}",
        "# Contributors:",
        "#               {contributors}",
        "# Description:",
        "#               {description}",
        "# Revisions: {version}"
    ]
}



@click.group()
@click.option("--file", "-f", "input_file", required=True, help="Input file path", type=click.Path(exists=True))
@click.option("--verbose", "-v", is_flag=True, default=False, help="Display extended debug information")
@click.option("--config", "-c", "config_file", default=None, help="Config file path", type=click.Path(exists=True))
@click.pass_context
def main(ctx: click.Context, input_file: str, verbose: bool, config_file: str):
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    with open(input_file, "r") as f:
        ctx.obj["file"] = f.read().split("\n")
        ctx.obj["file_path"] = input_file
    
    if config_file:
        with open(config_file, "r") as f:
            ctx.obj["config"] = json.load(f)
    else:
        ctx.obj["config"] = DEFAULT_OPTIONS

@main.command(help="Finds lines that do not match the style guide")
@click.option("--fix", is_flag=True, default=False, help="Automatically fix source file when possible")
@click.pass_context
def lint(ctx: click.Context, fix: bool = False):
    context: LintContext = ctx.obj
    result = lint_main(context["file"], context["config"], context["verbose"])
    if fix:
        with open(context["file_path"], "w") as to_fix:
            to_fix.write("\n".join(result))
    else:
        print("\n".join(result))

@main.command(help="Adds document author data, headers, etc")
@click.option("--lint/--no-lint", default=True, help="Lint source code before adding header info")
@click.pass_context
def pack(ctx: click.Context, lint: bool = True):
    context: LintContext = ctx.obj

if __name__ == "__main__":
    main()

