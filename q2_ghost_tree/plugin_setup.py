import qiime2.plugin
# from q2_types.feature_data import FeatureData, Sequence, Taxonomy, AlignedSequence
from q2_types.feature_data import FeatureData, Sequence, AlignedSequence
from q2_types.tree import Phylogeny, Rooted

import q2_ghost_tree
from ._scaffold_hybrid_tree import scaffold_hybrid_tree
from ._extensions_cluster import extensions_cluster
from ._tip_to_tip_distances import tip_to_tip_distances
from ._otu_map import OtuMapFormat, OtuMapDirectoryFormat
from ._taxonomy import TaxonomyGTFormat, TaxonomyGTDirectoryFormat

# initiate Qiime2 plugin
plugin = qiime2.plugin.Plugin(
    name='ghost-tree',
    description='ghost-tree is a bioinformatics tool that combines sequence '
                'data from two genetic marker databases '
                'into one phylogenetic tree that can be used for diversity '
                'analyses. One database is used as a "foundation tree" '
                'because it provides better phylogeny across all phyla, '
                'and the other database provides finer taxonomic resolution.',
    version=q2_ghost_tree.__version__,
    website='https://github.com/JTFouquier/ghost-tree',
    package='q2_ghost_tree',
    user_support_text=None,
    citation_text='ghost-tree: creating hybrid-gene phylogenetic trees for '
                  'diversity analyses. Fouquier J, Rideout JR, Bolyen E, '
                  'Chase J, Shiffer A, McDonald D, Knight R, Caporaso JG, and '
                  'Kelley ST',
    short_description='Plugin for creating hybrid-gene phylogenetic trees.',
)

OtuMap = qiime2.plugin.SemanticType('OtuMap')
plugin.register_formats(OtuMapFormat, OtuMapDirectoryFormat)
plugin.register_semantic_types(OtuMap)
plugin.register_semantic_type_to_format(OtuMap,
                                        artifact_format=OtuMapDirectoryFormat)


TaxonomyGT = qiime2.plugin.SemanticType('TaxonomyGT')
plugin.register_formats(TaxonomyGTFormat, TaxonomyGTDirectoryFormat)
plugin.register_semantic_types(TaxonomyGT)
plugin.register_semantic_type_to_format(TaxonomyGT,
                                        artifact_format=TaxonomyGTDirectoryFormat)


# Register all methods used by ghost-tree
plugin.methods.register_function(
    function=scaffold_hybrid_tree,
    inputs={
        'otu_map': OtuMap, # ghost-tree semantic type
        'extension_taxonomy': TaxonomyGT,
        'extension_sequences': FeatureData[Sequence],
        'foundation_alignment': FeatureData[AlignedSequence]
    },
    parameters={
    },
    outputs=[
        ('ghost_tree', Phylogeny[Rooted]),
    ],
    name='scaffold-hybrid-tree',
    description='This method creates a hybrid-gene phylogenetic tree.'
)


# setup similarity threshold
p = qiime2.plugin
p = p.Float % p.Range(0.00, 1.00)

plugin.methods.register_function(
    function=extensions_cluster,
    inputs={
        'extension_sequences': FeatureData[Sequence],
    },
    parameters={'similarity_threshold': p
    },
    outputs=[
        ('otu_map', OtuMap),
    ],
    name='extensions-cluster',
    description='Groups sequences in .fasta file by similarity threshold'
)

# plugin.methods.register_function(
#     function=tip_to_tip_distances,
#     inputs={
#         'tree_1': Phylogeny[Rooted],
#         'tree_2': Phylogeny[Rooted],
#     },
#     parameters={'method': str,
#     },
#     outputs=[
#         ('otu_formatted', str),
#     ],
#     name='tip_to_tip_distances',
#     description='Compare to tip distances in two phylogenetic trees using Mantel test'
# )


# # (NOTE this is extremely SILVA specific. Need to review how we
# # accomplished this)
# plugin.methods.register_function(
#     function=extract_fungi,
#     inputs={
#         'tree_1': Phylogeny[Rooted],
#         'tree_2': Phylogeny[Rooted],
#     },
#     parameters={'method': str,
#     },
#     outputs=[
#         ('otu_formatted', str),
#     ],
#     name='extract_fungi',
#     description=''
# )
