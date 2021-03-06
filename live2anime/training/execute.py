import tensorflow as tf
from live2anime.models.discriminator import define_discriminator
from live2anime.models.generator import define_generator
from live2anime.models.gan import define_gan
from live2anime.training.train import train
from live2anime.io.load import load_real_samples

#config for using gpu on tensorflow...https://github.com/tensorflow/tensorflow/issues/24496
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
	try:
		for gpu in gpus:
			tf.config.experimental.set_memory_growth(gpu, True)
	except RuntimeError as e:
		print(e)

# load image data
dataset = load_real_samples('data/npz_files/pictures.npz')
print('Loaded', dataset[0].shape, dataset[1].shape)
# define input shape based on the loaded dataset
image_shape = dataset[0].shape[1:]
# define the models
d_model = define_discriminator(image_shape)
g_model = define_generator(image_shape)
# define the composite model
gan_model = define_gan(g_model, d_model, image_shape)
# train model
train(d_model, g_model, gan_model, dataset, 'results/', 'data/models/')
