import numpy as np
import subprocess
import ffmpeg

# TODO:
# - Docker container to test out streaming to RSTP or HTTP


class Streamer(object):
    """The Streamer class accepts an input of RGB matrices of the form
    [[R], [G], [B]] and writes them directly to an ongoing video stream

    Parameters:
        outfile: The name of the output video file
        width: The width of the images that will be passed to the stream
        height: The height of the images
        framerate: The video frame rate
        videoformat: The encoding format for the video file
            e.g., "h264", "rawvideo" etc (see ffmpeg docs for details)
    """

    def __init__(self, outfile, width=512, height=512, framerate=25, videoformat="flv"):
        """Initialises a Streamer object"""
        self.outfile = outfile
        self.width = width
        self.height = height
        self.framerate = framerate
        self.videoformat = videoformat

    def start(self):
        """Start a stream"""

        streamargs = (
            ffmpeg.input(
                "pipe:",
                format="rawvideo",
                pix_fmt="rgb24",
                s="{}x{}".format(self.width, self.height),
            )
            .output(self.outfile, framerate=self.framerate, format=self.videoformat)
            .overwrite_output()
            .compile()
        )

        # streamargs = (
        #     ffmpeg.input(
        #         "pipe:",
        #         format="rawvideo",
        #         pix_fmt="rgb24",
        #         s="{}x{}".format(self.width, self.height),
        #     )
        #     .output("http://127.0.0.1:8080", codec="copy", listen="1", f="flv")
        #     .overwrite_output()
        #     .compile()
        # )

        self.stream = subprocess.Popen(streamargs, stdin=subprocess.PIPE)

    def write_frame(self, frame):
        """Write a frame to the open stream"""
        self.stream.stdin.write(frame.astype(np.uint8).tobytes())

    def stop(self):
        """Close the stream"""
        self.stream.stdin.close()
        # self.stream.stdin.wait()

    def __repr__(self):
        return (
            f"Stream obj\nOutput file: {self.outfile}\n"
            + f"Output format: {self.videoformat}\n"
            + f"Frame rate: {self.framerate}\n"
            + f"Input image size: {self.width} {self.height}"
        )
