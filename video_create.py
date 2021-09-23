import av
import numpy as np

# frames[frameIdx, rowIdx, ColIdx]
def generate_video(frames, fname="test.mp4", fps=30):

	container = av.open(fname, mode='w')

	stream = container.add_stream('mpeg4', rate=fps)
	stream.width = frames.shape[2]
	stream.height = frames.shape[1]
	stream.pix_fmt = 'yuv420p'

	for frame_i in range(frames.shape[0]):

		frame = av.VideoFrame.from_ndarray(frames[frame_i], format='rgb24')
		for packet in stream.encode(frame):
			container.mux(packet)

	# Flush stream
	for packet in stream.encode():
		container.mux(packet)

	# Close the file
	container.close()

def generate_tiled_fake_data(N=64, TILE_SIZE=8, FRAMES=30*10):
	img = np.random.random((FRAMES, N, N, 1)) # get random data
	img = np.round(255 * img).astype(np.uint8) # convert to uint8
	img = np.clip(img, 0, 255) # clip
	img = np.repeat(img, TILE_SIZE, axis=1) # tile
	img = np.repeat(img, TILE_SIZE, axis=2) # tile
	img = np.repeat(img, 3, axis=3) # color channels

	return img

if __name__ == "__main__":
	generate_video(generate_tiled_fake_data())