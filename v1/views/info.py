from functools import reduce

#import spacy
from pypdf import PdfReader
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.status import HTTP_404_NOT_FOUND

from core.models.userinfo import UserInfo


class FileViewSet(CreateModelMixin, GenericViewSet):
    def create(self, request, *args, **kwargs):
        import spacy

        email = request.data.get('email', None)
        file = request.FILES.get('file', None)
        reader = PdfReader(file)
        text = reduce(lambda a, b: a + b.extract_text(), reader.pages, '')
        tokens = spacy.load('en_core_web_sm')(text)
        nouns = set([str(t) for t in tokens if t.pos_ == 'NOUN'])
        verbs = set([str(t) for t in tokens if t.pos_ == 'VERB'])
        info = UserInfo.objects(email=email).first()
        data = dict(email=email, nouns=nouns, verbs=verbs)
        if info:
            info.nouns = list(nouns)
            info.verbs = list(verbs)
            info.save()
        else:
            UserInfo(**data).save()
        return Response(data)

    @action(detail=False, methods=['post'])
    def search(self, request, *args, **kwargs):
        email = request.data.get('email', '')
        info = UserInfo.objects(email=email).first()
        if info:
            data = dict(info.to_mongo())
            data['id'] = str(data.pop('_id'))
            return Response(data)
        return Response({}, status=HTTP_404_NOT_FOUND)
