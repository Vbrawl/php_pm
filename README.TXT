This is a package manager for PHP.

The package manager is written in python and is used to download packages and libraries for PHP.


How to make it work:
* Download packages from github.
* Store them in a folder in the system.
* Update them when needed.
* On project initialization write a requirements.php.txt with all requirements.
* On project build send all libraries to (project_root)/pm_libraries


Package Requirements:
* project.json : A json formatted file with information about the project.
Package Recommendations:
* LICENCE.TXT : A file with the licence of the package.
* README.TXT : A file with information about the library.




project.json example:
{
    "project_name": "TestProject",
    "project_version": "1.6.5",
    "project_url": "https://aurltoagitdirectory.tld",
    "project_library_directory": "pm_library"
    "project_requirements": {
        "project_name_of_another_project": "url_to_the_project"
    }
}