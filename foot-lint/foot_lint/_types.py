from typing_extensions import TypedDict

class LintOptions(TypedDict):
    columnWidth: int
    labelColumn: int
    instructionColumn: int
    operandColumn: int
    commentSpace: int
    lineLength: int
    fileHeader: list[str]

class LintContext(TypedDict):
    verbose: bool
    file: list[str]
    file_path: str
    config: LintOptions

