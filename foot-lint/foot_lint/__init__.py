import click, rich

@click.group()
@click.option("--file", "-f", "input_file", required=True, help="Input file path", type=click.Path(exists=True))
@click.option("--verbose", "-v", is_flag=True, default=False, help="Display extended debug information")
@click.pass_context
def main(ctx: click.Context, verbose: bool = False):
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose

@main.command(help="Finds lines that do not match the style guide")
@click.option("--fix", is_flag=True, default=False, help="Automatically fix source file when possible")
@click.pass_context
def lint(ctx: click.Context, fix: bool = False):
    pass

@main.command(help="Adds document author data, headers, etc")
@click.option("--lint/--no-lint", default=True, help="Lint source code before adding header info")
@click.pass_context
def pack(ctx: click.Context, fix: bool = False):
    pass

if __name__ == "__main__":
    main()

