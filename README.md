# Mashcima

> Handwritten music image synthesizer for HMR

A Python library that produces synthetic images of monophonic handwritten music. One of the following images is synthetic, take a guess:

```
[image here]
```

The upper staff was synthesized by this tool, the lower is taken from the [CVC-MUSCIMA dataset](http://www.cvc.uab.es/cvcmuscima/index_database.html).


## Notes

Python packaging info: https://packaging.python.org/tutorials/packaging-projects/
And also: https://the-hitchhikers-guide-to-packaging.readthedocs.io/en/latest/creation.html

To execute inspections: `python -m mashcima.inspections.inspect_foo` from the root folder.

To play around with mashcima during development create a venv and install it like this: `pip install -e ../Mashcima` where `-e` means it will link the folder and all changes will propagate immediately.

PrIMuS download: https://grfia.dlsi.ua.es/primus/packages/primusCalvoRizoAppliedSciences2018.tgz
MUSCIMA++ download: https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11372/LRT-2372/MUSCIMA-pp_v1.0.zip
