# fyCursor
A simple cursor for managing sqlite3 databases

## Installation 
You can simply use pip: &nbsp;
\$```pip3 install fyCursor```

<!-- Repobeats analytics -->
#  Analytics 
![Alt](https://repobeats.axiom.co/api/embed/0dda89a6c675987fd8c7d580fc77c9a05cd58b62.svg "Repobeats analytics image")

# Changelog 📄
### 📀 v0.1.x
- New fyCursor methods:
    - create_table (BETA)
- Table and Fields (‼️ BETA):
    - Table class:
        - TableError
        - ``insert`` method
        - ``create`` method
        
    - Field class with following components
        - name 
        - types
        - primary_key
        - default
        - nullable
- Type hints
- ``fetch`` and ``one`` now support ``execute`` method

### 🎎 v0.0.x
- Basic fyCursor methods:
    - add
    - set
    - update
    - select
    - fetch
    - one
    - commit
    - where
- Connect (#todo: all arguments)
- Bug fixes 
