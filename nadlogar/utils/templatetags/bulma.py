from django import template

register = template.Library()


@register.filter(name="add_class")
def add_class(field, css_class):
    classes = field.field.widget.attrs.get("class", "")
    classes += f" {css_class}"
    field.field.widget.attrs["class"] = classes
    return field


@register.filter(name="is_danger_if_errors")
def is_danger_if_errors(field):
    if field.errors:
        return add_class(field, "is-danger")
    else:
        return field
