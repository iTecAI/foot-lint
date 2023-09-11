from ._types import *
import json


def boolmask(true: list[str], false: list[str], parts: dict[str, str]) -> bool:
    return all([bool(parts[t]) for t in true]) and all(
        [not bool(parts[f]) for f in false]
    )


def smartwrap(input: str, max_length: int) -> list[str]:
    lines = []
    current = ""
    tokens = input.split(" ")
    for t in tokens:
        if len(current + " " + t) > max_length:
            lines.append(current)
            current = t
        else:
            current += " " + t

    if len(current) > 0:
        lines.append(current)
    return [l.strip() for l in lines if len(l) > 0]


def tabs(count: int, config: LintOptions) -> str:
    return " " * count * config["columnWidth"]


def lint_main(lines: list[str], config: LintOptions, verbose: bool) -> list[str]:
    expanded_lines = []
    is_block_comment = False
    for line in lines:
        tokens = [i for i in line.split(" ") if len(i) > 0]
        parts = {"label": None, "mnemonic": None, "parameters": [], "comment": []}
        expanded = {
            "lines": [],
            "endline": None
        }

        ct = 0

        for t in tokens:
            if t.startswith("#"):
                parts["comment"].append(t)
                continue

            if len(parts["comment"]) > 0:
                parts["comment"].append(t)
                continue

            if not parts["label"] and t.endswith(":") and ct == 0:
                parts["label"] = t
                continue

            if not parts["mnemonic"] and not "," in t and not "$" in t:
                parts["mnemonic"] = t
                continue

            parts["parameters"].append(t)
            ct += 1

        parts["comment"] = (
            " ".join(parts["comment"]) if len(parts["comment"]) > 0 else None
        )
        parts["parameters"] = (
            " ".join(parts["parameters"]) if len(parts["parameters"]) > 0 else None
        )

        if boolmask(["comment"], ["label", "mnemonic", "parameters"], parts):
            expanded["lines"].extend(
                [
                    "# " + l
                    for l in smartwrap(
                        parts["comment"].lstrip("# "), config["lineLength"] - 2
                    )
                ]
            )

            is_block_comment = True
        else:
            if is_block_comment:
                is_block_comment = False
                expanded["lines"].append("")
            if parts["label"]:
                expanded["lines"].append(parts["label"].strip())

            if parts["comment"] and parts["mnemonic"]:
                expanded["endline"] = parts["comment"]
            
            if not "=" in ((parts["mnemonic"] if parts["mnemonic"] else "") + (parts["parameters"] if parts["parameters"] else "")) and parts["mnemonic"]:
                expanded["lines"].append(
                    tabs(1, config)
                    + parts["mnemonic"]
                    + " "
                    * (
                        config["columnWidth"] * (config["operandColumn"] - config["instructionColumn"])
                        - len(parts["mnemonic"])
                    )
                    + (parts["parameters"] if parts["parameters"] else "")
                )
            
            if "=" in ((parts["mnemonic"] if parts["mnemonic"] else "") + (parts["parameters"] if parts["parameters"] else "")) and parts["mnemonic"]:
                expanded["lines"].append(parts["mnemonic"] + " " + (parts["parameters"] if parts["parameters"] else ""))

        expanded_lines.append(expanded)

    min_comment_tab = max([max([len(i) for i in l["lines"]]) for l in expanded_lines if l["endline"]]) + config["columnWidth"] * config["commentSpace"]
    fixed = []
    for l in expanded_lines:
        if l["endline"]:
            if len(l["lines"][-1] + (" " * (min_comment_tab - len(l["lines"][-1]))) + l["endline"]) > config["lineLength"]:
                fixed.extend(l["lines"][:-1])
                fixed.extend([(tabs(config["instructionColumn"], config) if not "=" in l["lines"][-1] else "") + "# " + i.strip("# ") for i in smartwrap(l["endline"], config["lineLength"] - config["columnWidth"] * config["instructionColumn"] - 2)])
                fixed.append(l["lines"][-1])
            else:
                fixed.extend(l["lines"][:-1])
                fixed.append(l["lines"][-1] + (" " * (min_comment_tab - len(l["lines"][-1]))) + l["endline"])
        else:
            fixed.extend(l["lines"])
    
    final = [fixed[0]]
    for i in range(1, len(fixed)):
        if fixed[i].strip().startswith("#") and not fixed[i - 1].strip().startswith("#"):
            final.append("")
            final.append(fixed[i])
        else:
            final.append(fixed[i])

    return final
