We introduce a method to automatically align vocal melodies in consumer available music to the
corresponding lyrics. We take a song as an input and extract the vocal using robust principle component
analysis (RPCA). The extracted vocal is denoised by using a graph cut algorithm to create
a binary mask for noise and vocal components. The denoised vocal is placed into an HMM acoustic
model for phone recognition, and this is followed by a forced alignment.
