#!/usr/bin/env python3

import uno
import traceback
from com.sun.star.beans import PropertyValue, UnknownPropertyException
from com.sun.star.uno import Exception as UnoException
from com.sun.star.awt import Point, Size
from com.sun.star.awt.FontWeight import BOLD

def delete_slide(impress_doc, slide_index):
    try:
        draw_pages = impress_doc.getDrawPages()
        if slide_index < draw_pages.getCount():
            draw_pages.remove(draw_pages.getByIndex(slide_index))
            print(f"Slide {slide_index} deleted successfully.")
        else:
            print(f"Slide {slide_index} does not exist.")
    except UnoException as e:
        print(f"UnoException while deleting slide: {e.Message}")
        traceback.print_exc()
    except Exception as e:
        print(f"An error occurred while deleting slide: {e}")
        traceback.print_exc()

def create_impress_document(save_path, image_path):
    try:
        # Get the local context
        local_ctx = uno.getComponentContext()

        # Create the UnoUrlResolver
        resolver = local_ctx.ServiceManager.createInstanceWithContext(
            "com.sun.star.bridge.UnoUrlResolver", local_ctx
        )

        # Connect to the running office
        ctx = resolver.resolve("uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")

        # Get the central desktop object
        desktop = ctx.ServiceManager.createInstanceWithContext(
            "com.sun.star.frame.Desktop", ctx
        )

        # Create a new empty Impress document
        impress_doc = desktop.loadComponentFromURL(
            "private:factory/simpress", "_blank", 0, ()
        )

        # Add a blank slide
        draw_pages = impress_doc.getDrawPages()
        blank_slide = draw_pages.insertNewByIndex(0)

        # Add an image to the blank slide
        image_shape = impress_doc.createInstance("com.sun.star.drawing.GraphicObjectShape")
        image_shape.GraphicURL = uno.systemPathToFileUrl(image_path)
        image_shape.Position = Point(0, 0)
        image_shape.Size = Size(28000, 21000)  # Assuming the slide size is 28cm x 21cm
        blank_slide.add(image_shape)

        # Send the image to the background by setting ZOrder to 0
        image_shape.setPropertyValue("ZOrder", 0)

        # Add a textbox named txtContent
        textbox = impress_doc.createInstance("com.sun.star.drawing.TextShape")
        textbox.Name = "txtContent"
        # Center the textbox horizontally and vertically
        textbox.Position = Point(14000 - 12500, 10500 - 10500)  # Centering the textbox on the slide
        textbox.Size = Size(25000, 21000)  # Adjust size as needed

        blank_slide.add(textbox)

        text_range = textbox.getText()
        text_range.setString("Your text here")

        # Set font and size for the text box
        cursor = text_range.createTextCursor()
        properties = cursor.PropertySetInfo.getProperties()
        try:
            cursor.setPropertyValue("CharFontName", "DejaVu Sans")
        except UnknownPropertyException as e:
            print(f"Failed to set CharFontName: {e.Message}")
        try:
            cursor.setPropertyValue("CharHeight", 34)
        except UnknownPropertyException as e:
            print(f"Failed to set CharHeight: {e.Message}")

        try:
            cursor.setPropertyValue("CharWeight", BOLD)
        except UnknownPropertyException as e:
            print(f"Failed to set CharWeight: {e.Message}")

        # Center the text within the textbox
        text_range.setPropertyValue("ParaAdjust", 1)  # 1 corresponds to CENTER in com.sun.star.style.ParagraphAdjust
        cursor.setPropertyValue("ParaVertAlign", 2)  # 2 corresponds to CENTER in com.sun.star.style.ParagraphVertAlign

        # Save the document to the specified path
        save_properties = PropertyValue()
        save_properties.Name = "FilterName"
        save_properties.Value = "impress8"  # LibreOffice Impress format
        save_url = uno.systemPathToFileUrl(save_path)
        impress_doc.storeToURL(save_url, (save_properties,))

        # Close the document
        impress_doc.dispose()
        print("Document created, image added to background, textbox added, and saved successfully.")

    except UnoException as e:
        print(f"UnoException: {e.Message}")
        traceback.print_exc()
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    save_path = "/hbc/document.odp"
    image_path = "/hbc/media/images/hbc/logo/logo-base-1920x1080.png"
    create_impress_document(save_path, image_path)
    # delete_slide(impress_doc, 0)