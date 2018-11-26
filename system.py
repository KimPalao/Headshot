from matplotlib import pyplot as plt


def plot_pictures(rows, cols, *images):
    for i, image in enumerate(images):
        try:
            plt.subplot(rows, cols, i + 1)
            plt.imshow(image)
            plt.xticks([])
            plt.yticks([])
        except Exception as e:
            print(f'Crashed at: {i} {e}')
    plt.show()
