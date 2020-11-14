from django.conf import settings
from django.core.files.storage import FileSystemStorage
from filebrowser.sites import site

# http://django-filebrowser.readthedocs.io/en/latest/settings.html
FILEBROWSER_DEFAULT_PERMISSIONS = 0o644
FILEBROWSER_EXTENSIONS = {
    "Image": [".jpg", ".jpeg", ".gif", ".png", ".tif", ".tiff"],
    "Document": [],  # ['.pdf','.doc','.rtf','.txt','.xls','.csv'],
    "Video": [],  # ['.mov','.wmv','.mpeg','.mpg','.avi','.rm'],
    "Audio": [],  # ['.mp3','.mp4','.wav','.aiff','.midi','.m4p']
}
FILEBROWSER_ADMIN_VERSIONS = ["big"]  # 'thumbnail', 'small', 'medium', 'large'

# TODO: this could be the NFS share to inspect the queue dir + processed dir
# where the atlas-web interfac drops simulation input (queue), and picks up
# failed/completed jobs after SLURM is done with it and parked the files there.
site.storage = FileSystemStorage(location=settings.STATIC_ROOT, base_url="/static/")
site.directory = "images/"
