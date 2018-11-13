from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
    UniqueIdProperty, RelationshipTo, RelationshipFrom)

config.DATABASE_URL = 'bolt://neo4j:ElectricWizard113@localhost:7687'

class Source(StructuredNode):
    name = StringProperty()
    description = StringProperty()

    sample = RelationshipTo('Sample', 'PROVIDED_SAMPLE')

class Sample(StructuredNode):
    name = StringProperty()
    name_fs  = StringProperty()
    description = StringProperty()

    # traverse outgoing CONTAINS relations, inflate to SampleMgContainer objects
    container = RelationshipTo('SampleMgContainer', 'CONTAINS')

class SampleMg(StructuredNode):
    name = StringProperty()
    name_fs  = StringProperty()
    description = StringProperty()

    # traverse outgoing CONTAINS relations, inflate to SampleMgContainer objects
    container = RelationshipTo('SampleMgContainer', 'CONTAINS')



class SampleMgContainer(StructuredNode):
    preproc = StringProperty()
    # traverse incoming CONTAINS relation, inflate to SampleMg objects
    sample = RelationshipFrom('SampleMg', 'CONTAINS')


class SampleMgContainerFile(StructuredNode):
    strand = StringProperty()
    orig_file_location = StringProperty()
    # traverse incoming IS_FROM relation, inflate to Person objects
    sample_mg_container = RelationshipFrom('SampleMgContainer', 'CONTAINS')