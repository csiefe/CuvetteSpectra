# CuvetteSpectra
Code to run cuvette holder (Quantum Northwest qpod 2e) and spectrometer (Ocean Optics) using seabreeze, simultaneously. This code has been tested on a Windows operating system.

## Getting Started

These instructions will install the CuvetteSpectra GUI and connect a cuvette holder and spectrometer.

### Prerequisites

### Installing

Python packages used:
PyQt5
serial
time
seabreeze
datetime
pandas
numpy
matplotlib

After downloading files from repository into the same folder, using your favorite Python interpreter run CuvetteSpectra_ControlFile.py. The GUI should promptly open (see below).

![Alt text](https://github.com/mcleca8/CuvetteSpectra/blob/master/CuvetteSpectra%20GUI.PNG?raw=true)

Type in the correct COM port for your cuvette holder. You can determine this by looking at your Device Manager.
Click "Initialize Spectrometer" and "Initialize Cuvette Holder" and ensure there are no errors (you will be prompted if there are). ##You're ready to take data!

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
