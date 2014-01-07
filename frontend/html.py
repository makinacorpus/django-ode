def modal_link(target_prefix, url, text):
    return (u'<a data-toggle="modal" '
            u'data-target="#{}-modal" '
            u'href="{}">{}</a>'
            .format(target_prefix, url, text))


def link(url, text):
    return u'<a href="{}">{}</a>'.format(url, text)


def checkbox(css_class, data_id):
    return ('<input type="checkbox" class="{}"'
            ' data-id="{}">').format(css_class, data_id)
