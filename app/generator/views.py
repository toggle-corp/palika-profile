from io import BytesIO
from zipfile import ZipFile

from django.http import FileResponse, HttpResponse, Http404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Export


@login_required()
def list(request):
    return render(request, 'generator/list.html')


@login_required()
def add(request):
    return render(request, 'generator/add.html')


def get_latest_palika_pdf(request, palika_code):
    export = Export.objects.filter(
        palika_code=palika_code,
    ).order_by('-pk').first()
    if export:
        response = FileResponse(export.file)
        return response
    raise Http404('Document not found for {}'.format(palika_code))


def download_export_as_zip(request):
    palikas_code = [
        int(x) for x in request.GET.get('exports_id', '').split(',')
    ]
    exports = Export.objects.filter(pk__in=palikas_code)
    if exports.count():
        mem = BytesIO()
        zip = ZipFile(mem, 'a')
        for i, export in enumerate(exports.all()):
            zip.writestr(
                export.title or 'Document-{}.pdf'.format(i),
                export.file.read(),
            )
        for file in zip.filelist:
            file.create_system = 0
        zip.close()
        response = HttpResponse(content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=download.zip'
        mem.seek(0)
        response.write(mem.read())
        return response
    raise Http404(
        'Document not found for palikas_code={}'.format(palikas_code),
    )
