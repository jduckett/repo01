#!/usr/bin/env python3

import uno
from com.sun.star.beans import PropertyValue
from com.sun.star.uno import Exception as UnoException
from com.sun.star.awt import Point, Size

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
        # blank_slide.add(image_shape)

        # Send the image to the background by setting ZOrder to 0
        # image_shape.setPropertyValue("ZOrder", 0)

        # Add a textbox named txtContent
        textbox = impress_doc.createInstance("com.sun.star.drawing.TextShape")
        textbox.Name = "txtContent"
        textbox.setString("Your text here")
        textbox.Position = Point(0, 0)
        textbox.Size = Size(28000, 21000)  # Make the textbox take up the entire canvas area
        textbox.CharFontName = "DejaVu Sans"
        textbox.CharHeight = 34
        blank_slide.add(textbox)

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
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    save_path = "/hbc/document.odp"
    image_path = "/hbc/media/images/hbc/logo/logo-base-1920x1080.png"
    create_impress_document(save_path, image_path)
