import sys
import os
from jinja2 import Environment, FileSystemLoader


def main():
    incoming_path = sys.argv[1]

    environment = Environment(
        loader=FileSystemLoader(incoming_path),
        block_start_string='[%',
        block_end_string='%]',
        variable_start_string='[[',
        variable_end_string=']]'
    )

    for template in environment.list_templates():
        print(f"Processing imports in {template}...")
        finished = environment.get_template(template).render()

        with open(os.path.join(incoming_path, template), "w") as output:
            output.write(finished)


if __name__ == "__main__":
    main()
