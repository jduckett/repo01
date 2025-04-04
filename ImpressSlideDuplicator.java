import com.sun.star.beans.PropertyValue;
import com.sun.star.comp.helper.Bootstrap;
import com.sun.star.frame.XComponentLoader;
import com.sun.star.lang.XComponent;
import com.sun.star.uno.UnoRuntime;
import com.sun.star.uno.XComponentContext;
import com.sun.star.drawing.XDrawPages;
import com.sun.star.drawing.XDrawPage;
import com.sun.star.drawing.XDrawPageDuplicator;
import com.sun.star.text.XText;
import com.sun.star.beans.XPropertySet;

public class ImpressSlideDuplicator {
    public static void main(String[] args) {
        try {
            // Bootstrap the UNO context
            XComponentContext xContext = Bootstrap.bootstrap();
            if (xContext == null) {
                throw new Exception("Could not bootstrap UNO context");
            }

            // Get the desktop service to load documents
            XComponentLoader xLoader = UnoRuntime.queryInterface(
                XComponentLoader.class,
                xContext.getServiceManager().createInstanceWithContext("com.sun.star.frame.Desktop", xContext)
            );

            // Open the Impress presentation
            String filePath = "/hbc/docs/services/sunday/morning/template-sermon-02.odp"; // Replace with your file path
            String fileUrl = "file://" + filePath;
            PropertyVPropertyValue[] loadProps = new PropertyValue[] {
                new PropertyValue("Hidden", 0, true, 0) // Open in background
            };
            XComponent xDoc = xLoader.loadComponentFromURL(fileUrl, "_blank", 0, loadProps);

            // Get the slides (XDrawPages)
            XDrawPages xSlides = UnoRuntime.queryInterface(XDrawPages.class, xDoc);
            int slideIndex = 1; // Index of slide to duplicate (0-based)

            // Get the source slide
            XDrawPage sourceSlide = UnoRuntime.queryInterface(XDrawPage.class, xSlides.getByIndex(slideIndex));

            // Duplicate the slide
            XDrawPageDuplicator xDuplicator = UnoRuntime.queryInterface(XDrawPageDuplicator.class, xSlides);
            XDrawPage newSlide = xDuplicator.duplicate(sourceSlide);
            // Move the new slide to the position after the original
            xSlides.remove(newSlide);
            xSlides.insertByIndex(newSlide, slideIndex + 1);

            // Set text in an existing text box
            String textBoxName = "txtContent"; // Name of the text box (set in Impress)
            String newText = "This is the new text content!";
            for (int i = 0; i < newSlide.getCount(); i++) {
                Object shape = newSlide.getByIndex(i);
                XPropertySet xShapeProps = UnoRuntime.queryInterface(XPropertySet.class, shape);
                if (xShapeProps != null && textBoxName.equals(xShapeProps.getPropertyValue("Name"))) {
                    XText xText = UnoRuntime.queryInterface(XText.class, shape);
                    if (xText != null) {
                        xText.setString(newText);
                        break;
                    }
                }
            }

            // Save the modified document
            UnoRuntime.queryInterface(com.sun.star.util.XStorable.class, xDoc).store();

            System.out.println("Slide duplicated and text updated successfully!");

            // Clean up
            xDoc.dispose();
        } catch (Exception e) {
            System.err.println("Error: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
