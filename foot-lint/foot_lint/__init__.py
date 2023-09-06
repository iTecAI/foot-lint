import click, rich

@click.group()
@click.option("--file", "-f", "input_file", required=True, help="Input file path", type=click.Path(exists=True))
@click.option("--verbose", "-v", is_flag=True, default=False, show_default=True, help="Display extended debug information")
@click.pass_context
def root(ctx: click.Context, verbose: bool = False):
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose

if __name__ == "__main__":
    root()

