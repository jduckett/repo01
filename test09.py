#!/usr/bin/env python3

import uno
from com.sun.star.beans import PropertyValue
from com.sun.star.uno import Exception as UnoException
from com.sun.star.lang import XComponent

def create_impress_document(save_path):
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
        draw_pages.insertNewByIndex(0)

        # Save the document to the specified path
        save_properties = PropertyValue()
        save_properties.Name = "FilterName"
        save_properties.Value = "impress8"  # LibreOffice Impress format
        save_url = uno.systemPathToFileUrl(save_path)
        impress_doc.storeToURL(save_url, (save_properties,))

        # Close the document
        impress_doc.dispose()
        print("Document created, blank slide added, and saved successfully.")

    except UnoException as e:
        print(f"UnoException: {e.Message}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    save_path = "/hbc/document.odp"
    create_impress_document(save_path)