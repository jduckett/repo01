#!/usr/bin/env python3

import uno
import traceback
from com.sun.star.beans import PropertyValue
from com.sun.star.text import XText

def connect_to_libreoffice():
    """Establish a connection to a running LibreOffice instance."""
    local_context = uno.getComponentContext()
    resolver = local_context.ServiceManager.createInstanceWithContext(
        "com.sun.star.bridge.UnoUrlResolver", local_context)
    context = resolver.resolve("uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
    desktop = context.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", context)
    return desktop

def open_presentation(desktop, file_path):
    """Open an existing Impress presentation."""
    url = uno.systemPathToFileUrl(file_path)
    properties = (PropertyValue("Hidden", 0, True, 0),)  # Open in background
    document = desktop.loadComponentFromURL(url, "_blank", 0, properties)
    return document

def duplicate_slide(document, slide_index):
    """Duplicate a slide at the given index."""
    slides = document.getDrawPages()
    if slide_index < slides.getCount():
        # Get the source slide
        source_slide = slides.getByIndex(slide_index)
        # Create a new slide
        new_slide = slides.insertNewByIndex(slide_index + 1)
        # Copy contents from the source slide to the new slide
        for i in range(source_slide.getCount()):
            shape = source_slide.getByIndex(i)
            new_shape = shape.createShape(shape.getPosition(), shape.getSize())
            new_slide.add(new_shape)
        return new_slide
    else:
        raise Exception("Slide index out of range")

def set_text_box_content(slide, text_box_name, new_text):
    """Set the text content of an existing text box by its name."""
    for i in range(slide.getCount()):
        shape = slide.getByIndex(i)
        if shape.supportsService("com.sun.star.drawing.TextShape") and shape.getName() == text_box_name:
            text = shape.getText()
            text.setString(new_text)
            return True
    raise Exception(f"Text box '{text_box_name}' not found on slide")

def main():
    # Configuration
    file_path = "/hbc/docs/services/sunday/morning/template-sermon-02.odp"
    slide_index_to_duplicate = 1
    text_box_name = "txtContent"
    new_text_content = "This is the new text content!"

    try:
        # Connect to LibreOffice
        desktop = connect_to_libreoffice()

        # Open the presentation
        document = open_presentation(desktop, file_path)

        # Duplicate the slide
        new_slide = duplicate_slide(document, slide_index_to_duplicate)

        # Set text box content on the duplicated slide
        set_text_box_content(new_slide, text_box_name, new_text_content)

        # Save the modified document (optional)
        document.store()

        print("Slide duplicated and text updated successfully!")

    except Exception as e:
        print(f"Error: {str(e)}")
        traceback.print_exc()

    finally:
        # Close the document
        if 'document' in locals():
            document.dispose()

if __name__ == "__main__":
    main()