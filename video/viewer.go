package video

import (
	"bytes"
	"fmt"
	"image"
	"time"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/canvas"
	"fyne.io/fyne/v2/widget"
	"github.com/go-gst/go-gst/gst"
	gstApp "github.com/go-gst/go-gst/gst/app"
	// streamer "github.com/metal3d/fyne-streamer"
	// "github.com/metal3d/fyne-streamer/internal/utils"
)

var _ fyne.Widget = (*Viewer)(nil)
// var _ utils.MediaControl = (*Viewer)(nil)
// var _ utils.MediaDuration = (*Viewer)(nil)
// var _ utils.MediaOpener = (*Viewer)(nil)
// var _ utils.MediaSeeker = (*Viewer)(nil)

// Viewer widget is a simple video player with no controls to display.
// This is a base widget to only read a video or that can be extended to create a video player with controls.
type Viewer struct {
	widget.BaseWidget
	appSink          *gstApp.Sink
	bus              *gst.Bus
	pipeline         *gst.Pipeline
	// onNewFrame       func(time.Duration)
	// onPreRoll        func()
	// onEOS            func()
	// onPaused         func()
	// onStartPlaying   func()
	// onTitle          func(string)
	rate             int
	imageQuality     int
	width            int
	height           int
	duration         time.Duration
	frame            *canvas.Image
	// fullscreenWindow fyne.Window
	// currentWindow    fyne.Window

	// currentWindowFinder is a function that returns the current window of the
	// widget. It is used to find the current window when the widget is in
	// fullscreen mode.
	// This is necessary because the current widget can be composed in another.
	// Use setCurrentWindowFinder to set this function.
	// currentWindowFinder func() fyne.Window

	// originalViewerWidget is the object that is really displayed in the window.
	// This is important to get it for the fullscreen mode.
	// originalViewerWidget fyne.CanvasObject
}

func NewViewer() *Viewer {
	fmt.Println("NewViewer()")

	v := &Viewer{
				frame: canvas.NewImageFromResource(nil),
				 rate: 30,
		 imageQuality: 85,
	}

	v.SetFillMode(canvas.ImageFillContain)
	v.SetScaleMode(canvas.ImageScaleFastest)

	v.BaseWidget.ExtendBaseWidget(v)

	return v
}

func (v *Viewer) CreatePipeline(pipeline string) (err error) {

	v.pipeline, err = gst.NewPipelineFromString(pipeline)

	fmt.Println(v.pipeline)

	v.createBus()

	appelement, err := v.pipeline.GetElementByName("viewersink")
	fmt.Println(err)
	fmt.Println(appelement)
	// if err != nil || appelement == nil {
	// 	fyne.LogError("Failed to find the appsink element", err)
	// 	return fmt.Errorf("Failed to find the mandatory %s element %w", streamer.AppSinkElementName, err)
	// }
	v.appSink = gstApp.SinkFromElement(appelement)
	v.appSink.SetCallbacks(&gstApp.SinkCallbacks{
	// 	EOSFunc:        v.eosFunc,
	// 	NewPrerollFunc: v.prerollFunc,
		NewSampleFunc:  v.newSampleFunc,
	})

	return err
}

func (v *Viewer) newSampleFunc(appSink *gstApp.Sink) gst.FlowReturn {
	fmt.Println("newSampleFunc()")


	sample := appSink.PullSample()
	if sample == nil {
		return gst.FlowEOS
	}

	fmt.Println(sample)

	buffer := sample.GetBuffer()
	if buffer == nil {
		return gst.FlowError
	}

	defer buffer.Unmap()

	samples := buffer.Map(gst.MapRead).AsUint8Slice()
	if samples == nil {
		return gst.FlowError
	}

	// the sample is a jpeg
	reader := bytes.NewReader(samples)
	img, _, err := image.Decode(reader)
	if err != nil {
		fmt.Println("unable to decode...")
		return gst.FlowError
	}

	// v.BaseWidget.Queue(func() {
    //      v.frame.Image = img
    //      v.frame.Refresh()
    // })

	// v.Queue(func() {
    //     v.frame.Image = img
    //     v.frame.Refresh()
    // })

	func() {
		v.frame.Image = img
		v.frame.Refresh()
	}()

	// _, pos := v.pipeline.QueryPosition(gst.FormatTime)
	// if v.onNewFrame != nil {
	// 	// get the current time of the pipeline
	// 	go v.onNewFrame(time.Duration(float64(pos)))
	// }

	// return ret
	return gst.FlowOK
}


