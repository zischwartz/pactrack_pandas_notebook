# pactrack_pandas_notebook

Jupyter notebook to parse [bulk FEC data](https://www.fec.gov/data/advanced/?tab=bulk-data).

The visualization uses output from `process.ipynb` but there's a more basic example in `explore.ipynb`. Both rely on a method in `download_data.py`

To easily run this locally, make sure you have docker installed and from this directory run:

```bash
docker run -it --rm -v $PWD:/home/jovyan/work --rm -p 8888:8888 jupyter/datascience-notebook start-notebook.sh --NotebookApp.token=''
```

If you have `yarn` you can also just run `yarn jupyter`.

Next navigate to a notebook on http://localhost:8888, like this [`explore.ipynb`](http://localhost:8888/notebooks/work/explore.ipynb)

**Warning**: _This isn't secure, in the real world you should not run a server with a blank token._
