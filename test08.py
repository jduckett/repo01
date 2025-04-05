#!/usr/bin/env python3

import uno
from com.sun.star.beans import PropertyValue
from com.sun.star.lang import XComponent
from com.sun.star.uno import Exception as UnoException

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

        # Save the document to the specified path
        save_property = PropertyValue()
        save_property.Name = "FilterName"
        save_property.Value = "impress8"  # LibreOffice Impress format
        impress_doc.storeToURL(uno.systemPathToFileUrl(save_path), (save_property,))

        # Close the document
        impress_doc.dispose()
        print("Document created and saved successfully.")

    except UnoException as e:
        print(f"UnoException: {e.Message}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    save_path = "/alldata/document.odp"
    create_impress_document(save_path)
