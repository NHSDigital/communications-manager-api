import argparse
import os
import sys

default_config = [
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

alternate_config = [
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


def get_config_default(path, endpoint, url, template_tag, environment):
    tag_type = "Template" if template_tag else "Value"
    match_block = [
        "<AssignVariable>",
        "<Name>requestpath</Name>",
        f"<{tag_type}>{endpoint}</{tag_type}>",
        "</AssignVariable>",
    ]
    formatted_url = url.format(environment=environment)
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


def get_config_alternate(path, environment):
    match_block = [
        "<LoadBalancer>",
        "<Server name=\"{{ TARGET_SERVER_OVERRIDE | default('communications-manager-target') }}\"/>",
        "</LoadBalancer>",
        "<Path>{requestpath}</Path>",
    ]
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


def get_config_by_type(block_type, *args):
    if block_type == "default":
        return get_config_default(*args)
    elif block_type == "alternate":
        return get_config_alternate(*args)
    else:
        raise ValueError(f"Unknown block type: {block_type}")


def update_file(environment, file_path, match_block, insertion_lines):
    lines = read_file(file_path)
    match_block = [line.strip() for line in match_block]

    insertion_lines = [
        line.replace("{environment}", environment) for line in insertion_lines
    ]

    block_found, new_lines = False, []
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
                new_lines.extend(
                    f"{line}\n" for line in insertion_lines
                )  # Insert new lines
                continue
        new_lines.append(lines[i])
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
        description="Script to update proxy configuration files based on the environment argument."
    )
    parser.add_argument(
        "environment", type=str, help="Environment identifier (e.g. 'de-gith1')"
    )
    args = parser.parse_args()

    # Process `default` block type configs
    for path, endpoint, url, template_tag in default_config:
        file_path, match_block, insertion_lines = get_config_by_type(
            "default", path, endpoint, url, template_tag, args.environment
        )
        update_file(args.environment, file_path, match_block, insertion_lines)

    # Process `alternate` block type configs
    for path, environment in alternate_config:
        file_path, match_block, insertion_lines = get_config_by_type(
            "alternate", path, args.environment
        )
        update_file(args.environment, file_path, match_block, insertion_lines)
