# Thermodynamic database of material properties

<img height="200" alt="PEARL_logo_Fran" src="https://github.com/user-attachments/assets/158d5053-e398-4e48-8a59-655de048b543" />

This repository is the *backend* of the thermodynamic database of material properties for planetary modelling. The *frontend* is our collaboration website, which you can find here:
1. PEARL website: [https://pearl-database-demo.onrender.com](https://pearl-database-demo.onrender.com)
2. About PEARL: [https://pearl-database-demo.onrender.com/about/](https://pearl-database-demo.onrender.com/about/)
3. PEARL's team: [https://pearl-database-demo.onrender.com/team/](https://pearl-database-demo.onrender.com/team/)

The purpose of the database is to collect **thermodynamic properties of materials** and **equations of state (EOS)** that exist in the literature.

This repository serves 3 purposes:
- store thermodynamic properties and equations of state (EOS)
- provide users quick access to the available/existing data
- create a structure that can easily be injected in our *frontend* website

Since this repository is the *backend* for our website, it has more advanced tools intended for more advanced users.

# Contents of the repository

- [data](data/) contains the repository data.
- [docs](docs/) contains the documentation: [https://an0wen.github.io/pearl-database/](https://an0wen.github.io/pearl-database/).
- [modules](modules/) contains modules used to handle the contents of the database (in `data/`)
- [output](output/) contains figures and tables generated using the modules
- [schemas](schemas/) contains reference information on properties of entries
- [scripts](scripts/) contains standalone scripts used to manipulate the data or perform checks
- [tests](tests/) contains test scripts, useful when adding new entries to verify it is loaded as intended

# How to use this database

1. You can navigate the `data` folder to manually navigate through the contents of the database. 
2. You can use the `EOSdatabase_demo_v*` notebooks to see how to load and manipulate the database.

# How to add more data

To add more data, we recommend using the following workflow:

1. **Fork the repository**: it will create a copy of the repository on your github account.
2. **Use the templates [data/_templates/](data/_templates/) to create a new entry**.
    - One entry is one folder that corresponds to one peer-reviewed publication (at least accepted, preferably published).
    - The name of the entry (folder), `[source_id]`, follows the author-year naming convention, with letters a, b, c etc. used when necessary.
    - Each entry can contain as many thermodynamic tables and EOSs as necessary
    - Add one `[source_id]_[thermo_label]_thermo.dat` and `[source_id]_[thermo_label]_thermo.toml` file per thermodynamic table. The `*_thermo.dat` file contains ascii tab-separated machine readable thermodynamic data. The `.toml` file contains metadata, i.e. information related to the thermodynamic data.
    - Contributors are heavily encouraged to provide the raw thermodynamic data, as published by the original authors: `[source_id]_[thermo_label]_thermo_raw.*` (can be any format); and a python script `[source_id]_[thermo_label]_thermo.py` used to convert the raw data into database-readable files. These file will be ignored, but they greatly improve reproducibility.
3. Once all entries are added, **run tests** to verify that new entries follow the required format:
    ```
    python tests/test_load.py
    python tests/test_schemas.py
    ```
4. **Verify fields coverage** by running `python scripts/check_schema_coverage.py`. This verifies that all fields used in the database (including new entries) are defined in the [schemas](schemas/) (and hence the documentation and templates).
    - If the output is empty, you can proceed.
    - If the output is not empty, make sure that you intended to create new fields, otherwise try following the existing structure.
5. **Push the changes** to your github repository.
    - *If you are new to github*: remember that your computer and your github repo are not synced. You need to "push" your changes manually so they are uploaded on github.
6. **Make the pull request (PR)**.
    - *If you are new to github*: once you pushed the changes on your fork, github will detect that you are "ahead" of the database, and will propose to make a "pull request". This will send us a request to implement your changes. After review, the PR will be accepted so the new entries can be added.
  
If you don't have a github account, or are worried the learning curve is too steep: **contact us**, and we will be happy to assist you!
You can contact us by using our [content request form](https://docs.google.com/forms/d/e/1FAIpQLSftstLjyRFI_QHUJcg1xsdBVSfIpkdVIdQBl1ou_xs0jy_R4Q/viewform?usp=header). Leaving your email adress will allow us to follow-up with your request and make it process faster.

# All contributions are welcome

We welcome all forms of contributions: adding more data, reviewing existing data, adding new features, and overall any improvements to this repository.

# Credits

We are working on our first official release of the PEARL database. In the meantime, if you used PEARL (frontend or backend) please include the following in your acknowledgements:
```
This work has benefitted from the PEARL database (https://github.com/an0wen/pearl-database).
```
