#!/usr/bin/env python3

import uno

from com.sun.star.beans import PropertyValue
from com.sun.star.presentation import XPresentationSupplier

def connect_to_libreoffice():
    local_context = uno.getComponentContext()
    resolver = local_context.ServiceManager.createInstanceWithContext(
        "com.sun.star.bridge.UnoUrlResolver", local_context)
    context = resolver.resolve(
        "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
    return context

def load_presentation(context, file_url):
    service_manager = context.ServiceManager
    desktop = service_manager.createInstanceWithContext("com.sun.star.frame.Desktop", context)
    file_props = [PropertyValue(Name="Hidden", Value=True)]
    return desktop.loadComponentFromURL(file_url, "_blank", 0, file_props)

def duplicate_slide(presentation, slide_index):
    draw_pages = presentation.getDrawPages()
    slide = draw_pages.getByIndex(slide_index)
    new_slide = draw_pages.insertNewByIndex(slide_index + 1)
    new_slide.setPropertyValues(slide.getPropertySetInfo().getPropertiesAsPropertyValues())
    # Copy content from original slide to new slide
    shapes = slide.getShapes()
    for i in range(shapes.getCount()):
        new_slide.add(shapes.getByIndex(i).createCopy())

def main():

    file_path = "file:///hbc/docs/services/sunday/morning/template-sermon-02.odp"
    context = connect_to_libreoffice()
    presentation = load_presentation(context, file_path)
    duplicate_slide(presentation, 1)  # Duplicate the first slide

if __name__ == "__main__":
    main()
