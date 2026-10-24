# Thermodynamic database of material properties

This repository is the backend of the thermodynamic database of material properties for planetary modelling. The frontend is our collaboration website, which you can find here: TBD.

The purpose of the database is to collect all thermodynamic properties of materials, as well as equations of state (EOS) that exist in the literature.

This repository serves 3 purposes:
- store the thermodynamic properties and equations of state (EOS) or materials that exist in the literature
- provide users quick access to the available/existing data
- create a structure that can easily be injected in our frontend website

Since this repository is the backend for our website, this is not meant to be a user-friendly EOS navigation tool, but it can be used as such.

# Who are we?

We are a group of scientists with a wide range of expertise, all connected to the field of planetary science. You can learn more about us and our collaboration by visiting our website: TBD.

We also welcome new collaborators.

# How to use this database

1. You can navigate the `data` folder to manually navigate through the contents of the database. 
2. You can use the `EOSdatabase_demo_v*` notebooks to see how to load and manipulate the database.

# How to add more data

To add more data, we recommend using the following workflow.

## Recommended workflow
### Fork
Start by forking this repository to make a copy in your github account.

### Template

The contributor templates and data-format documentation are generated from shared
schemas. See [schemas/README.md](schemas/README.md) for editing, regeneration,
and checking which data fields still need schema definitions.

In the `data` folder, create a new folder for every source you want to add. We recommend use `data/_template` as a template.

### Contents
<b>Each source corresponds to one peer-reviewed scientific paper</b> with an author and a DOI. Add the `[source_id]_source.toml` file, containing bibliographic information about the source (paper). There should be only one source file per folder.

<b>Add one `[source_id]_[eos_label]_eos.toml` file per EOS</b>. Each folder (source) can have as many EOS as needed.

<b>Add one `[source_id]_[thermo_label]_thermo.dat` and `[source_id]_[thermo_label]_thermo.toml` file per thermodynamic table</b>. The `.dat` file contains ascii tab-separated machine readable thermodynamic data. The `.toml` file contains metadata, i.e. information related to the thermodynamic data. Each folder (source) can have as many EOS as needed.

In addition to thermodynamic data, contributors are heavily encouraged to provide the raw thermodynamic data, as published by the original authors: `[source_id]_[thermo_label]_thermo_raw.dat`; and a python script `[source_id]_[thermo_label]_thermo.py` used to convert the raw data into database-readable files. These file will be ignored, but they greatly improve reproducibility.

### Load test
Once all the new content has been created, test your contribution by running:
```
python tests/test_load.py
```

This script verifies that:
1. All modules are imported successfully
2. All files/data are loaded successfully

A successful output will look like:
```
Source code imported successfully.

Loaded thermo-data file: data/solomatovacaracas2021/solomatovacaracas2021_pyrolite_thermo.dat
Loaded thermo-data file: data/fischer2011/fischer2011_b8feo_thermo.dat
[...]
Loaded source file: data/solomatovacaracas2021/solomatovacaracas2021_source.toml
Loaded source file: data/fischer2011/fischer2011_source.toml
[...]
Loaded EOS file: data/dorogokupets2017/dorogokupets2017_liquidfe_eos.toml
Loaded EOS file: data/dorogokupets2017/dorogokupets2017_fccfe_eos.toml
All data loaded successfully from ./data.
Database located at './data' loaded successfully.

All tests passed. Please use the 'EOSdatabase_demo_*.' notebook to verify that your entry has the expected behavior.
```

As indicated in the last line, this script merely verifies that all modules are imported and all files are loaded. It does not guarantee that various parameters and variables have actually been implemented correctly.

### Pull Request
If the new content passed all the tests, use git add/commit/push to submit your implementations. Navigate to the forked repository, and make a pull request (PR). The core contributors will verify the PR and validate it or leave comments to resolve.

# Other forms of contribution

We welcome all forms of contributions: adding more data, reviewing existing data, adding new features, and overall any improvements to this repository.