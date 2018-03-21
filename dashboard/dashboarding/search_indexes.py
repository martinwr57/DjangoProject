#!/usr/bin/env python
import re
import datetime
from haystack.indexes import *
from haystack import site
from dashboarding.models import Result


class ResultIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    serialnumber = CharField(model_attr='serialnumber')
    serialnumber_exact = CharField(model_attr='serialnumber', indexed=False)
    modelnumber = CharField(model_attr='modelnumber')
    testname = CharField(model_attr='testname')
    timestamp = CharField(model_attr='timestamp')

    #def get_queryset(self):
        #"""Used when the entire index for model is updated."""
        #    #return Result.objects.filter(timestamp__lte=datetime.datetime.now())
        #return Result.objects.filter(testname)"""



site.register(Result, ResultIndex)