// func (v *Viewer) getCurrentFrame(appSink *app.Sink, latest bool) (image.Image, gst.FlowReturn) {
// 	// fmt.Println("getCurrentFrame()")
// 	var sample *gst.Sample
// 	if !latest {
// 		sample = appSink.PullSample()
// 	} else {
// 		sample = appSink.GetLastSample()
// 	}
// 	if sample == nil {
// 		return nil, gst.FlowEOS
// 	}

// 	buffer := sample.GetBuffer() // Get the buffer from the sample
// 	if buffer == nil {
// 		return nil, gst.FlowError
// 	}
// 	defer buffer.Unmap()

// 	samples := buffer.Map(gst.MapRead).AsUint8Slice()
// 	if samples == nil {
// 		return nil, gst.FlowError
// 	}

// 	// the sample is a jpeg
// 	reader := bytes.NewReader(samples)
// 	img, _, err := image.Decode(reader)
// 	if err != nil {
// 		fyne.LogError("Failed to decode image: %w", err)
// 		return nil, gst.FlowError
// 	}

// 	return img, gst.FlowOK
// }


func (v *Viewer) createBus() {
	fmt.Println("createBus()")
	if v.pipeline == nil {
		return
	}

	v.bus = v.pipeline.GetPipelineBus()
	v.bus.AddWatch(func(msg *gst.Message) bool {
		fmt.Println("bus.message")
		fmt.Println(msg)
		// switch msg.Type() {
		// case gst.MessageTag:
		// 	tags := msg.ParseTags()
		// 	title, ok := tags.GetString(gst.TagTitle)
		// 	if v.onTitle != nil && ok {
		// 		v.onTitle(title)
		// 	}
		// }
		return true
	})

}






















// Clear the pipeline. Use it with caution, it may cause some issues.
func (v *Viewer) Clear() error {
	fmt.Println("Clear()")
	// if v.pipeline == nil {
	// 	return streamer.ErrNoPipeline
	// }
	// defer v.resync()
	// v.pipeline.Clear()
	return nil
}

// CreateRenderer creates a renderer for the video widget.
//
// Implements: fyne.Widget
func (v *Viewer) CreateRenderer() fyne.WidgetRenderer {
	fmt.Println("CreateRenderer()")
	return widget.NewSimpleRenderer(v.frame)
}

// // ExtendBaseWidget overrides the ExtendBaseWidget method of the BaseWidget.
// // It is used to set the currentWindowFinder function and the object that
// // is really displayed in the window (to ensure that fullscreen
// // will use the right object).
// func (v *Viewer) ExtendBaseWidget(w fyne.Widget) {
// 	fmt.Println("ExtendBaseWidget()")
// 	v.BaseWidget.ExtendBaseWidget(w)
// 	// v.setCurrentWindowFinder(w)
// 	// v.originalViewerWidget = w
// }

// Frame returns the canvas.Image that is used to display the video.
func (v *Viewer) Frame() *canvas.Image {
	fmt.Println("Frame()")
	return v.frame
}

// SetFillMode sets the fill mode of the image.
func (v *Viewer) SetFillMode(mode canvas.ImageFill) {
	fmt.Println("SetFillMode()")
	// v.frame.FillMode = mode
}

// SetScaleMode sets the scale mode of the image. It's not recommended to use other
// mode than canvas.ImageScaleFastest because it can be very slow.
func (v *Viewer) SetScaleMode(mode canvas.ImageScale) {
	fmt.Println("SetScaleMode()")
	// v.frame.ScaleMode = mode
}

// Play the stream if the pipeline is not nil.
func (v *Viewer) Play() error {
	fmt.Println("Play()")
	if v.pipeline == nil {
		// return streamer.ErrNoPipeline
	}
	// defer func() {
	// 	if v.onStartPlaying != nil {
	// 		v.onStartPlaying()
	// 	}
	// }()

	return v.pipeline.SetState(gst.StatePlaying)
}

// func (v *Viewer) SetState(state gst.State) error {
// 	fmt.Println("SetState()")
// 	// defer v.resync()
// 	return v.setState(state)
// }
