from django.shortcuts import render
from django.http import HttpResponse
from .models import TermsConditions
import logging


def index(_request):
    tnc = TermsConditions.objects.last()
    html_content = tnc.content if tnc and tnc.content else ""

    html_content = """
<style>
div p span {
font-size: 42px !important;
line-height: 1.7 !important;
}
div {
padding: 15px 25px !important;
}
div h1 span, div h2 span, div h3 span, div h4 span, div h5 span, div h6 span {
font-size: 72px !important;
}
div p {
margin-bottom: 0px !important;
}
div h1, div h2, div h3, div h4, div h5, div h6 {
margin-top: 45px !important;
}
</style>
<div>
%s
</div>
    """ % html_content

    return HttpResponse(html_content, content_type='text/html')
