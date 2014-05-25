from audit.models import Event


ADD_TAG_TO_DOCUMENT = Event.objects.get(id=1)

REMOVE_TAG_TO_DOCUMENT = Event.objects.get(id=2)

FILE_ATTACHED = Event.objects.get(id=3)

FILE_DETACHED = Event.objects.get(id=4)

CLASSIFY_DOCUMENT = Event.objects.get(id=5)

REMOVE_CLASSIFY_DOCUMENT = Event.objects.get(id=6)

DOCUMENT_SHARED = Event.objects.get(id=7)

DOCUMENT_UNSHARED = Event.objects.get(id=8)