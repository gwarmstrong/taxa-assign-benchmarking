#!/usr/bin/env python3
# Citation: Script modified from WoL by Qiyun Zhu
# https://biocore.github.io/wol/
"""Generate pseudo taxonomic hierarchies based on a tree.

Usage:
    tree_to_taxonomy.py tree.nwk support_cutoff brlen_cutoff

Output:
    g2lineage.txt, g2tid.txt
    nodes.dmp, names.dmp
    tree.nids.nwk (optional)
"""

# from sys import argv
from skbio import TreeNode
import argparse
import os

parser = argparse.ArgumentParser(description='Create a taxdump from a given '
                                             'tree')
parser.add_argument('tree', type=str, help="tree (newick format)to convert "
                                           "into taxdump")
parser.add_argument('--support-cutoff', type=float, default=None,
                    help="value to use to collapse poorly supported nodes")
parser.add_argument('--brlen-cutoff', type=float, default=None,
                    help="length at which to cut off shorter branches")
parser.add_argument('--out-directory', type=str, default=os.path.curdir,
                    help="directory to save the taxdump into")

args = parser.parse_args()


out_dir = args.out_directory
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

tree = TreeNode.read(args.tree)

print('Number of nodes: %d.' % tree.count())


def collapse(nodes):
    """Collapse internal nodes of a tree."""
    for node in nodes:
        length = node.length
        parent = node.parent
        for child in node.children:
            child.length += length
        parent.remove(node)
        parent.extend(node.children)


# collapse poorly supported nodes
if args.support_cutoff is not None:
    support_cutoff = args.support_cutoff
    nodes_to_collapse = []
    for node in tree.non_tips():
        if node.name is not None:
            support = float(node.name)
            if support < support_cutoff:
                nodes_to_collapse.append(node)
    collapse(nodes_to_collapse)
    print('Number of nodes: %d.' % tree.count())

# collapse short branches
if args.brlen_cutoff is not None:
    length_cutoff = args.brlen_cutoff
    while True:
        nodes_to_collapse = []
        for node in tree.non_tips():
            if node.length < length_cutoff:
                nodes_to_collapse.append(node)
        if not nodes_to_collapse:
            break
        collapse(nodes_to_collapse)
    print('Number of nodes: %d.' % tree.count())

# assign node IDs if not already done
if tree.name is None:
    idx = 1
    for node in tree.levelorder():
        if (node.name is None) and (not node.is_tip()):
            node.name = 'Ext%d' % idx
            idx += 1
    print('Internal node labels Ext1..Ext%d assigned.' % idx)

    tree.write(os.path.join(out_dir, 'tree.nids.nwk'))

# generate Greengenes-style lineage map:
# taxon <tab> N1;N5;N12;N46;N113
lineages = {}
for tip in tree.tips():
    node = tip
    lineage = [tip.name]
    while True:
        if node.parent is not None:
            node = node.parent
            if node.is_root():
                break
            lineage.append(node.name)
    lineages[tip.name] = ';'.join(lineage[::-1])
with open(os.path.join(out_dir, 'g2lineage.txt'), 'w') as f:
    for taxon, lineage in lineages.items():
        f.write('%s\t%s\n' % (taxon, lineage))

# generate fake TaxID map
tip2idx = {}
idx = 1
for node in tree.non_tips():
    idx = max(idx, int(node.name[1:]) + 1)
for tip in tree.tips():
    tip2idx[tip.name] = str(idx)
    idx += 1
with open(os.path.join(out_dir, 'g2tid.txt'), 'w') as f:
    for tip in sorted(tip2idx):
        f.write('%s\t%s\n' % (tip, tip2idx[tip]))

# generate NCBI-style taxdump files:
fnodes = open(os.path.join(out_dir, 'nodes.dmp'), 'w')
fnames = open(os.path.join(out_dir, 'names.dmp'), 'w')
for node in tree.levelorder():
    taxid = tip2idx[node.name] if node.is_tip() else node.name[1:]
    parent_taxid = node.parent.name[1:] if node.parent is not None else '1'
    fnodes.write('%s\t|\t%s\t|\tno rank\t|\n'
                 % (taxid, parent_taxid))
    fnames.write('%s\t|\t%s\t|\t\t|\tscientific name\t|\n'
                 % (taxid, node.name))
fnodes.close()
fnames.close()
