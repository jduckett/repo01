#!/usr/bin/env python3

# from . common import get_connection
import common

from duck.libs.apps.arguments import ArgumentParser, Arguments
from duck.libs.apps.core import strings, ts, files, directory, AppInfo

import duck.libs.apps.config.default_arguments
import json
import os

import uno
import traceback
from com.sun.star.beans import PropertyValue, UnknownPropertyException
from com.sun.star.uno import Exception as UnoException
from com.sun.star.awt import Point, Size
from com.sun.star.awt.FontWeight import BOLD

from com.sun.star.drawing.TextHorizontalAdjust import CENTER as HORZ_CENTER
from com.sun.star.drawing.TextVerticalAdjust import CENTER as VERT_CENTER


def add_blank_slide(document, name="txtContent", text="content"):

	# Add a blank slide
	draw_pages = document.getDrawPages()
	blank_slide = draw_pages.insertNewByIndex(0)

	# Add an image to the blank slide
	image_shape = document.createInstance("com.sun.star.drawing.GraphicObjectShape")
	image_shape.GraphicURL = uno.systemPathToFileUrl(file_spec_image)
	image_shape.Position = Point(0, 0)
	image_shape.Size = Size(28000, 21000)  # Assuming the slide size is 28cm x 21cm

	blank_slide.add(image_shape)

	# Send the image to the background by setting ZOrder to 0
	image_shape.setPropertyValue("ZOrder", 0)

	# Add a textbox named txtContent
	textbox = document.createInstance("com.sun.star.drawing.TextShape")
	textbox.Name = name
	textbox.Position = Point(0, 0)
	# textbox.Size = Size(28000, 21000)  # Make the textbox take up the entire canvas area
	textbox.Size = Size(25000, 21000)  # Make the textbox take up the entire canvas area

	blank_slide.add(textbox)

	text_range = textbox.getText()
	text_range.setString(text)

	text_range.setPropertyValue("TextHorizontalAdjust", HORZ_CENTER)
	text_range.setPropertyValue("TextVerticalAdjust", VERT_CENTER)

	props = text_range.PropertySetInfo.getProperties()

	# Set font and size for the text box
	cursor = text_range.createTextCursor()

	try:
		cursor.setPropertyValue("CharFontName", "DejaVu Sans")
		cursor.setPropertyValue("CharHeight", 34)
		cursor.setPropertyValue("CharWeight", BOLD)
	except UnknownPropertyException as e:
		print(f"Failed to set CharFontName: {e.Message}")

	return blank_slide


args_parser = ArgumentParser(prog="HBC Hymn Generator", description="Generates a hymn as a libreoffice impress document.")

args_parser.o.include("prefix", "version")

args_parser.p.create("hymn_number",
	"hymn_number",
	help="The Number of the hymn you would like to generate.",
	type=int,
	default=0)

args_parser.p.create("image",
	"image",
	default="/hbc/media/images/defaults/beige-coffee-stain.jpg",
	help="Full path to a background image.",
	nargs="?",
	)

args_parser.p.include("hymn_number", "image")

args = args_parser.parse()

dir_base = "/hbc/docs/hymns/json"
dir_current = os.getcwd()

if args.hymn_number:

	file_spec_image = args.image

	file_name_source = ""
	file_spec_source = ""

	hymn_number = f"{args.hymn_number:03d}"

	prefix = f"{hymn_number}-"

	for file_name in os.listdir(dir_base):

		if file_name.startswith(prefix):

			file_name_source = file_name
			file_spec_source = os.path.join(dir_base, file_name)

			break


	if not os.path.exists(file_spec_image):

		print(f"IMAGE NOT FOUND: {file_spec_image}")

	if os.path.exists(file_spec_source) and os.path.exists(file_spec_image):

		file_name_target = file_name_source.replace(".json", ".odp")
		if args.prefix:
			file_name_target = f"{args.prefix}-{file_name_target}"


		file_spec_target = os.path.join(dir_current, file_name_target)

		json_content = ""

		with open(file_spec_source) as f:

			json_content = json.load(f)


		# print(json.dumps(json_content, indent=4))
		print(file_spec_source)
		print(dir_current)
		print(file_name_target)
		print(file_spec_target)

		try:

			desktop = common.get_connection()

			# Create a new empty Impress document
			document = desktop.loadComponentFromURL(
			    "private:factory/simpress", "_blank", 0, ()
			)

			draw_pages = document.getDrawPages()

			content = json_content.get("title", "Unknown Title")

			for author in json_content.get("authors", []):
				content += f"\n{author}"

			add_blank_slide(document,
				name="txtTitle",
				text=content)










			# this removes the first blank slide that is created by default.
			draw_pages.remove(draw_pages.getByIndex(0))

			# Save the document to the specified path
			save_properties = PropertyValue()
			save_properties.Name = "FilterName"
			save_properties.Value = "impress8"  # LibreOffice Impress format
			save_url = uno.systemPathToFileUrl(file_spec_target)
			document.storeToURL(save_url, (save_properties,))

		except UnoException as e:
			print(f"UnoException: {e.Message}")
			traceback.print_exc()

		except Exception as e:
			print(f"An error occurred: {e}")
			traceback.print_exc()

		finally:
			# close the document
			if 'document' in locals():
				document.dispose()




















