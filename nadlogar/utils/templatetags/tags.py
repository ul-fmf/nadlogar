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


@register.simple_tag
def pluralize(number, singular, dual, plural_34, plural):
    print(number)
    choice = {1: singular, 2: dual, 3: plural_34, 4: plural_34}.get(
        number % 100, plural
    )
    return f"{number} {choice}"
