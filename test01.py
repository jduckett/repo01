#!/usr/bin/env python3

import uno
from com.sun.star.beans import PropertyValue
from com.sun.star.text.ControlCharacter import PARAGRAPH_BREAK

def create_impress_document():
    # Initialize the UNO components
    localContext = uno.getComponentContext()
    resolver = localContext.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", localContext)
    context = resolver.resolve("uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")

    # Access the Desktop to create a new document
    desktop = context.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", context)
    document = desktop.loadComponentFromURL("private:factory/simpress", "_blank", 0, ())

    # Create a few slides
    slide_count = 3
    for i in range(slide_count):
        slide = document.createInstance("com.sun.star.drawing.Page")
        document.getDrawPages().insertByIndex(i, slide)
        add_text_to_slide(slide, f"Slide {i + 1}", f"This is the text for slide {i + 1}")

    # Save the document
    save_properties = (
        PropertyValue("FilterName", 0, "impress8", 0),
        PropertyValue("Overwrite", 0, True, 0)
    )
    document.storeAsURL("file:///path/to/your/presentation.odp", save_properties)

def add_text_to_slide(slide, title, text):
    # Create a text shape and set its properties
    text_shape = slide.createInstance("com.sun.star.drawing.TextShape")
    text_shape.setSize(20000, 10000)
    text_shape.setPosition(5000, 5000)
    text_shape.setString(title)

    # Add the text shape to the slide
    slide.add(text_shape)

    # Append the additional text
    text_cursor = text_shape.getText().createTextCursor()
    text_cursor.gotoEnd(False)
    text_shape.getText().insertControlCharacter(text_cursor, PARAGRAPH_BREAK, False)
    text_cursor.gotoEnd(False)
    text_shape.getText().insertString(text_cursor, text, False)

if __name__ == "__main__":
    create_impress_document()
