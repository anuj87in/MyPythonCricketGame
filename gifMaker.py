import imageio.v3 as iio

filenames = ['def1.png', 'def2.png','def3.png']
images = [ ]

for filename in filenames:
  images.append(iio.imread(filename))

iio.imwrite('backfootdef.gif', images, duration = 500, loop = 0)
