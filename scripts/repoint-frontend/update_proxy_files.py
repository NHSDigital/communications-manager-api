import argparse
import os
import sys

default_setup = [
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

alternate_setup = [
    ("proxies/live/apiproxy/targets/target.xml", "{environment}"),
]


def read_file(file_path):
    if not os.path.exists(file_path):
        print(f"Error: The file at {file_path} does not exist.")
        sys.exit(1)
    with open(file_path, "r") as file:
        return file.readlines()


def write_file(file_path, lines):
    with open(file_path, "w") as file:
        file.writelines(lines)


def setup_default_block(path, endpoint, url, template_tag, environment):
    """
    Common setup for most proxy files.
    """
    tag_type = "Template" if template_tag else "Value"
    # Block of lines we're looking to replace in the file
    match_block = [
        "<AssignVariable>",
        "<Name>requestpath</Name>",
        f"<{tag_type}>{endpoint}</{tag_type}>",
        "</AssignVariable>",
    ]
    formatted_url = url.format(environment=environment)
    # Lines that will replace `match_block`
    insertion_lines = [
        "    {% if ENVIRONMENT_TYPE == 'sandbox' %}",
        "       <AssignVariable>",
        "           <Name>requestpath</Name>",
        f"           <{tag_type}>{endpoint}</{tag_type}>",
        "       </AssignVariable>",
        "    {% else %}",
        "        <AssignVariable>",
        "            <Name>target.url</Name>",
        f"            <Value>{formatted_url}</Value>",
        "        </AssignVariable>",
        "    {% endif %}",
    ]
    return path, match_block, insertion_lines


def setup_alternate_block(path, environment):
    """
    Specific setup for target.xml
    """
    # Block of lines we're looking to replace in the file
    match_block = [
        "<LoadBalancer>",
        "<Server name=\"{{ TARGET_SERVER_OVERRIDE | default('communications-manager-target') }}\"/>",
        "</LoadBalancer>",
        "<Path>{requestpath}</Path>",
    ]
    # Lines that will replace `match_block`
    insertion_lines = [
        "       {% if ENVIRONMENT_TYPE == 'sandbox' %}",
        "           <LoadBalancer>",
        "	            <Server name=\"{{ TARGET_SERVER_OVERRIDE | default('communications-manager-target') }}\"/>",
        "           </LoadBalancer>",
        "           <Path>{requestpath}</Path>",
        "       {% else %}",
        f"           <URL>https://comms-apim.{environment}.communications.national.nhs.uk</URL>",
        "       {% endif %}",
    ]
    return path, match_block, insertion_lines


def configure_block_by_type(block_type, *args):
    """
    Wrapper function to select the appropriate setup
    """
    if block_type == "default":
        return setup_default_block(*args)
    elif block_type == "alternate":
        return setup_alternate_block(*args)
    else:
        raise ValueError(f"Unknown block type: {block_type}")

#
# update_file
#
# Scans for a set of lines that match match_block exactly
# When found it will substitute that set of lines with the set of lines
# defined in insertion_lines, exception where {environment} is replaced
# with the value of the environment argument
#
def update_file(environment, file_path, match_block, insertion_lines):
    lines = read_file(file_path)
    match_block = [line.strip() for line in match_block]

    insertion_lines = [
        line.replace("{environment}", environment) for line in insertion_lines
    ]

    block_found = False
    new_lines = []
    i = 0

    while i < len(lines):
        # Check if current line matches the start of match_block
        if lines[i].strip() == match_block[0]:
            # Check if the full match_block matches line-by-line
            match = all(
                lines[i + j].strip() == match_block[j] for j in range(len(match_block))
            )
            if match:
                block_found = True
                i += len(match_block)
                # Insert new lines
                new_lines.extend(
                    f"{line}\n" for line in insertion_lines
                )
        else:
            new_lines.append(lines[i])
            i += 1

    if not block_found:
        print(f"Error: No matching block found in the file at {file_path}.")
        return

    write_file(file_path, new_lines)
    print(f"Lines successfully added in {file_path}.")


if __name__ == "__main__":
    # Ensure script is run from the correct directory
    if os.path.basename(os.getcwd()) != "communications-manager-api":
        print("Error: the script must be run from the project root.")
        sys.exit(1)

    parser = argparse.ArgumentParser(
        description="Script to update proxy configuration files based on the environment argument."
    )
    parser.add_argument(
        "environment", type=str, help="Environment identifier (e.g. 'de-gith1')"
    )
    args = parser.parse_args()

    # Process the standard proxy file configurations (default setup)
    #
    # The purpose of this is to edit the files under proxies/shared/policies and
    # override their target.url variables with a hardcoded URL that points to
    # the targetted environment
    for path, endpoint, url, template_tag in default_setup:
        file_path, match_block, insertion_lines = configure_block_by_type(
            "default", path, endpoint, url, template_tag, args.environment
        )
        update_file(args.environment, file_path, match_block, insertion_lines)

    # Process the target.xml-specific configurations (alternate setup)
    #
    # The purpose of this is to edit target.xml under proxies/live/apiproxy so
    # that it as a hard-coded URL to point to the given target environment
    for path, environment in alternate_setup:
        file_path, match_block, insertion_lines = configure_block_by_type(
            "alternate", path, args.environment
        )
        update_file(args.environment, file_path, match_block, insertion_lines)
