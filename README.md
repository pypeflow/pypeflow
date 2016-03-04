Pypeflow
========

A static site generator for python developers

The idea behind this project is that everything is a plugin, so, that is really easy for developers do anything that runs away from a blog site, using Python.

You create a .py file where you specify your build process, basically, the paths, datas, and what plugins to use.

Pypeflow is very simple:

1. Read all files in source_path creating a big dict with all files
2. Call the plugins, which manipulates the dict in any way they need
3. Write all files in build_path


Installation
------------
Use pip:

```
pip install pypeflow
```

Install the plugins needed for your build, see a list of disponible plugins bellow


A complete example
------------------

```python
pypeflow = Pypeflow(
    source_path=os.path.join(BASE_DIR, 'content'),
    build_path=os.path.join(BASE_DIR, 'output'),
    templates_path=os.path.join(BASE_DIR, 'templates'),
    collections={  # Collections are for group files by pattern, so you can pass same data for multiple files
        'recipes': {
            'pattern': r'^/recipes/',
            'permalink': '/recipes/:category/:title/',  # used by permalinks plugin
            'sort': 'date',
            'reverse': True,
        },
    },
    plugins=(
        FrontmatterPlugin(filter_pattern=r'\.md$'),  # extract frontmatter data from file
        MarkdownPlugin(),  # convert markdown to html
        PaginatePlugin(  # create pagination pages (/recipes/, /recipes/2/, ...)
            filter_collections=['recipes'],
            per_page=10,
            template='recipes.html',
            permalink_first='/recipes/',
            permalink='/recipes/:page/',
            sort='date',
            sort_reverse=True,
        ),
        PermalinksPlugin(filter_collections=['recipes']),  # generate url for pages
        ExcerptsPlugin(size=160),  # generates excerpts from file contents
        FeedPlugin(filter_collections=['recipes']),  # creates a RSS xml file
        Jinja2Plugin(), # render template
    )
)
pypeflow.build()  # write files on build_path
pypeflow.serve()  # starts a dev server using build_path as root
```

Plugins
-------

Follow the link of the plugin for details on dependencies and instructions to use them.

- [Excerpts](https://github.com/pypeflow/pypeflow-excerpts) Create excerpts property from text
- [Feed](https://github.com/pypeflow/pypeflow-feed) Create RSS feed
- [Frontmatter](https://github.com/pypeflow/pypeflow-frontmatter) Read frontmatter data and update files
- [Jinja2](https://github.com/pypeflow/pypeflow-jinja2) Template engine used to render html files
- [Less](https://github.com/pypeflow/pypeflow-less) Compile less to css
- [Markdown](https://github.com/pypeflow/pypeflow-markdown) Compile markdown to html
- [Paginate](https://github.com/pypeflow/pypeflow-paginate) Creates pagination pages
- [Permalinks](https://github.com/pypeflow/pypeflow-permalinks) Creates url property
- [Thumbnail](https://github.com/pypeflow/pypeflow-thumbnail) Creates thumbnails for images


Custom Plugins
--------------

It is very easy to do a plugin, just make a python class with a run(self, pypeflow, files) method

```python
class ByPypeflowPlugin(object):
    def run(self, pypeflow, files):
        for path, file in files.items():
            if path.endswith('.html'):
                new_contents = '{} <p>By pypeflow</p>'.format(file['contents'].read().decode('utf-8))
                file['contents'] = io.BytesIO(new_contents)
```

For convenience, there is Base plugins classes:
- pypeflow.plugins.BasePlugin - Base class, implements filter by pattern or collection
- pypeflow.plugins.BaseThreadPlugin - Used for threaded processing files
- pypeflow.plugins.BaseAsyncPlugin - Used when there is need for high I/O operations

The above example using the BasePlugin:

```python
class ByPypeflowPlugin(object):
    def process_file(self, path, file):
        new_contents = '{} <p>By pypeflow</p>'.format(file['contents'].read().decode('utf-8))
        file['contents'] = io.BytesIO(new_contents)

# using the plugin like this
ByPypeflowPlugin(filter_pattern=r'.html$')
```
