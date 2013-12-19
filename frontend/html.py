def modal_link(target_prefix, url, text):
    return (u'<a data-toggle="modal" '
            u'data-target="#{}-modal" '
            u'href="{}">{}</a>'
            .format(target_prefix, url, text))
