import os
import sys
import datetime
from commandr import Commandr, load_yaml
from markdowngenerator.markdowngenerator import MarkdownGenerator


# pip3 install git+https://github.com/Nicceboy/python-markdown-generator

NODESCR = "No description given."

if __name__ == "__main__":

    # Example usage:
    # python main.py -i ../commandr/config/demo3.cmdr.yaml

    print("Starting Documentor...")

    cmdr = Commandr()
    cmdr.add_argument("infile", "-i", type="str", required=True, loadconfig=True)
    cmdr.build()
    args, configs = cmdr.parse()
    cfg = configs["infile"]

    today = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")
    documentor_version = "1.0"

    with MarkdownGenerator(
        # By setting enable_write as False, content of the file is written
        # into buffer at first, instead of writing directly into the file
        # This enables for example the generation of table of contents
        filename="target/example.md", enable_TOC=False, enable_write=False
    ) as doc:

        name = cfg["name"]
        title = cfg["title"]
        description = cfg.get("description", NODESCR)

        doc.addHeader(1, name)
        doc.addHeader(2, title)
        doc.writeTextLine(description)
        doc.writeTextLine("")
        doc.writeTextLine(f"*Generated {today} by Documentor {documentor_version}.*")

        doc.addHeader(2, "Parameters")

        for arg in cfg["args"]:
            print(arg)

            argname = arg["name"]
            argtitle = arg.get("title")
            argtype = arg.get("type", 'str')
            argdesc = arg.get("description") or arg.get("help")
            argcli = arg.get("cli")
            argreq = arg.get("required")
            argdef = arg.get("default")
            argconf = arg.get("loadconfig")
            argenv = arg.get("env")

            doc.writeTextLine(f"* ### `{argcli}`")

            if argtitle:
                doc.writeTextLine(f"  {argtitle}")

            if argdesc:
                doc.writeTextLine(f"  {argdesc}")

            doc.writeTextLine(f"")

            doc.writeTextLine(f"  Name: **{argname}**")
            doc.writeTextLine(f"  Type: **{argtype}**")

            if argenv:
                doc.writeTextLine(f"  Env: `{argenv}`")

            if argdef:
                doc.writeTextLine(f"  Default: `{argdef}`")

            if argreq:
                doc.writeTextLine(f"  **REQUIRED**")

            if argconf:
                doc.writeTextLine(f"  **LOADCONFIG**")

            doc.writeTextLine(f"")

        """
        table = [
            {"Column1": "col1row1 data", "Column2": "col2row1 data"},
            {"Column1": "col1row2 data", "Column2": "col2row2 data"},
        ]

        doc.addTable(dictionary_list=table)
        doc.writeTextLine("Ending the document....") 
        """



