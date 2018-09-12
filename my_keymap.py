
# coding: utf-8

# In[ ]:


get_ipython().run_cell_magic('javascript', '', 'require(["codemirror/keymap/sublime", "notebook/js/cell", "base/js/namespace"],\n    function(sublime_keymap, cell, IPython) {\n        cell.Cell.options_default.cm_config.keyMap = \'sublime\';\n        var cells = IPython.notebook.get_cells();\n        for(var cl=0; cl< cells.length ; cl++){\n            cells[cl].code_mirror.setOption(\'keyMap\', \'sublime\');\n        }\n    }\n);')

