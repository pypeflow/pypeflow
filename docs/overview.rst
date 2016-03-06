Overview
========

Requirements
------------

Pypeflow alone only needs Python 3, but each plugin has its own requirements

Architecture & Design
---------------------

Everything is a plugin, the core has the minimal code to cordinate the plugins, basically,
PypeFlow reads all files and put them on a dict, and each plugin manipulates this dict on its own terms,
and after all plugins processed, Pypeflow writes all files on the dict on build directory
