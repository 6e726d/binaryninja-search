#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 Andrés Blanco <6e726d@gmail.com>
#
# Permission to use, copy, modify, and/or distribute this software for
# any purpose with or without fee is hereby granted.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN
# AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
# OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.


from binaryninja import *


def instruction_text_token_to_string(instruction_token_list):
    """
    Returns a string with the instruction contained in an InstructionTextToken.
    """
    aux_lst = list()
    for instruction_token in instruction_token_list:
        if not isinstance(instruction_token, function.InstructionTextToken):
            raise TypeError('List must contain InstructionTextToken objects only.')
        aux_lst.append(instruction_token.text.strip())
    return " ".join(aux_lst)


def process_immediate(immediate):
    """
    Returns a integer object from a string object.
    """
    if not isinstance(immediate, str):
        raise TypeError('Immediate must be a String object.')
    if immediate.startswith("0x"):
        return int(immediate, 16)
    else:
        return int(immediate)


def lookup_for_immediate(bv, immediate):
    """
    Go through all functions looking for instructions with the immediate.
    """
    result = list()
    for function_item in bv.functions:
        function_instructions = function_item.instructions
        try:
            while 1:
                (instruction, address) = function_instructions.next()
                for token in instruction:
                    if token.type == InstructionTextTokenType.PossibleAddressToken:
                        if token.value == immediate:
                            instruction_text = instruction_text_token_to_string(instruction)
                            result.append((address, function_item.name, instruction_text))
        except StopIteration:
            pass
    return result


def show_results_report(bv, value, results):
    """
    Show html report with the results of the search.
    """
    html = str()
    plaintext = str()
    html += "<!DOCTYPE html>\n"
    html += "<html>\n\t<body>\n"
    html += "\t\t<table>\n"
    html += "\t\t\t<tr>\n"
    html += "\t\t\t\t<th width=\"150\">Address</th>\n"
    html += "\t\t\t\t<th width=\"150\">Function</th>\n"
    html += "\t\t\t\t<th>Instruction</th>\n"
    html += "\t\t\t</tr>\n"
    for item in results:
        html += "\t\t\t<tr>\n"
        html += "\t\t\t\t<td><pre>0x%016X</pre></td>\n" % item[0]
        html += "\t\t\t\t<td><pre>%s</pre></td>\n" % item[1]
        html += "\t\t\t\t<td><pre>%s</pre></td>\n" % item[2]
        html += "\t\t\t</tr>\n"
    html += "\t\t</table>\n"
    html += "\t</body>\n</html>"
    bv.show_html_report("Search immediate - 0x%X" % value, html, plaintext)


def do_stuff(bv):
    immediate_str = get_text_line_input('Value to search', 'Search Immediate')
    immediate = process_immediate(immediate_str)
    results = lookup_for_immediate(bv, immediate)
    show_results_report(bv, immediate, results)


name = "Search Immediate"
description = "Search for the specific value in the instruction operands."
PluginCommand.register(name, description, do_stuff)
