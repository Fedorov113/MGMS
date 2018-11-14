from msys.neomodels.mg_data_models import SampleMg, Source, Sample, Study
from rest_framework.views import APIView
from django.http import HttpResponse
import json
from py2neo.ogm import GraphObject, Property, Label, RelatedTo
from py2neo.data import Node, Relationship, walk
from py2neo import Graph, NodeMatcher

import uuid


def serialize_sample_mg_full(node):
    props = node.__properties__
    props['containers'] = []
    for c in node.container.all():
        props['containers'].append(serialize_sample_mg_container_full(c))
    return props


def serialize_sample_mg_container_full(node):
    props = node.__properties__
    return node.__properties__


class SampleMgList(APIView):
    def get(self, params):
        print('GETTING NODES')
        mg_sample_full = []
        s = SampleMg.nodes.all()
        print(s)
        for node in s:
            mg_sample_full.append(serialize_sample_mg_full(node))

        print('samples')
        return HttpResponse(json.dumps(mg_sample_full), content_type='application/json')


def serialize_source(node):
    return node.__properties__


class SourceList(APIView):
    def get(self, params, study=None):
        sources_list = []
        if study is None:
            sources = Source.nodes.all()
            for s in sources:
                sources_list.append(serialize_source(s))
        else:
            study = Study.nodes.get(name=study)
            for s in study.sources:
                sources_list.append(s.__properties__)

        return HttpResponse(json.dumps(sources_list), content_type='application/json')

    def post(self, request):
        data = request.data
        s = Source(name=data['name'], description=data['description']).save()
        if 'study' in data.keys():
            study = Study.nodes.get(name=data['study'])
            s.study.connect(study)

        return HttpResponse(json.dumps(serialize_source(s)), content_type='application/json')


def serialize_study(node):
    return node.__properties__


class StudyList(APIView):
    def get(self, params):
        studies = Study.nodes.all()
        studies_list = []
        for s in studies:
            studies_list.append(serialize_study(s))
        return HttpResponse(json.dumps(studies_list), content_type='application/json')

    def post(self, request):
        data = request.data
        s = Study(name=data['name'], description=data['description']).save()
        return HttpResponse(json.dumps(serialize_study(s)), content_type='application/json')


class Disease(GraphObject):
    uuid = Property()
    name = Property()
    mesh_code = Property()

    def to_dict(self):
        return {'uuid': self.uuid,
                'name': self.name,
                'mesh_code': self.mesh_code}

    def __init__(self, uuid, name, mesh_code):
        self.uuid = uuid
        self.name = name
        self.mesh_code = mesh_code


class DiseaseList(APIView):
    def get(self, params):
        graph = Graph("bolt://localhost:7687", auth=("neo4j", "ElectricWizard113"))
        list_of_nodes = [a.to_dict() for a in Disease.match(graph)]
        return HttpResponse(json.dumps(list_of_nodes), content_type='application/json')

    def post(self, request):
        data = request.data
        graph = Graph("bolt://localhost:7687", auth=("neo4j", "ElectricWizard113"))
        node = Disease(name=data['name'], mesh_code=data['mesh_code'], uuid=str(uuid.uuid4()))
        graph.push(node)
        return HttpResponse(json.dumps(node.to_dict()), content_type='application/json')


class Diagnosis(GraphObject):
    __primarylabel__ = "Diagnosis"

    evaluation = Label(name="EVALUATION")

    name = Property()
    diag_disease = RelatedTo("Disease")

    def to_dict(self):
        return {'name': self.name, }


class Test(APIView):

    def get(self, params):
        print('connecting')
        graph = Graph("bolt://localhost:7687", auth=("neo4j", "ElectricWizard113"))
        print('done')

        # Create new diagnosis object
        diag = Diagnosis()
        diag.name = 'dfgdfgs'
        diag.evaluation = True
        disease = Disease.match(graph).where(mesh_code='D003424').first()
        diag.diag_disease.add(disease)
        print(disease.to_dict())
        # pp.name='testddd'
        graph.push(diag)
        aa = [a for a in Diagnosis.match(graph)]

        for a in aa:
            print(a.to_dict())
        return HttpResponse(json.dumps('kk'), content_type='application/json')


class AddEntry(APIView):
    def get(self, params, source):

        graph = Graph("bolt://localhost:7687", auth=("neo4j", "ElectricWizard113"))
        matcher = NodeMatcher(graph)
        s = matcher.match("Source", name=source).first()

        entries = graph.relationships.match((s,None), None)
        entries_for_source = []
        for e in entries:
            entries_for_source.append({'labels': list(e.end_node.labels), 'data':e.end_node})

        return HttpResponse(json.dumps(entries_for_source), content_type='application/json')


    def post(self, request):
        data = request.data
        graph = Graph("bolt://localhost:7687", auth=("neo4j", "ElectricWizard113"))
        # CREATE GRAPH NODE USING DATA IN REQUEST
        a = Node(data['schema'], data['entry_type'], 'ENTRY', uuid=str(uuid.uuid4()), **data['data']['props'])
        graph.create(a)

        # DEAL WITH RELATIONSHIP
        if '_relationship' in data['data'].keys():
            rel = data['data']['_relationship']
            ent = graph.nodes.match(rel['to_label']).where(**rel['lookup']).first()
            ab = Relationship(a, rel['rel_label'], ent, **rel['props'])
            graph.create(ab)

        # DEAL WITH PARENT
        par = data['_parent']
        ent = graph.nodes.match(par['to_label']).where(**par['lookup']).first()
        if par['direction'] == 'FROM':
            props = {}
            if 'props' in par.keys():
                props=par['props']
            ab = Relationship(ent, par['rel_label'], a, **props)
            graph.create(ab)


        return HttpResponse(json.dumps(a), content_type='application/json')
