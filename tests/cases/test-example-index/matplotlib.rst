Matplotlib plot
===============

.. example:: Matplotlib plot
   :tags: images

   .. plot::

      import matplotlib
      import matplotlib.pyplot as plt
      import numpy as np

      # Data for plotting
      x = [1., 2., 3.]
      y = [2., 4., 9.]

      fig, ax = plt.subplots()
      ax.plot(x, y)

      ax.set(xlabel='x', ylabel='y',
             title='Matplotlib plot')
      ax.grid()
