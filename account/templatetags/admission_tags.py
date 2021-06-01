from django import template

register = template.Library()

@register.filter()
def to_string(value):
    return value

@register.inclusion_tag('account/includes/passing_year_options.html')
def generateCourseYearList(start_year, end_year, form, selectedYear):
        yearList = list(range(int(start_year), int(end_year)))
        return {'yearList' : yearList, 'form' : form, 'selectedYear' : selectedYear}

@register.inclusion_tag('account/includes/display_validation_error.html')
def displayValidationError(errors):
    return {'errors' : errors}

@register.simple_tag
def compareValuesAndReturnSelected(value1, value2, is_bound):
    if is_bound:
        if str(value1) == str(value2):
            return "selected"

@register.simple_tag
def getOldFormValue(is_bound, value):
    if is_bound and value !="":
        return value
    else:
        return ""
        