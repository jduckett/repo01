package main

import (
	"fmt"
	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/app"
	"gst-fyne/video"
	"github.com/go-gst/go-glib/glib"
	"github.com/go-gst/go-gst/gst"
)

func main() {


// filesrc location=/path/to/video.mp4

	// pipeline := `
    // videotestsrc name={{ .InputElementName }} !
    // videoconvert n-threads=4 ! # convert to something usable
    // videorate name={{ .VideoRateElementName }} max-rate=30 !
    // jpegenc name={{ .ImageEncoderElementName }} quality=80 !
    // appsink name={{ .AppSinkElementName }} drop=true max-lateness=33333 sync=true
    // `

// filesrc location=/path/to/video.mp4 ! decodebin ! videoconvert ! autovideosink

	// pipeline := `
    // filesrc location=/alldata/test.mov ! decodebin ! videoconvert !
    // jpegenc name={{ .ImageEncoderElementName }} quality=80 !
    // appsink name={{ .AppSinkElementName }} drop=true max-lateness=33333 sync=true
    // `

	pipeline := `
    souphttpsrc location=http://10.229.224.242/test01.mkv ! decodebin ! videoconvert !
    jpegenc name=imageencoder quality=80 !
    appsink name=viewersink drop=true max-lateness=33333 sync=true
    `
    // fmt.Println(pipeline)

	gst.Init(nil)

	mainLoop := glib.NewMainLoop(glib.MainContextDefault(), false)

	defer mainLoop.Quit()

	go mainLoop.Run()

	a := app.New()

	fmt.Println(pipeline)
	w := a.NewWindow("Video 01")

	viewer := video.NewViewer()

	viewer.CreatePipeline(pipeline)

	viewer.Play()

	w.Resize(fyne.NewSize(640, 480))
	w.SetContent(viewer)


	w.ShowAndRun()

}
