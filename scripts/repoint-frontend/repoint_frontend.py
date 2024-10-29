import argparse
import os
import sys

remove_lines = [
    "<LoadBalancer>",
    "<Server name=\"{{ TARGET_SERVER_OVERRIDE | default(\'communications-manager-target\') }}\"/>",
    "</LoadBalancer>",
    "<Path>{requestpath}</Path>",
]

replacement_line = "        <URL>https://comms-apim.{environment}.communications.national.nhs.uk</URL>\n"

configs = [
    (
        "proxies/shared/policies/AssignMessage.MessageBatches.Create.Request.xml",
        "/api/v1/send",
        "https://comms-apim.{environment}.communications.national.nhs.uk/api/v1/send",
        False,
    ),
    (
        "proxies/shared/policies/AssignMessage.Messages.Create.Request.xml",
        "/api/v1/messages",
        "https://comms-apim.{environment}.communications.national.nhs.uk/api/v1/messages",
        False,
    ),
    (
        "proxies/shared/policies/AssignMessage.Messages.GetSingle.Request.xml",
        "/api/v1/messages/{data.messageId}",
        "https://comms-apim.{environment}.communications.national.nhs.uk/api/v1/messages/{{data.messageId}}",
        True,
    ),
    (
        "proxies/shared/policies/AssignMessage.NhsAppAccounts.Get.Request.xml",
        "/api/channels/nhsapp/accounts",
        "https://comms-apim.{environment}.communications.national.nhs.uk/api/channels/nhsapp/accounts",
        False,
    ),
]


# Helper function to check file existence
def read_file(file_path):
    if not os.path.exists(file_path):
        print(f"Error: The file at {file_path} does not exist.")
        sys.exit(1)
    with open(file_path, "r") as file:
        return file.readlines()


def write_file(file_path, lines):
    with open(file_path, "w") as file:
        file.writelines(lines)


def modify_target_file(environment, file_path):
    replaced_line = replacement_line.format(environment=environment)
    lines = read_file(file_path)

    new_lines = []
    skip = False

    for line in lines:
        # if the line matches the start of the block we want to remove
        if line.strip() == remove_lines[0].strip():
            skip = True
        # if we are skipping lines, and we reach the end of the block
        elif skip and line.strip() == remove_lines[-1].strip():
            skip = False
            # Instead of adding the removed lines, add the replacement line
            new_lines.append(replaced_line)
        # if we are not skipping, add the line to the new content
        elif not skip:
            new_lines.append(line)

    write_file(file_path, new_lines)

    print(f"File at {file_path} successfully updated with environment '{environment}'.")


def get_config(path, endpoint, url, template_tag, environment):
    file_path = path
    tag_type = "Template" if template_tag else "Value"
    match_block = [
        "<AssignVariable>",
        "<Name>requestpath</Name>",
        f"<{tag_type}>{endpoint}</{tag_type}>",
        "</AssignVariable>",
    ]

    formatted_url = url.format(environment=environment)
    insertion_lines = [
        "    {% if ENVIRONMENT_TYPE != 'sandbox' %}",
        "        <AssignVariable>",
        "            <Name>target.url</Name>",
        f"            <Value>{formatted_url}</Value>",
        "        </AssignVariable>",
        "    {% endif %}",
    ]
    return file_path, match_block, insertion_lines


def add_lines_after_block(environment, file_path, match_block, insertion_lines):
    lines = read_file(file_path)
    match_block = [line.strip() for line in match_block]

    # Format lines to add with environment where necessary
    insertion_lines = [line.replace("{environment}", environment) for line in insertion_lines]

    block_found, new_lines = False, []
    i = 0
    while i < len(lines):
        new_lines.append(lines[i])
        if lines[i].strip() == match_block[0]:
            match = all(
                lines[i + j].strip() == match_block[j]
                for j in range(len(match_block))
            )
            if match:
                block_found = True
                i += len(match_block)
                new_lines.extend(f"{line}\n" for line in insertion_lines)
                continue
        i += 1

    if not block_found:
        print(f"Error: Block not found in the file at {file_path}.")
        return

    write_file(file_path, new_lines)
    print(f"Lines successfully added after the specified block in {file_path}.")


if __name__ == "__main__":
    # Ensure script is run from the correct directory
    if os.path.basename(os.getcwd()) != "communications-manager-api":
        print("Error: repoint_frontend must be run from the project root.")
        sys.exit(1)

    parser = argparse.ArgumentParser(
        description="Script to modify target.xml based on the environment argument."
    )
    parser.add_argument(
        "environment", type=str, help="Environment identifier (e.g. 'de-gith1')"
    )
    args = parser.parse_args()

    # Modify target.xml file
    modify_target_file(args.environment, "proxies/live/apiproxy/targets/target.xml")

    # Process each config entry
    for path, endpoint, url, template_tag in configs:
        file_path, match_block, insertion_lines = get_config(
            path, endpoint, url, template_tag, args.environment
        )
        add_lines_after_block(args.environment, file_path, match_block, insertion_lines)
