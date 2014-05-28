from django.dispatch import Signal

post_attach_file = Signal(providing_args=["file", "document", "user"])

post_detach_file = Signal(providing_args=["file", "document", "user"])

post_add_tag_document = Signal(providing_args=["tag", "document", "user"])

post_remove_tag_document = Signal(providing_args=["tag", "document", "user"])

post_classify_document = Signal(providing_args=["document", "user"])

post_remove_classify_document = Signal(providing_args=["document", "user"])

post_document_shared_to_user = Signal(providing_args=["shared_from", "shared_to", "document", "permission"])

post_document_unshared_to_user = Signal(providing_args=["shared_from", "shared_to", "document", "permission"])

post_document_shared_to_group = Signal(providing_args=["shared_from", "shared_to", "document", "permission"])

post_document_unshared_to_group = Signal(providing_args=["shared_from", "shared_to", "document", "permission"])

post_document_shared_to_all = Signal(providing_args=["shared_from", "document", "permission"])

post_document_unshared_to_all = Signal(providing_args=["shared_from", "document", "permission"])

post_download_attachment = Signal(providing_args=["file", "document", "user"])


