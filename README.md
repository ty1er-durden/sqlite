# sqlite

SQL Lite Examples

## Installing vscode Exension

[SQLite extension](https://marketplace.visualstudio.com/items?itemName=alexcvzz.vscode-sqlite)

## Installing a Newer Version of SQLite (optional)

Add the `sqlite` directory in this project to your path variable.

### Linux

Download SQL Lite from the [downloads page](https://www.sqlite.org/download.html), specifically the `sqlite-autoconf-*.tar.gz` file from the **Source Code** section. Install in to the `sqlite` directory in this project:

```bash
tar -xvfz /tmp/sqlite-autoconf-3300000.tar.gz
/tmp/sqlite-autoconf-3300000/configure --prefix=/path/to/this/project/sqlite
sudo make
sudo make install
```

### Windows

Download SQL Lite from the [downloads page](https://www.sqlite.org/download.html), specifically:

- `sqlite-dll-win32-x86-*.zip`
- `sqlite-tools-win32-x86-*.zip`

Extract both files in to the `sqlite` directory in this project.

# References

- [SQLITE TUTORIAL](https://www.sqlitetutorial.net/sqlite-python/)
