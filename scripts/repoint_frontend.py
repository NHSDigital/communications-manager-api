import argparse
import os
import sys


def modify_target_file(shortcode, file_path):
    # lines to remove
    remove_lines = [
        '<LoadBalancer>',
        '<Server name="{{ TARGET_SERVER_OVERRIDE | default(\'communications-manager-target\') }}"/>',
        '</LoadBalancer>',
        '<Path>{requestpath}</Path>'
    ]

    # replacement line with the shortcode
    replacement_line = f'        <URL>https://comms-apim.de-{shortcode}.communications.national.nhs.uk</URL>\n'  # noqa: E221 E231 E501

    if not os.path.exists(file_path):
        print(f"Error: The file at {file_path} does not exist.")
        return

    with open(file_path, 'r') as file:
        lines = file.readlines()

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
            new_lines.append(replacement_line)
        # if we are not skipping, add the line to the new content
        elif not skip:
            new_lines.append(line)

    with open(file_path, 'w') as file:
        file.writelines(new_lines)

    print(f"File at {file_path} successfully updated with shortcode '{shortcode}'.")


def add_lines_after_block(shortcode, file_path, block_to_follow, lines_to_add):
    if not os.path.exists(file_path):
        print(f"Error: The file at {file_path} does not exist.")
        return

    with open(file_path, 'r') as file:
        lines = file.readlines()

    block_to_follow = [line.strip() for line in block_to_follow]
    temp = []
    for line in lines_to_add:
        try:
            temp.append(line.format(shortcode=shortcode))
        except (ValueError, KeyError):
            # this function trips up on  the {% %} syntax, dirty workaround is to add those lines without formatting
            temp.append(line)

    lines_to_add = temp

    block_found = False
    new_lines = []
    i = 0

    while i < len(lines):
        # add lines to the new content
        new_lines.append(lines[i])

        # check for the block start
        if lines[i].strip() == block_to_follow[0]:
            block_match = True
            # check if the subsequent lines match the rest of the block
            for j in range(1, len(block_to_follow)):
                if i + j >= len(lines):
                    block_match = False
                    break

                # add inspected lines to the new content
                new_lines.append(lines[i + j])

                if lines[i + j].strip() != block_to_follow[j]:
                    block_match = False
                    break

            # if the block matches fully add lines after the block
            if block_match:
                block_found = True
                # move the index to the end of the block
                i += len(block_to_follow)
                # add the lines after the block
                new_lines.extend([f"{line}\n" for line in lines_to_add])
                continue  # skip to next iteration after inserting lines

        i += 1

    if not block_found:  # noqa: E713
        print(f"Error: Block not found in the file at {file_path}.")
        return

    with open(file_path, 'w') as file:
        file.writelines(new_lines)

    print(f"Lines successfully added after the specified block in {file_path}.")


if __name__ == "__main__":
    current_directory = os.getcwd()
    directory_name = os.path.basename(current_directory)

    if (directory_name != "communications-manager-api"):
        print("Error: repoint_frontend must be run from the project root. Current dir:", directory_name)
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Script to modify the target.xml file based on the environment argument.")  # noqa: E501

    parser.add_argument('shortcode', type=str, help="Environment identifier (e.g. 'gith1')")
    args = parser.parse_args()

    # modify target.xml
    file_path = 'proxies/live/apiproxy/targets/target.xml'
    modify_target_file(args.shortcode, file_path)

    # modify AssignMessage.MessageBatches.Create.Request.xml
    file_path = 'proxies/shared/policies/AssignMessage.MessageBatches.Create.Request.xml'
    block_to_follow = [
        '<AssignVariable>',
        '<Name>requestpath</Name>',
        '<Value>/api/v1/send</Value>',
        '</AssignVariable>'
    ]
    lines_to_add = [
        '    {{% if ENVIRONMENT_TYPE != \'sandbox\' %}}',
        '        <AssignVariable>',
        '            <Name>target.url</Name>',
        '            <Value>https://comms-apim.de-{shortcode}.communications.national.nhs.uk/api/v1/send</Value>',
        '        </AssignVariable>',
        '    {% endif %}'
    ]
    add_lines_after_block(args.shortcode, file_path, block_to_follow, lines_to_add)

    # modify proxies/shared/policies/AssignMessage.Messages.Create.Request.xml
    file_path = 'proxies/shared/policies/AssignMessage.Messages.Create.Request.xml'
    block_to_follow = [
        '<AssignVariable>',
        '<Name>requestpath</Name>',
        '<Value>/api/v1/messages</Value>',
        '</AssignVariable>'
    ]
    lines_to_add = [
        '    {% if ENVIRONMENT_TYPE != \'sandbox\' %}',
        '        <AssignVariable>',
        '            <Name>target.url</Name>',
        '            <Value>https://comms-apim.de-{shortcode}.communications.national.nhs.uk/api/v1/messages</Value>',
        '        </AssignVariable>',
        '    {% endif %}'
    ]
    add_lines_after_block(args.shortcode, file_path, block_to_follow, lines_to_add)

    # modify proxies/shared/policies/AssignMessage.Messages.GetSingle.Request.xml
    file_path = 'proxies/shared/policies/AssignMessage.Messages.GetSingle.Request.xml'
    block_to_follow = [
        '<AssignVariable>',
        '<Name>requestpath</Name>',
        '<Template>/api/v1/messages/{data.messageId}</Template>',
        '</AssignVariable>'
    ]
    lines_to_add = [
        '    {% if ENVIRONMENT_TYPE != \'sandbox\' %}',
        '        <AssignVariable>',
        '            <Name>target.url</Name>',
        '            <Value>https://comms-apim.de-{shortcode}.communications.national.nhs.uk/api/v1/messages/{{data.messageId}}</Value>',  # noqa: E501
        '        </AssignVariable>',
        '    {% endif %}'
    ]
    add_lines_after_block(args.shortcode, file_path, block_to_follow, lines_to_add)

    # modify proxies/shared/policies/AssignMessage.NhsAppAccounts.Get.Request.xml
    file_path = "proxies/shared/policies/AssignMessage.NhsAppAccounts.Get.Request.xml"
    block_to_follow = [
        '<AssignVariable>',
        '<Name>requestpath</Name>',
        '<Value>/api/channels/nhsapp/accounts</Value>',
        '</AssignVariable>'
    ]
    lines_to_add = [
        '    {% if ENVIRONMENT_TYPE != \'sandbox\' %}',
        '        <AssignVariable>',
        '            <Name>target.url</Name>',
        '            <Value>https://comms-apim.de-{shortcode}.communications.national.nhs.uk/api/channels/nhsapp/accounts</Value>',  # noqa: E501
        '        </AssignVariable>',
        '    {% endif %}'
    ]
    add_lines_after_block(args.shortcode, file_path, block_to_follow, lines_to_add)
